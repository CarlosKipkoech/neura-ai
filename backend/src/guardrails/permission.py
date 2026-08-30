import re

from src.guardrails.base import BaseGuardrail, GuardrailResult


class PermissionGuardrail(BaseGuardrail):
    name = "permission"

    def evaluate(self, question: str, role: str, retrieved_documents: list, answer: str) -> GuardrailResult:
        if not role:
            return GuardrailResult(False, "No role supplied for permission checks.")

        text = question.lower()
        sensitive_terms = [
            "payroll",
            "salary",
            "termination",
            "disciplinary",
            "medical",
            "personal",
        ]

        if not any(term in text for term in sensitive_terms):
            return GuardrailResult(True, "Question does not target sensitive employee data.")

        allowed_roles = {
            "payroll": {"hr", "admin"},
            "salary": {"hr", "admin"},
            "termination": {"hr", "admin"},
            "disciplinary": {"hr", "admin"},
            "medical": {"hr", "admin"},
            "personal": {"hr", "admin"},
        }

        for term in sensitive_terms:
            if term in text:
                allowed = allowed_roles.get(term, set())
                if role not in allowed:
                    return GuardrailResult(False, f"Permission denied for sensitive term '{term}'.")

        return GuardrailResult(True, "Role is permitted to access the requested information.")
