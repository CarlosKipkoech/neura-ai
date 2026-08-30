from src.guardrails.base import BaseGuardrail, GuardrailResult
from src.guardrails.context import ContextGuardrail
from src.guardrails.input import InputGuardrail
from src.guardrails.output import OutputGuardrail
from src.guardrails.permission import PermissionGuardrail


class GuardrailManager:
    def __init__(self):
        self.guardrails = [
            InputGuardrail(),
            PermissionGuardrail(),
            ContextGuardrail(),
            OutputGuardrail(),
        ]

    def run(self, question, role, retrieved_documents, answer):
        for guardrail in self.guardrails:
            result = guardrail.evaluate(question, role, retrieved_documents, answer)
            if not result.passed:
                return GuardrailResult(False, f"{guardrail.name} guardrail failed: {result.reason}", [result.reason])

        return GuardrailResult(True, "All guardrails passed.")


def check_question_scope(question):
    return InputGuardrail().evaluate(question, "", [], "").passed
