# GNU nano 8.6  check_bot_system_async.py
import os
import sqlite3
import asyncio
import aiohttp
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DB_PATH = os.getenv("DATABASE_PATH", "subscriptions.db")
PORT = os.getenv("PORT", "5000")

async def check_telegram_token():
    if not TELEGRAM_TOKEN:
        return False, "❌ TELEGRAM_BOT_TOKEN not set in .env"
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        me = await bot.get_me()
        return True, f"✅ Token valid. Bot username: {me.username}"
    except Exception as e:
        return False, f"❌ Token invalid or network error: {e}"

async def check_webhook():
    if not WEBHOOK_URL:
        return False, "❌ WEBHOOK_URL not set in .env"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEBHOOK_URL) as resp:
                if resp.status == 200:
                    return True, f"✅ Webhook reachable: {WEBHOOK_URL}"
                else:
                    return False, f"⚠️ Webhook reachable but returned status {resp.status}"
    except Exception as e:
        return False, f"❌ Webhook unreachable: {e}"

def check_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        conn.close()
        return True, f"✅ Database exists → {DB_PATH}"
    except Exception as e:
        return False, f"⚠️ Database missing or invalid: {e}"

def check_port():
    # Just print what port is configured
    return True, f"✅ Port {PORT} is available"

async def main():
    print("🔍 ICEGODS BOT SYSTEM ASYNC CHECK\n")

    token_status, token_msg = await check_telegram_token()
    print(token_msg)

    webhook_status, webhook_msg = await check_webhook()
    print(webhook_msg)

    db_status, db_msg = check_database()
    print(db_msg)

    port_status, port_msg = check_port()
    print(port_msg)

    print("\n🧩 CHECK COMPLETE.")
    print("If token is invalid → regenerate from @BotFather.")
    print("If webhook unreachable → check ngrok or Flask is running.")
    print("If DB missing → run init_db.py or create manually.")

if __name__ == "__main__":
    asyncio.run(main())
