"""Fleet-standard bus base — TSV + JSONL backends, file locking, retention.

Copy this module into any repo that needs a local bus.
Zero third-party dependencies. Platform-aware locking (fcntl/msvcrt).
"""

from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class Backend(Enum):
    TSV = "tsv"
    JSONL = "jsonl"


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    """When to prune old messages. Zero means unlimited."""

    max_messages: int = 0
    max_age_days: int = 0


@dataclass(frozen=True, slots=True)
class BusConfig:
    """Bus configuration."""

    bus_file: Path
    backend: Backend = Backend.TSV
    retention: RetentionPolicy = field(default_factory=RetentionPolicy)
    identity: str = "agent"


class BusBase:
    """Append-only message bus with locking and retention."""

    _TSV_HEADER = "timestamp\tfrom\tto\ttype\tmessage\n"

    def __init__(self, config: BusConfig) -> None:
        self.config = config
        self._lock = _FileLock(config.bus_file)

    def post(self, from_: str, to: str, type_: str, message: str) -> None:
        """Append a message to the bus."""
        self._ensure_init()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with self._lock:
            if self.config.backend is Backend.TSV:
                line = f"{ts}\t{from_}\t{to}\t{type_}\t{message}\n"
                with self.config.bus_file.open("a", encoding="utf-8") as f:
                    f.write(line)
            else:
                record = {"timestamp": ts, "from": from_, "to": to, "type": type_, "message": message}
                with self.config.bus_file.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

            self._apply_retention()

    def read(self, limit: int = 50) -> list[dict[str, str]]:
        """Read the most recent N messages as dicts."""
        if not self.config.bus_file.exists():
            return []

        with self._lock:
            raw = self.config.bus_file.read_text(encoding="utf-8").strip().split("\n")

        if self.config.backend is Backend.TSV:
            if not raw or raw[0] != self._TSV_HEADER.strip():
                return []
            entries = raw[1:]
            rows: list[dict[str, str]] = []
            for line in entries:
                parts = line.split("\t")
                if len(parts) != 5:
                    continue
                rows.append(
                    {
                        "timestamp": parts[0],
                        "from": parts[1],
                        "to": parts[2],
                        "type": parts[3],
                        "message": parts[4],
                    }
                )
            return rows[-limit:]
        else:
            rows = []
            for line in raw:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            return rows[-limit:]

    def search(self, pattern: str, limit: int = 50) -> list[dict[str, str]]:
        """Case-insensitive search in message payloads."""
        all_msgs = self.read(limit=10000)
        pat = pattern.lower()
        return [m for m in all_msgs if pat in m.get("message", "").lower()][-limit:]

    def status(self) -> dict[str, Any]:
        """Bus statistics."""
        msgs = self.read(limit=10000)
        types: dict[str, int] = {}
        for m in msgs:
            t = m.get("type", "UNKNOWN")
            types[t] = types.get(t, 0) + 1
        return {
            "total": len(msgs),
            "by_type": types,
            "file": str(self.config.bus_file),
            "backend": self.config.backend.value,
        }

    def clear(self) -> None:
        """Truncate the bus (destructive)."""
        with self._lock:
            if self.config.backend is Backend.TSV:
                self.config.bus_file.write_text(self._TSV_HEADER, encoding="utf-8")
            else:
                self.config.bus_file.write_text("", encoding="utf-8")

    def _ensure_init(self) -> None:
        if self.config.bus_file.exists():
            return
        self.config.bus_file.parent.mkdir(parents=True, exist_ok=True)
        if self.config.backend is Backend.TSV:
            self.config.bus_file.write_text(self._TSV_HEADER, encoding="utf-8")
        else:
            self.config.bus_file.write_text("", encoding="utf-8")

    def _apply_retention(self) -> None:
        rp = self.config.retention
        if rp.max_messages <= 0 and rp.max_age_days <= 0:
            return

        all_msgs = self.read(limit=100000)
        cutoff = datetime.now(timezone.utc) - timedelta(days=rp.max_age_days)

        pruned: list[dict[str, str]] = []
        for m in all_msgs:
            if rp.max_age_days > 0:
                try:
                    ts = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
                    if ts < cutoff:
                        continue
                except (ValueError, KeyError):
                    pass
            pruned.append(m)

        if rp.max_messages > 0:
            pruned = pruned[-rp.max_messages:]

        if len(pruned) >= len(all_msgs):
            return

        tmp = self.config.bus_file.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            if self.config.backend is Backend.TSV:
                f.write(self._TSV_HEADER)
                for m in pruned:
                    f.write(
                        f"{m['timestamp']}\t{m['from']}\t{m['to']}\t{m['type']}\t{m['message']}\n"
                    )
            else:
                for m in pruned:
                    f.write(json.dumps(m, ensure_ascii=False) + "\n")
        os.replace(str(tmp), str(self.config.bus_file))


class _FileLock:
    """Context manager for platform-aware file locking.

    Uses a separate *.lock file so the data file remains openable
    while the lock is held (critical on Windows where msvcrt.locking
    is mandatory and would block re-opening the same path).
    """

    def __init__(self, path: Path) -> None:
        self.lock_file = path.with_suffix(path.suffix + ".lock")
        self._handle: Any = None

    def __enter__(self) -> None:
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        if platform.system() == "Windows":
            import msvcrt
            self._handle = open(self.lock_file, "a", encoding="utf-8")
            msvcrt.locking(self._handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            self._handle = open(self.lock_file, "a", encoding="utf-8")
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX)

    def __exit__(self, *args: Any) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None
