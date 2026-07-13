"""Tests for bus/crab_bus.py."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bus"))
import crab_bus as cb  # noqa: E402


@pytest.fixture(autouse=True)
def _tmp_bus_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect BUS_FILE to a temporary path for every test."""
    monkeypatch.setattr(cb, "BUS_FILE", tmp_path / "messages.tsv")


class TestWriteAndRead:
    def test_post_creates_file(self) -> None:
        cb.write_bus("crab", "all", "STATUS", "OK")
        assert cb.BUS_FILE.exists()

    def test_roundtrip(self) -> None:
        cb.write_bus("crab", "all", "STATUS", "hello")
        msgs = cb.read_bus()
        assert len(msgs) == 1
        assert msgs[0][1] == "crab"
        assert msgs[0][2] == "all"
        assert msgs[0][3] == "STATUS"
        assert msgs[0][4] == "hello"

    def test_read_limit(self) -> None:
        for i in range(5):
            cb.write_bus("crab", "all", "STATUS", str(i))
        msgs = cb.read_bus(limit=2)
        assert len(msgs) == 2
        assert msgs[-1][4] == "4"

    def test_read_empty(self) -> None:
        assert cb.read_bus() == []


class TestCLI:
    def test_post_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        rc = cb.main(["post", "crab", "all", "STATUS", "hello"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Posted" in out

    def test_read_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        cb.write_bus("crab", "all", "STATUS", "hello")
        rc = cb.main(["read", "--limit", "10"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "hello" in out

    def test_status_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        cb.write_bus("crab", "all", "STATUS", "a")
        cb.write_bus("crab", "all", "DECISION", "b")
        rc = cb.main(["status"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "STATUS: 1" in out
        assert "DECISION: 1" in out

    def test_clear_command(self) -> None:
        cb.write_bus("crab", "all", "STATUS", "a")
        rc = cb.main(["clear"])
        assert rc == 0
        assert cb.read_bus() == []

    def test_search_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        cb.write_bus("crab", "all", "STATUS", "hello world")
        rc = cb.main(["search", "world"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "hello world" in out


class TestGlobalBridge:
    def test_global_types_set(self) -> None:
        assert "STATUS" in cb._GLOBAL_TYPES
        assert "DECISION" in cb._GLOBAL_TYPES
        assert "BLOCKED" in cb._GLOBAL_TYPES
        assert "HANDOFF" in cb._GLOBAL_TYPES

    def test_idea_not_global(self) -> None:
        assert "IDEA" not in cb._GLOBAL_TYPES
