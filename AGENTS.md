# AGENTS.md — crab

## Project

**crab** — CRAB methodology: Check, Reason, Act, Bus — a lightweight coordination protocol for multi-agent systems. Every autonomous turn reads live state, decides whether to act, performs the work, and posts a receipt to a coordination bus. Python 3.11+, zero runtime dependencies (stdlib only).

## Scope

- In scope: 4-step protocol (CRAWL/Check → Reason → Act → Bus), pluggable bus backends (TSV, JSONL, stdout, custom callback), multi-lane work streams with separate schedules and stop conditions, daemon (`crab_daemon.py`), lane optimizer (`crab_lane_optimizer.py`), FM bridge (`bridge_crab_fm.py`), examples and docs
- Out of scope: Consumer app features, governance primitive implementation (lives in `hummbl-governance`)

## Setup

```bash
git clone https://github.com/hummbl-dev/crab.git && cd crab
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"

# Generate a default config
python crab_daemon.py --init

# Run one turn
python crab_daemon.py --once --verbose

# Run continuously
python crab_daemon.py --verbose
```

## Testing

```bash
python -m pytest tests/ -v
```

Test extras: `pytest>=8`. Test paths: `tests/`, files matching `test_*.py`.

## Conventions

- Python 3.11+ required
- Zero runtime dependencies (stdlib only) — no runtime `pip install`
- Container ready: single file, drop into Docker/Kubernetes/systemd
- Every turn produces a timestamped receipt; replay any session
- Daemon reads `crab-daemon/config.json` for identity, bus backend, poll interval, and lanes
- Commit format: Conventional Commits
- Branch naming: `type/agent/short-desc`
- Apache 2.0 license

## CI

GitHub Actions workflow: `ci.yml` (lint + test gates).
