def get_wax_response(user_name: str, message: str) -> str:
    message = message.lower()

    # basic fallback brain (you can upgrade later with AI API)
    if "hello" in message or "hi" in message:
        return f"Hi {user_name}. What topic are we learning today?"

    if "graph" in message:
        return (
            "A graph shows relationships between values.\n"
            "Example: distance vs time graph.\n"
            "Question: What does a graph show?"
        )

    if "what is maths" in message:
        return (
            "Maths is the study of numbers.\n"
            "Example: 2 + 2 = 4\n"
            "Question: What is 2 + 3?"
        )

    return (
        f"Alright {user_name}, I understand.\n"
        "Let’s break it step by step.\n"
        "What exactly do you want to learn?"
    )
