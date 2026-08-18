import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app.auth import get_current_user
from app.auth_routes import router as auth_router
from app.chat import ask
from app.database import initialize_database
from app.ingest import ingest
from app.logging_config import setup_logging
from app.models import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Production RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)


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
        "status": "healthy",
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
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
def ingest_documents(
    current_user=Depends(get_current_user),
):
    logger.info("Document ingestion requested")

    ingest()

    logger.info("Documents ingested successfully")

    return {
        "message": "Documents ingested successfully.",
    }