import os
import asyncio
from app import app, bot
from telegram import Bot
from dotenv import load_dotenv
import sqlite3

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "subscriptions.db")
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def check_database():
    if not os.path.exists(DB_PATH):
        print(f"⚠️ DB missing. Creating {DB_PATH}...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id TEXT NOT NULL,
                          plan TEXT NOT NULL
                          );""")
        conn.commit()
        conn.close()
        print("✅ DB created.")
    else:
        print(f"✅ Database exists → {DB_PATH}")

async def set_webhook():
    try:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook set → {WEBHOOK_URL}")
    except Exception as e:
        print(f"⚠️ Failed to set webhook: {e}")

def main():
    check_database()
    asyncio.run(set_webhook())
    print(f"🚀 Launching Flask app on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
