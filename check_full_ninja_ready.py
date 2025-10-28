#!/usr/bin/env python3
import os
import sqlite3
import socket
import importlib.util
import requests

print("🔍 NINJA-DASHBOARD BOT FULL DEPLOYMENT CHECK\n")

# -------------------------
# .env Check
# -------------------------
ENV_FILE = ".env"
if not os.path.exists(ENV_FILE):
    print(f"❌ {ENV_FILE} missing. Copy .env.example and fill required values.")
else:
    print(f"✅ {ENV_FILE} found and loaded")

required_env = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ADMIN_ID",
    "TELEGRAM_CHANNEL_ID",
    "DATABASE_URL",
    "WEBHOOK_URL",
]

missing_env = []
for key in required_env:
    value = os.getenv(key)
    if not value:
        missing_env.append(key)

print("\n🌿 Checking environment variables...")
if missing_env:
    for m in missing_env:
        print(f"❌ {m} missing or empty")
else:
    for key in required_env:
        print(f"✅ {key} detected")

# -------------------------
# Python Modules Check
# -------------------------
modules = ["flask", "requests", "sqlalchemy", "aiohttp", "web3", "telegram", "dotenv"]
print("\n📦 Checking Python modules...")
for m in modules:
    if importlib.util.find_spec(m) is None:
        print(f"❌ Missing module: {m}")
    else:
        print(f"✅ Module loaded: {m}")

# -------------------------
# Database Check
# -------------------------
print("\n💾 Checking database...")
db_path = os.getenv("DATABASE_PATH", "subscriptions.db")
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        conn.close()
        print(f"✅ Database ready → {db_path}")
    except Exception as e:
        print(f"❌ Database exists but cannot connect: {e}")
else:
    print(f"❌ Database file missing → {db_path}")

# -------------------------
# Port & Internet Check
# -------------------------
PORT = int(os.getenv("PORT", 5000))
print("\n🔌 Checking port...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind(("0.0.0.0", PORT))
        print(f"✅ Port {PORT} is free")
    except OSError:
        print(f"❌ Port {PORT} is in use")

print("🌐 Checking internet connectivity...")
try:
    requests.get("https://google.com", timeout=5)
    print("✅ Internet connection OK")
except Exception:
    print("❌ Internet connection failed")

# -------------------------
# Project Files Check
# -------------------------
required_files = [
    "app.py",
    "main.py",
    "bot.py",
    "bot_handlers.py",
    "requirements.txt",
    "Dockerfile",
    "init_db.py",
    "start_icegods.py",
    "utils"
]

print("\n📁 Checking project files...")
for f in required_files:
    if os.path.exists(f):
        print(f"✅ Found: {f}")
    else:
        print(f"❌ Missing: {f}")

# -------------------------
# Summary
# -------------------------
print("\n🧩 DEPLOYMENT READINESS CHECK COMPLETE.")
print("💡 If all checks passed, the bot is ready to host.")
print("⚠️ Any missing modules, env vars, database, or files must be fixed before deployment.")
