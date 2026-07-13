# CRAB Repo Boundaries

**Status:** Internal hygiene guidance — not a public release decision.

This repository is currently a private incubator. It contains both the portable CRAB protocol implementation and HUMMBL-internal planning, bridge, research, and brand artifacts. A future public release should use a smaller, audited surface.

## Public/core candidate

Keep these in a public-ready CRAB artifact after a repo-wide public-release audit. This is a candidate list, not a claim that the current files already satisfy the public-release standard.

- `crab_daemon.py` — portable reference daemon.
- `tests/` — isolated tests only; bridge tests must be mocked or excluded from the public-core subset until they no longer touch HUMMBL-local bus paths.
- `examples/` — examples that work without HUMMBL infrastructure.
- `README.md`.
- `LICENSE`.
- `CODE_OF_CONDUCT.md`.
- `CONTRIBUTING.md`.
- `docs/methodology.md`.
- `docs/implementation-guide.md`.
- `docs/adoption-checklist.md`.
- `docs/message-types.md`.
- `docs/source-notes.md`.
- `docs/RELEASE_NOTES.md`.
- `docs/index.html`, if scrubbed and kept accurate.

Optional public candidates after separate review:

- `crab_lane_optimizer.py`, if positioned as experimental lane tuning rather than core protocol.
- `bus/bus_base.py` and `bus/crab_bus.py`, if the bus API boundary is documented and tested as portable.

Public positioning should stay narrow:

- Coordination Receipts for Agent Behavior.
- CRAWL/Check -> Reason -> Act -> Bus.
- Reference daemon is stdlib-only Python 3.11+.
- No benchmarked safety or reliability claims unless measured against a control.

## Private/internal candidate

Keep these private or move them under an internal namespace before any public release:

- `bridge_crab_fm.py` — HUMMBL/founder-mode bridge with local infrastructure assumptions.
- `docs/BUS_ALIGNMENT_founder_mode.md`.
- `docs/DEMO_governance_maturity.md`, if it remains HUMMBL-demo-specific.
- `PRODUCTIZATION.md`.
- `GITEA_MIRROR.md`.
- `docs/UNIFIED_ROADMAP.md`.
- `docs/peer_reviews/*`.
- `docs/research/*`, until citation and evidence hardening is complete.
- `docs/branding/*`, unless intentionally released as a brand/artpack package.
- `_state/` handoffs.
- Runtime state such as `crab-daemon/config.json`, logs, turns, and local bus messages.

## Recommended split strategy

1. Keep this private repo as the incubator.
2. Classify public-core versus internal artifacts here.
3. When release is approved, create a fresh public repo from the audited public-core subset.
4. Avoid `git-filter-repo` unless history preservation is more important than leakage risk.

No file movement is implied by this document. It records the boundary so future cleanup can be deliberate and operator-gated.

## Relocated artifacts (2026-07-12)

The following artifacts were previously tracked in this repo and have been
removed from the public tree. They are retained in internal/private storage:

- `docs/ai-notary-*` — notary framework docs; moved to internal-only storage.
- `docs/universal-jv-outreach-framework.md` — JV outreach framework; moved to
  internal-only storage.
