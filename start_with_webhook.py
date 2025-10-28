#!/usr/bin/env python3
import os
import logging
from pyngrok import ngrok
import subprocess
from dotenv import load_dotenv, set_key

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load .env
dotenv_path = os.path.join(os.getcwd(), ".env")
if not os.path.exists(dotenv_path):
    logging.error(".env not found! Make sure .env exists.")
    exit(1)
load_dotenv(dotenv_path)

# Start ngrok tunnel
NGROK_AUTH_TOKEN = "30dxkFANa3LoR0RV57mBFSs6Ndz_47MGq6BqgwQehk22KgeWz"  # Your ngrok token
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

logging.info("Starting ngrok tunnel on port 5000...")
public_url = ngrok.connect(5000, bind_tls=True)
logging.info(f"Ngrok tunnel created: {public_url}")

# Update WEBHOOK_URL in .env automatically
set_key(dotenv_path, "WEBHOOK_URL", f"{public_url}/webhook")
logging.info("Updated WEBHOOK_URL in .env")

# Start the bot
logging.info("Starting Ninja-dashboard bot...")
subprocess.run(["python3", "start_icegods.py"])
