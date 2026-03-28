import requests
import os

def send_message(to: str, message: str):

    url = f"https://graph.facebook.com/v19.0/{os.getenv('PHONE_NUMBER_ID')}/messages"

    token = os.getenv('WHATSAPP_TOKEN')

    if not token:
        print("❌ TOKEN MISSING")
        return

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
        print("❌ REQUEST FAILED:", str(e))
