import sqlite3
import os
from datetime import datetime

import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), 'stats.db')

def get_identifier(req):
    """Generate an anonymized unique identifier for the request based on IP address."""
    ip = req.remote_addr or 'unknown'
    return hashlib.sha256(ip.encode()).hexdigest()[:16]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_type TEXT NOT NULL,
                  language TEXT,
                  identifier TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_event(event_type, language=None, identifier=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO events (event_type, language, identifier) VALUES (?, ?, ?)", (event_type, language, identifier))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging event: {e}")

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total counts
    # For generations, we count every row
    c.execute("SELECT COUNT(*) FROM events WHERE event_type = 'generation'")
    gen_total = c.fetchone()[0]
    
    # For connections, we count unique (day, identifier)
    # COALESCE(identifier, id) ensures old data (pre-identifier) is still counted as 1-per-hit
    c.execute("SELECT COUNT(DISTINCT strftime('%Y-%m-%d', timestamp) || COALESCE(identifier, id)) FROM events WHERE event_type = 'connection'")
    conn_total = c.fetchone()[0]
    
    totals = {'generation': gen_total, 'connection': conn_total}
    
    # Stats by month and type
    # We'll calculate them separately and combine
    
    # Generations by month (simple count)
    c.execute('''SELECT strftime('%Y-%m', timestamp) as month, COUNT(*) 
                 FROM events 
                 WHERE event_type = 'generation'
                 GROUP BY month''')
    gen_monthly = {m: ('generation', count) for m, count in c.fetchall()}
    
    # Connections by month (sum of daily uniques)
    c.execute('''SELECT strftime('%Y-%m', timestamp) as month, COUNT(DISTINCT strftime('%Y-%m-%d', timestamp) || COALESCE(identifier, id))
                 FROM events 
                 WHERE event_type = 'connection'
                 GROUP BY month''')
    conn_monthly = {m: ('connection', count) for m, count in c.fetchall()}
    
    # Combine and sort
    all_months = sorted(set(list(gen_monthly.keys()) + list(conn_monthly.keys())), reverse=True)
    monthly_raw = []
    for m in all_months:
        if m in conn_monthly:
            monthly_raw.append((m, 'connection', conn_monthly[m][1]))
        if m in gen_monthly:
            monthly_raw.append((m, 'generation', gen_monthly[m][1]))
    
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
