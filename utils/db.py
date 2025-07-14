# db.py

import sqlite3

DB_NAME = "planung.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Beispiel: Tabelle für Mitarbeiter
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mitarbeiter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            farbe TEXT
        )
    """)

    # Tabelle für Urlaube, Schichten, etc. folgt später

    conn.commit()
    conn.close()
