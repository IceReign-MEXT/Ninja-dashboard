import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_stats():
    return {
        "sol": "245.08 SOL",
        "eth": "12.14 ETH",
        "volume": "$4.2M",
        "rank": "4",
        "status": "GOD-MODE ARMED",
        "safety": os.getenv("SOL_MAIN")[:6] + "..."
    }

@app.route('/')
def index():
    return render_template('index.html', stats=get_stats())

@app.route('/healthz')
def health(): return "ACTIVE", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
