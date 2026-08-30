from fastapi import HTTPException, status

from src.auth.database import create_user, get_user_by_username
from src.auth.schemas import AuthResponse, LoginRequest, SignUpRequest, UserResponse
from src.auth.security import create_access_token, hash_password, verify_password
from src.auth.dependencies import user_response_from_row


def signup_user(payload: SignUpRequest) -> AuthResponse:
    if get_user_by_username(payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    row = create_user(
        username=payload.username,
        name=payload.name,
        role=payload.role,
        password_hash=hash_password(payload.password),
    )
    user = user_response_from_row(row)
    token = create_access_token(row["id"], row["username"], row["role"])
    return AuthResponse(access_token=token, user=user)


def login_user(payload: LoginRequest) -> AuthResponse:
    row = get_user_by_username(payload.username)
    if row is None or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user = user_response_from_row(row)
    token = create_access_token(row["id"], row["username"], row["role"])
    return AuthResponse(access_token=token, user=user)


def seed_demo_users() -> None:
    """Create demo accounts on first boot if the database is empty."""
    from src.auth.database import get_connection

    with get_connection() as connection:
        count = connection.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
        if count:
            return

    demos = [
        ("alice.chen", "Alice Chen", "finance", "demo12345"),
        ("bob.martinez", "Bob Martinez", "hr", "demo12345"),
        ("carol.williams", "Carol Williams", "marketing", "demo12345"),
        ("david.kim", "David Kim", "engineering", "demo12345"),
        ("elena.rodriguez", "Elena Rodriguez", "executive", "demo12345"),
        ("frank.johnson", "Frank Johnson", "employee", "demo12345"),
        ("admin", "System Admin", "admin", "admin12345"),
    ]

    for username, name, role, password in demos:
        if get_user_by_username(username):
            continue
        create_user(
            username=username,
            name=name,
            role=role,
            password_hash=hash_password(password),
        )
