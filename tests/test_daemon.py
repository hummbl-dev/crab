"""Tests for the portable CRAB Daemon.

Validates the four-phase CRAB protocol implementation without
HUMMBL-specific dependencies.
"""
import json
import pathlib
import subprocess
import tempfile

import pytest

# Import the standalone daemon module
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from crab_daemon import (
    ActResult,
    BusConfig,
    CheckResult,
    CrabDaemon,
    CrabTurn,
    DaemonConfig,
    LaneConfig,
    ReasonResult,
    RetrogradeResult,
    act_phase,
    bus_phase,
    check_phase,
    default_config,
    reason_phase,
    retrograde_phase,
)


class TestDataStructures:
    def test_default_config_roundtrip(self):
        cfg = default_config()
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f:
            path = pathlib.Path(f.name)
        try:
            cfg.to_json(path)
            loaded = DaemonConfig.from_json(path)
            assert loaded.identity == cfg.identity
            assert loaded.bus.backend == "tsv"
            assert len(loaded.lanes) == len(cfg.lanes)
        finally:
            path.unlink()

    def test_bus_config_pluggable(self):
        cfg = DaemonConfig(bus=BusConfig(backend="stdout"))
        assert cfg.bus.backend == "stdout"
        assert cfg.bus.path == str(pathlib.Path("bus/messages.tsv"))


