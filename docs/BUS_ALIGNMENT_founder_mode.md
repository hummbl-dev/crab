# CRAB ↔ Founder-Mode Bus Alignment

**Date:** 2026-05-11
**Status:** Gap analysis complete — bridge spec needed for cross-machine demo

---

## Format Comparison

### CRAB Bus (current)

| Column | Example | Notes |
|---|---|---|
| `timestamp` | `2026-05-11T20:37:00Z` | ISO8601 with Z suffix |
| `identity` | `crab-daemon` | Single sender field |
| `message_type` | `STATUS` | PROPOSAL, ACK, STATUS, BLOCKED |
| `rationale` | `[cleanup] OK — Pruned 2 branches` | Free-text, human-readable |

**Backends:** `tsv` (default), `jsonl`, `callback` (HTTP POST), `stdout`
**Path:** Configurable via `bus.path` (default: `bus/messages.tsv`)
**Locking:** None — append-only, no flock

### Founder-Mode Bus (canonical)

| Column | Example | Notes |
|---|---|---|
| `timestamp_utc` | `2026-05-11T20:37:00Z` | Same format, different header name |
| `from` | `devin` | Bare canonical agent identity |
| `to` | `all` | Target agent or broadcast |
| `type` | `STATUS` | Same vocabulary |
| `message` | `HANDOFF: CRAB Track 1 Phase A complete` | Free-text |

**Backends:** TSV only (flock-based locking via `fcntl`/`msvcrt`)
**Path:** `founder_mode/_state/coordination/messages.tsv`
**Locking:** `LOCK_EX` mutual exclusion
**Signing:** Optional HMAC-SHA256 via `BUS_SIGNING_SECRET`
**Validation:** Agent identity registry, message type whitelist, field escaping, correlation IDs

---

## Gaps

| # | Gap | Severity | Fix |
|---|---|---|---|
| 1 | **`to` column resolved in current daemon** | DONE | Current TSV/JSONL posts emit `to=all`; keep bridge docs aligned with 5-column founder-mode shape |
| 2 | **No flock locking** | HIGH | CRAB TSV backend races under multi-process |
| 3 | **No identity validation** | MEDIUM | CRAB accepts any `identity` string |
| 4 | **No signing** | LOW | Founder-mode signing is opt-in; CRAB can defer |
| 5 | **Path resolution** | MEDIUM | CRAB uses `Path(config.bus.path)`; founder-mode uses repo-relative resolution |
| 6 | **Message vocabulary** | LOW | CRAB uses `PROPOSAL, ACK, STATUS, BLOCKED`; founder-mode adds `SITREP, DECISION, QUESTION, MILESTONE` |

---

## Bridge Spec (for cross-machine demo)

### Option A: CRAB writes directly to founder-mode bus
```python
# In CRAB config
"bus": {
    "backend": "tsv",
    "path": "../founder-mode/founder_mode/_state/coordination/messages.tsv",
    "format": "founder_mode"  # new: emit 5-column TSV
}
```

CRAB `bus_phase` would emit:
```
2026-05-11T20:37:00Z\tcrab-daemon\tall\tSTATUS\t[cleanup] OK — Pruned 2 branches
```

### Option B: Bridge agent (recommended)
A small bridge script polls CRAB's local bus and re-posts to founder-mode bus with validation:
```python
# bridge_crab_fm.py
for line in crab_bus.tail(n=1):
    if line["type"] == "STATUS" and line["dissonance"] is not None:
        post_to_fm_bus(
            from_="crab-daemon",
            to="all",
            type="STATUS",
            message=f"CRAB [{line['lane']}] validated={line['retrograde']['validated']} dissonance={line['retrograde']['dissonance']}"
        )
```

### Option C: Unified bus module (future)
Extract founder-mode `bus_writer_core` into a shared stdlib-only module that both projects import. CRAB already has zero third-party deps; this would preserve that constraint.

---

## Recommended Next Step

Implement **Option B** (bridge agent) as a 30-line script. It:
- Keeps CRAB self-contained
- Adds founder-mode validation/locking for cross-machine visibility
- Can be demoed immediately

---

## Demo Narrative

> "CRAB runs on Anvil. It prunes stale branches, validates its own work with Retrograde, and posts a receipt. The bridge agent picks up that receipt and posts it to the founder-mode coordination bus on nodezero. Now the fleet health dashboard shows CRAB's dissonance score alongside every other agent's status."
