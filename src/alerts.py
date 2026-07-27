import os
import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def send_slack_alert(message: str):
    response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    response.raise_for_status()