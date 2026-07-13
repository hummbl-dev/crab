# CRAB

**Coordination Receipts for Agent Behavior**

[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![Runtime Deps](https://img.shields.io/badge/runtime%20deps-zero-brightgreen)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

CRAB is a lightweight coordination protocol for multi-agent systems:

> **CRAWL/Check → Reason → Act → Bus**

Every consequential autonomous turn reads live state, decides whether to act, performs the work, and posts a receipt to a coordination bus. `Check` is the short-form first step; `CRAWL` is the expanded live-state method: Context, Repo, Agents, Wire, Limits. No more waking up wondering what your agents did overnight.

[Landing Page](docs/index.html) · [Docs](docs/methodology.md) · [Examples](examples/) · [Issues](https://github.com/hummbl-dev/crab/issues)

---

## Why CRAB

Multi-agent systems fail when agents:
- Work on stale state
- Overwrite each other's changes
- Fail silently and leave no trace
- Race each other without coordination

CRAB makes every agent turn **observable** and **accountable**. The bus receipt tells you exactly what happened, when, and why.

## Features

- **4-step protocol** — CRAWL/Check, Reason, Act, Bus. Structured, repeatable, safe.
- **Pluggable bus backends** — TSV, JSONL, stdout, or custom callback. One-line switch.
- **Multi-lane work streams** — Independent lanes with separate schedules and stop conditions.
- **Zero runtime dependencies** — Python 3.11+ stdlib only. No runtime `pip install`.
- **Container ready** — Single file. Drop into Docker, Kubernetes, or systemd.
- **Observable by design** — Every turn produces a timestamped receipt. Replay any session.

## Quick Start

```bash
# Clone and enter the repo
git clone https://github.com/hummbl-dev/crab.git
cd crab

# Generate a default config
python crab_daemon.py --init
# → Default config written to: crab-daemon/config.json

# Run one turn and see the output
python crab_daemon.py --once --verbose

# Run continuously (press Ctrl+C to stop)
python crab_daemon.py --verbose
```

### Config file

The daemon reads `crab-daemon/config.json`:

```json
{
  "identity": "my-agent",
  "bus": {
    "backend": "tsv",
    "path": "bus/messages.tsv"
  },
  "poll_interval": 60.0,
  "lanes": [
    {
      "name": "cleanup",
      "enabled": true,
      "interval_seconds": 3600.0
    }
  ]
}
```

| Backend | Output | Best for |
|---------|--------|----------|
| `tsv` | Tab-separated file | Human-readable, grep-friendly |
| `jsonl` | JSON lines | Structured parsing, databases |
| `stdout` | Console | Development, containers, systemd |
| `callback` | Shell command | Webhooks, Slack, CI triggers |

### CLI reference

```bash
python crab_daemon.py --init              # Write default config
python crab_daemon.py --once             # Run one iteration and exit
python crab_daemon.py --once --dry-run    # Simulate without posting
python crab_daemon.py --lane cleanup      # Run only the cleanup lane
python crab_daemon.py --verbose           # Debug logging
python crab_daemon.py --config path.json  # Custom config file
```

## Examples

See the [`examples/`](examples/) directory:

| Example | What it shows |
|---------|-------------|
| [`basic.py`](examples/basic.py) | stdout backend, single turn |
| [`custom_backend.py`](examples/custom_backend.py) | Slack webhook via callback backend |
| [`docker-compose.yml`](examples/docker-compose.yml) | Fleet of daemons with different backends |

```bash
# Run the basic example
python examples/basic.py

# Run the Slack webhook example
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python examples/custom_backend.py

# Run the container fleet
docker-compose -f examples/docker-compose.yml up --build
```

## Built-in Lanes

| Lane | What it does |
|------|-------------|
| `cleanup` | Prune stale `[gone]` branches, report untracked files |
| `git-audit` | Check worktree state, stale locks, uncommitted changes |
| `bus-audit` | Verify bus integrity, count messages, detect malformed lines |

## Adding Custom Lanes

Register a handler and add the lane to your config:

```python
# my_lanes.py
from crab_daemon import LANE_REGISTRY, ActResult

def my_lane_handler(config, lane):
    # Your logic here
    return ActResult(success=True, actions_taken=["did the thing"], artifacts=[], errors=[])

LANE_REGISTRY["my-lane"] = my_lane_handler
```

```json
{
  "lanes": [
    {
      "name": "my-lane",
      "enabled": true,
      "interval_seconds": 300.0
    }
  ]
}
```

## Programmatic API

```python
from crab_daemon import CrabDaemon, DaemonConfig, BusConfig, LaneConfig

config = DaemonConfig(
    identity="my-agent",
    bus=BusConfig(backend="stdout"),
    lanes=[LaneConfig(name="git-audit", enabled=True)]
)

daemon = CrabDaemon(config)

# Run one iteration
turns = daemon.run_once()

# Or run continuously
daemon.run()  # Press Ctrl+C to stop
daemon.stop()
```

## Architecture

```
┌─────────────────────────────────────┐
│           CrabDaemon                │
│  ┌─────┐ ┌──────┐ ┌───┐ ┌─────┐   │
│  │CRAWL│→│Reason│→│Act│→│ Bus │   │
│  │Check│ └──────┘ └───┘ └─────┘   │
│       ↑___________________↓        │
│         (receipt posted)            │
└─────────────────────────────────────┘
              ↓
         ┌──────────┐
         │ Bus Log  │  ← tsv / jsonl / stdout / callback
         │ (append) │
         └──────────┘
```

## Testing

```bash
python -m pytest tests/ -v
```

The test suite covers:
- Config serialization/deserialization
- CRAWL/Check phase (live state, git state, bus tail, blockers)
- Reason phase (stop conditions, lane selection)
- Act phase (cleanup, audit, error handling)
- Bus phase (all four backends)
- Daemon lifecycle (run_once, run, stop)

Run `python -m pytest tests/ -q` to validate the local suite. Bridge tests (`TestBusBridge`) write to a local founder-mode bus path and should be mocked or excluded with `-k 'not TestBusBridge'` when running outside that environment.

## Documentation

- [Methodology](docs/methodology.md) — the canonical CRAB method
- [Implementation Guide](docs/implementation-guide.md) — adapt CRAB to your repo or team
- [Adoption Checklist](docs/adoption-checklist.md) — practical rollout checklist
- [Message Types](docs/message-types.md) — bus message taxonomy
- [Source Notes](docs/source-notes.md) — origin and relation to HUMMBL founder-mode
- [Release Notes](docs/RELEASE_NOTES.md) — draft/stable protocol status
- [Repo Boundaries](docs/REPO_BOUNDARIES.md) — public-core vs. HUMMBL-internal surfaces
- [Security Audit](AUDIT.md) — redteam audit results (10/10 PASS)
- [Productization Plan](PRODUCTIZATION.md) — roadmap from internal ops to marketable product

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code standards
- Commit message format
- Pull request process

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Status

- **Protocol**: v1.1 draft — CRAWL/Check wording proposed for docs-first adoption; v1.0 Check terminology remains compatible
- **Daemon**: v1.0 — reference implementation, tested, audited for its portable core
- **Retrograde**: implemented in the reference daemon as optional validation behavior; not yet a required public protocol phase
- **Security**: [Redteam audit](AUDIT.md) — daemon-scoped 10/10 PASS; repo-wide public-release audit still required
- **Publication**: public; see [Repo Boundaries](docs/REPO_BOUNDARIES.md) for scope details

## Repository Health

See [REPO_HEALTH.md](docs/REPO_HEALTH.md) for validation command expectations and
branch-protection posture.

Created by [HUMMBL Research Institute](https://hummbl.io).