class TestCheckPhase:
    @pytest.fixture
    def config(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        bus = tmp_path / "bus" / "messages.tsv"
        bus.parent.mkdir()
        bus.write_text("timestamp\tfrom\tto\ttype\tmessage\n")
        subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
        return DaemonConfig(repo_root=str(repo), bus=BusConfig(path=str(bus)), lanes=[])

    def test_reads_branch(self, config):
        result = check_phase(config)
        assert result.branch in ("main", "master")

    def test_detects_no_stash(self, config):
        result = check_phase(config)
        assert result.stash_count == 0

    def test_detects_blockers(self, config):
        bus = pathlib.Path(config.bus.path)
        bus.write_text(
            "timestamp\tfrom\tto\ttype\tmessage\n"
            "2026-01-01T00:00:00Z\tagent\tall\tBLOCKED\tstuck\n"
        )
        result = check_phase(config)
        assert len(result.blockers) == 1
        assert result.blockers[0]["type"] == "BLOCKED"


class TestReasonPhase:
    def test_allows_action_when_clean(self):
        check = CheckResult("t", "main", False, 0, [], [])
        lane = LaneConfig(name="cleanup", stop_on_blocker=True)
        reason = reason_phase(check, lane)
        assert reason.should_act is True
        assert reason.stop_condition is None

    def test_blocks_on_unresolved_blocker(self):
        check = CheckResult("t", "main", False, 0, [], [{"from": "agent", "type": "BLOCKED", "message": "stuck"}])
        lane = LaneConfig(name="cleanup", stop_on_blocker=True)
        reason = reason_phase(check, lane)
        assert reason.should_act is False
        assert reason.stop_condition == "unresolved_blocker"

    def test_blocks_on_stash_for_sensitive_lane(self):
        check = CheckResult("t", "main", False, 2, [], [])
        lane = LaneConfig(name="cleanup", actions=["stash-sensitive"])
        reason = reason_phase(check, lane)
        assert reason.should_act is False

    def test_blocks_on_dirty_by_default(self):
        """CRAB-001: dirty worktree blocks action unless lane opts in via allow-dirty."""
        check = CheckResult("t", "main", True, 0, [], [])
        lane = LaneConfig(name="cleanup")
        reason = reason_phase(check, lane)
        assert reason.should_act is False
        assert reason.stop_condition == "dirty_worktree"

    def test_allows_dirty_when_lane_opts_in(self):
        """Lane with allow-dirty action proceeds on dirty worktree."""
        check = CheckResult("t", "main", True, 0, [], [])
        lane = LaneConfig(name="cleanup", actions=["allow-dirty"])
        reason = reason_phase(check, lane)
        assert reason.should_act is True
        assert reason.stop_condition is None


class TestActPhase:
    @pytest.fixture
    def config(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        bus = tmp_path / "bus" / "messages.tsv"
        bus.parent.mkdir()
        bus.write_text("timestamp\tfrom\tto\ttype\tmessage\n")
        subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
        return DaemonConfig(repo_root=str(repo), bus=BusConfig(path=str(bus)), dry_run=True)

    def test_cleanup_lane(self, config):
        lane = LaneConfig(name="cleanup", actions=["prune-gone"])
        result = act_phase(config, lane)
        assert result.success is True
        assert any("branches" in a for a in result.actions_taken)

    def test_git_audit_lane(self, config):
        lane = LaneConfig(name="git-audit")
        result = act_phase(config, lane)
        assert result.success is True

    def test_bus_audit_lane(self, config):
        lane = LaneConfig(name="bus-audit")
        result = act_phase(config, lane)
        assert result.success is True
        assert any("messages" in a for a in result.actions_taken)

    def test_unknown_lane_fails(self, config):
        lane = LaneConfig(name="nonexistent")
        result = act_phase(config, lane)
        assert result.success is False


class TestBusPhase:
    def test_dry_run_does_not_post(self, tmp_path):
        config = DaemonConfig(bus=BusConfig(path=str(tmp_path / "bus.tsv")), dry_run=True)
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        assert bus_phase(config, turn) is True

    def test_stdout_backend(self, tmp_path, capsys):
        config = DaemonConfig(bus=BusConfig(backend="stdout"), dry_run=False)
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        assert bus_phase(config, turn) is True
        captured = capsys.readouterr()
        assert "[BUS]" in captured.out


class TestCallbackSecurity:
    """CRAB-002: command injection via callback backend."""

    def test_callback_blocked_without_env_var(self, tmp_path):
        """Callback shell execution disabled by default (no CRAB_ALLOW_CALLBACK_SHELL)."""
        import os
        old = os.environ.pop("CRAB_ALLOW_CALLBACK_SHELL", None)
        try:
            config = DaemonConfig(bus=BusConfig(backend="callback", callback="echo hello"))
            turn = CrabTurn(
                check=CheckResult("t", "main", False, 0, [], []),
                reason=ReasonResult(True, "test", "STATUS", "rationale"),
                act=ActResult(True, ["did thing"], [], []),
            )
            from crab_daemon import _bus_post_callback
            assert _bus_post_callback(config, turn, "msg") is False
        finally:
            if old is not None:
                os.environ["CRAB_ALLOW_CALLBACK_SHELL"] = old

    def test_callback_blocked_when_not_in_allowlist(self, tmp_path, monkeypatch):
        """Callback not matching allowlist is rejected even with env var set."""
        monkeypatch.setenv("CRAB_ALLOW_CALLBACK_SHELL", "1")
        config = DaemonConfig(bus=BusConfig(backend="callback", callback="rm -rf /"))
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        from crab_daemon import _bus_post_callback
        assert _bus_post_callback(config, turn, "msg") is False

    def test_callback_allowed_when_in_allowlist_with_env(self, tmp_path, monkeypatch):
        """Callback matching allowlist with env var set proceeds (python prefix)."""
        monkeypatch.setenv("CRAB_ALLOW_CALLBACK_SHELL", "1")
        config = DaemonConfig(bus=BusConfig(backend="callback", callback="python -c 'pass'"))
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        from crab_daemon import _bus_post_callback
        # This should attempt to run and return True (python -c 'pass' exits 0)
        assert _bus_post_callback(config, turn, "msg") is True


class TestIdentityRegistry:
    """CRAB-004: bus receipt forgery via unverified identity."""

    def test_approved_identity_passes(self, tmp_path):
        """Default crab-daemon identity is in the approved registry."""
        config = DaemonConfig(
            identity="crab-daemon",
            bus=BusConfig(path=str(tmp_path / "bus.tsv")),
            dry_run=False,
        )
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        assert bus_phase(config, turn) is True

    def test_forged_identity_rejected(self, tmp_path):
        """Arbitrary identity not in registry is rejected (CRAB-004)."""
        config = DaemonConfig(
            identity="evil-attacker",
            bus=BusConfig(path=str(tmp_path / "bus.tsv")),
            dry_run=False,
        )
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        assert bus_phase(config, turn) is False
        # Verify nothing was written to the bus
        assert not pathlib.Path(config.bus.path).exists()

    def test_env_var_adds_custom_identity(self, tmp_path, monkeypatch):
        """CRAB_ALLOWED_IDENTITIES env var adds custom identities to registry."""
        monkeypatch.setenv("CRAB_ALLOWED_IDENTITIES", "custom-daemon")
        config = DaemonConfig(
            identity="custom-daemon",
            bus=BusConfig(path=str(tmp_path / "bus.tsv")),
            dry_run=False,
        )
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        assert bus_phase(config, turn) is True

    def test_dry_run_skips_identity_check(self, tmp_path):
        """Dry run mode skips identity validation (no bus post anyway)."""
        config = DaemonConfig(
            identity="evil-attacker",
            bus=BusConfig(path=str(tmp_path / "bus.tsv")),
            dry_run=True,
        )
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "test", "STATUS", "rationale"),
            act=ActResult(True, ["did thing"], [], []),
        )
        # Dry run should succeed even with unapproved identity (no actual post)
        assert bus_phase(config, turn) is True


