from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

from app.embeddings import get_embeddings


DATA_DIR = Path("data")

#This code loads all PDF documents from a folder and converts them into LangChain Document objects
def load_documents():
    documents = []

    for pdf_file in DATA_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())

    return documents

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    return chunks

CHROMA_DIR = "chroma_db"

def create_vector_store(chunks):

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )

    return vector_db

def ingest():

    print("Loading documents...")

    documents = load_documents()

    print(f"{len(documents)} pages loaded.")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"{len(chunks)} chunks created.")

    print("Generating embeddings...")

    create_vector_store(chunks)

    print("Done!")

if __name__ == "__main__":
    ingest()

