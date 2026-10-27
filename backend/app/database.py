import sqlite3
import json
from datetime import datetime
from app.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Datasets metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL,
        source_type TEXT NOT NULL,
        total_rows INTEGER DEFAULT 0,
        total_columns INTEGER DEFAULT 0,
        missing_count INTEGER DEFAULT 0,
        duplicate_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # Jobs metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        dataset_id TEXT NOT NULL,
        status TEXT NOT NULL,
        processing_mode TEXT NOT NULL,
        total_records INTEGER DEFAULT 0,
        duration_ms REAL DEFAULT 0,
        positive_count INTEGER DEFAULT 0,
        negative_count INTEGER DEFAULT 0,
        neutral_count INTEGER DEFAULT 0,
        unique_words INTEGER DEFAULT 0,
        metrics_json TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (dataset_id) REFERENCES datasets(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()
