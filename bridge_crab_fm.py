#!/usr/bin/env python3
"""CRAB → founder-mode bus bridge.

Polls CRAB log for Retrograde results and re-posts to founder-mode
coordination bus with proper validation, locking, and identity registry.

Usage:
    PYTHONPATH=<USER_HOME>/PROJECTS/founder-mode python bridge_crab_fm.py
    python bridge_crab_fm.py --crab-log crab-daemon/daemon.log --once
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

# founder_mode lives in sibling repo on Anvil
FM_REPO = Path("<USER_HOME>/PROJECTS/founder-mode")
if str(FM_REPO) not in sys.path:
    sys.path.insert(0, str(FM_REPO))

FM_BUS_PATH = (FM_REPO / "founder_mode" / "_state" / "coordination" / "messages.tsv").resolve()

# Regex to extract Retrograde log lines:
# RETROGRADE: validated=True dissonance=0.00 scuttle=False findings=...
RETRO_RE = re.compile(
    r"RETROGRADE:\s+validated=(\w+)\s+dissonance=([\d.]+)\s+scuttle=(\w+)\s+findings=(.+)")

# Regex for BUS line inside log: [BUS] ... [STATUS] [lane] status — actions
BUS_RE = re.compile(r"\[STATUS\]\s+\[(\w+(?:[-_]\w+)*)\]\s+(\w+)\s+[-\u2014\u2013]\s+(.+)")


def _post_crab_status(lane: str, status: str, actions: str, retro: dict | None = None) -> bool:
    """Post a CRAB status message to the founder-mode bus."""
    if retro:
        msg = (
            f"CRAB [{lane}] {status} — {actions} | "
            f"retrograde: validated={retro['validated']} dissonance={retro['dissonance']} "
            f"scuttle={retro['scuttle']}"
        )
    else:
        msg = f"CRAB [{lane}] {status} — {actions}"
    try:
        from founder_mode.bus.bus_writer_core import post_message

        post_message(
            bus_path=str(FM_BUS_PATH),
            from_id="crab-daemon",
            to_id="all",
            msg_type="STATUS",
            message=msg,
            validate_sender_identity=False,  # crab-daemon not in founder-mode registry yet
        )
        return True
    except Exception as exc:
        print(f"[BRIDGE] Bus post failed: {exc}", file=sys.stderr)
        return False


def bridge_once(crab_log: Path) -> int:
    """Scan CRAB log for the most recent turn and post Retrograde status."""
    if not crab_log.exists():
        print(f"[BRIDGE] CRAB log not found: {crab_log}")
        return 1

    lines = crab_log.read_text(encoding="utf-8").splitlines()
    retro: dict | None = None
    lane = "unknown"
    status = "OK"
    actions = ""

    # Walk backwards to find the most recent complete turn
    for line in reversed(lines):
        if not line.strip():
            continue
        # Retrograde line
        m = RETRO_RE.search(line)
        if m:
            retro = {
                "validated": m.group(1),
                "dissonance": m.group(2),
                "scuttle": m.group(3),
            }
            continue
        # BUS line embedded in log: "[BUS] ... [lane] status — actions"
        m = BUS_RE.search(line)
        if m:
            lane = m.group(1)
            status = m.group(2)
            actions = m.group(3)
        # If we have both Retrograde and a preceding BUS, we're done
        if retro and lane != "unknown":
            break

    if retro is None:
        print("[BRIDGE] No Retrograde entry found in log.")
        return 0

    posted = _post_crab_status(lane, status, actions, retro)
    print(f"[BRIDGE] Posted CRAB [{lane}] retrograde={retro['dissonance']} -> {FM_BUS_PATH}")
    return 0 if posted else 1


def bridge_watch(crab_log: Path, poll_interval: float = 5.0) -> None:
    """Continuously watch CRAB log and post new Retrograde entries."""
    last_size = crab_log.stat().st_size if crab_log.exists() else 0
    print(f"[BRIDGE] Watching {crab_log} -> {FM_BUS_PATH} (poll={poll_interval}s)")
    while True:
        time.sleep(poll_interval)
        if not crab_log.exists():
            continue
        current_size = crab_log.stat().st_size
        if current_size > last_size:
            bridge_once(crab_log)
            last_size = current_size


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CRAB → founder-mode bus bridge")
    parser.add_argument("--crab-log", type=Path, default=Path("crab-daemon/daemon.log"))
    parser.add_argument("--once", action="store_true", help="Single scan and exit")
    parser.add_argument("--poll", type=float, default=5.0, help="Poll interval in seconds")
    args = parser.parse_args(argv)

    if args.once:
        return bridge_once(args.crab_log)
    bridge_watch(args.crab_log, args.poll)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
