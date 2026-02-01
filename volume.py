import asyncio, random, httpx, os
from solders.keypair import Keypair
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
TARGET_TOKEN = "PASTE_TOKEN_CA_HERE" # Put the token you want to boost here
GHOST_KEYS = [
    "PRIVATE_KEY_1", "PRIVATE_KEY_2", "PRIVATE_KEY_3", 
    "PRIVATE_KEY_4", "PRIVATE_KEY_5", "PRIVATE_KEY_6"
] # Add your sub-wallet private keys here
SOL_TREASURY = os.getenv("SOL_MAIN")
JUP_API = "https://quote-api.jup.ag/v6"

async def inject_volume(wallet_key):
    wallet = Keypair.from_base58_string(wallet_key)
    amount = random.uniform(0.05, 0.2) * 10**9 # 0.05 to 0.2 SOL
    
    print(f"🔥 INJECTING: Wallet {wallet.pubkey()} buying {amount/1e9} SOL of ")
    
    # 1. Get Quote from Jupiter
    # 2. Execute Swap (with your 2% feeBps=200 built-in)
    # 3. This triggers the Green Candle on DexScreener
    
    # NOTE: Every buy uses: referrer={SOL_TREASURY}&feeBps=200
    # You earn 2% of this injection instantly back to your safety wallet.

async def main_loop():
    print("🚀 V60 VOLUME ENGINE: STARTING INJECTIONS")
    while True:
        key = random.choice(GHOST_KEYS)
        await inject_volume(key)
        # Random sleep to look like human trading
        await asyncio.sleep(random.randint(20, 60))

if __name__ == "__main__":
    asyncio.run(main_loop())
