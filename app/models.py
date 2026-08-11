from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str | None
    page: int | None
    excerpt: str | None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]