from fastapi import APIRouter, Request
from config import WEBHOOK_VERIFY_TOKEN
from wax_brain import get_wax_response
from whatsapp import send_message

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    token = params.get("hub.verify_token")
    if token == WEBHOOK_VERIFY_TOKEN:
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
        phone_number = message["from"]
        
        if message.get("type") == "text":
            message_text = message["text"]["body"]
            wax_response = get_wax_response(message_text)
            send_message(phone_number, wax_response)
        else:
            send_message(phone_number, "Hey! Wax only understands text for now. Type your question and I'll help you 😊")
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error"}
