"""SQLite database manager for Poo"""
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from config.settings import SETTINGS

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_path = SETTINGS.DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    context TEXT
                );
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS plugins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    enabled INTEGER DEFAULT 1,
                    config TEXT,
                    installed_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)
            logger.info("Database initialized")

    def save_conversation(self, user_msg: str, ai_resp: str, lang: str = "en", context: Optional[str] = None):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO conversations (user_message, ai_response, language, context) VALUES (?, ?, ?, ?)",
                (user_msg, ai_resp, lang, context)
            )

    def get_recent_context(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT user_message, ai_response FROM conversations ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [{"user": r["user_message"], "ai": r["ai_response"]} for r in reversed(rows)]

    def get_memory(self, key: str) -> Optional[str]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT value FROM memory WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else None

    def set_memory(self, key: str, value: str):
        with self._get_connection() as conn:
            conn.execute(
                """INSERT INTO memory (key, value, updated_at) VALUES (?, ?, ?)
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at""",
                (key, value, datetime.now().isoformat())
            )

    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM conversations ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def clear_history(self):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM conversations")

    def save_setting(self, key: str, value: str):
        with self._get_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))

    def get_setting(self, key: str, default: str = "") -> str:
        with self._get_connection() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else default

db = DatabaseManager()
