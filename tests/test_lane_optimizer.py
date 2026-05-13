"""Tests for crab_lane_optimizer.

Pure stdlib. No network.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import crab_lane_optimizer as clo


class TestComputeLaneStats(unittest.TestCase):
    def test_empty(self):
        stats = clo.compute_lane_stats([])
        self.assertEqual(stats, {})

    def test_single_lane(self):
        turns = [
            {
                "reason": {"lane": "cleanup"},
                "retrograde": {"dissonance": 0.2, "scuttle": False, "validated": True},
            },
            {
                "reason": {"lane": "cleanup"},
                "retrograde": {"dissonance": 0.8, "scuttle": True, "validated": False},
            },
        ]
        stats = clo.compute_lane_stats(turns)
        self.assertIn("cleanup", stats)
        self.assertEqual(stats["cleanup"]["turns"], 2)
        self.assertEqual(stats["cleanup"]["mean_dissonance"], 0.5)
        self.assertEqual(stats["cleanup"]["scuttle_rate"], 0.5)
        self.assertEqual(stats["cleanup"]["validation_rate"], 0.5)


class TestAttributeConfigCause(unittest.TestCase):
    def setUp(self):
        self.config = {
            "lanes": [
                {"name": "cleanup", "max_actions_per_turn": 5, "cooldown_seconds": 3600},
            ]
        }

    def test_too_aggressive(self):
        stats = {"mean_dissonance": 0.7, "scuttle_rate": 0.4, "std_dissonance": 0.1,
                "validation_rate": 0.3, "turns": 10}
        cause, delta, conf = clo.attribute_config_cause("cleanup", stats, self.config)
        self.assertEqual(cause, "too_aggressive")
        self.assertIn("max_actions_per_turn", delta)
        self.assertLess(delta["max_actions_per_turn"], 5)
        self.assertGreater(delta["cooldown_seconds"], 3600)
        self.assertGreater(conf, 0.5)

    def test_room_to_accelerate(self):
        stats = {"mean_dissonance": 0.1, "scuttle_rate": 0.0, "std_dissonance": 0.0,
                "validation_rate": 1.0, "turns": 10}
        cause, delta, conf = clo.attribute_config_cause("cleanup", stats, self.config)
        self.assertEqual(cause, "room_to_accelerate")
        self.assertGreater(delta["max_actions_per_turn"], 5)
        self.assertLess(delta["cooldown_seconds"], 3600)


class TestBuildTrialConfig(unittest.TestCase):
    def test_merge_delta(self):
        config = {
            "identity": "crab",
            "lanes": [
                {"name": "cleanup", "max_actions_per_turn": 5, "cooldown_seconds": 3600},
                {"name": "git-audit", "max_actions_per_turn": 5},
            ]
        }
        proposals = {"cleanup": {"max_actions_per_turn": 3, "cooldown_seconds": 5400}}
        trial = clo.build_trial_config(config, proposals)
        cleanup = next(l for l in trial["lanes"] if l["name"] == "cleanup")
        self.assertEqual(cleanup["max_actions_per_turn"], 3)
        self.assertEqual(cleanup["cooldown_seconds"], 5400)
        git_audit = next(l for l in trial["lanes"] if l["name"] == "git-audit")
        self.assertEqual(git_audit["max_actions_per_turn"], 5)


class TestAnalyzeEndToEnd(unittest.TestCase):
    def test_no_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            turns_path = Path(tmp) / "turns.jsonl"
            config_path = Path(tmp) / "config.json"
            config_path.write_text(json.dumps({"lanes": []}), encoding="utf-8")
            report = clo.analyze(turns_path, config_path)
            self.assertEqual(report["turns_loaded"], 0)
            self.assertEqual(report["overall_health"], "no_data")

    def test_with_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            turns_path = Path(tmp) / "turns.jsonl"
            turns = [
                {"reason": {"lane": "cleanup"},
                 "retrograde": {"dissonance": 0.7, "scuttle": True, "validated": False}},
                {"reason": {"lane": "cleanup"},
                 "retrograde": {"dissonance": 0.6, "scuttle": True, "validated": False}},
            ]
            turns_path.write_text(
                "\n".join(json.dumps(t) for t in turns), encoding="utf-8")

            config_path = Path(tmp) / "config.json"
            config = {
                "lanes": [
                    {"name": "cleanup", "max_actions_per_turn": 5,
                     "cooldown_seconds": 3600, "interval_seconds": 3600},
                ]
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")

            report = clo.analyze(turns_path, config_path)
            self.assertEqual(report["overall_health"], "critical")
            self.assertIn("cleanup", report["proposals"])
            self.assertIn("trial_config", report)


class TestMainCli(unittest.TestCase):
    def _write_inputs(self, tmp: Path) -> tuple[Path, Path]:
        turns_path = tmp / "turns.jsonl"
        turns_path.write_text(
            json.dumps({
                "reason": {"lane": "cleanup"},
                "retrograde": {"dissonance": 0.7, "scuttle": True, "validated": False},
            }) + "\n",
            encoding="utf-8",
        )
        config_path = tmp / "config.json"
        config_path.write_text(
            json.dumps({
                "lanes": [
                    {"name": "cleanup", "max_actions_per_turn": 5,
                     "cooldown_seconds": 3600, "interval_seconds": 3600},
                ]
            }),
            encoding="utf-8",
        )
        return turns_path, config_path

    def test_main_writes_output_report(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            turns_path, config_path = self._write_inputs(tmp)
            output_path = tmp / "reports" / "report.md"

            rc = clo.main([
                "--turn-log", str(turns_path),
                "--config", str(config_path),
                "--output", str(output_path),
            ])

            self.assertEqual(rc, 0)
            self.assertTrue(output_path.exists())
            self.assertIn("CRAB Lane Optimizer Report",
                          output_path.read_text(encoding="utf-8"))

    def test_main_apply_creates_trial_directory(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            turns_path, config_path = self._write_inputs(tmp)
            old_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp)

                rc = clo.main([
                    "--turn-log", str(turns_path),
                    "--config", str(config_path),
                    "--apply",
                    "--format", "json",
                ])
            finally:
                os.chdir(old_cwd)

            self.assertEqual(rc, 0)
            self.assertTrue((tmp / "crab-daemon" / "config-trial.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
