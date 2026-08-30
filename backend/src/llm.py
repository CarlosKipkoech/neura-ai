from src.prompts import build_prompt
from src.config import GOOGLE_API_KEY


llm = None
if GOOGLE_API_KEY:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except Exception:
        llm = None
    else:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
        )


def _fallback_answer(question, context):
    context_excerpt = " ".join(context.split())[:700]
    return (
        "I couldn't reach the configured Gemini model in this environment, so I'm using a local fallback response. "
        f"Question: {question}\n\nContext summary: {context_excerpt}"
    )


def generate_answer(question, context):
    if llm is None:
        return _fallback_answer(question, context)

    prompt = build_prompt(context=context, question=question)

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception:
        return _fallback_answer(question, context)