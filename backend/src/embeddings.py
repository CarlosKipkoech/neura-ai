from langchain_core.embeddings import Embeddings

from src.config import EMBEDDING_MODEL_NAME, GOOGLE_API_KEY


class _FallbackEmbeddings(Embeddings):
    def embed_query(self, text):
        return [0.0]

    def embed_documents(self, texts):
        return [[0.0] for _ in texts]


def get_embedding_model():
    """
    Prefer Google embeddings in production (lightweight, no local ML model).
    Fall back to HuggingFace locally when no API key is configured.
    """
    if GOOGLE_API_KEY:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=GOOGLE_API_KEY,
            )
        except Exception as exc:
            print(f"Google embeddings unavailable: {exc}")

    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    except Exception:
        return _FallbackEmbeddings()
