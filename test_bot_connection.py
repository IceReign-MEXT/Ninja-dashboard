import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

async def check_bot():
    me = await bot.get_me()
    print(f"Bot connected: {me.username}")

asyncio.run(check_bot())
