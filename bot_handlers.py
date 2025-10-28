from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID

bot = None

def init_bot_objects(b):
    global bot
    bot = b

async def handle_text_command(bot, update: Update):
    message = update.message
    chat_id = message.chat.id
    text = message.text.strip().lower()

    if text == "/start":
        await bot.send_message(chat_id, "👋 Welcome to IceGods Bot!\nUse /help to see commands.")
    elif text == "/help":
        await bot.send_message(chat_id, "📌 Commands:\n/start - Welcome\n/help - Command list\n/vip - Join VIP group")
    elif text == "/vip":
        await bot.send_message(chat_id, "💎 To access VIP, please subscribe.")
    elif str(chat_id) == str(ADMIN_ID):
        await bot.send_message(chat_id, "🔑 Hello Admin!")
    else:
        await bot.send_message(chat_id, "🤖 Command not recognized. Use /help")
