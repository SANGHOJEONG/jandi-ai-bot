import requests
import os
from dotenv import load_dotenv

load_dotenv()

JANDI_WEBHOOK_URL = os.getenv("JANDI_INCOMING_WEBHOOK_URL")

def send_to_jandi(answer: str):
    response = requests.post(
        JANDI_WEBHOOK_URL,
        json={"body": answer},
        headers={"Accept": "application/vnd.tosslab.jandi-v2+json"}
    )
    return response.status_code