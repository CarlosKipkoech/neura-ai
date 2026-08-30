from qdrant_client.models import Filter, FieldCondition, MatchAny

from src.embeddings import get_embedding_model
from src.config import QDRANT_PATH, COLLECTION_NAME


class Retriever:
    """
    1. Connecting to Qdrant vector database
    2. Creating query embeddings
    3. Applying RBAC filtering
    4. Returning authorized documents only
    """

    def __init__(self):
        from langchain_qdrant import QdrantVectorStore

        self.embeddings = get_embedding_model()
        self.vectorstore = QdrantVectorStore.from_existing_collection(
            path=QDRANT_PATH,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
        )

    def search(self, query, user_role, k=3):
        """Search documents with semantic similarity and role-based filtering."""
        if user_role == "admin":
            return self.vectorstore.similarity_search(query=query, k=k)

        role_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.allowed_roles",
                    match=MatchAny(any=[user_role]),
                )
            ]
        )

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=role_filter,
        )
