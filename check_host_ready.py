#!/usr/bin/env python3
# File: check_host_ready.py
# Purpose: Full system readiness check for Ninja-dashboard bot

import os
import sys
import sqlite3
import importlib
import requests
from pathlib import Path
from dotenv import load_dotenv

print("🔍 NINJA-DASHBOARD BOT DEPLOYMENT CHECK\n")

# Load .env
dotenv_path = Path(".env")
if dotenv_path.exists():
    load_dotenv(dotenv_path)
    print("✅ .env found and loaded")
else:
    print("❌ .env file missing. Copy env.example to .env and fill required values.")

# Required environment variables
env_vars = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ADMIN_ID",
    "TELEGRAM_CHANNEL_ID",
    "DATABASE_URL",
    "WEBHOOK_URL",
]

print("\n🌿 Checking environment variables...")
for var in env_vars:
    value = os.getenv(var)
    if value and value.strip():
        print(f"✅ {var} detected")
    else:
        print(f"❌ {var} missing or empty")

# Required Python modules
modules = ["flask", "requests", "sqlalchemy", "aiohttp", "web3", "telegram", "dotenv"]
print("\n📦 Checking Python modules...")
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"✅ Module loaded: {mod}")
    except ImportError:
        print(f"❌ Missing module: {mod}")

# Database check
db_url = os.getenv("DATABASE_URL", "sqlite:///subscriptions.db")
print("\n💾 Checking database...")
try:
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if Path(db_path).exists():
            print(f"✅ Database ready → {db_url}")
        else:
            print(f"❌ Database file missing → {db_path}")
    else:
        print("⚠️ Non-SQLite database, manual check needed")
except Exception as e:
    print(f"❌ Database error: {e}")

# Internet check
print("\n🌐 Checking internet connectivity...")
try:
    requests.get("https://www.google.com", timeout=5)
    print("✅ Internet connection OK")
except:
    print("❌ No internet connectivity")

# Telegram bot connectivity (basic)
print("\n🤖 Checking Telegram bot connection...")
try:
    from telegram import Bot
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        bot = Bot(token=bot_token)
        me = bot.get_me()
        print(f"✅ Telegram bot connected → @{me.username}")
    else:
        print("❌ TELEGRAM_BOT_TOKEN not set")
except Exception as e:
    print(f"❌ Telegram bot connection failed: {e}")

# Files check
required_files = [
    "app.py", "main.py", "bot.py", "bot_handlers.py",
    "requirements.txt", "Dockerfile", "init_db.py", "start_icegods.py",
    "utils"
]
print("\n📁 Checking project files...")
for f in required_files:
    if Path(f).exists():
        print(f"✅ Found: {f}")
    else:
        print(f"❌ Missing: {f}")

print("\n🧩 DEPLOYMENT READINESS CHECK COMPLETE.")
print("💡 If all checks passed, the bot is ready to host.")
print("⚠️ Any missing modules, env vars, or files must be fixed before deployment.")
