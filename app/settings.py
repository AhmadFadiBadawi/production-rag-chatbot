import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash",
    )

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "models/gemini-embedding-001",
    )

    CHROMA_DIR: str = os.getenv(
        "CHROMA_DIR",
        "chroma_db",
    )

    TOP_K: int = int(
        os.getenv("TOP_K", "4")
    )

    TEMPERATURE: float = float(
        os.getenv("TEMPERATURE", "0.2")
    )

    MAX_OUTPUT_TOKENS: int = int(
        os.getenv("MAX_OUTPUT_TOKENS", "1024")
    )


settings = Settings()


if not settings.GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not configured."
    )