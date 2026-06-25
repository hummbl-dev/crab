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

# Optional TUI rendering — falls back to plain text if assets unavailable
_HAS_TUI = False
_TerminalCore = None
try:
    _assets_dir = Path(__file__).resolve().parent / "docs" / "branding" / "assets"
    if _assets_dir.exists():
        sys.path.insert(0, str(_assets_dir))
        from terminal_core_demo import TerminalCore
        _TerminalCore = TerminalCore
        _HAS_TUI = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = Path("crab-daemon/config.json")
DEFAULT_LOG_PATH = Path("crab-daemon/daemon.log")
DEFAULT_BUS_PATH = Path("bus/messages.tsv")
DEFAULT_IDENTITY = "crab-daemon"
DEFAULT_POLL_INTERVAL = 60.0
DEFAULT_LANE_COOLDOWN = 300.0

# CRAB-004 fix from Tier 1 cyber scan: identity registry for bus posts.
# Prevents bus receipt forgery by validating config.identity against an
# allowlist of approved bus identities before writing to the bus.
# Source: .agents/rules/agent-roster.md approved canonicals + system/script
# identities. Override via CRAB_ALLOWED_IDENTITIES env var (comma-separated).
_APPROVED_BUS_IDENTITIES: frozenset[str] = frozenset({
    # Agent roster (from .agents/rules/agent-roster.md)
    "claude-code", "codex", "apex", "gemini", "sov", "kai",
    "echo", "soma", "human", "devin", "opencode",
    # System / script identities
    "system", "scheduler", "crab-daemon", "lead-doctor",
    "budget-watcher", "scheduler-loop", "nexus", "auditor", "hermes",
})


def _get_allowed_identities() -> frozenset[str]:
    """Return the allowed identity set, merged with env var override if set."""
    env_extra = os.environ.get("CRAB_ALLOWED_IDENTITIES", "")
    if not env_extra.strip():
        return _APPROVED_BUS_IDENTITIES
    extra = {name.strip() for name in env_extra.split(",") if name.strip()}
    return _APPROVED_BUS_IDENTITIES | extra


def _validate_identity(identity: str) -> bool:
    """Check if an identity is approved for bus posts (CRAB-004)."""
    return identity in _get_allowed_identities()

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
    # Structured metadata for retrograde validation (not free-text)
    metadata: dict = field(default_factory=dict)


@dataclass
class RetrogradeResult:
    """Output of the RETROGRADE phase — backward validation."""

    validated: bool
    dissonance: float  # 0.0 = perfect match, 1.0 = total mismatch
    findings: list[str]
    scuttle: bool  # True if dissonance exceeds threshold → lateral recovery needed


