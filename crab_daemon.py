#!/usr/bin/env python3
"""CRAB Daemon — autonomous agent loop that runs unattended.

Implements the full CRAB protocol (Check → Reason → Act → Bus) as a
continuous background process. Each iteration of the loop is a "turn" that:

1. CHECK: reads live state (git, bus, stashes, blockers)
2. REASON: decides if action is needed, chooses message type
3. ACT: performs the work via configurable lane handlers
4. BUS: posts a coordination receipt

The daemon supports multiple "lanes" — independent work streams that can
each follow CRAB on their own schedule. Each lane is a self-contained
unit of autonomy.

CLI:
    ./crab_daemon.py --config path/to/config.json
    ./crab_daemon.py --once --lane cleanup
    ./crab_daemon.py --dry-run
    ./crab_daemon.py --init          # write default config and exit

Zero third-party dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = Path("crab-daemon/config.json")
DEFAULT_LOG_PATH = Path("crab-daemon/daemon.log")
DEFAULT_BUS_PATH = Path("bus/messages.tsv")
DEFAULT_IDENTITY = "crab-daemon"
DEFAULT_POLL_INTERVAL = 60.0
DEFAULT_LANE_COOLDOWN = 300.0

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    """Output of the CHECK phase."""

    timestamp: str
    branch: str
    dirty: bool
    stash_count: int
    bus_tail: list[dict]
    blockers: list[dict]
    health_status: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)


@dataclass
class ReasonResult:
    """Output of the REASON phase."""

    should_act: bool
    lane: str
    message_type: str
    rationale: str
    stop_condition: str | None = None


@dataclass
class ActResult:
    """Output of the ACT phase."""

    success: bool
    actions_taken: list[str]
    artifacts: list[str]
    errors: list[str]


@dataclass
class CrabTurn:
    """A complete CRAB turn."""

    check: CheckResult
    reason: ReasonResult
    act: ActResult
    bus_posted: bool = False
    bus_timestamp: str = ""


@dataclass
class LaneConfig:
    """Configuration for a single autonomous lane."""

    name: str
    enabled: bool = True
    interval_seconds: float = 300.0
    cooldown_seconds: float = 300.0
    max_actions_per_turn: int = 5
    stop_on_blocker: bool = True
    actions: list[str] = field(default_factory=list)


@dataclass
class BusConfig:
    """Bus backend configuration — pluggable."""

    backend: str = "tsv"  # "tsv", "jsonl", "callback", "stdout"
    path: str = str(DEFAULT_BUS_PATH)
    # For "callback" backend: a Python callable or shell command
    callback: str | None = None


@dataclass
class DaemonConfig:
    """Top-level daemon configuration."""

    identity: str = DEFAULT_IDENTITY
    bus: BusConfig = field(default_factory=BusConfig)
    log_path: str = str(DEFAULT_LOG_PATH)
    poll_interval: float = DEFAULT_POLL_INTERVAL
    lanes: list[LaneConfig] = field(default_factory=list)
    repo_root: str = "."
    dry_run: bool = False
    verbose: bool = False

    @classmethod
    def from_json(cls, path: Path) -> "DaemonConfig":
        raw = json.loads(path.read_text(encoding="utf-8"))
        bus_raw = raw.pop("bus", {})
        bus = BusConfig(**bus_raw)
        lanes = [LaneConfig(**l) for l in raw.pop("lanes", [])]
        return cls(bus=bus, lanes=lanes, **raw)

    def to_json(self, path: Path) -> None:
        raw = {
            "identity": self.identity,
            "bus": {
                "backend": self.bus.backend,
                "path": self.bus.path,
                "callback": self.bus.callback,
            },
            "log_path": self.log_path,
            "poll_interval": self.poll_interval,
            "repo_root": self.repo_root,
            "dry_run": self.dry_run,
            "verbose": self.verbose,
            "lanes": [
                {
                    "name": l.name,
                    "enabled": l.enabled,
                    "interval_seconds": l.interval_seconds,
                    "cooldown_seconds": l.cooldown_seconds,
                    "max_actions_per_turn": l.max_actions_per_turn,
                    "stop_on_blocker": l.stop_on_blocker,
                    "actions": l.actions,
                }
                for l in self.lanes
            ],
        }
        path.write_text(json.dumps(raw, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_shell(cmd: list[str], cwd: str | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124, stdout="", stderr="timeout")
    except Exception as e:
        return subprocess.CompletedProcess(cmd, returncode=1, stdout="", stderr=str(e))


def _repo_root(config: DaemonConfig) -> Path:
    return Path(config.repo_root).resolve()


# ---------------------------------------------------------------------------
# CHECK phase
# ---------------------------------------------------------------------------


def check_phase(config: DaemonConfig) -> CheckResult:
    repo = _repo_root(config)
    ts = _now()

    branch_proc = _run_shell(["git", "branch", "--show-current"], cwd=str(repo))
    branch = branch_proc.stdout.strip() if branch_proc.returncode == 0 else "unknown"

    status_proc = _run_shell(["git", "status", "--short"], cwd=str(repo))
    dirty = bool(status_proc.stdout.strip())

    stash_proc = _run_shell(["git", "stash", "list"], cwd=str(repo))
    stash_count = len([l for l in stash_proc.stdout.splitlines() if l.strip()])

    bus_tail: list[dict] = []
    bus_path = Path(config.bus.path)
    if bus_path.exists():
        try:
            lines = bus_path.read_text(encoding="utf-8").splitlines()
            for line in lines[-10:]:
                line = line.strip()
                if not line or line.startswith("timestamp"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 5:
                    bus_tail.append({"timestamp": parts[0], "from": parts[1], "to": parts[2], "type": parts[3], "message": parts[4]})
        except Exception as exc:
            logger.warning("Bus read failed: %s", exc)

    blockers = [m for m in bus_tail if m.get("type") == "BLOCKED"]

    return CheckResult(
        timestamp=ts, branch=branch, dirty=dirty,
        stash_count=stash_count, bus_tail=bus_tail, blockers=blockers,
    )


# ---------------------------------------------------------------------------
# REASON phase
# ---------------------------------------------------------------------------


def reason_phase(check: CheckResult, lane: LaneConfig) -> ReasonResult:
    if lane.stop_on_blocker and check.blockers:
        blocker = check.blockers[0]
        return ReasonResult(
            should_act=False, lane=lane.name, message_type="BLOCKED",
            rationale=f"Unresolved BLOCKED from {blocker['from']}: {blocker['message'][:80]}",
            stop_condition="unresolved_blocker",
        )

    if check.stash_count > 0 and "stash-sensitive" in lane.actions:
        return ReasonResult(
            should_act=False, lane=lane.name, message_type="STATUS",
            rationale=f"Stash non-empty ({check.stash_count}) — skipping stash-sensitive lane",
            stop_condition="non_empty_stash",
        )

    return ReasonResult(
        should_act=True, lane=lane.name, message_type="STATUS",
        rationale=f"Lane {lane.name} ready. Branch={check.branch}, dirty={check.dirty}, stashes={check.stash_count}",
    )


# ---------------------------------------------------------------------------
# ACT phase — built-in lane implementations
# ---------------------------------------------------------------------------


def _act_cleanup(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    actions: list[str] = []
    errors: list[str] = []
    repo = _repo_root(config)

    proc = _run_shell(["git", "branch", "-vv"], cwd=str(repo))
    gone = [line.strip() for line in proc.stdout.splitlines() if ": gone]" in line]
    if gone:
        actions.append(f"Found {len(gone)} stale [gone] branches")
        if not config.dry_run and "prune-gone" in lane.actions:
            for gb in gone:
                bname = gb.split()[0]
                _run_shell(["git", "branch", "-D", bname], cwd=str(repo))
            actions.append(f"Pruned {len(gone)} gone branches")
    else:
        actions.append("No stale [gone] branches found")

    proc = _run_shell(["git", "status", "--short"], cwd=str(repo))
    untracked = [l for l in proc.stdout.splitlines() if l.startswith("??")]
    if untracked:
        actions.append(f"{len(untracked)} untracked files")
    else:
        actions.append("Worktree clean (no untracked)")

    return ActResult(success=len(errors) == 0, actions_taken=actions, artifacts=[], errors=errors)


def _act_git_audit(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    """Audit lane: check repo health (equivalent to bus-audit but for the repo)."""
    actions: list[str] = []
    errors: list[str] = []
    repo = _repo_root(config)

    # Check for large untracked files
    proc = _run_shell(["git", "status", "--short"], cwd=str(repo))
    untracked = [l for l in proc.stdout.splitlines() if l.startswith("??")]
    if untracked:
        actions.append(f"{len(untracked)} untracked files in worktree")
    else:
        actions.append("Worktree clean")

    # Check for uncommitted changes
    modified = [l for l in proc.stdout.splitlines() if l.startswith((" M", "M ", "A ", " D", "D "))]
    if modified:
        actions.append(f"{len(modified)} modified/staged files")
    else:
        actions.append("No modified/staged files")

    # Check for stale locks
    lock_proc = _run_shell(["find", ".git", "-name", "*.lock", "-mmin", "+5"], cwd=str(repo))
    if lock_proc.stdout.strip():
        actions.append(f"Stale lock files detected: {lock_proc.stdout.strip()}")
    else:
        actions.append("No stale lock files")

    return ActResult(success=len(errors) == 0, actions_taken=actions, artifacts=[], errors=errors)


def _act_bus_audit(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    actions: list[str] = []
    errors: list[str] = []
    bus_path = Path(config.bus.path)
    if not bus_path.exists():
        errors.append(f"Bus file missing: {bus_path}")
        return ActResult(success=False, actions_taken=actions, artifacts=[], errors=errors)

    try:
        lines = bus_path.read_text(encoding="utf-8").splitlines()
        data_lines = [l for l in lines[1:] if l.strip()]
        actions.append(f"Bus has {len(data_lines)} messages")

        bad_lines = 0
        for line in data_lines[-100:]:
            parts = line.split("\t")
            if len(parts) < 5:
                bad_lines += 1
        if bad_lines:
            actions.append(f"{bad_lines} malformed lines in last 100")
        else:
            actions.append("Last 100 lines well-formed")

        identities = set()
        for line in data_lines[-500:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                identities.add(parts[1])
        actions.append(f"Recent identities: {', '.join(sorted(identities))[:200]}")

    except Exception as exc:
        errors.append(f"Bus audit failed: {exc}")

    return ActResult(success=len(errors) == 0, actions_taken=actions, artifacts=[], errors=errors)


LANE_REGISTRY: dict[str, Callable[[DaemonConfig, LaneConfig], ActResult]] = {
    "cleanup": _act_cleanup,
    "git-audit": _act_git_audit,
    "bus-audit": _act_bus_audit,
}


def act_phase(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    handler = LANE_REGISTRY.get(lane.name)
    if handler is None:
        return ActResult(
            success=False, actions_taken=[], artifacts=[],
            errors=[f"Unknown lane: {lane.name}. Registered: {list(LANE_REGISTRY.keys())}"],
        )
    return handler(config, lane)


# ---------------------------------------------------------------------------
# BUS phase — pluggable backends
# ---------------------------------------------------------------------------


def _bus_post_tsv(config: DaemonConfig, turn: CrabTurn, message: str) -> bool:
    bus_path = Path(config.bus.path)
    try:
        bus_path.parent.mkdir(parents=True, exist_ok=True)
        with bus_path.open("a", encoding="utf-8") as f:
            f.write(f"{_now()}\t{config.identity}\tall\t{turn.reason.message_type}\t{message}\n")
        return True
    except Exception as exc:
        logger.error("TSV bus post failed: %s", exc)
        return False


def _bus_post_jsonl(config: DaemonConfig, turn: CrabTurn, message: str) -> bool:
    path = Path(config.bus.path).with_suffix(".jsonl")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": _now(),
            "from": config.identity,
            "to": "all",
            "type": turn.reason.message_type,
            "message": message,
            "lane": turn.reason.lane,
            "success": turn.act.success,
        }
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return True
    except Exception as exc:
        logger.error("JSONL bus post failed: %s", exc)
        return False


def _bus_post_callback(config: DaemonConfig, turn: CrabTurn, message: str) -> bool:
    cb = config.bus.callback
    if not cb:
        logger.error("Callback backend selected but no callback configured")
        return False
    try:
        # Try as Python callable first (if running inside Python that has it)
        # Otherwise as shell command
        _run_shell(["sh", "-c", cb])
        return True
    except Exception as exc:
        logger.error("Callback bus post failed: %s", exc)
        return False


def _bus_post_stdout(config: DaemonConfig, turn: CrabTurn, message: str) -> bool:
    print(f"[BUS] {_now()} {config.identity} -> all [{turn.reason.message_type}] {message}")
    return True


BUS_BACKENDS: dict[str, Callable[[DaemonConfig, CrabTurn, str], bool]] = {
    "tsv": _bus_post_tsv,
    "jsonl": _bus_post_jsonl,
    "callback": _bus_post_callback,
    "stdout": _bus_post_stdout,
}


def bus_phase(config: DaemonConfig, turn: CrabTurn) -> bool:
    if config.dry_run:
        logger.info("[DRY RUN] Would post: %s %s %s",
                    config.identity, turn.reason.message_type, turn.reason.rationale)
        return True

    status = "OK" if turn.act.success else "FAIL"
    actions_str = "; ".join(turn.act.actions_taken[:3])
    if turn.act.errors:
        actions_str += f" | errors: {turn.act.errors[0][:100]}"
    message = f"[{turn.reason.lane}] {status} — {actions_str}"

    backend = BUS_BACKENDS.get(config.bus.backend, _bus_post_tsv)
    return backend(config, turn, message)


# ---------------------------------------------------------------------------
# Daemon core
# ---------------------------------------------------------------------------


class CrabDaemon:
    def __init__(self, config: DaemonConfig):
        self.config = config
        self._last_run: dict[str, float] = {}
        self._running = False

    def run_lane(self, lane: LaneConfig) -> CrabTurn:
        logger.info("=== CRAB turn: %s ===", lane.name)

        check = check_phase(self.config)
        logger.info("CHECK: branch=%s dirty=%s stashes=%s blockers=%d",
                    check.branch, check.dirty, check.stash_count, len(check.blockers))

        reason = reason_phase(check, lane)
        logger.info("REASON: should_act=%s type=%s rationale=%s",
                    reason.should_act, reason.message_type, reason.rationale)

        if not reason.should_act:
            act = ActResult(success=True, actions_taken=[reason.rationale], artifacts=[], errors=[])
            turn = CrabTurn(check=check, reason=reason, act=act, bus_posted=False)
            logger.info("Stopped: %s", reason.stop_condition)
            return turn

        act = act_phase(self.config, lane)
        logger.info("ACT: success=%s actions=%d errors=%d",
                    act.success, len(act.actions_taken), len(act.errors))

        turn = CrabTurn(check=check, reason=reason, act=act)
        turn.bus_posted = bus_phase(self.config, turn)
        turn.bus_timestamp = _now()
        logger.info("BUS: posted=%s", turn.bus_posted)

        return turn

    def run_once(self) -> list[CrabTurn]:
        turns: list[CrabTurn] = []
        now = time.monotonic()

        for lane in self.config.lanes:
            if not lane.enabled:
                continue
            last = self._last_run.get(lane.name, 0)
            if now - last < lane.cooldown_seconds:
                logger.debug("Lane %s in cooldown (%.0fs left)",
                             lane.name, lane.cooldown_seconds - (now - last))
                continue
            turn = self.run_lane(lane)
            turns.append(turn)
            self._last_run[lane.name] = now
            time.sleep(0.1)

        return turns

    def run(self) -> None:
        self._running = True
        logger.info("CRAB Daemon started — identity=%s lanes=%s",
                    self.config.identity,
                    [l.name for l in self.config.lanes if l.enabled])

        while self._running:
            try:
                self.run_once()
            except Exception as exc:
                logger.exception("Turn failed: %s", exc)
            time.sleep(self.config.poll_interval)

    def stop(self) -> None:
        self._running = False


# ---------------------------------------------------------------------------
# Default config factory
# ---------------------------------------------------------------------------


def default_config() -> DaemonConfig:
    return DaemonConfig(
        identity="crab-daemon",
        bus=BusConfig(backend="tsv", path=str(DEFAULT_BUS_PATH)),
        poll_interval=60.0,
        lanes=[
            LaneConfig(name="cleanup", enabled=True, interval_seconds=3600.0, cooldown_seconds=3600.0, actions=["prune-gone"]),
            LaneConfig(name="git-audit", enabled=True, interval_seconds=1800.0, cooldown_seconds=1800.0),
            LaneConfig(name="bus-audit", enabled=True, interval_seconds=600.0, cooldown_seconds=600.0),
        ],
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CRAB Daemon — autonomous agent loop")
    parser.add_argument("--config", type=Path, default=None, help="Path to config JSON")
    parser.add_argument("--init", action="store_true", help="Write default config and exit")
    parser.add_argument("--once", action="store_true", help="Run one iteration and exit")
    parser.add_argument("--lane", type=str, default=None, help="Run only this lane")
    parser.add_argument("--dry-run", action="store_true", help="Do not post to bus or mutate state")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    parser.add_argument("--identity", type=str, default=DEFAULT_IDENTITY, help="Bus identity")
    parser.add_argument("--repo-root", type=str, default=".", help="Repository root path")
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    config_path = args.config or DEFAULT_CONFIG_PATH
    if args.init:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        cfg = default_config()
        cfg.to_json(config_path)
        print(f"Default config written to: {config_path}")
        return 0

    if config_path.exists():
        cfg = DaemonConfig.from_json(config_path)
    else:
        logger.warning("Config not found at %s, using defaults", config_path)
        cfg = default_config()

    cfg.dry_run = args.dry_run or cfg.dry_run
    cfg.verbose = args.verbose or cfg.verbose
    cfg.identity = args.identity or cfg.identity
    cfg.repo_root = args.repo_root or cfg.repo_root

    if args.lane:
        for lane in cfg.lanes:
            lane.enabled = (lane.name == args.lane)

    daemon = CrabDaemon(cfg)

    if args.once:
        turns = daemon.run_once()
        for turn in turns:
            print(f"[{turn.reason.lane}] success={turn.act.success} bus={turn.bus_posted}")
        return 0 if all(t.act.success for t in turns) else 1

    try:
        daemon.run()
    except KeyboardInterrupt:
        logger.info("CRAB Daemon stopped by user")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
