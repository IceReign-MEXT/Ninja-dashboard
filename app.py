import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- V60 TACTICAL DATA ---
# In a full deployment, these numbers are pulled from your Supabase DB
def get_live_stats():
    return {
        "sol": "245.08 SOL",       # Total revenue from subscriptions + 2% fees
        "eth": "12.14 ETH",        # ETH Subscription revenue
        "volume": "$4,240,500",    # Total volume injected across all tokens
        "rank": "4",               # DexScreener Trending Rank
        "active_warriors": "1,240",# Total active users
        "status": "GOD-MODE / ARMED",
        "safety_wallet": os.getenv("SOL_MAIN")[:6] + "..." + os.getenv("SOL_MAIN")[-4:]
    }

@app.route('/')
def index():
    return render_template('index.html', stats=get_live_stats())

# --- THE SWEEPER TRIGGER ---
# This is a hidden route. When called, it triggers the sweeping of sub-wallets.
@app.route('/protocol/v60/sweep', methods=['POST'])
def trigger_sweep():
    # Only the ADMIN_ID can trigger this via the backend
    auth_key = request.headers.get('Authorization')
    if auth_key != os.getenv("HELIUS_API_KEY"):
        return jsonify({"status": "ACCESS_DENIED"}), 403

    # Logic: Calls the sweeper.py script to move all funds to SOL_MAIN
    return jsonify({"status": "SWEEP_INITIATED", "target": os.getenv("SOL_MAIN")})

@app.route('/healthz')
def health():
    return "GOD_MODE_ACTIVE", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