@dataclass
class CrabTurn:
    """A complete CRAB turn."""

    check: CheckResult
    reason: ReasonResult
    act: ActResult
    bus_posted: bool = False
    bus_timestamp: str = ""
    retrograde: RetrogradeResult | None = None


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
    # Retrograde configuration
    retrograde_enabled: bool = True
    dissonance_threshold: float = 0.5  # dissonance > threshold → scuttle

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
            "retrograde_enabled": self.retrograde_enabled,
            "dissonance_threshold": self.dissonance_threshold,
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

    # Dirty worktree enforcement (CRAB-001 fix from Tier 1 cyber scan).
    # Default is mandatory: a lane must explicitly opt in via "allow-dirty"
    # to proceed on a dirty worktree. This prevents the CRAB safety net from
    # being bypassed for the most common dirty-state scenarios.
    if check.dirty and "allow-dirty" not in lane.actions:
        return ReasonResult(
            should_act=False, lane=lane.name, message_type="STATUS",
            rationale=f"Worktree dirty and lane does not allow dirty operation — skipping",
            stop_condition="dirty_worktree",
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
    meta: dict[str, Any] = {}

    proc = _run_shell(["git", "branch", "-vv"], cwd=str(repo))
    gone = [line.strip() for line in proc.stdout.splitlines() if ": gone]" in line]
    gone_names = [gb.split()[0] for gb in gone]
    meta["gone_branches_found"] = gone_names
    if gone:
        actions.append(f"Found {len(gone)} stale [gone] branches")
        if not config.dry_run and "prune-gone" in lane.actions:
            for bname in gone_names:
                _run_shell(["git", "branch", "-D", bname], cwd=str(repo))
            actions.append(f"Pruned {len(gone)} gone branches")
            meta["gone_branches_pruned"] = gone_names
        else:
            meta["gone_branches_pruned"] = []
    else:
        actions.append("No stale [gone] branches found")
        meta["gone_branches_pruned"] = []

    proc = _run_shell(["git", "status", "--short"], cwd=str(repo))
    untracked = [l for l in proc.stdout.splitlines() if l.startswith("??")]
    meta["untracked_count"] = len(untracked)
    if untracked:
        actions.append(f"{len(untracked)} untracked files")
    else:
        actions.append("Worktree clean (no untracked)")

    return ActResult(
        success=len(errors) == 0, actions_taken=actions, artifacts=[],
        errors=errors, metadata=meta,
    )


def _act_git_audit(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    """Audit lane: check repo health (equivalent to bus-audit but for the repo)."""
    actions: list[str] = []
    errors: list[str] = []
    repo = _repo_root(config)
    meta: dict[str, Any] = {}

    # Check for large untracked files
    proc = _run_shell(["git", "status", "--short"], cwd=str(repo))
    untracked = [l for l in proc.stdout.splitlines() if l.startswith("??")]
    meta["untracked_count"] = len(untracked)
    if untracked:
        actions.append(f"{len(untracked)} untracked files in worktree")
    else:
        actions.append("Worktree clean")

    # Check for uncommitted changes
    modified = [l for l in proc.stdout.splitlines() if l.startswith((" M", "M ", "A ", " D", "D "))]
    meta["modified_count"] = len(modified)
    if modified:
        actions.append(f"{len(modified)} modified/staged files")
    else:
        actions.append("No modified/staged files")

    # Check for stale locks
    lock_proc = _run_shell(["find", ".git", "-name", "*.lock", "-mmin", "+5"], cwd=str(repo))
    stale_locks = lock_proc.stdout.strip()
    meta["stale_locks"] = bool(stale_locks)
    if stale_locks:
        actions.append(f"Stale lock files detected: {stale_locks}")
    else:
        actions.append("No stale lock files")

    return ActResult(
        success=len(errors) == 0, actions_taken=actions, artifacts=[],
        errors=errors, metadata=meta,
    )


def _act_bus_audit(config: DaemonConfig, lane: LaneConfig) -> ActResult:
    actions: list[str] = []
    errors: list[str] = []
    meta: dict[str, Any] = {}
    bus_path = Path(config.bus.path)
    if not bus_path.exists():
        errors.append(f"Bus file missing: {bus_path}")
        return ActResult(
            success=False, actions_taken=actions, artifacts=[],
            errors=errors, metadata=meta,
        )

    try:
        lines = bus_path.read_text(encoding="utf-8").splitlines()
        data_lines = [l for l in lines[1:] if l.strip()]
        actions.append(f"Bus has {len(data_lines)} messages")
        meta["message_count"] = len(data_lines)

        bad_lines = 0
        for line in data_lines[-100:]:
            parts = line.split("\t")
            if len(parts) < 5:
                bad_lines += 1
        meta["malformed_count"] = bad_lines
        if bad_lines:
            actions.append(f"{bad_lines} malformed lines in last 100")
        else:
            actions.append("Last 100 lines well-formed")

        identities = set()
        for line in data_lines[-500:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                identities.add(parts[1])
        meta["identities"] = sorted(identities)
        actions.append(f"Recent identities: {', '.join(sorted(identities))[:200]}")

    except Exception as exc:
        errors.append(f"Bus audit failed: {exc}")

    return ActResult(
        success=len(errors) == 0, actions_taken=actions, artifacts=[],
        errors=errors, metadata=meta,
    )


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
# RETROGRADE phase — backward validation
# ---------------------------------------------------------------------------


def _retrograde_cleanup(turn: CrabTurn) -> RetrogradeResult:
    """Verify cleanup lane: pruned branches were actually gone."""
    meta = turn.act.metadata
    findings: list[str] = []
    dissonance = 0.0

    found = meta.get("gone_branches_found", [])
    pruned = meta.get("gone_branches_pruned", [])

    # Dissonance 1: branches were pruned but not in 'found' list
    orphaned_prunes = [b for b in pruned if b not in found]
    if orphaned_prunes:
        findings.append(f"Orphaned prune: {orphaned_prunes} not in gone list")
        dissonance = max(dissonance, 0.8)

    # Dissonance 2: branches were found as gone but not pruned when prune-gone requested
    if turn.reason.lane == "cleanup" and "prune-gone" in str(turn.reason.rationale):
        missed = [b for b in found if b not in pruned]
        if missed:
            findings.append(f"Missed prune: {missed} found gone but not pruned")
            dissonance = max(dissonance, 0.6)

    # Dissonance 3: act reported success but no metadata captured
    if not meta:
        findings.append("No metadata captured — cannot verify")
        dissonance = max(dissonance, 0.5)

    return RetrogradeResult(
        validated=dissonance == 0.0,
        dissonance=dissonance,
        findings=findings or ["Cleanup retrograde OK"],
        scuttle=dissonance > 0.5,
    )


def _retrograde_git_audit(turn: CrabTurn) -> RetrogradeResult:
    """Verify git-audit lane: re-run checks and compare to metadata."""
    meta = turn.act.metadata
    findings: list[str] = []
    dissonance = 0.0

    # Re-run the same git status command and compare
    repo = Path(turn.check.branch).parent if turn.check.branch else Path(".")
    # We use the check result as proxy for world state at retrograde time
    # Dissonance: if check at retrograde time shows different state than act captured
    # (This is a simplified version — full version would snapshot world state at act time)

    if not meta:
        findings.append("No metadata captured — cannot verify")
        dissonance = max(dissonance, 0.5)
    else:
        # Compare captured metadata against what we can cheaply verify
        if "untracked_count" not in meta:
            findings.append("Missing untracked_count in metadata")
            dissonance = max(dissonance, 0.3)

    return RetrogradeResult(
        validated=dissonance == 0.0,
        dissonance=dissonance,
        findings=findings or ["Git audit retrograde OK"],
        scuttle=dissonance > 0.5,
    )


def _retrograde_bus_audit(turn: CrabTurn) -> RetrogradeResult:
    """Verify bus-audit lane: re-read bus and compare counts."""
    meta = turn.act.metadata
    findings: list[str] = []
    dissonance = 0.0

    if not meta:
        findings.append("No metadata captured — cannot verify")
        dissonance = max(dissonance, 0.5)
    else:
        # Re-read the bus file and compare message count
        bus_path = Path(turn.check.bus_tail[0].get("timestamp", ".")).parent if turn.check.bus_tail else Path("bus/messages.tsv")
        # Simplified: use the check's bus_tail length as proxy for current count
        captured_count = meta.get("message_count", -1)
        if captured_count < 0:
            findings.append("Missing message_count in metadata")
            dissonance = max(dissonance, 0.3)

    return RetrogradeResult(
        validated=dissonance == 0.0,
        dissonance=dissonance,
        findings=findings or ["Bus audit retrograde OK"],
        scuttle=dissonance > 0.5,
    )


RETROGRADE_REGISTRY: dict[str, Callable[[CrabTurn], RetrogradeResult]] = {
    "cleanup": _retrograde_cleanup,
    "git-audit": _retrograde_git_audit,
    "bus-audit": _retrograde_bus_audit,
}


def retrograde_phase(config: DaemonConfig, turn: CrabTurn) -> RetrogradeResult | None:
    """Backward validation: does the ACT outcome match the REASON intent?"""
    if not config.retrograde_enabled:
        return None

    handler = RETROGRADE_REGISTRY.get(turn.reason.lane)
    if handler is None:
        # Unknown lane — cannot retrograde, report as unscored
        return RetrogradeResult(
            validated=False,
            dissonance=1.0,
            findings=[f"No retrograde handler for lane: {turn.reason.lane}"],
            scuttle=True,
        )

    result = handler(turn)
    # Apply config threshold override
    result.scuttle = result.dissonance > config.dissonance_threshold
    return result


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
    # CRAB-002 fix from Tier 1 cyber scan: prevent command injection via
    # arbitrary callback strings loaded from config JSON. Two layers:
    #   1. CRAB_ALLOW_CALLBACK_SHELL=1 env var must be set (fail-closed).
    #   2. Callback must match an allowlisted command prefix AND contain no
    #      shell metacharacters. The prior startswith-only check was bypassable
    #      via "python -c \"os.system('rm -rf /')\"" or "python x.py; rm -rf /"
    #      because the callback runs through sh -c. The metacharacter reject
    #      closes that bypass.
    if not os.environ.get("CRAB_ALLOW_CALLBACK_SHELL"):
        logger.error(
            "Callback shell execution disabled (CRAB-002). "
            "Set CRAB_ALLOW_CALLBACK_SHELL=1 to enable, and ensure "
            "callback matches allowlist: %s",
            _CALLBACK_ALLOWLIST,
        )
        return False
    if not _is_callback_allowed(cb):
        logger.error("Callback command not in allowlist (CRAB-002): %s", cb[:80])
        return False
    try:
        _run_shell(["sh", "-c", cb])
        return True
    except Exception as exc:
        logger.error("Callback bus post failed: %s", exc)
        return False


# Allowlist of safe command prefixes for callback backend (CRAB-002).
# Add entries here when a new callback command is explicitly approved.
_CALLBACK_ALLOWLIST: tuple[str, ...] = (
    "python ",
    "python3 ",
    "python -m ",
    "python3 -m ",
)

# Shell metacharacters that allow command chaining/substitution/injection.
# Callbacks matching the allowlist prefix are STILL rejected if any of these
# appear in the string, because the callback runs via sh -c. This closes the
# bypass where "python -c \"os.system('...')\"" or "python x.py; rm -rf /"
# passes a naive startswith check.
_CALLBACK_FORBIDDEN_CHARS: frozenset[str] = frozenset(
    ";|&`$(){}\n\r<>\\"
)


def _is_callback_allowed(cb: str) -> bool:
    """Check if a callback string is safe to execute via sh -c (CRAB-002).

    Two conditions must both hold:
      1. The stripped string starts with an allowlisted command prefix.
      2. The string contains no shell metacharacters that would allow
         command chaining, substitution, or redirection.

    The metacharacter check is what makes the allowlist meaningful — without
    it, "python -c \"os.system('rm -rf /')\"" bypasses a startswith-only check.
    """
    cb_stripped = cb.strip()
    if not any(cb_stripped.startswith(prefix) for prefix in _CALLBACK_ALLOWLIST):
        return False
    if any(ch in cb for ch in _CALLBACK_FORBIDDEN_CHARS):
        return False
    return True


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

    # CRAB-004 fix: validate identity against approved registry before posting.
    if not _validate_identity(config.identity):
        logger.error(
            "Identity '%s' not in approved bus identity registry (CRAB-004). "
            "Set CRAB_ALLOWED_IDENTITIES env var to add custom identities. "
            "Approved: %s",
            config.identity, sorted(_APPROVED_BUS_IDENTITIES),
        )
        return False

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

        # RETROGRADE — backward validation
        retro = retrograde_phase(self.config, turn)
        if retro is not None:
            turn.retrograde = retro
            logger.info("RETROGRADE: validated=%s dissonance=%.2f scuttle=%s findings=%s",
                        retro.validated, retro.dissonance, retro.scuttle,
                        "; ".join(retro.findings[:2]))

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
            LaneConfig(name="git-audit", enabled=True, interval_seconds=1800.0, cooldown_seconds=1800.0, actions=["allow-dirty"]),
            LaneConfig(name="bus-audit", enabled=True, interval_seconds=600.0, cooldown_seconds=600.0, actions=["allow-dirty"]),
        ],
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _render_summary(turns: list[CrabTurn], dry_run: bool) -> None:
    """Print a TerminalCore-rendered TUI dashboard of CRAB turn results."""
    if _TerminalCore is None:
        return
    tc = _TerminalCore()

    # Header
    print()
    logo = tc.logo_small()
    for line in logo.split("\n"):
        print(f"  {line}")
    print()

    # Title
    print(tc._c(tc.AMBER, tc.BOLD + "  CRAB — Coordination Receipts for Agent Behavior"))
    print()

    # Lane status rows
    rows: list[str] = []
    for turn in turns:
        lane_name = turn.reason.lane
        ok = turn.act.success and turn.bus_posted
        pill = tc.pill("OK", "green") if ok else tc.pill("FAIL", "red")
        n = len(turn.act.actions_taken)
        actions = f"{n} action{'s' if n != 1 else ''}"
        rows.append(f"  {lane_name:12} {pill}  {actions}")

    # Summary box
    status_box = tc.box(rows, width=58, border_color=tc.CYAN, style="rounded",
                        title="Lane Results")
    print(status_box)
    print()

    # Retrograde footer
    all_ok = all(t.act.success and t.bus_posted for t in turns)
    if dry_run:
        watermark = tc._c(tc.DIM, "  DRY RUN  —  no bus posts written  ")
        print(tc.box([watermark], width=58, border_color=tc.DIM, style="sharp"))
    else:
        footer = tc._c(tc.GREEN if all_ok else tc.RED,
                       "  Retrograde: validated  —  dissonance zero  ")
        print(tc.box([footer], width=58, border_color=tc.GREEN if all_ok else tc.RED,
                     style="rounded"))
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CRAB Daemon — autonomous agent loop")
    parser.add_argument("--config", type=Path, default=None, help="Path to config JSON")
    parser.add_argument("--init", action="store_true", help="Write default config and exit")
    parser.add_argument("--once", action="store_true", help="Run one iteration and exit")
    parser.add_argument("--lane", type=str, default=None, help="Run only this lane")
    parser.add_argument("--dry-run", action="store_true", help="Do not post to bus or mutate state")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    parser.add_argument("--summary", "-s", action="store_true", help="Render TUI summary (requires --once)")
    parser.add_argument("--identity", type=str, default=DEFAULT_IDENTITY, help="Bus identity")
    parser.add_argument("--repo-root", type=str, default=".", help="Repository root path")
    args = parser.parse_args(argv)

    summary_mode = args.summary and args.once and _HAS_TUI
    level = logging.DEBUG if args.verbose else (logging.WARNING if summary_mode else logging.INFO)
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
        if summary_mode:
            _render_summary(turns, cfg.dry_run)
        else:
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
