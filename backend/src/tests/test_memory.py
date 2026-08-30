from src.memory import ConversationMemory


def test_memory_is_isolated_per_user():
    memory = ConversationMemory(max_messages_per_user=5)

    memory.add_message("alice", "finance", "Q1", "A1")
    memory.add_message("bob", "hr", "Q2", "A2")

    assert len(memory.get_history("alice", "finance")) == 1
    assert len(memory.get_history("bob", "hr")) == 1
    assert memory.get_history("alice", "finance")[0]["question"] == "Q1"
    assert memory.get_history("bob", "hr")[0]["question"] == "Q2"


def test_memory_trims_old_messages():
    memory = ConversationMemory(max_messages_per_user=2)

    memory.add_message("alice", "finance", "Q1", "A1")
    memory.add_message("alice", "finance", "Q2", "A2")
    memory.add_message("alice", "finance", "Q3", "A3")

    history = memory.get_history("alice", "finance")
    assert len(history) == 2
    assert history[0]["question"] == "Q2"
    assert history[1]["question"] == "Q3"
