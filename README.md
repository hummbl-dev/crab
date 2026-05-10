# CRAB

CRAB is a lightweight operating methodology for multi-agent work:

**Check -> Reason -> Act -> Bus**

It exists to keep autonomous or semi-autonomous workers synchronized when more
than one session, host, model, or human can touch the same work surface.

CRAB is not a chat ritual. It is a coordination contract:

1. **Check** the live state before acting.
2. **Reason** against the current state, instructions, and stop conditions.
3. **Act** only after the work surface is understood.
4. **Bus** the result before closing the loop with the requester.

## Why It Exists

Multi-agent systems fail when agents inherit stale state, act on the wrong
branch, miss another worker's blocker, or rely on a human to relay context
between sessions. CRAB makes the state check and the coordination receipt part
of every meaningful turn.

## Repository Contents

- [Methodology](docs/methodology.md) - the canonical CRAB method.
- [Implementation Guide](docs/implementation-guide.md) - how to adapt CRAB to a repo, team, or agent fleet.
- [Adoption Checklist](docs/adoption-checklist.md) - practical rollout checklist.
- [Message Types](docs/message-types.md) - common bus message taxonomy.
- [Source Notes](docs/source-notes.md) - origin and relation to HUMMBL founder-mode.
- `crab_daemon.py` — **portable reference implementation** (see below)

## CRAB Daemon — Autonomous Agent Loop

`crab_daemon.py` is a standalone, zero-dependency Python script that implements
the full CRAB protocol as a continuous background process. You can start it and
leave it running unattended.

### Features

- **Pluggable bus backends**: TSV, JSONL, stdout, or custom callback
- **Lane-based work streams**: independent lanes with their own schedules
- **CRAB stop conditions**: respects BLOCKED messages, stash checks, cooldowns
- **Stdlib-only**: no pip install required
- **Configurable via JSON**: edit `crab-daemon/config.json`

### Quick start

```bash
# Initialize default config
./crab_daemon.py --init

# Run one iteration and see what it would do
./crab_daemon.py --once --dry-run

# Run continuously (foreground)
./crab_daemon.py

# Run only the cleanup lane
./crab_daemon.py --once --lane cleanup
```

### Built-in lanes

| Lane | What it does |
|------|-------------|
| `cleanup` | Prune stale `[gone]` branches, report untracked files |
| `git-audit` | Check worktree state, stale locks, uncommitted changes |
| `bus-audit` | Verify bus integrity, count messages, detect malformed lines |

### Adding custom lanes

Register a handler in `LANE_REGISTRY` and add the lane to your config:

```python
LANE_REGISTRY["my-lane"] = my_lane_handler
```

```json
{
  "lanes": [
    {
      "name": "my-lane",
      "enabled": true,
      "interval_seconds": 300.0,
      "actions": []
    }
  ]
}
```

### Bus backends

| Backend | Format | Use case |
|---------|--------|----------|
| `tsv` | Tab-separated lines | Simple text bus (default) |
| `jsonl` | JSON lines | Structured log consumption |
| `stdout` | Console output | Development / dry-run |
| `callback` | Shell command | Integration with existing systems |

## Status

- **Methodology**: v1.0 — stable, used in production at HUMMBL
- **Daemon**: reference implementation in development (see Issue #1)
- **Public release**: gated on security audit + operator decision

This repo is the portable methodology home; project-specific rules should
keep their local host paths, command wrappers, identities, and guardrails in
their own repos.
