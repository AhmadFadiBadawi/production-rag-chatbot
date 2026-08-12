import logging

from app.llm import get_llm
from app.prompts import RAG_PROMPT
from app.rag import (
    retrieve_documents,
    format_context,
    extract_sources,
)


logger = logging.getLogger(__name__)


def ask(question: str):

    logger.info("Starting RAG request")

    if not question.strip():
        logger.warning("Empty question received")
        raise ValueError("Question cannot be empty.")

    documents = retrieve_documents(question)

    logger.info(
        "Retrieved %d documents for RAG",
        len(documents),
    )

    if not documents:
        logger.warning("No relevant documents found")

        return {
            "answer": "No relevant documents were found.",
            "sources": [],
        }

    context = format_context(documents)

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    logger.info("Sending request to Gemini")

    response = get_llm().invoke(prompt)

    logger.info("Gemini response received")

    return {
        "answer": response.content,
        "sources": extract_sources(documents),
    }