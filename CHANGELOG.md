# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (placeholder for upcoming changes)

## [v1.0.0] - 2026-05-10

### Added
- Portable CRAB Daemon (`crab_daemon.py`) — stdlib-only, zero dependencies
- 4 pluggable bus backends: TSV, JSONL, stdout, callback
- 3 built-in lanes: cleanup, git-audit, bus-audit
- Multi-lane work streams with independent schedules
- CRAB stop conditions (blockers, stashes, cooldowns)
- Dry-run mode for safe testing
- 18 unit tests, all passing
- Redteam security audit: 10/10 PASS
- Apache-2.0 license
