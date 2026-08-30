from pydantic import BaseModel, Field, field_validator

from src.auth.database import SIGNUP_ROLES, VALID_ROLES


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    name: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=8, max_length=128)
    role: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned.replace(".", "").replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username may only contain letters, numbers, dots, underscores, and hyphens")
        return cleaned

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        role = value.strip().lower()
        if role not in SIGNUP_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(sorted(SIGNUP_ROLES))}")
        return role


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    id: str
    username: str
    name: str
    role: str
    department: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
