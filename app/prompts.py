from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer cannot be found in the context, reply exactly:

"I couldn't find the answer in the uploaded documents."

Keep answers concise and accurate.

Context:
{context}

Question:
{question}
"""
)