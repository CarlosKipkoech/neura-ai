from src.guardrails.base import BaseGuardrail, GuardrailResult


class ContextGuardrail(BaseGuardrail):
    name = "context"

    def evaluate(self, question: str, role: str, retrieved_documents: list, answer: str) -> GuardrailResult:
        if not retrieved_documents:
            return GuardrailResult(False, "No retrieved context was available for the question.")

        context_text = "\n".join(
            getattr(doc, "page_content", "")
            for doc in retrieved_documents
            if getattr(doc, "page_content", None)
        )

        if not context_text.strip():
            return GuardrailResult(False, "Retrieved documents did not contain usable context.")

        return GuardrailResult(True, "Retrieved context is present for the answer.")
