import sqlite3
import os

DB_PATH = os.getenv("DATABASE_PATH", "subscriptions.db")

if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id TEXT NOT NULL,
                 plan TEXT NOT NULL
                 );""")
    conn.commit()
    conn.close()
    print("✅ Database created.")
else:
    print("✅ Database exists.")
