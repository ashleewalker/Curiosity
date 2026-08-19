from __future__ import annotations

import argparse
import json

from .service import MemoryService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="curiosity", description="Local-first memory for AI agents")
    parser.add_argument("--db", default="curiosity.db", help="SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Store a memory")
    add.add_argument("--kind", choices=["memory", "knowledge", "skill"], default="memory")
    add.add_argument("--text", required=True)
    add.add_argument("--tags", default="", help="Comma-separated tags")

    search = sub.add_parser("search", help="Retrieve relevant context")
    search.add_argument("query")
    search.add_argument("--kind", choices=["memory", "knowledge", "skill"])
    search.add_argument("--limit", type=int, default=10)

    listing = sub.add_parser("list", help="List stored context")
    listing.add_argument("--kind", choices=["memory", "knowledge", "skill"])

    forget = sub.add_parser("forget", help="Delete a memory by id")
    forget.add_argument("id", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = MemoryService(args.db)

    if args.command == "add":
        tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
        memory = service.remember(args.text, kind=args.kind, tags=tags)
        print(json.dumps({"id": memory.id, "kind": memory.kind, "text": memory.text, "tags": memory.tags}))
    elif args.command == "search":
        for result in service.search(args.query, kind=args.kind, limit=args.limit):
            print(json.dumps({"score": result.score, "id": result.memory.id, "kind": result.memory.kind, "text": result.memory.text, "tags": result.memory.tags}))
    elif args.command == "list":
        for memory in service.list(kind=args.kind):
            print(json.dumps({"id": memory.id, "kind": memory.kind, "text": memory.text, "tags": memory.tags}))
    elif args.command == "forget":
        if not service.forget(args.id):
            raise SystemExit(f"memory {args.id} not found")
        print(f"deleted {args.id}")


if __name__ == "__main__":
    main()
