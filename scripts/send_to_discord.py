import os

import requests
from dotenv import load_dotenv


def send_message(content: str):
    load_dotenv()
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not set in .env")

    response = requests.post(webhook_url, json={"content": content}, timeout=30)
    response.raise_for_status()


if __name__ == "__main__":
    sample = "Discord webhook 測試成功。"
    send_message(sample)
    print("Message sent.")
