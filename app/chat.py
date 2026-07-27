from app.llm import get_llm
from app.prompts import RAG_PROMPT
from app.rag import (
    retrieve_documents,
    format_context,
    extract_sources,
)


def ask(question: str):
    documents = retrieve_documents(question)

    context = format_context(documents)

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": extract_sources(documents),
    }