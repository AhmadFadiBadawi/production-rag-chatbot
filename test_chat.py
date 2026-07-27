from app.chat import ask

question = "What are the general office hours of the Office of International Affairs?"

result = ask(question)

print(result["answer"])

print()

print(result["sources"])