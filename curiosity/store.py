from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import Memory


class Store:
    """SQLite persistence layer for Curiosity."""

    def __init__(self, path: str | Path = "curiosity.db") -> None:
        self.path = str(path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    text TEXT NOT NULL,
                    tags TEXT NOT NULL DEFAULT '[]',
                    metadata TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memories_kind ON memories(kind)")

    def add(self, memory: Memory) -> Memory:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO memories(kind,text,tags,metadata,created_at) VALUES (?,?,?,?,?)",
                (memory.kind, memory.text, json.dumps(memory.tags), json.dumps(memory.metadata), memory.created_at),
            )
            return Memory(memory.id if memory.id is not None else cursor.lastrowid, memory.kind, memory.text, memory.tags, memory.metadata, memory.created_at)

    def list(self, kind: str | None = None) -> list[Memory]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM memories WHERE (? IS NULL OR kind=?) ORDER BY id DESC", (kind, kind)
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def get(self, memory_id: int) -> Memory | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()
        return self._from_row(row) if row else None

    def delete(self, memory_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _from_row(row: sqlite3.Row) -> Memory:
        return Memory(
            id=row["id"],
            kind=row["kind"],
            text=row["text"],
            tags=tuple(json.loads(row["tags"])),
            metadata=json.loads(row["metadata"]),
            created_at=row["created_at"],
        )