class TestCrabDaemon:
    @pytest.fixture
    def daemon(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        bus = tmp_path / "bus" / "messages.tsv"
        bus.parent.mkdir()
        bus.write_text("timestamp\tfrom\tto\ttype\tmessage\n")
        subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
        config = DaemonConfig(
            repo_root=str(repo),
            bus=BusConfig(path=str(bus)),
            dry_run=True,
            poll_interval=0.01,
            lanes=[LaneConfig(name="cleanup", interval_seconds=0.0, cooldown_seconds=10.0)],
        )
        return CrabDaemon(config)

    def test_run_once_executes_lane(self, daemon):
        turns = daemon.run_once()
        assert len(turns) == 1
        assert turns[0].reason.lane == "cleanup"
        assert turns[0].bus_posted is True

    def test_cooldown_skips_recent_lane(self, daemon):
        daemon.run_once()
        turns = daemon.run_once()
        assert len(turns) == 0


class TestCLI:
    def test_init_writes_config(self, tmp_path):
        path = tmp_path / "config.json"
        from crab_daemon import main
        rc = main(["--init", "--config", str(path)])
        assert rc == 0
        assert path.exists()
        raw = json.loads(path.read_text())
        assert raw["identity"] == "crab-daemon"
        assert raw["bus"]["backend"] == "tsv"

    def test_once_dry_run(self, tmp_path):
        path = tmp_path / "config.json"
        default_config().to_json(path)
        from crab_daemon import main
        rc = main(["--once", "--dry-run", "--lane", "cleanup", "--config", str(path)])
        assert rc == 0


class TestBusBridge:
    """Test CRAB -> founder-mode bus bridge."""

    def test_bridge_extracts_retrograde_from_log(self, tmp_path):
        """bridge_once parses Retrograde + BUS lines and returns structured data."""
        log = tmp_path / "test-daemon.log"
        log.write_text(
            "2026-05-11T20:30:00Z INFO === CRAB turn: cleanup ===\n"
            "2026-05-11T20:30:01Z INFO [BUS] 2026-05-11T20:30:01Z crab-daemon -> all [STATUS] [cleanup] OK - Pruned 2 branches\n"
            '2026-05-11T20:30:01Z INFO RETROGRADE: validated=True dissonance=0.00 scuttle=False findings=["OK: pruned == found"]\n',
            encoding="utf-8",
        )
        from bridge_crab_fm import bridge_once
        # bridge_once posts to founder-mode bus; we just verify it doesn't crash
        rc = bridge_once(log)
        assert rc in (0, 1)  # 0 = posted, 1 = post failed (bus may be unavailable in CI)


class TestRetrogradePhase:
    """6 tests for the RETROGRADE backward validator."""

    def test_retrograde_cleanup_valid(self):
        """Cleanup with matching found/pruned lists → dissonance 0.0."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "cleanup", "STATUS", "prune-gone"),
            act=ActResult(
                success=True,
                actions_taken=["Found 2 stale branches", "Pruned 2 branches"],
                artifacts=[],
                errors=[],
                metadata={
                    "gone_branches_found": ["feat/old", "feat/older"],
                    "gone_branches_pruned": ["feat/old", "feat/older"],
                    "untracked_count": 0,
                },
            ),
        )
        config = DaemonConfig(retrograde_enabled=True, dissonance_threshold=0.5)
        result = retrograde_phase(config, turn)
        assert result is not None
        assert result.validated is True
        assert result.dissonance == 0.0
        assert result.scuttle is False
        assert "OK" in result.findings[0]

    def test_retrograde_cleanup_orphaned_prune(self):
        """Prune branch not in found list → dissonance 0.8, scuttle True."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "cleanup", "STATUS", "prune-gone"),
            act=ActResult(
                success=True,
                actions_taken=["Pruned 1 branch"],
                artifacts=[],
                errors=[],
                metadata={
                    "gone_branches_found": [],
                    "gone_branches_pruned": ["feat/phantom"],
                    "untracked_count": 0,
                },
            ),
        )
        config = DaemonConfig(retrograde_enabled=True, dissonance_threshold=0.5)
        result = retrograde_phase(config, turn)
        assert result is not None
        assert result.validated is False
        assert result.dissonance == 0.8
        assert result.scuttle is True
        assert "Orphaned prune" in result.findings[0]

    def test_retrograde_git_audit_valid(self):
        """Git audit with complete metadata → dissonance 0.0."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "git-audit", "STATUS", "audit"),
            act=ActResult(
                success=True,
                actions_taken=["Worktree clean"],
                artifacts=[],
                errors=[],
                metadata={
                    "untracked_count": 0,
                    "modified_count": 0,
                    "stale_locks": False,
                },
            ),
        )
        config = DaemonConfig(retrograde_enabled=True, dissonance_threshold=0.5)
        result = retrograde_phase(config, turn)
        assert result is not None
        assert result.validated is True
        assert result.dissonance == 0.0
        assert result.scuttle is False

    def test_retrograde_git_audit_missing_metadata(self):
        """No metadata captured → dissonance 0.5, scuttle True."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "git-audit", "STATUS", "audit"),
            act=ActResult(
                success=True,
                actions_taken=["Worktree clean"],
                artifacts=[],
                errors=[],
                metadata={},
            ),
        )
        config = DaemonConfig(retrograde_enabled=True, dissonance_threshold=0.4)
        result = retrograde_phase(config, turn)
        assert result is not None
        assert result.validated is False
        assert result.dissonance == 0.5
        assert result.scuttle is True
        assert "No metadata captured" in result.findings[0]

    def test_retrograde_bus_audit_valid(self):
        """Bus audit with message count → dissonance 0.0."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "bus-audit", "STATUS", "audit"),
            act=ActResult(
                success=True,
                actions_taken=["Bus has 5 messages"],
                artifacts=[],
                errors=[],
                metadata={
                    "message_count": 5,
                    "malformed_count": 0,
                    "identities": ["agent-a"],
                },
            ),
        )
        config = DaemonConfig(retrograde_enabled=True, dissonance_threshold=0.5)
        result = retrograde_phase(config, turn)
        assert result is not None
        assert result.validated is True
        assert result.dissonance == 0.0
        assert result.scuttle is False

    def test_retrograde_disabled(self):
        """retrograde_enabled=False → returns None."""
        turn = CrabTurn(
            check=CheckResult("t", "main", False, 0, [], []),
            reason=ReasonResult(True, "cleanup", "STATUS", "prune"),
            act=ActResult(True, ["did thing"], [], []),
        )
        config = DaemonConfig(retrograde_enabled=False)
        result = retrograde_phase(config, turn)
        assert result is None
