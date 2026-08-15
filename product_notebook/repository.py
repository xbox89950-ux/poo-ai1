"""SQLite persistence for Product Notebook and research history."""
import json
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from config.settings import SETTINGS
from product_notebook.models import ProductRecord


class ProductNotebook:
    def __init__(self, db_path=None):
        self.db_path = db_path or SETTINGS.DB_PATH
        self._init_schema()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    product_code TEXT,
                    product_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS product_research_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    researched_at TEXT NOT NULL,
                    research_json TEXT NOT NULL,
                    FOREIGN KEY(product_id) REFERENCES products(product_id)
                );
                """
            )

    def upsert(self, product: ProductRecord) -> None:
        now = datetime.now(timezone.utc).isoformat()
        payload = json.dumps(product.to_dict(), ensure_ascii=False)
        with self._connect() as conn:
            exists = conn.execute(
                "SELECT 1 FROM products WHERE product_id = ?", (product.product_id,)
            ).fetchone()
            if exists:
                conn.execute(
                    "UPDATE products SET product_code=?, product_name=?, category=?, data_json=?, updated_at=? WHERE product_id=?",
                    (product.product_code, product.product_name, product.category, payload, now, product.product_id),
                )
            else:
                conn.execute(
                    "INSERT INTO products(product_id,product_code,product_name,category,data_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                    (product.product_id, product.product_code, product.product_name, product.category, payload, now, now),
                )
            conn.execute(
                "INSERT INTO product_research_history(product_id, researched_at, research_json) VALUES(?,?,?)",
                (product.product_id, now, payload),
            )

    def get(self, product_id: str) -> Optional[ProductRecord]:
        with self._connect() as conn:
            row = conn.execute("SELECT data_json FROM products WHERE product_id=?", (product_id,)).fetchone()
        return ProductRecord(**json.loads(row["data_json"])) if row else None

    def history(self, product_id: str) -> List[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT researched_at, research_json FROM product_research_history WHERE product_id=? ORDER BY id DESC",
                (product_id,),
            ).fetchall()
        return [{"researched_at": r["researched_at"], "research": json.loads(r["research_json"])} for r in rows]
