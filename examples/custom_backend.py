#!/usr/bin/env python3
"""
CRAB Custom Callback Example
============================
Route CRAB receipts to a Slack webhook using the callback backend.

This example shows how to:
1. Generate a config with a custom callback command
2. Run the daemon with the callback backend

Usage:
    export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
    python examples/custom_backend.py
"""

import subprocess
import sys
import os
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAEMON = os.path.join(REPO_ROOT, "crab_daemon.py")
CONFIG_PATH = os.path.join(REPO_ROOT, "crab-daemon", "callback-config.json")


def main():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        print("Error: Set SLACK_WEBHOOK_URL environment variable.")
        print("Example: export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'")
        sys.exit(1)

    # Build a curl command that sends the receipt to Slack
    callback_cmd = (
        f'curl -s -X POST -H "Content-Type: application/json" '
        f'-d "{{\\"text\\": \\"CRAB receipt from basic-agent\\"}}" '
        f'{webhook_url}'
    )

    config = {
        "identity": "slack-agent",
        "bus": {
            "backend": "callback",
            "path": "/tmp/crab-bus.tsv",
            "callback": callback_cmd,
        },
        "log_path": "/tmp/crab-callback.log",
        "poll_interval": 5.0,
        "lanes": [
            {
                "name": "git-audit",
                "enabled": True,
                "interval_seconds": 0,
                "cooldown_seconds": 0,
            }
        ],
    }

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print("=" * 60)
    print("CRAB Daemon — Callback Backend Example (Slack Webhook)")
    print("=" * 60)
    print(f"\nConfig written to: {CONFIG_PATH}")
    print(f"Webhook: {webhook_url[:50]}...")
    print("\nRunning one turn...\n")

    result = subprocess.run(
        ["python", DAEMON, "--once", "--verbose", "--config", CONFIG_PATH],
        cwd=REPO_ROOT,
        capture_output=False,
    )

    print(f"\nExit code: {result.returncode}")
    print("\nIn production, expand the callback command to include turn details.")
    print("=" * 60)


if __name__ == "__main__":
    main()
