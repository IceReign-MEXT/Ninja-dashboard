import os, psycopg2
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_db_stats():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
    except: return 0

@app.route('/')
def index():
    user_count = get_db_stats()
    stats = {
        "sol": f"{245 + (user_count * 0.5)} SOL",
        "armies": 45 + user_count,
        "vol": "$12.4M",
        "rank": "1"
    }
    return render_template('index.html', stats=stats)

@app.route('/healthz')
def health(): return "ACTIVE", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 10000))
