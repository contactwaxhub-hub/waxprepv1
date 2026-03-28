import requests
import os

def send_message(to: str, message: str):

    phone_number_id = os.getenv("PHONE_NUMBER_ID")
    token = os.getenv("WHATSAPP_TOKEN")

    if not phone_number_id:
        print("❌ PHONE_NUMBER_ID missing")
        return

    if not token:
        print("❌ WHATSAPP_TOKEN missing")
        return

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("📩 STATUS:", response.status_code)
        print("📩 RESPONSE:", response.text)

    except Exception as e:
        print("❌ SEND ERROR:", str(e))
