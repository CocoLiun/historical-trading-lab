"""SQLite persistence for local development. Cloud disks may be ephemeral."""
from contextlib import closing
import json
import os
import sqlite3
from pathlib import Path

def db_path():
    return os.environ.get("HTL_DB_PATH", "data/historical_trading_lab.sqlite3")

def connect():
    path = Path(db_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("PRAGMA journal_mode=WAL")
    return con

def initialize():
    with closing(connect()) as con, con:
        con.execute("""CREATE TABLE IF NOT EXISTS datasets (
            fingerprint TEXT PRIMARY KEY, filename TEXT NOT NULL,
            content BLOB NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS sessions (
            session_name TEXT PRIMARY KEY, state_json TEXT NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

def save_dataset(fingerprint, filename, content):
    with closing(connect()) as con, con:
        con.execute("INSERT INTO datasets(fingerprint,filename,content) VALUES(?,?,?) ON CONFLICT(fingerprint) DO NOTHING",
                    (fingerprint, filename, sqlite3.Binary(content)))

def load_dataset(fingerprint):
    with closing(connect()) as con, con:
        row = con.execute("SELECT filename,content FROM datasets WHERE fingerprint=?", (fingerprint,)).fetchone()
    return (row[0], bytes(row[1])) if row else None

def save_session(name, state):
    payload = json.dumps(state, ensure_ascii=False)
    with closing(connect()) as con, con:
        con.execute("""INSERT INTO sessions(session_name,state_json,updated_at)
            VALUES(?,?,CURRENT_TIMESTAMP)
            ON CONFLICT(session_name) DO UPDATE SET
            state_json=excluded.state_json, updated_at=CURRENT_TIMESTAMP""", (name, payload))

def load_session(name):
    with closing(connect()) as con, con:
        row = con.execute("SELECT state_json FROM sessions WHERE session_name=?", (name,)).fetchone()
    return json.loads(row[0]) if row else None

def list_sessions():
    with closing(connect()) as con, con:
        return [r[0] for r in con.execute("SELECT session_name FROM sessions ORDER BY session_name")]
