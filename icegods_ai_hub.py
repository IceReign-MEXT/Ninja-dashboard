#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
from termcolor import colored

# ==========================
# Setup logging
# ==========================
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logging.info("Starting ICEGODS AI Hub...")

# ==========================
# Load environment variables
# ==========================
load_dotenv()

ETH_WALLET = os.getenv("ETH_WALLET")
SOL_WALLET = os.getenv("SOL_WALLET")
MAIN_ADMIN = os.getenv("MAIN_ADMIN_NAME")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
INFURA_API_KEY = os.getenv("INFURA_API_KEY")
ALCHEMY_ZORA_RPC = os.getenv("ALCHEMY_ZORA_RPC")
PROJECT_KEY_1 = os.getenv("PROJECT_KEY_1")

# ==========================
# Banner
# ==========================
banner = """
  ___ ___ ___ ___ ___ ___ ___ ___ ___
 |   |   |   |   |   |   |   |   |   |
 |  I  C  E  G  O  D  S   A  I  H  |
 |___|___|___|___|___|___|___|___|___|

        🥷 Welcome, Digital Ninja 🥷

Mission Briefing:
- Move silently through the hub directories.
- Detect missing files and environment keys.
- Track wallets and Telegram channels.
- Complete your scan without leaving traces.
"""
print(colored(banner, "cyan"))
logging.info("Displayed banner.")

# ==========================
# Bot/Service scan
# ==========================
bot_summary = [
    {".git": "None", "Status": "Incomplete"},
    {"utils": "address_tracker.py, __init__.py, extract_image_tokens.py, bot.py, sample_bot.py", "Status": "Active"},
    {"images": "None", "Status": "Incomplete"}
]

print("╒═══════════════╤═════════════════════════════════════════════════════════════════════════════════╤════════════╤════════════╕")
print("│ Bot/Service   │ Main Files                                                                      │ ENV Keys   │ Status     │")
print("╞═══════════════╪═════════════════════════════════════════════════════════════════════════════════╪════════════╪════════════╡")

for bot in bot_summary:
    name = list(bot.keys())[0]
    files = bot[name]
    status = bot["Status"]
    print(f"│ {name:<13} │ {files:<75} │ {0 if status=='Incomplete' else 1:<10} │ {status:<10} │")
    if status == "Incomplete":
        print(colored(f"⚠️ Ninja Alert: {name} is missing files or env keys!", "yellow"))
        logging.warning(f"{name} is missing files or env keys!")
    else:
        print(colored(f"✅ Ninja Stealth: {name} is fully operational.", "green"))
        logging.info(f"{name} is fully operational.")

print("╘═══════════════╧═════════════════════════════════════════════════════════════════════════════════╧════════════╧════════════╛")

# ==========================
# Wallet Summary
# ==========================
print("\n=== Wallet Summary ===")
print(f"ETH_WALLET: {ETH_WALLET or 'Not Found'}")
print(f"SOL_WALLET: {SOL_WALLET or 'Not Found'}")
logging.info(f"ETH_WALLET: {ETH_WALLET}, SOL_WALLET: {SOL_WALLET}")

# ==========================
# Telegram Summary
# ==========================
print("\n=== Telegram Summary ===")
print(f"Main Admin: {MAIN_ADMIN or 'N/A'}")
print(f"Channel ID: {CHANNEL_ID or 'N/A'}")
logging.info(f"Main Admin: {MAIN_ADMIN}, Channel ID: {CHANNEL_ID}")

# ==========================
# Blockchain API Keys
# ==========================
print("\n=== Blockchain API Keys ===")
print(f"ETHERSCAN_API_KEY: {ETHERSCAN_API_KEY or 'Not Found'}")
print(f"INFURA_API_KEY: {INFURA_API_KEY or 'Not Found'}")
print(f"ALCHEMY_ZORA_RPC: {ALCHEMY_ZORA_RPC or 'Not Found'}")
print(f"PROJECT_KEY_1: {PROJECT_KEY_1 or 'Not Found'}")
logging.info("Displayed all API keys status.")

print("\n[AI Ninja Scan Complete. Terminal dashboard active.]")
logging.info("ICEGODS AI Hub scan complete.")
