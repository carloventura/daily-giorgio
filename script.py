import requests
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
THREAD_ID = os.getenv("THREAD_ID")

def post_to_thread(message):
    if not WEBHOOK_URL or not THREAD_ID:
        print("WEBHOOK_URL and THREAD_ID must be set in environment variables.")
        return

    payload = {
        "content": message,
        "thread_id": THREAD_ID
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    message = "Hello, this is a message posted to the thread!"
    post_to_thread(message)