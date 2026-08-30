import os
import tempfile
import uuid
from pathlib import Path

import pytest

from src.auth.database import init_db
from src.auth.service import login_user, seed_demo_users, signup_user
from src.auth.schemas import LoginRequest, SignUpRequest


@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(os.path.join(tmpdir, "test.db"))
        monkeypatch.setattr("src.auth.database.DATABASE_PATH", db_path)
        init_db()
        yield


def test_signup_and_login_flow():
    username = f"user.{uuid.uuid4().hex[:8]}"
    signup_payload = SignUpRequest(
        username=username,
        name="Test User",
        password="password123",
        role="finance",
    )
    signup_response = signup_user(signup_payload)
    assert signup_response.user.username == username
    assert signup_response.user.role == "finance"
    assert signup_response.access_token

    login_response = login_user(
        LoginRequest(username=username, password="password123")
    )
    assert login_response.user.username == username
    assert login_response.access_token
