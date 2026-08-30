class ConversationMemory:
    """Per-user conversation memory storage."""

    def __init__(self, max_messages_per_user: int = 10):
        self.sessions: dict[str, list[dict[str, str]]] = {}
        self.max_messages_per_user = max_messages_per_user

    def _session_key(self, username: str, role: str) -> str:
        return f"{username.strip().lower()}::{role.strip().lower()}"

    def add_message(self, username: str, role: str, question: str, answer: str) -> None:
        key = self._session_key(username, role)
        history = self.sessions.setdefault(key, [])
        history.append({"question": question, "answer": answer})
        if len(history) > self.max_messages_per_user:
            self.sessions[key] = history[-self.max_messages_per_user :]

    def get_history(self, username: str, role: str) -> list[dict[str, str]]:
        return self.sessions.get(self._session_key(username, role), [])
