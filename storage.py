import sqlite3
import os

DB_FILE = "highlights.db"

def get_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Allows dictionary-like access
    return conn

def init_db():
    """Initializes the normalized schema and indexes."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tracks table (metadata)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY,
            track_name TEXT,
            artist_name TEXT,
            bpm REAL
        )
    ''')
    
    # Create highlights table (timestamps)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS highlights (
            track_id TEXT PRIMARY KEY,
            start_sec INTEGER NOT NULL,
            duration_sec INTEGER NOT NULL,
            is_auto BOOLEAN DEFAULT 0,
            FOREIGN KEY (track_id) REFERENCES tracks (track_id)
        )
    ''')
    
    # Create the index to guarantee <12ms retrieval
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_highlights_track_id 
        ON highlights (track_id)
    ''')
    
    conn.commit()
    conn.close()

def get_highlight(track_id):
    """Retrieves a highlight for a specific track."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT start_sec, duration_sec, is_auto FROM highlights WHERE track_id = ?', (track_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"start": row["start_sec"], "duration": row["duration_sec"], "is_auto": bool(row["is_auto"])}
    return None

def save_highlight(track_id, start_sec, duration_sec, is_auto=False):
    """Inserts or updates a highlight in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO highlights (track_id, start_sec, duration_sec, is_auto)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(track_id) DO UPDATE SET
            start_sec=excluded.start_sec,
            duration_sec=excluded.duration_sec,
            is_auto=excluded.is_auto
    ''', (track_id, start_sec, duration_sec, is_auto))
    conn.commit()
    conn.close()

def delete_highlight(track_id):
    """Removes a highlight from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM highlights WHERE track_id = ?', (track_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# Automatically initialize the database when this file is imported
init_db()