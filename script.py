import html
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RSS_URL = os.getenv("RSS_URL")
FORCE_PUBLISH = os.getenv("FORCE_PUBLISH", "false").lower() == "true"
FILE_MEMORIA = "last_post.txt"


def post_to_channel(post, webhook_url):
    if not webhook_url:
        print("WEBHOOK_URL must be set in environment variables.")
        return None

    caption_html = post.get("content_html", "")
    caption = html.unescape(re.sub(r"<[^>]+>", "", caption_html)).strip()
    caption = re.sub(r"\n{3,}", "\n\n", caption)
    if len(caption) > 4096:
        caption = caption[:4093] + "..."

    thumbnail = post.get("_rssbridge", {}).get("thumbnail")
    if not thumbnail and post.get("attachments"):
        thumbnail = post["attachments"][0].get("url")

    embed = {
        "title": post.get("title", "Nuovo post di Kevin!"),
        "url": post.get("url"),
        "description": caption or "Nuovo post su Instagram",
        "color": 0xE1306C,
        "author": {
            "name": post.get("author", {}).get("name", "kevinbele_hy"),
        },
    }
    if thumbnail:
        embed["image"] = {"url": thumbnail}

    payload = {
        "content": "📢 **Nuovo post di Kevin!**",
        "embeds": [embed],
    }

    response = requests.post(webhook_url, json=payload, timeout=15)

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

    # 2. Confronta, a meno che la pubblicazione non sia stata forzata manualmente
    if latest_url == last_saved_url and not FORCE_PUBLISH:
        print("Nessun nuovo post trovato. Chiudo.")
        return

    # 3. Invia al canale principale Discord
    print(f"Nuovo post trovato: {latest_url}. Invio a Discord...")
    res = post_to_channel(latest_post, WEBHOOK_URL)

    if res and res.status_code == 204:
        # 4. Aggiorna la memoria locale
        with open(FILE_MEMORIA, "w") as f:
            f.write(latest_url)
        print("Inviato con successo.")
    elif res:
        print(f"Errore invio Discord: {res.status_code}")

if __name__ == "__main__":
    main()