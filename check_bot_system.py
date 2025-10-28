import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    print("❌ BOT_TOKEN missing in .env")
    exit()

try:
    bot = Bot(token=token)
    me = bot.get_me()
    print(f"✅ Token valid! Bot username: @{me.username}")
except Exception as e:
    print("❌ Token invalid or network issue:", e)
