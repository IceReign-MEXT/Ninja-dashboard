import os, random
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- SAAS METRICS (The "Million Dollar" View) ---
def get_saas_stats():
    # In a full-scale war, these would pull from your Supabase DB
    return {
        "sol_treasury": "452.10 SOL",
        "eth_treasury": "18.05 ETH",
        "active_armies": random.randint(45, 60), # Number of users who paid 0.5 SOL
        "total_volume": "$12.4M",
        "newspaper_headline": "🐋 WHALE ALERT: 15,000 SOL move detected in Pump.fun Root."
    }

@app.route('/')
def index():
    return render_template('index.html', stats=get_saas_stats())

@app.route('/healthz')
def health():
    return "GOD_MODE_ACTIVE", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
