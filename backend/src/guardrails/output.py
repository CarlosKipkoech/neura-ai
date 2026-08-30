import re

from src.guardrails.base import BaseGuardrail, GuardrailResult


def _normalize_numbers(text: str) -> set[str]:
    """Extract comparable numeric tokens from text."""
    values: set[str] = set()
    for match in re.findall(r"\$?\d+(?:,\d{3})*(?:\.\d+)?", text):
        cleaned = match.replace("$", "").replace(",", "").strip()
        if cleaned:
            values.add(cleaned)
            if "." in cleaned:
                values.add(cleaned.split(".")[0])
    return values


def _numbers_overlap(answer_numbers: set[str], context_numbers: set[str]) -> bool:
    if not answer_numbers or not context_numbers:
        return True

    for answer_num in answer_numbers:
        if answer_num in context_numbers:
            return True
        # Allow partial match for values like 198.7 vs 198.7M context fragments
        for ctx_num in context_numbers:
            if answer_num.startswith(ctx_num) or ctx_num.startswith(answer_num):
                return True

    return False


class OutputGuardrail(BaseGuardrail):
    name = "output"

    def evaluate(self, question: str, role: str, retrieved_documents: list, answer: str) -> GuardrailResult:
        if not isinstance(answer, str) or not answer.strip():
            return GuardrailResult(False, "The model did not produce an answer.")

        insufficient = "don't have enough information" in answer.lower()
        if insufficient:
            return GuardrailResult(True, "Model declined to answer due to missing context.")

        if answer.startswith("I couldn't reach the configured Gemini"):
            return GuardrailResult(True, "Local fallback response.")

        context_text = "\n".join(
            getattr(doc, "page_content", "")
            for doc in retrieved_documents
            if getattr(doc, "page_content", None)
        )

        answer_numbers = _normalize_numbers(answer)
        context_numbers = _normalize_numbers(context_text)

        if context_numbers and answer_numbers and not _numbers_overlap(answer_numbers, context_numbers):
            return GuardrailResult(False, "The answer is not grounded in the retrieved context.")

        return GuardrailResult(True, "The answer is grounded in the retrieved context.")
