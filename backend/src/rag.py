from src.retriever import Retriever
from src.llm import generate_answer
from src.guardrails import GuardrailManager, check_question_scope
from src.auth.users import get_user, normalize_username
from src.memory import ConversationMemory
from src.ingest import run_ingestion
import re

memory = ConversationMemory()
retriever = None
guardrail_manager = GuardrailManager()

RETRIEVAL_K = 6
CONTEXT_K = 4


class UnavailableRetriever:
    def search(self, query, user_role, k=3):
        return []


def _extract_query_numbers(question: str) -> set[str]:
    """Normalize numeric tokens from the question for chunk matching."""
    numbers = set()
    for match in re.findall(r"\$?\d+(?:,\d{3})*(?:\.\d+)?", question):
        normalized = match.replace("$", "").replace(",", "")
        numbers.add(normalized)
        if "." in normalized:
            numbers.add(normalized.split(".")[0])
    return numbers


def _rerank_results(question: str, results: list) -> list:
    """
    Boost chunks that contain numeric values or key terms from the question.
    Vector search alone often misses table rows with specific thresholds.
    """
    numbers = _extract_query_numbers(question)
    keywords = {
        token
        for token in re.sub(r"[^a-z0-9\s]", " ", question.lower()).split()
        if len(token) > 3
    }

    scored = []
    for rank, doc in enumerate(results):
        content = doc.page_content.lower()
        content_numbers = {
            value.replace(",", "")
            for value in re.findall(r"\$?\d+(?:,\d{3})*(?:\.\d+)?", doc.page_content)
        }

        score = 0.0
        score += sum(2.0 for num in numbers if num in content_numbers)
        score += sum(1.0 for kw in keywords if kw in content)
        if "approval" in content and "approval" in question.lower():
            score += 1.5
        if "approver" in content and ("approval" in question.lower() or "workflow" in question.lower()):
            score += 1.5
        if "roi" in content and "roi" in question.lower():
            score += 2.0
        if "pto" in content and "pto" in question.lower():
            score += 2.0

        scored.append((score, rank, doc))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [doc for _, _, doc in scored]


def get_retriever():
    global retriever
    if retriever is None:
        try:
            retriever = Retriever()
        except Exception:
            try:
                run_ingestion()
                retriever = Retriever()
            except Exception:
                retriever = UnavailableRetriever()
    return retriever


def ensure_vector_store(force_reload: bool = False):
    global retriever
    if force_reload:
        retriever = None
    get_retriever()


def rag_pipeline(question, username, role=None):
    """
    Complete RAG pipeline:
    1. Retrieve relevant documents from the vector store using the question.
    2. Generate an answer using the retrieved documents as context.
    3. send context and question to the LLM and return the answer
    """

    user = get_user(username)
    resolved_role = role or (user["role"] if user else None)

    if not resolved_role:
        return {
            "answer": "User not found.",
            "sources": [],
        }

    user_key = normalize_username(username) if user else username.strip().lower()
    role = resolved_role

    if not check_question_scope(question):
        return {
            "answer": "The question is out of scope.",
            "sources": [],
        }

    raw_results = get_retriever().search(
        query=question,
        user_role=role,
        k=RETRIEVAL_K,
    )
    results = _rerank_results(question, raw_results)[:CONTEXT_K]

    if not results:
        return {
            "answer": "No authorized documents found for your role.",
            "sources": [],
        }

    context = "\n\n".join(result.page_content for result in results)

    history = memory.get_history(user_key, role)
    history_text = "\n\n".join(
        f"User: {item['question']}\nAssistant: {item['answer']}"
        for item in history
    )
    full_context = f"""
Conversation History:
{history_text}

Retrieved Documents:
{context}
"""

    answer = generate_answer(question, full_context)

    guardrail_result = guardrail_manager.run(
        question=question,
        role=role,
        retrieved_documents=results,
        answer=answer,
    )

    if not guardrail_result.passed:
        return {
            "answer": f"The request was blocked by guardrails: {guardrail_result.reason}",
            "sources": [],
        }

    memory.add_message(user_key, role, question, answer)

    sources = []
    for doc in results:
        sources.append(
            {
                "department": doc.metadata.get("department"),
                "allowed_roles": doc.metadata.get("allowed_roles"),
                "title": doc.metadata.get("title"),
                "source": doc.metadata.get("source"),
                "classification": doc.metadata.get("classification"),
                "content": doc.page_content[:140],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    username = "john"
    question = "What information is available about company budgets?"

    response = rag_pipeline(question, username, "admin")

    print("\nANSWER:")
    print(response["answer"])

    print("\nSOURCES:")
    for source in response["sources"]:
        print(source)
