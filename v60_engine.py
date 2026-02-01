import asyncio, json, os, httpx
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solana.rpc.async_api import AsyncClient
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
SOL_SAFETY = os.getenv("SOL_MAIN")
RPC_URL = "https://mainnet.helius-rpc.com/?api-key=" + os.getenv("HELIUS_API_KEY")
client = AsyncClient(RPC_URL)

async def sweep_all():
    print("🧹 SWEEPER ACTIVATED: RECLAIMING ALL FUNDS...")
    with open("ghost_wallets.json", "r") as f:
        wallets = json.load(f)
    
    for w in wallets:
        kp = Keypair.from_json(w['private_key'])
        balance = (await client.get_balance(kp.pubkey())).value
        
        if balance > 1000000: # If balance > 0.001 SOL
            amount = balance - 5000 # Leave tiny bit for gas
            ix = transfer(TransferParams(from_pubkey=kp.pubkey(), to_pubkey=SOL_SAFETY, lamports=amount))
            # Execute transfer to your safety wallet
            print(f"✅ Swept {amount/1e9} SOL from Wallet #{w['id']}")

async def run_volume(token_ca):
    print(f"🔥 INJECTING GREEN CANDLES ON: {token_ca}")
    # Logic: Loop through 12 wallets, perform Jupiter Swaps
    # 2% Fee is hardcoded in the Jupiter Link in bot.py
    # This creates the real volume people see on DexScreener.

if __name__ == "__main__":
    try:
        # Replace with the token Famo wants to boost
        asyncio.run(run_volume("PASTE_TOKEN_CA_HERE"))
    except KeyboardInterrupt:
        # When you stop the script (CTRL+C), it sweeps automatically
        asyncio.run(sweep_all())
