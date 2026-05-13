#!/usr/bin/env python3
"""CRAB Bus — local project bus for crab-specific events.

Follows the fleet TSV schema: timestamp\tfrom\tto\ttype\tmessage
Stdlib only. Bridges to global bus for STATUS/DECISION/BLOCKED/HANDOFF types.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from bus_base import Backend, BusBase, BusConfig, RetentionPolicy

BUS_FILE = Path(__file__).parent / "messages.tsv"
_GLOBAL_TYPES = {"STATUS", "DECISION", "BLOCKED", "HANDOFF"}


def _make_bus() -> BusBase:
    cfg = BusConfig(
        bus_file=BUS_FILE,
        backend=Backend.TSV,
        retention=RetentionPolicy(max_messages=5000, max_age_days=30),
        identity="crab",
    )
    return BusBase(cfg)


def write_bus(from_: str, to: str, type_: str, message: str) -> None:
    """Append a message to the local bus."""
    bus = _make_bus()
    bus.post(from_, to, type_, message)


def read_bus(limit: int = 50) -> list[list[str]]:
    """Read the most recent N messages."""
    bus = _make_bus()
    rows = bus.read(limit=limit)
    return [[r["timestamp"], r["from"], r["to"], r["type"], r["message"]] for r in rows]


def write_global(from_: str, to: str, type_: str, message: str) -> bool:
    """Bridge to the founder-mode global coordination bus."""
    try:
        subprocess.run(
            [
                sys.executable,
                "<USER_HOME>/bin/bus-global.py",
                "post", from_, to, type_, message,
            ],
            check=False,
            capture_output=True,
            timeout=10,
        )
        return True
    except Exception:
        return False


def cmd_post(args: argparse.Namespace) -> int:
    bus = _make_bus()
    bus.post(args.from_, args.to, args.type, args.message)
    if args.bridge and args.type in _GLOBAL_TYPES:
        ok = write_global(args.from_, args.to, args.type, args.message)
        print(f"Posted locally{' + global' if ok else ' (global failed)'}")
    else:
        print(f"Posted: [{args.type}] {args.message}")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    rows = read_bus(args.limit)
    if not rows:
        print("No messages.")
        return 0
    for row in rows:
        print(" | ".join(row))
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    bus = _make_bus()
    stats = bus.status()
    print("CRAB Bus Status")
    print("=" * 40)
    print(f"Total messages: {stats['total']}")
    for t, c in sorted(stats["by_type"].items()):
        print(f"  {t}: {c}")
    return 0


def cmd_clear(_args: argparse.Namespace) -> int:
    bus = _make_bus()
    bus.clear()
    print("Bus cleared.")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    bus = _make_bus()
    results = bus.search(args.pattern, limit=args.limit)
    if not results:
        print("No matches.")
        return 0
    for r in results:
        print(f"{r['timestamp']} | {r['from']} → {r['to']} | {r['type']} | {r['message']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crab-bus")
    sub = parser.add_subparsers(dest="command")

    p_post = sub.add_parser("post", help="Post a message")
    p_post.add_argument("from_", help="Sender identity")
    p_post.add_argument("to", help="Recipient")
    p_post.add_argument("type", help="Message type")
    p_post.add_argument("message", help="Payload")
    p_post.add_argument("--bridge", action="store_true", help="Bridge to global bus")
    p_post.set_defaults(func=cmd_post)

    p_read = sub.add_parser("read", help="Read recent messages")
    p_read.add_argument("--limit", type=int, default=50)
    p_read.set_defaults(func=cmd_read)

    p_status = sub.add_parser("status", help="Show bus stats")
    p_status.set_defaults(func=cmd_status)

    p_search = sub.add_parser("search", help="Search message payloads")
    p_search.add_argument("pattern", help="Search pattern")
    p_search.add_argument("--limit", type=int, default=50)
    p_search.set_defaults(func=cmd_search)

    p_clear = sub.add_parser("clear", help="Clear the bus log")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
