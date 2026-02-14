import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
THREAD_ID = os.getenv("THREAD_ID")
RSS_URL = os.getenv("RSS_URL")


def post_to_thread(message):
    if not WEBHOOK_URL or not THREAD_ID:
        print("WEBHOOK_URL and THREAD_ID must be set in environment variables.")
        return

    payload = {
        "content": message,
    }

    endpoint = f"{WEBHOOK_URL}?thread_id={THREAD_ID}"

    response = requests.post(endpoint, json=payload)

    if response.status_code == 204:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message. Status code: {response.status_code}, Response: {response.text}")

def get_latest_post():
    # try:
    #     response = requests.get(RSS_URL)
    # Placeholder for retrieving the last post from a file or database
    return "This is the last post content."

if __name__ == "__main__":
    message = "Hello, this is a message posted to the thread!"
    post_to_thread(message)