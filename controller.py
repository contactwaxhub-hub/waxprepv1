# controller.py

from wax_brain import get_wax_response

# Temporary memory (we will replace with Firebase later)
users = {}


def handle_message(user_id, message, msg_type):
    # Create user if new
    if user_id not in users:
        users[user_id] = {
            "state": "NEW",
            "name": None,
            "class": None,
            "subject": None,
            "current_topic": None
        }

    user = users[user_id]

    # ROUTER
    if user["state"] == "NEW":
        return handle_new_user(user)

    elif user["state"] == "ONBOARDING":
        return handle_onboarding(user, message)

    elif user["state"] == "LEARNING":
        return handle_learning(user, message)

    else:
        user["state"] = "NEW"
        return "Let’s restart. Hi, I'm Wax. What is your name?"


# ---------------- NEW USER ----------------
def handle_new_user(user):
    user["state"] = "ONBOARDING"
    return "Hi, I'm Wax. What is your name?"


# ---------------- ONBOARDING ----------------
def handle_onboarding(user, message):

    # Step 1: Name
    if not user["name"]:
        user["name"] = message
        return f"Nice to meet you, {message}. What class are you in?"

    # Step 2: Class
    elif not user["class"]:
        user["class"] = message
        return "What subject do you want to start with?"

    # Step 3: Subject
    elif not user["subject"]:
        user["subject"] = message
        user["state"] = "LEARNING"
        return f"Alright {user['name']}, let's start {message}. What topic do you want to learn?"

    else:
        user["state"] = "LEARNING"
        return "Let's begin learning. What topic do you want?"


# ---------------- LEARNING (AI CONTROLLED) ----------------
def handle_learning(user, message):

    topic = user.get("current_topic")

    # If no topic set yet
    if not topic:
        user["current_topic"] = message
        topic = message

        return get_wax_response(
            user["name"],
            f"Teach {topic} from beginner level. Explain simply with one example and ask one question."
        )

    # If user says they don't know
    if message.lower() in ["nothing", "i don't know", "i dont know", "no idea"]:
        return get_wax_response(
            user["name"],
            f"Explain {topic} from absolute zero. Break it down like a beginner student and give one simple example."
        )

    # Continue learning
    return get_wax_response(
        user["name"],
        f"Student said: '{message}'. Continue teaching {topic} step by step and ask one question."
    )
