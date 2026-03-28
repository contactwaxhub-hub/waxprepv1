from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from config import WEBHOOK_VERIFY_TOKEN
from controller import handle_message
from whatsapp import send_message

router = APIRouter()


# =========================
# VERIFY WEBHOOK (IMPORTANT FIX)
# =========================
@router.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("WEBHOOK VERIFY HIT:", params)

    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)

    return PlainTextResponse(content="failed", status_code=403)


# =========================
# RECEIVE MESSAGE
# =========================
@router.post("/webhook")
async def receive_message(request: Request):
    try:
        data = await request.json()
        print("🔥 WEBHOOK HIT:", data)

        entry = data.get("entry", [])
        if not entry:
            return {"status": "no entry"}

        changes = entry[0].get("changes", [])
        if not changes:
            return {"status": "no changes"}

        value = changes[0].get("value", {})

        messages = value.get("messages")
        if not messages:
            return {"status": "no message"}

        message = messages[0]

        phone = message.get("from")
        msg_type = message.get("type")

        if msg_type == "text":
            text = message["text"]["body"]
            reply = handle_message(phone, text, "text")
        else:
            reply = "I only understand text for now."

        print(f"📩 FROM: {phone} | MESSAGE: {msg_type}")

        send_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("❌ WEBHOOK ERROR:", str(e))
        return {"status": "error", "message": str(e)}
