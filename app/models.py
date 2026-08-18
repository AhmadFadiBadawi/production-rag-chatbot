from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str | None
    page: int | None
    excerpt: str | None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]