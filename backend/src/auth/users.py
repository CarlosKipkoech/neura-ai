from src.auth.database import get_user_by_username


def normalize_username(username: str) -> str:
    if not username:
        return ""
    return username.strip().lower().split("@")[0]


def get_user(username: str):
    """Backward-compatible lookup used by RAG memory keys."""
    row = get_user_by_username(username)
    if row is None:
        return None
    return {
        "name": row["name"],
        "role": row["role"],
    }
