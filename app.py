import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def dashboard():
    # Simulated V50 Streams
    stats = {
        "revenue_sol": "142.08",
        "revenue_eth": "4.12",
        "volume_boosted": ".2M",
        "green_candles": "84",
        "active_warriors": "2,408"
    }
    return render_template('index.html', stats=stats)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
