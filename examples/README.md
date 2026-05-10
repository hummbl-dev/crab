# CRAB Examples

This directory contains runnable examples demonstrating how to use the CRAB Daemon in different contexts.

## Quick Start

All examples assume you are in the repo root:

```bash
cd /path/to/crab
```

## Examples

### `basic.py` — Stdout Backend
The simplest possible usage. Generate a config and run one turn with stdout output.

```bash
python examples/basic.py
```

### `custom_backend.py` — Callback Backend (Slack Webhook)
Shows how to configure the callback backend to send receipts to a Slack webhook.

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python examples/custom_backend.py
```

### `docker-compose.yml` — Container Fleet
Runs three CRAB daemons in Docker containers with different backends.

```bash
docker-compose -f examples/docker-compose.yml up --build
```

Inspect shared outputs:
```bash
cat examples/data/receipts.tsv
cat examples/data/receipts.jsonl
```

## CLI Reference

The daemon supports these arguments:

```
python crab_daemon.py --init              # Write default config
python crab_daemon.py --once             # Run one iteration and exit
python crab_daemon.py --once --dry-run   # Simulate without posting to bus
python crab_daemon.py --lane cleanup       # Run only the cleanup lane
python crab_daemon.py --verbose          # Debug logging
python crab_daemon.py --config path.json # Use custom config
```

## Config File

Generate a default config with `--init`, then edit `crab-daemon/config.json`:

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

Backend options: `tsv`, `jsonl`, `stdout`, `callback`.
