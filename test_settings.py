from app.settings import settings


print("Model:", settings.MODEL_NAME)
print("Embedding:", settings.EMBEDDING_MODEL)
print("Chroma:", settings.CHROMA_DIR)
print("Top K:", settings.TOP_K)
print("Temperature:", settings.TEMPERATURE)
print("Max tokens:", settings.MAX_OUTPUT_TOKENS)