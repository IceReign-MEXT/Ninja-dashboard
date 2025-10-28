import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.error import TelegramError
from bot_handlers import handle_text_command, init_bot_objects
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in environment!")

bot = Bot(token=TOKEN)
init_bot_objects(bot)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        await handle_text_command(bot, update)
    except TelegramError as e:
        print("❌ Telegram API error:", e)
    except Exception as e:
        print("❌ General error:", e)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "🤖 ICEGODS Bot Running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
