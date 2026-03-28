from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Wax.

You are a strict AI tutor for Nigerian students.

RULES:
- Never introduce yourself again
- Never do onboarding
- Never ask for name, class, or subject
- Assume all student profile is already handled externally
- Teach only the topic given
- Keep answers short (max 3 paragraphs)
- Always explain + example + 1 question
- Stay consistent and focused
- Never reset conversation
"""

def call_groq(user_message, system_extra=""):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + system_extra},
            {"role": "user", "content": user_message}
        ],
        max_tokens=700
    )
    return completion.choices[0].message.content


def get_wax_response(phone_number, message, message_type="text"):
    if message_type == "audio":
        return "I can only read text for now. Type your question."

    if message_type == "image":
        return "I cannot view images yet. Type your question."

    return call_groq(message)
