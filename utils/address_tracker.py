# utils/address_tracker.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_status(wallet_address):
    if wallet_address.startswith("0x"):  # Ethereum wallet
        if not ETHERSCAN_API_KEY:
            return "Missing ETHERSCAN_API_KEY in .env file."

        url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["status"] == "1":
                return f"ETH Balance: {int(data['result']) / 10**18:.4f} ETH"
            else:
                return f"Error: {data.get('message', 'Failed to fetch ETH balance.')}"
        except Exception as e:
            return f"Error fetching ETH balance: {str(e)}"

    elif len(wallet_address) > 30:  # Likely Solana
        url = f"https://api.mainnet-beta.solana.com"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [wallet_address]
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers)
            sol = response.json()["result"]["value"] / 10**9
            return f"SOL Balance: {sol:.4f} SOL"
        except Exception as e:
            return f"Error fetching SOL balance: {str(e)}"

    else:
        return "Invalid wallet address."