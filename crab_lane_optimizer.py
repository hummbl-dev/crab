"""CRAB Lane Optimizer — RSI module for tuning lane configurations.

Reads turn history (JSONL of CrabTurn-like dicts), computes per-lane
dissonance statistics, attributes root causes to config parameters, and
proposes a trial config.json with adjusted settings.

Usage:
    python crab_lane_optimizer.py --turn-log crab-daemon/turns.jsonl
    python crab_lane_optimizer.py --turn-log turns.jsonl --apply

Pure stdlib. No network.
"""
from __future__ import annotations

import argparse
import copy
import json
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path("crab-daemon/config.json")
DEFAULT_TURNS_PATH = Path("crab-daemon/turns.jsonl")


def load_turns(path: Path) -> list[dict]:
    """Load CrabTurn JSONL records."""
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_lane_stats(turns: list[dict]) -> dict[str, dict]:
    """Return per-lane aggregated statistics."""
    by_lane: dict[str, list[dict]] = defaultdict(list)
    for turn in turns:
        lane = turn.get("reason", {}).get("lane", "unknown")
        by_lane[lane].append(turn)

    stats: dict[str, dict] = {}
    for lane, lane_turns in by_lane.items():
        retrogrades = [t.get("retrograde", {}) for t in lane_turns if t.get("retrograde")]
        if not retrogrades:
            continue

        dissonances = [r.get("dissonance", 0.0) for r in retrogrades]
        scuttles = sum(1 for r in retrogrades if r.get("scuttle", False))
        validated = sum(1 for r in retrogrades if r.get("validated", False))

        stats[lane] = {
            "turns": len(lane_turns),
            "mean_dissonance": round(statistics.mean(dissonances), 3) if dissonances else 0.0,
            "max_dissonance": round(max(dissonances), 3) if dissonances else 0.0,
            "std_dissonance": round(statistics.stdev(dissonances), 3) if len(dissonances) > 1 else 0.0,
            "scuttle_rate": round(scuttles / len(retrogrades), 3) if retrogrades else 0.0,
            "validation_rate": round(validated / len(retrogrades), 3) if retrogrades else 0.0,
        }
    return stats


def attribute_config_cause(lane: str, stats: dict, current_config: dict) -> tuple[str, dict, float]:
    """Return (root_cause, proposed_config_delta, confidence)."""
    mean_d = stats["mean_dissonance"]
    scuttle_r = stats["scuttle_rate"]
    std_d = stats["std_dissonance"]

    # Find current lane config
    lane_cfg = next((l for l in current_config.get("lanes", []) if l.get("name") == lane), {})
    if not lane_cfg:
        return "unknown_lane", {}, 0.0

    delta: dict[str, Any] = {}
    confidence = 0.5

    # Rule 1: High dissonance + high scuttle → actions too aggressive
    if mean_d > 0.5 and scuttle_r > 0.3:
        cause = "too_aggressive"
        delta["max_actions_per_turn"] = max(1, lane_cfg.get("max_actions_per_turn", 5) - 1)
        delta["cooldown_seconds"] = lane_cfg.get("cooldown_seconds", 300) * 1.5
        confidence = min(0.95, 0.6 + scuttle_r)
        return cause, delta, confidence

    # Rule 2: Moderate dissonance with high variance → unstable; widen cooldown
    if mean_d > 0.3 and std_d > 0.3:
        cause = "unstable_variance"
        delta["cooldown_seconds"] = lane_cfg.get("cooldown_seconds", 300) * 1.3
        delta["interval_seconds"] = lane_cfg.get("interval_seconds", 300) * 1.2
        confidence = 0.6
        return cause, delta, confidence

    # Rule 3: Low dissonance but low validation rate → retrograde too strict
    if mean_d < 0.2 and stats["validation_rate"] < 0.5:
        cause = "overstrict_retrograde"
        # Suggest lowering dissonance threshold (this is a daemon-level param)
        delta["_daemon_note"] = "Consider raising dissonance_threshold by 0.1"
        confidence = 0.4
        return cause, delta, confidence

    # Rule 4: Everything green → can tighten (reduce cooldown, increase actions)
    if mean_d < 0.15 and scuttle_r == 0.0:
        cause = "room_to_accelerate"
        delta["cooldown_seconds"] = max(60, lane_cfg.get("cooldown_seconds", 300) * 0.8)
        delta["max_actions_per_turn"] = lane_cfg.get("max_actions_per_turn", 5) + 1
        confidence = 0.5
        return cause, delta, confidence

    cause = "no_clear_signal"
    return cause, delta, confidence


