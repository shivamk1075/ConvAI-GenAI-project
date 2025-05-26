# storage.py

import sqlite3
import json
from datetime import datetime

# === Configuration ===
DB_FILE = "chat.db"
MAX_RECENT = 10     # must match summary_block_size in ChatSession

# === Initialize SQLite ===
_db = sqlite3.connect(DB_FILE, check_same_thread=False)
_db.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id     TEXT PRIMARY KEY,
    summary     TEXT    DEFAULT '',
    recent      TEXT    DEFAULT '[]',      -- JSON list of (role, text) tuples
    updated_at  TEXT
)
""")
_db.commit()

def _upsert_user(user_id: str, summary: str, recent: list):
    """
    Insert or update the user row with given summary and recent history.
    """
    recent_json = json.dumps(recent)
    now = datetime.utcnow().isoformat()
    _db.execute("""
        INSERT INTO users(user_id, summary, recent, updated_at)
          VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
          summary     = excluded.summary,
          recent      = excluded.recent,
          updated_at  = excluded.updated_at
    """, (user_id, summary, recent_json, now))
    _db.commit()

def load_user_state(user_id: str):
    """
    Fetch the persistent summary and the recent-history cache for a user.
    Returns (summary: str, recent_history: List[(role, text)]).
    """
    cur = _db.execute(
        "SELECT summary, recent FROM users WHERE user_id = ?", (user_id,)
    )
    row = cur.fetchone()
    if row:
        summary, recent_json = row
        try:
            recent_history = json.loads(recent_json)
        except Exception:
            recent_history = []
    else:
        summary = ""
        recent_history = []

    return summary, recent_history

def save_summary(user_id: str, summary: str):
    """
    Update only the rolling summary for this user (keeping recent history intact).
    """
    # fetch existing recent history
    _, recent_history = load_user_state(user_id)
    _upsert_user(user_id, summary, recent_history)

def append_to_cache(user_id: str, role: str, text: str):
    """
    Add a new turn to the recent-history list (JSON) in SQLite,
    trimming to the last MAX_RECENT entries.
    """
    summary, recent_history = load_user_state(user_id)
    recent_history.append((role, text))
    # keep only the last MAX_RECENT items
    recent_history = recent_history[-MAX_RECENT:]
    _upsert_user(user_id, summary, recent_history)

def get_recent_history(user_id: str):
    """
    Return the list of (role, text) tuples from SQLite for this user.
    """
    _, recent_history = load_user_state(user_id)
    return recent_history

def clear_cache(user_id: str):
    """
    Empty the recent-history list for this user.
    """
    summary, _ = load_user_state(user_id)
    _upsert_user(user_id, summary, [])
