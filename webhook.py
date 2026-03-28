from fastapi import APIRouter, Request
from config import WEBHOOK_VERIFY_TOKEN
from controller import handle_message
from whatsapp import send_message

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)

    if params.get("hub.verify_token") == WEBHOOK_VERIFY_TOKEN:
        return int(params.get("hub.challenge"))

    return {"error": "failed"}


@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]["value"]

        if "messages" not in changes:
            return {"status": "no message"}

        message = changes["messages"][0]
        phone = message["from"]
        msg_type = message.get("type")

        if msg_type == "text":
            text = message["text"]["body"]
            reply = handle_message(phone, text, "text")

        else:
            reply = "I only understand text for now."

        send_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("ERROR:", e)
        return {"status": "error"}
