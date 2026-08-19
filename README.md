# Curiosity

A lightweight, local-first context memory for AI agents.

Curiosity is an independent alternative to large context-database projects: it stores memories, skills, and knowledge snippets in SQLite and retrieves relevant context using a transparent lexical ranking algorithm. It is designed to be easy to run, inspect, test, and extend.

## Features

- Local SQLite storage with no external services.
- Memory CRUD with tags and metadata.
- Relevance-ranked context retrieval.
- Separate `memory`, `knowledge`, and `skill` namespaces.
- Simple Python API and CLI.
- Deterministic tests with the standard library only.
- No API keys required.

## Quick start

Requires Python 3.11+.

```bash
python -m curiosity add --kind memory --text "User prefers concise technical answers" --tags preference,style
python -m curiosity add --kind knowledge --text "SQLite supports full-text search through FTS5" --tags sqlite,search
python -m curiosity search "concise technical answers"
python -m curiosity list
```

For development:

```bash
python -m unittest discover -s tests -v
```

## Design

Curiosity intentionally keeps the core small:

1. `Store` persists records in SQLite.
2. `Ranker` tokenizes a query and scores records using weighted term overlap, tag matches, and recency.
3. `MemoryService` provides the stable application interface.
4. The CLI exposes the same service without requiring a web server.

This makes the project suitable as a foundation for an agent-memory layer while avoiding vendor lock-in or a mandatory vector database.

## Roadmap

- Optional embeddings/vector search adapter.
- FastAPI HTTP interface.
- Import/export to JSONL.
- Memory consolidation and deduplication.
- Agent/tool adapters.

## License

MIT
