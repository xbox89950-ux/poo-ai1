"""Structured activity log for Supervisor & Learning AI."""
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from config.settings import SETTINGS


class ActivityLog:
    def __init__(self, db_path=None):
        self.db_path = db_path or SETTINGS.DB_PATH
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS ai1_activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity_type TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    product_id TEXT,
                    summary_bn TEXT NOT NULL,
                    details_json TEXT NOT NULL
                )"""
            )

    def record(
        self,
        activity_type: str,
        summary_bn: str,
        product_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        occurred_at = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO ai1_activity_log(activity_type,occurred_at,product_id,summary_bn,details_json) VALUES(?,?,?,?,?)",
                (activity_type, occurred_at, product_id, summary_bn, json.dumps(details or {}, ensure_ascii=False)),
            )

    def recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM ai1_activity_log ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]
