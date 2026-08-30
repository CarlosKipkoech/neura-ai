import os
import sqlite3
from pathlib import Path

from src.config import BACKEND_DIR

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BACKEND_DIR / "data" / "neura.db"))

VALID_ROLES = {
    "finance",
    "hr",
    "marketing",
    "engineering",
    "executive",
    "employee",
    "admin",
}

SIGNUP_ROLES = VALID_ROLES - {"admin"}


def get_connection() -> sqlite3.Connection:
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path), check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def get_user_by_username(username: str) -> sqlite3.Row | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, username, name, role, password_hash FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
        return row


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, username, name, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return row


def create_user(username: str, name: str, role: str, password_hash: str) -> sqlite3.Row:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (username, name, role, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (username.strip(), name.strip(), role, password_hash),
        )
        connection.commit()
        user_id = cursor.lastrowid
        row = connection.execute(
            "SELECT id, username, name, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Failed to create user")
        return row
