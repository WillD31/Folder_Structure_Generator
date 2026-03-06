import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'stats.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_type TEXT NOT NULL,
                  language TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_event(event_type, language=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO events (event_type, language) VALUES (?, ?)", (event_type, language))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging event: {e}")

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total counts
    c.execute("SELECT event_type, COUNT(*) FROM events GROUP BY event_type")
    totals = dict(c.fetchall())
    
    # Stats by month and type
    c.execute('''SELECT strftime('%Y-%m', timestamp) as month, event_type, COUNT(*) 
                 FROM events 
                 GROUP BY month, event_type 
                 ORDER BY month DESC''')
    monthly_raw = c.fetchall()
    
    # Stats by language for generations
    c.execute('''SELECT language, COUNT(*) 
                 FROM events 
                 WHERE event_type = 'generation' 
                 GROUP BY language''')
    languages = dict(c.fetchall())
    
    conn.close()
    
    return {
        'totals': totals,
        'monthly': monthly_raw,
        'languages': languages
    }

if __name__ == "__main__":
    init_db()
