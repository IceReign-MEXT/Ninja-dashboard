#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------
# Load .env
# ----------------------------
env_path = Path('.') / '.env'
if not env_path.exists():
    print("❌ .env file missing! Create one with TELEGRAM_BOT_TOKEN, WEBHOOK_URL, DATABASE_URL, etc.")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DB_PATH = os.getenv("DATABASE_PATH", "subscriptions.db")
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "0.0.0.0")

if not TOKEN or not WEBHOOK_URL:
    print("❌ TELEGRAM_BOT_TOKEN or WEBHOOK_URL missing in .env")
    sys.exit(1)

# ----------------------------
# Install dependencies
# ----------------------------
print("🚀 Installing required Python packages...")
requirements = [
    "flask",
    "python-telegram-bot==20.7",
    "python-dotenv",
    "requests",
    "web3",
    "SQLAlchemy>=2.0.36",
]

subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install"] + requirements, check=True)

# ----------------------------
# Initialize SQLite DB if missing
# ----------------------------
if not Path(DB_PATH).exists():
    print(f"🗄 Database {DB_PATH} not found. Creating...")
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Example table for subscriptions (customize as needed)
    c.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        plan TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database {DB_PATH} created successfully.")

# ----------------------------
# Set Telegram Webhook
# ----------------------------
print(f"🌐 Setting webhook to {WEBHOOK_URL} ...")
from telegram import Bot
bot = Bot(token=TOKEN)

try:
    import asyncio
    async def set_webhook():
        await bot.set_webhook(url=WEBHOOK_URL)
        print("✅ Webhook set successfully!")

    asyncio.run(set_webhook())
except Exception as e:
    print("❌ Failed to set webhook:", e)

# ----------------------------
# Run Flask app
# ----------------------------
print(f"🚀 Launching Flask app on {HOST}:{PORT} ...")
subprocess.run([sys.executable, "app.py"])
