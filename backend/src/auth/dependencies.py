from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.database import get_user_by_id
from src.auth.schemas import UserResponse
from src.auth.security import decode_access_token
from src.types import department_for_role
security = HTTPBearer(auto_error=False)


def user_response_from_row(row) -> UserResponse:
    role = row["role"]
    return UserResponse(
        id=str(row["id"]),
        username=row["username"],
        name=row["name"],
        role=role,
        department=department_for_role(role),
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserResponse:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    row = get_user_by_id(user_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_response_from_row(row)
