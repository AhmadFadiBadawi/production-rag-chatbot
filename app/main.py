from fastapi import FastAPI, HTTPException

from app.chat import ask
from app.ingest import ingest
from app.models import ChatRequest, ChatResponse

app = FastAPI(
    title="Production RAG Chatbot",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Production RAG Chatbot API",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    try:
        return ask(request.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@app.post("/ingest")
def ingest_documents():
    ingest()
    return {
        "message": "Documents ingested successfully."
    }