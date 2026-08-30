RAG_PROMPT = """
You are an AI assistant for a company.

Answer the user's question using ONLY the provided context.
The context may include policy tables formatted as rows — extract the relevant row(s).

If the answer is not found in the context, say:
"I don't have enough information to answer that."

Context:
{context}

Question:
{question}

Answer:
"""


def build_prompt(context: str, question: str) -> str:
    return RAG_PROMPT.format(context=context, question=question)
