import logging

from fastapi import FastAPI, HTTPException

from app.chat import ask
from app.ingest import ingest
from app.models import ChatRequest, ChatResponse
from app.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Production RAG Chatbot API",
    version="1.0.0",
)


@app.get("/")
def root():
    logger.info("Root endpoint requested")

    return {
        "message": "Production RAG Chatbot API",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    logger.info("Health check requested")

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    logger.info("Chat request received")

    try:
        result = ask(request.question)

        logger.info("Chat request completed successfully")

        return result

    except ValueError as e:
        logger.warning(
            "Invalid chat request: %s",
            str(e),
        )

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:
        logger.exception(
            "Unexpected error while processing chat request"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@app.post("/ingest")
def ingest_documents():
    logger.info("Document ingestion requested")

    ingest()

    logger.info("Documents ingested successfully")

    return {
        "message": "Documents ingested successfully."
    }