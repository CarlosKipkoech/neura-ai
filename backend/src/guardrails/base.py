from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class GuardrailResult:
    passed: bool
    reason: str = ""
    details: List[str] = field(default_factory=list)


class BaseGuardrail:
    name: str = "guardrail"

    def evaluate(self, question: str, role: str, retrieved_documents: list, answer: str) -> GuardrailResult:
        raise NotImplementedError
