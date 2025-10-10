#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from tabulate import tabulate
from termcolor import colored

# ==========================
# Load .env
# ==========================
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(colored("[WARNING] .env file not found!", "red"))

# ==========================
# Terminal AI Banner
# ==========================
banner = """
  ___ ___ ___ ___ ___ ___ ___ ___ ___
 |   |   |   |   |   |   |   |   |   |
 |  I  C  E  G  O  D  S   A  I  H  |
 |___|___|___|___|___|___|___|___|___|
"""
print(colored(banner, "cyan"))

# ==========================
# Scan Directories
# ==========================
ROOT_DIR = os.getcwd()
print(colored(f"Scanning root directory: {ROOT_DIR}", "green"))

folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

bot_summary = []

for folder in folders:
    bot_path = os.path.join(ROOT_DIR, folder)
    entries = os.listdir(bot_path)

    # Check for key files
    main_files = [f for f in entries if f.endswith('.py') or f.endswith('.js') or f.endswith('.Procfile')]

    # Instead of requiring folder-specific env keys, mark folders with files as Active
    status = "Incomplete"
    if main_files:
        status = "Active"

    bot_summary.append({
        "Bot/Service": folder,
        "Main Files": ", ".join(main_files) if main_files else "None",
        "ENV Keys": "N/A",  # Not relevant for local folders
        "Status": status
    })

# ==========================
# Display Table
# ==========================
table = tabulate(bot_summary, headers="keys", tablefmt="fancy_grid")
print(table)

# ==========================
# Terminal AI Alerts
# ==========================
for bot in bot_summary:
    if bot["Status"] == "Incomplete":
        print(colored(f"AI ALERT: {bot['Bot/Service']} is missing files!", "yellow"))

# ==========================
# Wallet & Payment Summary
# ==========================
eth_wallet = os.getenv("ETH_WALLET", "Not Found")
sol_wallet = os.getenv("SOL_WALLET", "Not Found")
print(colored("\n=== Wallet Summary ===", "magenta"))
print(f"ETH_WALLET: {eth_wallet}")
print(f"SOL_WALLET: {sol_wallet}")

# ==========================
# Telegram & Channel Info
# ==========================
main_admin = os.getenv("MAIN_ADMIN_NAME", "N/A")
channel_id = os.getenv("CHANNEL_ID", "N/A")
print(colored("\n=== Telegram Summary ===", "magenta"))
print(f"Main Admin: {main_admin}")
print(f"Channel ID: {channel_id}")

# ==========================
# End
# ==========================
print(colored("\n[AI] Scan complete. Terminal dashboard active.", "cyan"))
