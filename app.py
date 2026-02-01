import os, subprocess, psutil
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- IN-MEMORY PROCESS TRACKER ---
HOSTED_BOTS = {}

@app.route('/')
def dashboard():
    # In production, these pull from your Supabase DB
    stats = {
        "sol_revenue": "450.25 SOL",
        "eth_revenue": "18.10 ETH",
        "active_hosting": len(HOSTED_BOTS),
        "status": "ARMED / SUPREME",
        "newspaper": "🐋 WHALE ALERT: 5,000 SOL moved to Raydium LP"
    }
    return render_template('index.html', stats=stats)

@app.route('/deploy', methods=['POST'])
def deploy_bot():
    bot_token = request.form.get('token')
    # logic to trigger hosting after payment verification
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
