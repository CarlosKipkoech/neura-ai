import re

from src.guardrails.base import BaseGuardrail, GuardrailResult

# Clearly off-topic patterns — block these only
OFF_TOPIC_TERMS = {
    "weather",
    "football",
    "soccer",
    "recipe",
    "movie",
    "celebrity",
    "bitcoin price",
    "stock tip",
    "dating",
    "joke",
    "riddle",
}

# Enterprise knowledge-base scope — substring match (covers natural phrasing)
ENTERPRISE_TERMS = {
    "company",
    "policy",
    "policies",
    "employee",
    "employees",
    "work",
    "remote",
    "leave",
    "pto",
    "benefit",
    "benefits",
    "salary",
    "payroll",
    "hr",
    "human resources",
    "budget",
    "spending",
    "spend",
    "expense",
    "expenses",
    "travel",
    "finance",
    "financial",
    "cost",
    "revenue",
    "procurement",
    "approval",
    "approver",
    "workflow",
    "compliance",
    "sox",
    "audit",
    "incident",
    "security",
    "architecture",
    "engineering",
    "software",
    "development",
    "marketing",
    "campaign",
    "brand",
    "customer",
    "roi",
    "nps",
    "strategy",
    "roadmap",
    "risk",
    "risks",
    "board",
    "executive",
    "operations",
    "supplier",
    "vendor",
    "recruitment",
    "hiring",
    "performance",
    "handbook",
    "reimbursement",
    "forecast",
    "ebitda",
    "arr",
    "margin",
    "control",
    "controls",
    "sop",
    "procedure",
    "procedures",
    "neura",
    "headcount",
    "staffing",
}


class InputGuardrail(BaseGuardrail):
    name = "input"

    def evaluate(self, question: str, role: str, retrieved_documents: list, answer: str) -> GuardrailResult:
        if not isinstance(question, str) or not question.strip():
            return GuardrailResult(False, "No question provided.")

        normalized = question.lower().strip()

        if any(term in normalized for term in OFF_TOPIC_TERMS):
            return GuardrailResult(False, "The question appears to be outside the supported company policy scope.")

        if any(term in normalized for term in ENTERPRISE_TERMS):
            return GuardrailResult(True, "Question is within the supported policy scope.")

        # Short generic questions without enterprise context
        if len(normalized.split()) < 4:
            return GuardrailResult(False, "The question appears to be outside the supported company policy scope.")

        return GuardrailResult(True, "Question is within the supported policy scope.")
