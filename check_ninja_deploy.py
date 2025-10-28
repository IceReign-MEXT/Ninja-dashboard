#!/usr/bin/env python3
import os
import sqlite3
import socket
import requests
import importlib

print("🔍 NINJA-DASHBOARD BOT DEPLOYMENT CHECK\n")

# ==========================
# Environment
# ==========================
ENV_VARS = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ADMIN_ID",
    "TELEGRAM_CHANNEL_ID",
    "DATABASE_URL",
    "WEBHOOK_URL"
]

env_missing = False
for var in ENV_VARS:
    if not os.getenv(var):
        print(f"❌ {var} missing or empty")
        env_missing = True
    else:
        print(f"✅ {var} detected")

# ==========================
# Python modules
# ==========================
MODULES = ["flask", "requests", "sqlalchemy", "aiohttp", "web3", "telegram", "dotenv"]
for mod in MODULES:
    try:
        importlib.import_module(mod)
        print(f"✅ Module loaded: {mod}")
    except ImportError:
        print(f"❌ Missing module: {mod}")

# ==========================
# Database
# ==========================
db_path = os.getenv("DATABASE_PATH", "subscriptions.db")
if os.path.exists(db_path):
    print(f"✅ Database ready → {db_path}")
else:
    print(f"❌ Database file missing → {db_path}")

# ==========================
# Internet connectivity
# ==========================
try:
    requests.get("https://www.google.com", timeout=5)
    print("✅ Internet connection OK")
except:
    print("❌ Internet connection failed")

# ==========================
# Webhook check
# ==========================
webhook = os.getenv("WEBHOOK_URL")
if webhook:
    try:
        resp = requests.get(webhook, timeout=5)
        print(f"🌐 Webhook reachable → {webhook} [Status: {resp.status_code}]")
    except:
        print(f"❌ Webhook unreachable → {webhook}")
else:
    print("❌ Webhook URL not set")

# ==========================
# Telegram bot test (async)
# ==========================
try:
    from telegram import Bot
    import asyncio

    async def test_bot():
        bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        me = await bot.get_me()
        print(f"🤖 Telegram bot connected → @{me.username}")

    asyncio.run(test_bot())
except Exception as e:
    print(f"❌ Telegram bot connection failed: {e}")

# ==========================
# Project files
# ==========================
FILES = ["app.py", "main.py", "bot.py", "bot_handlers.py", "requirements.txt",
         "Dockerfile", "init_db.py", "start_icegods.py", "utils"]

for f in FILES:
    if os.path.exists(f):
        print(f"✅ Found: {f}")
    else:
        print(f"❌ Missing: {f}")

print("\n🧩 DEPLOYMENT READINESS CHECK COMPLETE.")
print("💡 If all checks passed, the bot is ready to host.")
print("⚠️ Any missing modules, env vars, or files must be fixed before deployment.")
