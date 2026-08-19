from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class Memory:
    id: int | None
    kind: str
    text: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        if self.kind not in {"memory", "knowledge", "skill"}:
            raise ValueError("kind must be memory, knowledge, or skill")
        if not self.text.strip():
            raise ValueError("text must not be empty")


@dataclass(frozen=True)
class SearchResult:
    memory: Memory
    score: float
