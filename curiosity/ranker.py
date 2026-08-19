from __future__ import annotations

import math
import re
from collections import Counter

from .models import Memory, SearchResult

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,}", re.I)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class Ranker:
    """Deterministic relevance ranking with no model or network dependency."""

    def rank(self, query: str, memories: list[Memory], limit: int = 10) -> list[SearchResult]:
        if limit < 1:
            return []
        query_tokens = Counter(tokenize(query))
        if not query_tokens:
            return []

        results: list[SearchResult] = []
        for memory in memories:
            text_tokens = Counter(tokenize(memory.text))
            tag_tokens = {token.lower() for tag in memory.tags for token in tokenize(tag)}
            overlap = sum(min(count, text_tokens[token]) for token, count in query_tokens.items())
            if overlap == 0 and not (set(query_tokens) & tag_tokens):
                continue
            norm = math.sqrt(sum(v * v for v in query_tokens.values()))
            density = overlap / max(1, sum(text_tokens.values()))
            tag_bonus = 0.25 * len(set(query_tokens) & tag_tokens)
            score = (overlap / norm) + density + tag_bonus
            results.append(SearchResult(memory, round(score, 6)))

        results.sort(key=lambda item: (-item.score, -(item.memory.id or 0)))
        return results[:limit]
