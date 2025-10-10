import requests

def get_wallet_status(wallet_address):
    if not wallet_address:
        return "No wallet configured."
    try:
        if wallet_address.startswith("0x"):
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
            r = requests.get(url, timeout=10).json()
            if r.get("status") == "1":
                balance = int(r['result']) / 10**18
                return f"ETH Balance: {balance:.6f} ETH"
            return "Failed to fetch ETH balance."
        elif len(wallet_address) > 30:
            url = "https://api.mainnet-beta.solana.com"
            payload = {"jsonrpc":"2.0","id":1,"method":"getBalance","params":[wallet_address]}
            r = requests.post(url, json=payload, timeout=10).json()
            sol = r.get("result", {}).get("value")
            if sol is None:
                return "Failed to fetch SOL balance."
            return f"SOL Balance: {sol/10**9:.6f} SOL"
        else:
            return "Invalid wallet address."
    except Exception as e:
        return f"Error: {str(e)}"