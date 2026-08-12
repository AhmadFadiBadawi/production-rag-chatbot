import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.settings import settings


logger = logging.getLogger(__name__)


def get_llm():

    logger.info(
        "Initializing Gemini model: %s",
        settings.MODEL_NAME,
    )

    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.TEMPERATURE,
        max_output_tokens=settings.MAX_OUTPUT_TOKENS,
    )