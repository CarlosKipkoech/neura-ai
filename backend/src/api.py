from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.database import init_db
from src.auth.dependencies import get_current_user
from src.auth.schemas import AuthResponse, ChatRequest, ChatResponse, LoginRequest, SignUpRequest, UserResponse
from src.auth.service import login_user, seed_demo_users, signup_user
from src.config import EXTRA_CORS_ORIGINS, FRONTEND_URL
from src.ingest import run_ingestion
from src.rag import ensure_vector_store, rag_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_demo_users()
    try:
        ensure_vector_store()
    except Exception as exc:
        print(f"Vector store initialization warning: {exc}")
    yield


app = FastAPI(
    title="Neura AI Enterprise RAG API",
    version="2.0.0",
    lifespan=lifespan,
)

allowed_origins = list(
    {
        FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        *EXTRA_CORS_ORIGINS,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Neura AI Enterprise RAG API Running", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/auth/signup", response_model=AuthResponse)
def signup(request: SignUpRequest):
    return signup_user(request)


@app.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest):
    return login_user(request)


@app.get("/auth/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    if not request.question.strip():
        return ChatResponse(answer="Please ask a question so I can help you.", sources=[])

    try:
        result = rag_pipeline(
            question=request.question,
            username=current_user.username,
            role=current_user.role,
        )
        return ChatResponse(answer=result.get("answer", ""), sources=result.get("sources", []))
    except Exception as exc:
        return ChatResponse(
            answer=f"Sorry, I hit an issue while processing your request: {exc}",
            sources=[],
        )


@app.post("/admin/reindex")
def reindex(current_user: UserResponse = Depends(get_current_user)):
    if current_user.role != "admin":
        return {"detail": "Admin access required"}
    run_ingestion()
    ensure_vector_store(force_reload=True)
    return {"message": "Knowledge base reindexed"}
