import os
import tempfile
from pathlib import Path

import pytest

from src.auth.database import DATABASE_PATH, init_db, create_user, get_user_by_username
from src.auth.security import hash_password, verify_password


@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(os.path.join(tmpdir, "test.db"))
        monkeypatch.setattr("src.auth.database.DATABASE_PATH", db_path)
        init_db()
        yield


def test_password_hash_roundtrip():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_fetch_user():
    create_user("jane.doe", "Jane Doe", "hr", hash_password("password123"))
    row = get_user_by_username("jane.doe")
    assert row is not None
    assert row["role"] == "hr"
