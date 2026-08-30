import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent.parent
QDRANT_PATH = str(Path(os.getenv("QDRANT_PATH", BACKEND_DIR / "qdrant.db")).resolve())

COLLECTION_NAME = "company_documents"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-neura-ai-secret-change-in-production")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5174")

# Comma-separated extra origins for CORS (e.g. Vercel preview URLs)
EXTRA_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("EXTRA_CORS_ORIGINS", "").split(",")
    if origin.strip()
]
