from langchain_chroma import Chroma

from app.embeddings import get_embeddings

CHROMA_DIR = "chroma_db"


def load_vector_store():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
    )


def get_retriever(k: int = 4):
    return load_vector_store().as_retriever(
        search_kwargs={"k": k}
    )


def retrieve_documents(question: str, k: int = 4):
    retriever = get_retriever(k)
    return retriever.invoke(question)


def retrieve_with_scores(question: str, k: int = 4):
    return load_vector_store().similarity_search_with_score(
        question,
        k=k,
    )


def extract_sources(documents):
    return [
        {
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
        }
        for doc in documents
    ]

def format_context(documents):
    return "\n\n".join(
        doc.page_content
        for doc in documents
    )