def build_trial_config(current_config: dict, proposals: dict[str, dict]) -> dict:
    """Merge proposed deltas into a copy of current config."""
    trial = copy.deepcopy(current_config)
    for lane in trial.get("lanes", []):
        name = lane.get("name", "")
        if name in proposals:
            for key, val in proposals[name].items():
                if not key.startswith("_"):
                    lane[key] = val
    return trial


def analyze(turns_path: Path = DEFAULT_TURNS_PATH,
            config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    turns = load_turns(turns_path)
    config = load_config(config_path)
    stats = compute_lane_stats(turns)

    report = {
        "turns_loaded": len(turns),
        "config_path": str(config_path),
        "lane_stats": stats,
        "proposals": {},
        "overall_health": "unknown",
    }

    if not stats:
        report["overall_health"] = "no_data"
        return report

    proposals: dict[str, dict] = {}
    overall_dissonances = []
    for lane, lane_stats in stats.items():
        cause, delta, conf = attribute_config_cause(lane, lane_stats, config)
        if delta:
            proposals[lane] = delta
        report["proposals"][lane] = {
            "cause": cause,
            "delta": delta,
            "confidence": conf,
        }
        overall_dissonances.append(lane_stats["mean_dissonance"])

    report["overall_health"] = (
        "healthy" if statistics.mean(overall_dissonances) < 0.3 else
        "degraded" if statistics.mean(overall_dissonances) < 0.6 else
        "critical"
    )
    report["trial_config"] = build_trial_config(config, proposals)
    return report


def render_report(report: dict) -> str:
    lines = ["# CRAB Lane Optimizer Report", ""]
    lines.append(f"- **Turns loaded:** {report['turns_loaded']}")
    lines.append(f"- **Overall health:** {report['overall_health']}")
    lines.append("")

    stats = report.get("lane_stats", {})
    if not stats:
        lines.append("No retrograde data available. Run CRAB daemon to generate turns.")
        return "\n".join(lines)

    for lane, lane_stats in stats.items():
        lines.append(f"## Lane: {lane}")
        lines.append(f"- **Turns:** {lane_stats['turns']}")
        lines.append(f"- **Mean dissonance:** {lane_stats['mean_dissonance']}")
        lines.append(f"- **Max dissonance:** {lane_stats['max_dissonance']}")
        lines.append(f"- **Scuttle rate:** {lane_stats['scuttle_rate']}")
        lines.append(f"- **Validation rate:** {lane_stats['validation_rate']}")

        prop = report["proposals"].get(lane, {})
        if prop.get("delta"):
            lines.append(f"- **Proposed change:** {prop['cause']} (conf={prop['confidence']})")
            for key, val in prop["delta"].items():
                lines.append(f"  - {key}: {val}")
        else:
            lines.append(f"- **Proposed change:** none ({prop.get('cause', 'no signal')})")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--turn-log", type=Path, default=DEFAULT_TURNS_PATH)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--apply", action="store_true",
                   help="write trial config next to selected config path")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = p.parse_args(argv)

    report = analyze(args.turn_log, args.config)

    if args.format == "json":
        out = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        out = render_report(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out + "\n", encoding="utf-8")
        print(f"wrote report to {args.output}", file=sys.stderr)

    if args.apply and report.get("trial_config"):
        trial_path = args.config.with_name("config-trial.json")
        trial_path.parent.mkdir(parents=True, exist_ok=True)
        trial_path.write_text(
            json.dumps(report["trial_config"], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"wrote trial config to {trial_path}", file=sys.stderr)

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
