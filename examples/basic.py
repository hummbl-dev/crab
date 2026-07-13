#!/usr/bin/env python3
"""
CRAB Basic Example
==================
Run a single CRAB turn with the stdout bus backend.

This example demonstrates how to:
1. Generate a default config
2. Run the daemon in --once mode with stdout output

Usage:
    python examples/basic.py
"""

import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAEMON = os.path.join(REPO_ROOT, "crab_daemon.py")


def main():
    print("=" * 60)
    print("CRAB Daemon — Basic Example")
    print("=" * 60)

    # Step 1: Generate a default config
    print("\n[1/2] Generating default config...")
    result = subprocess.run(
        ["python", DAEMON, "--init", "--verbose"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip() or "Config generated.")

    # Step 2: Run one turn with stdout backend
    print("\n[2/2] Running one CRAB turn with stdout bus...")
    print("-" * 60)
    result = subprocess.run(
        ["python", DAEMON, "--once", "--verbose",
         "--identity", "basic-agent"],
        cwd=REPO_ROOT,
        capture_output=False,  # Let output flow to terminal
    )
    print("-" * 60)

    print(f"\nExit code: {result.returncode}")
    print("\nEvery turn leaves a receipt on the bus.")
    print("With the stdout backend, receipts appear above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
