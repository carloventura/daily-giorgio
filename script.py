import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
THREAD_ID = os.getenv("THREAD_ID")
RSS_URL = os.getenv("RSS_URL")
FILE_MEMORIA = "last_post.txt"


def post_to_thread(message, webhook_url, thread_id):
    if not webhook_url or not thread_id:
        print("WEBHOOK_URL and THREAD_ID must be set in environment variables.")
        return

    payload = {
        "content": message,
    }

    endpoint = f"{webhook_url}?thread_id={thread_id}"

    response = requests.post(endpoint, json=payload)

    if response.status_code == 204:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message. Status code: {response.status_code}, Response: {response.text}")
    return response

def get_latest_post(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            latest_post = data["items"][0]
            return latest_post
    except Exception as e:
        print(f"Errore nel recupero RSS: {e}")
    return None

def main():
    latest_post = get_latest_post(RSS_URL)
    latest_url = latest_post.get("url") if latest_post else None

    if not latest_url:
        return

    # 1. Leggi l'ultimo post salvato per evitare duplicati
    last_saved_url = ""
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r") as f:
            last_saved_url = f.read().strip()

    # 2. Confronta
    if latest_url == last_saved_url:
        print("Nessun nuovo post trovato. Chiudo.")
        return

    # 3. Se nuovo, invia a Discord Thread
    print(f"Nuovo post trovato: {latest_url}. Invio a Discord...")
    res = post_to_thread(f"📢 **Nuovo post di Giorgione!**\n{latest_url}", WEBHOOK_URL, THREAD_ID)
    
    if res.status_code == 204:
        # 4. Aggiorna la memoria locale
        with open(FILE_MEMORIA, "w") as f:
            f.write(latest_url)
        print("Inviato con successo.")
    else:
        print(f"Errore invio Discord: {res.status_code}")

if __name__ == "__main__":
    main()