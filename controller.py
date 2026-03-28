# controller.py

# Temporary memory (we will connect Firebase later)
users = {}

def handle_message(user_id, message, msg_type):
    # Get or create user
    if user_id not in users:
        users[user_id] = {
            "state": "NEW",
            "name": None,
            "class": None,
            "subject": None,
        }

    user = users[user_id]

    # ROUTING BASED ON STATE
    if user["state"] == "NEW":
        return handle_new_user(user, message)

    elif user["state"] == "ONBOARDING":
        return handle_onboarding(user, message)

    elif user["state"] == "LEARNING":
        return handle_learning(user, message)

    else:
        return "Something went wrong. Let's start again."


def handle_new_user(user, message):
    user["state"] = "ONBOARDING"
    return "Hi, I'm Wax. What is your name?"


def handle_onboarding(user, message):
    # Ask for name
    if not user["name"]:
        user["name"] = message
        return f"Nice to meet you, {message}. What class are you in?"

    # Ask for class
    elif not user["class"]:
        user["class"] = message
        return "What subject do you want to start with?"

    # Ask for subject
    elif not user["subject"]:
        user["subject"] = message
        user["state"] = "LEARNING"
        return f"Alright, let's start {message}. Tell me what topic you want to learn."

    else:
        user["state"] = "LEARNING"
        return "Let's begin learning."


def handle_learning(user, message):
    # For now, simple response
    return f"Okay {user['name']}, let's learn this step by step. What do you understand about {message}?"
