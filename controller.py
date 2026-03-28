from wax_brain import get_wax_response

users = {}

def handle_message(user_id, message, msg_type):

    if user_id not in users:
        users[user_id] = {
            "state": "NEW",
            "name": None,
            "class": None,
            "subject": None,
            "current_topic": None
        }

    user = users[user_id]

    if user["state"] == "NEW":
        user["state"] = "ONBOARDING"
        return "Hi, I'm Wax. What is your name?"

    if user["state"] == "ONBOARDING":

        if not user["name"]:
            user["name"] = message
            return f"Nice to meet you, {message}. What class are you in?"

        if not user["class"]:
            user["class"] = message
            return "What subject do you want to start with?"

        if not user["subject"]:
            user["subject"] = message
            user["state"] = "LEARNING"
            return f"Alright {user['name']}, let's start {message}. What topic do you want to learn?"

    if user["state"] == "LEARNING":

        if not user["current_topic"]:
            user["current_topic"] = message
            return get_wax_response(user["name"], message)

        if message.lower() in ["i don't know", "idk", "no idea", "nothing"]:
            return get_wax_response(
                user["name"],
                f"Explain {user['current_topic']} from zero"
            )

        return get_wax_response(user["name"], message)

    user["state"] = "NEW"
    return "Restarting. Hi, I'm Wax. What is your name?"
