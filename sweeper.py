import os
import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from web3 import Web3

# --- CONFIG ---
SOL_SAFETY = os.getenv("SOL_MAIN")
ETH_SAFETY = os.getenv("ETH_MAIN")
SOL_RPC = "https://mainnet.helius-rpc.com/?api-key=" + os.getenv("HELIUS_API_KEY")
ETH_RPC = os.getenv("ETHEREUM_RPC")

async def sweep_solana(private_keys):
    client = AsyncClient(SOL_RPC)
    receiver = SOL_SAFETY

    for key in private_keys:
        try:
            sender = Keypair.from_base58_string(key)
            balance_resp = await client.get_balance(sender.pubkey())
            balance = balance_resp.value

            if balance > 1000000: # Sweep if > 0.001 SOL
                # Leave a tiny bit for gas (lamports)
                amount_to_send = balance - 5000

                txn = Transaction().add(transfer(TransferParams(
                    from_pubkey=sender.pubkey(),
                    to_pubkey=receiver,
                    lamports=amount_to_send
                )))

                await client.send_transaction(txn, sender)
                print(f"🧹 Swept {amount_to_send/1e9} SOL from {sender.pubkey()}")
        except Exception as e:
            print(f"❌ Sweep failed for wallet: {e}")

def sweep_ethereum(private_keys):
    w3 = Web3(Web3.HTTPProvider(ETH_RPC))
    for key in private_keys:
        try:
            account = w3.eth.account.from_key(key)
            balance = w3.eth.get_balance(account.address)
            gas_price = w3.eth.gas_price
            gas_limit = 21000

            cost = gas_price * gas_limit
            if balance > cost:
                tx = {
                    'nonce': w3.eth.get_transaction_count(account.address),
                    'to': ETH_SAFETY,
                    'value': balance - cost,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'chainId': 1 # Mainnet
                }
                signed_tx = w3.eth.account.sign_transaction(tx, key)
                w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"🧹 Swept ETH from {account.address}")
        except Exception as e:
            print(f"❌ ETH Sweep failed: {e}")

# This runs when the boosting session expires
if __name__ == "__main__":
    # Example usage: python sweeper.py
    # In production, the bot calls this automatically
    pass
