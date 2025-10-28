#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import socket
import sqlite3
import aiohttp
from telegram import Bot
from telegram.error import InvalidToken, TelegramError
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# Configuration
# --------------------------
REQUIRED_ENV_VARS = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ADMIN_ID",
    "TELEGRAM_CHANNEL_ID",
    "WEBHOOK_URL",
    "DATABASE_URL",
    "PORT",
]

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///subscriptions.db").replace("sqlite:///", "")
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --------------------------
# Async Telegram check
# --------------------------
async def check_telegram_token(token):
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        return True, me.username
    except InvalidToken:
        return False, "Invalid token"
    except TelegramError as e:
        return False, f"Telegram API error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

# --------------------------
# Webhook check
# --------------------------
async def check_webhook(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return resp.status
    except Exception as e:
        return f"Error: {e}"

# --------------------------
# Database check
# --------------------------
def check_database(db_path):
    if os.path.exists(db_path):
        return True
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        return True
    except Exception:
        return False

# --------------------------
# Port check
# --------------------------
def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            return True
        except OSError:
            return False

# --------------------------
# Main async runner
# --------------------------
async def main():
    print("🔍 ICEGODS BOT SYSTEM CHECK\n")

    # Env vars
    missing_env = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing_env:
        print("❌ Missing env vars:", ", ".join(missing_env))
    else:
        print("✅ All required env vars found.")

    # Telegram bot
    token_ok, token_status = await check_telegram_token(BOT_TOKEN)
    if token_ok:
        print(f"✅ Telegram token valid: @{token_status}")
    else:
        print(f"❌ Telegram token invalid or network issue: {token_status}")

    # Webhook
    if WEBHOOK_URL:
        webhook_status = await check_webhook(WEBHOOK_URL)
        if isinstance(webhook_status, int):
            print(f"🌐 Webhook reachable: HTTP {webhook_status}")
        else:
            print(f"❌ Webhook error: {webhook_status}")
    else:
        print("❌ WEBHOOK_URL not set")

    # Database
    if check_database(DB_PATH):
        print(f"✅ Database exists → {DB_PATH}")
    else:
        print(f"⚠️ Database missing or inaccessible: {DB_PATH}")

    # Port
    if check_port(PORT):
        print(f"✅ Port {PORT} is available.")
    else:
        print(f"⚠️ Port {PORT} is in use. Stop other processes before running the bot.")

    print("\n🧩 SYSTEM CHECK COMPLETE.")

if __name__ == "__main__":
    asyncio.run(main())










