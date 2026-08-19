from __future__ import annotations

from pathlib import Path

from .models import Memory, SearchResult
from .ranker import Ranker
from .store import Store


class MemoryService:
    def __init__(self, db_path: str | Path = "curiosity.db") -> None:
        self.store = Store(db_path)
        self.ranker = Ranker()

    def remember(self, text: str, *, kind: str = "memory", tags: list[str] | None = None, metadata: dict[str, str] | None = None) -> Memory:
        return self.store.add(Memory(None, kind, text, tuple(tags or []), metadata or {}))

    def search(self, query: str, *, kind: str | None = None, limit: int = 10) -> list[SearchResult]:
        return self.ranker.rank(query, self.store.list(kind), limit)

    def list(self, *, kind: str | None = None) -> list[Memory]:
        return self.store.list(kind)

    def forget(self, memory_id: int) -> bool:
        return self.store.delete(memory_id)
