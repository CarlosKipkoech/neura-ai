from langchain_core.embeddings import Embeddings

from src.config import EMBEDDING_MODEL_NAME


class _FallbackEmbeddings(Embeddings):
    def embed_query(self, text):
        return [0.0]

    def embed_documents(self, texts):
        return [[0.0] for _ in texts]


def get_embedding_model():
    """
    Returns an instance of the HuggingFaceEmbeddings model based on the specified model name.
    Falls back gracefully if the model dependency is unavailable in this environment.
    """
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except Exception:
        return _FallbackEmbeddings()

    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)