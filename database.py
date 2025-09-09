import sqlite3
import os

DB_NAME = os.getenv("DB_NAME", "default.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[Database] База данных '{DB_NAME}' инициализирована.")

def get_last_seen_tweet_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM bot_state WHERE key = 'last_seen_tweet_id'")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def set_last_seen_tweet_id(tweet_id: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO bot_state (key, value) VALUES (?, ?)", ('last_seen_tweet_id', tweet_id))
    conn.commit()
    conn.close()