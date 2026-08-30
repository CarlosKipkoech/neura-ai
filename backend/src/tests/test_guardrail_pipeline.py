from types import SimpleNamespace

from src.guardrails import GuardrailManager


def test_finance_question_is_allowed_for_finance_user():
    manager = GuardrailManager()
    result = manager.run(
        question="What are the travel spending limits?",
        role="finance",
        retrieved_documents=[SimpleNamespace(page_content="Travel spending limit is $500.")],
        answer="Travel spending limit is $500.",
    )

    assert result.passed is True


def test_payroll_question_is_blocked_for_finance_user():
    manager = GuardrailManager()
    result = manager.run(
        question="Who can view payroll information?",
        role="finance",
        retrieved_documents=[SimpleNamespace(page_content="Payroll data is restricted to HR.")],
        answer="Payroll data is available to anyone.",
    )

    assert result.passed is False
    assert "permission" in result.reason.lower() or "scope" in result.reason.lower()


def test_unrelated_question_is_blocked():
    manager = GuardrailManager()
    result = manager.run(
        question="What is the weather today?",
        role="finance",
        retrieved_documents=[],
        answer="It is sunny.",
    )

    assert result.passed is False


def test_hallucinated_answer_is_blocked():
    manager = GuardrailManager()
    result = manager.run(
        question="What is the travel spending limit?",
        role="finance",
        retrieved_documents=[SimpleNamespace(page_content="Travel spending limit is $500.")],
        answer="The travel spending limit is $2000.",
    )

    assert result.passed is False
    assert "grounded" in result.reason.lower() or "context" in result.reason.lower()
