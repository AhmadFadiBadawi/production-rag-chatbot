import logging

logger = logging.getLogger(__name__)

from langchain_chroma import Chroma

from app.embeddings import get_embeddings
from app.settings import settings


def load_vector_store():
    return Chroma(
        persist_directory=settings.CHROMA_DIR,
        embedding_function=get_embeddings(),
    )


def get_retriever(k: int | None = None):
    if k is None:
        k = settings.TOP_K

    return load_vector_store().as_retriever(
        search_kwargs={"k": k}
    )


def retrieve_documents(
    question: str,
    k: int | None = None,
):
    logger.info(
        "Retrieving documents for question"
    )

    retriever = get_retriever(k)

    documents = retriever.invoke(question)

    logger.info(
        "Retrieved %d documents",
        len(documents),
    )

    return documents


def retrieve_with_scores(
    question: str,
    k: int | None = None,
):
    if k is None:
        k = settings.TOP_K

    return load_vector_store().similarity_search_with_score(
        question,
        k=k,
    )


def extract_sources(documents):
    return [
        {
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "excerpt": doc.page_content[:200],
        }
        for doc in documents
    ]


def format_context(documents):
    return "\n\n".join(
        doc.page_content
        for doc in documents
    )