import time

from langchain_core.embeddings import Embeddings

from src.config import EMBEDDING_MODEL_NAME, GOOGLE_API_KEY


class _FallbackEmbeddings(Embeddings):
    def embed_query(self, text):
        return [0.0]

    def embed_documents(self, texts):
        return [[0.0] for _ in texts]


class _RateLimitedEmbeddings(Embeddings):
    """Batch + retry wrapper so free-tier Gemini embed quotas do not abort ingest."""

    def __init__(self, inner: Embeddings, batch_size: int = 16):
        self.inner = inner
        self.batch_size = batch_size

    def embed_query(self, text):
        return self._call_with_retry(lambda: self.inner.embed_query(text))

    def embed_documents(self, texts):
        vectors = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            print(f"Embedding batch {start + 1}-{start + len(batch)} of {len(texts)}")
            vectors.extend(self._call_with_retry(lambda: self.inner.embed_documents(batch)))
            time.sleep(1)
        return vectors

    def _call_with_retry(self, fn, attempts: int = 6):
        last_error = None
        for attempt in range(attempts):
            try:
                return fn()
            except Exception as exc:
                last_error = exc
                message = str(exc)
                if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                    raise
                wait = 25 + attempt * 5
                print(f"Embedding rate-limited, retrying in {wait}s")
                time.sleep(wait)
        raise last_error


def get_embedding_model():
    """
    Prefer Google embeddings in production (lightweight, no local ML model).
    Fall back to HuggingFace locally when no API key is configured.
    """
    if GOOGLE_API_KEY:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            return _RateLimitedEmbeddings(
                GoogleGenerativeAIEmbeddings(
                    model="models/gemini-embedding-001",
                    google_api_key=GOOGLE_API_KEY,
                )
            )
        except Exception as exc:
            print(f"Google embeddings unavailable: {exc}")

    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    except Exception:
        return _FallbackEmbeddings()
