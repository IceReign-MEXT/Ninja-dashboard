from solders.keypair import Keypair
import json

def create_army():
    army = []
    print("⚔️ GENERATING 12 GHOST WALLETS...")
    for i in range(12):
        kp = Keypair()
        army.append({
            "id": i + 1,
            "public_key": str(kp.pubkey()),
            "private_key": kp.to_json()
        })
    
    with open("ghost_wallets.json", "w") as f:
        json.dump(army, f, indent=4)
    
    print("✅ ARMY READY. Check 'ghost_wallets.json' for your keys.")
    print("⚠️ FUND THESE WALLETS WITH 0.1 SOL EACH TO START THE WAR.")

if __name__ == "__main__":
    create_army()
