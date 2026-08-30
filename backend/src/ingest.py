import base64
import json
import re
import zlib
from pathlib import Path

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import COLLECTION_NAME, QDRANT_PATH
from src.embeddings import get_embedding_model


REPO_ROOT = Path(__file__).resolve().parents[2]
POSSIBLE_KNOWLEDGE_BASE_DIRS = [
    REPO_ROOT / "knowledge_base",
    REPO_ROOT / "backend" / "knowledge_base",
    REPO_ROOT / "backend" / "data",
]
KNOWLEDGE_BASE_DIR = next((path for path in POSSIBLE_KNOWLEDGE_BASE_DIRS if path.exists()), None)


def _decode_pdf_literal(text: str) -> str:
    result = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            escaped = text[i + 1]
            mapping = {
                "n": "\n",
                "r": "\r",
                "t": "\t",
                "b": "\b",
                "f": "\f",
                "(": "(",
                ")": ")",
                "\\": "\\",
            }
            result.append(mapping.get(escaped, escaped))
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def _extract_text_from_pdf(pdf_path: Path) -> str:
    data = pdf_path.read_bytes()
    if not data.startswith(b"%PDF"):
        raise ValueError(f"Unsupported PDF format: {pdf_path}")

    stream_matches = re.findall(rb"stream\r?\n(.*?)endstream", data, re.S)
    if not stream_matches:
        return ""

    pieces = []
    for chunk in stream_matches:
        payload = chunk.strip()
        if not payload:
            continue
        payload = payload.rstrip(b"\n")
        if payload.endswith(b"~>"):
            payload = payload[:-2]

        decoded_stream = None
        try:
            decoded_payload = base64.a85decode(payload, adobe=False)
            decoded_stream = zlib.decompress(decoded_payload)
        except Exception:
            try:
                decoded_stream = zlib.decompress(payload)
            except Exception:
                continue

        if decoded_stream is None:
            continue

        stream_text = decoded_stream.decode("latin-1", errors="ignore")
        literals = []
        for match in re.finditer(r"\((?:\\.|[^()\\])*(?:\\)?\)", stream_text):
            literal = match.group(0)[1:-1]
            literals.append(_decode_pdf_literal(literal))

        if literals:
            pieces.append("\n".join([part for part in literals if part.strip()]))

    if not pieces:
        return ""

    cleaned = []
    for piece in pieces:
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in piece.split("\n")]
        lines = [line for line in lines if line]
        if lines:
            cleaned.append("\n".join(lines))
    return "\n\n".join(cleaned)


def load_pdf_documents():
    documents = []

    if not KNOWLEDGE_BASE_DIR:
        raise FileNotFoundError("Knowledge base directory not found. Expected one of: backend/knowledge_base or repo/knowledge_base")

    pdf_files = sorted(KNOWLEDGE_BASE_DIR.rglob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found under {KNOWLEDGE_BASE_DIR}")

    for pdf_path in pdf_files:
        metadata_path = pdf_path.with_suffix(".json")
        metadata = {}
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        extracted_text = _extract_text_from_pdf(pdf_path)
        if not extracted_text.strip():
            continue

        department = metadata.get("department") or pdf_path.parent.name.replace("_", " ")
        allowed_roles = metadata.get("access_roles") or [department.lower(), "employee", "executive"]
        if isinstance(allowed_roles, str):
            allowed_roles = [allowed_roles]
        if "admin" not in allowed_roles:
            allowed_roles = [*allowed_roles, "admin"]

        documents.append(
            Document(
                page_content=extracted_text,
                metadata={
                    "department": department,
                    "allowed_roles": allowed_roles,
                    "source": str(pdf_path.relative_to(REPO_ROOT)),
                    "title": metadata.get("title") or pdf_path.stem,
                    "classification": metadata.get("classification") or "Internal",
                    "version": metadata.get("version") or "unknown",
                },
            )
        )

    return documents


def run_ingestion():
    documents = load_pdf_documents()
    print(f"Loaded {len(documents)} PDF pages for ingestion")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    embeddings = get_embedding_model()
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )
    print("PDF knowledge base successfully stored in Qdrant")


if __name__ == "__main__":
    run_ingestion()