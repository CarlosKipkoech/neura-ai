from src.auth.database import init_db, create_user, get_user_by_username
from src.auth.security import hash_password
from src.auth.users import get_user, normalize_username


def test_normalize_username():
    assert normalize_username("Alice.Chen") == "alice.chen"


def test_get_user_from_database():
    init_db()
    if not get_user_by_username("alice.chen"):
        create_user("alice.chen", "Alice Chen", "finance", hash_password("demo12345"))

    user = get_user("alice.chen")
    assert user is not None
    assert user["role"] == "finance"
