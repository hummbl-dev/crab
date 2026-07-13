# CRAB Peer Review & Session Conventions
## Post-AAR Recommendation Implementation
**Date:** 2026-05-11  
**Source:** AAR_2026-05-11.md recommendations 1, 2, 4, 5, 6

---

## 1. Session-Close Checklist (Rec 1: Prevent Working Tree Loss)

**The failure:** The previous session ended with uncommitted v2.0 hardening edits. A subsequent `git checkout -- docs/UNIFIED_ROADMAP.md` between sessions discarded ~116 lines of hardening work. Recovery consumed ~35 minutes.

**The fix:** Every session that modifies files must execute this checklist before handoff.

```bash
# CRAB Session-Close Checklist
# Run this before ending any session that touched files

echo "=== SESSION CLOSE CHECKLIST ==="

echo "[1/5] Git status..."
git status --short

echo "[2/5] Diff stats..."
git diff --stat

echo "[3/5] Staged stats..."
git diff --cached --stat

echo "[4/5] Test run..."
uv run pytest tests/ -q || echo "TESTS FAILED -- DO NOT COMMIT"

echo "[5/5] Decision:"
# If any modified/untracked files exist:
#   - Commit if tests pass and changes are coherent
#   - Stash if tests fail or changes are incomplete
#   - Never leave working tree dirty without a commit or stash

if [ -n "$(git status --porcelain)" ]; then
    echo "WORKING TREE IS DIRTY. Options:"
    echo "  (a) git add && git commit"
    echo "  (b) git stash push -m '<session-desc>'"
    echo "  (c) git checkout -- <file>  # ONLY if discarding is intentional"
    echo "DO NOT end session without choosing (a) or (b)."
fi
```

**Hard rule:** A session with uncommitted changes and no stash is an incomplete session. The next session inherits technical debt equal to the time needed to reconstruct the lost state.

---

## 2. Human External Auditor Designation (Rec 2)

**The problem:** The Evidence Matrix, Status Legend, and all measurement artifacts are self-graded by the agents that authored the claims. The Measurement reviewer identified: "There is no measurement-independent observer anywhere in the system. Campbell drift is structurally inevitable."

**The requirement:** One human external auditor, designated by the operator, who:
- Re-grades the Evidence Matrix quarterly
- Reviews any claim upgraded from "Internal" or below to "External" or above
- Has read access to the repo but no write access (read-only independence)
- Is not an agent, not involved in CRAB development, and has no incentive to inflate grades

**Pending operator action:**

| Field | Status |
|---|---|
| Auditor name | **PENDING — operator to designate** |
| Auditor contact | **PENDING** |
| First review date | **PENDING — target: 2026-08-11 (3 months)** |
| Review scope | Evidence Matrix + Status Legend + any new metrics introduced since last review |
| Grade change rule | Any upgrade from Internal/Anecdotal → Empirical/External requires the auditor's sign-off |

**Until an auditor is designated:** All Evidence Matrix grades remain provisional. Any grade upgrade must include a note: "UNAUDITED — pending external reviewer."

---

## 3. Peer Review Swarm Conventions (Rec 4: Redteam Inclusion + Rec 5: Script Pre-Flight)

### 3A. Minimum Reviewer Set (Rec 4)

Future peer review swarms must include **at least 5 lenses**:

| # | Lens | Profile | What It Finds |
|---|---|---|---|
| 1 | Cybernetics | `ashby` | Requisite variety, feedback loops, homeostasis |
| 2 | Measurement | `measurement` | Goodhart/Campbell, metric gaming, calibration |
| 3 | Technical | `subagent_general` | Feasibility, implementation blockers, time realism |
| 4 | External Credibility | `subagent_general` | Academic/VC defensibility, prior work, market fit |
| 5 | **Security / Redteam** | `subagent_general` | **Injection, escape, adversarial exploitation** |

**The redteam reviewer is mandatory, not optional.** The Technical reviewer found LOBSTER safety issues; an explicit redteam lens would have found:
- Scuttlebutt injection vectors (poisoning provenance chains)
- LOBSTER escape paths (reflex lane bypassing governance)
- Bus message forgery (unvalidated identity in gossip layer)
- Retrograde manipulation (tuning dissonance threshold to hide failures)

**Redteam scope for document review:**
- If the document proposes a system: "How would an adversarial agent break this?"
- If the document proposes metrics: "How would an agent game this to look good while failing?"
- If the document claims safety: "What is the shortest path from normal operation to catastrophic failure?"

### 3B. Script Pre-Flight Convention (Rec 5)

**The failure:** The `_harden_roadmap.py` recovery script was written after a failed `edit` tool call, without inspecting the actual file content. Two edge cases were missed.

**The fix:** Before writing any bulk-edit or recovery script:

```python
# Pre-flight verification — run this BEFORE encoding assumptions in a script

import subprocess

# 1. Verify target strings are unique
targets = [
    "## Track 1: Protocol Evolution (The CRAB Daemon)",
    "## Status Legend",
    # ... all strings you plan to replace
]

for t in targets:
    result = subprocess.run(
        ["grep", "-n", "-c", t, "docs/UNIFIED_ROADMAP.md"],
        capture_output=True, text=True
    )
    count = int(result.stdout.strip())
    if count != 1:
        print(f"FAIL: '{t[:40]}...' appears {count} times (expected 1)")
    else:
        print(f"PASS: '{t[:40]}...' is unique")

# 2. Verify insertion anchors exist and are in expected order
anchors = [
    "## Phase Structure: The Unified Turn",
    "## Track 1: Protocol Evolution",
    "## Track 6: The Scuttlebutt Layer",
]
# ... check that each anchor appears exactly once and in sequence

# 3. Only after pre-flight passes, write the script
```

**Rule:** No bulk-edit script ships without passing pre-flight. Manual edits are acceptable for ≤3 changes; scripts are required for ≥4 changes, and scripts require pre-flight.

---

## 4. Session-State Snapshot Convention (Rec 6)

**The problem:** No snapshot of session state was captured before handoff. When the next session began, the working tree state was unknown and a `git checkout` silently destroyed work.

**The fix:** A lightweight snapshot script captures session state at close.

```bash
#!/bin/bash
# session-snapshot.sh — save session state before handoff
# Usage: ./session-snapshot.sh "<brief session description>"

DESC="${1:-unnamed session}"
SNAPDIR="_state/session-snapshots"
mkdir -p "$SNAPDIR"

TS=$(date -u +%Y%m%d-%H%MZ)
SNAPFILE="$SNAPDIR/$TS.txt"

echo "=== CRAB Session Snapshot ===" > "$SNAPFILE"
echo "Timestamp: $TS" >> "$SNAPFILE"
echo "Description: $DESC" >> "$SNAPFILE"
echo "" >> "$SNAPFILE"

echo "--- Git Status ---" >> "$SNAPFILE"
git status --short >> "$SNAPFILE"
echo "" >> "$SNAPFILE"

echo "--- Diff Stats ---" >> "$SNAPFILE"
git diff --stat >> "$SNAPFILE"
echo "" >> "$SNAPFILE"

echo "--- Commit Range (last 5) ---" >> "$SNAPFILE"
git log --oneline -5 >> "$SNAPFILE"
echo "" >> "$SNAPFILE"

echo "--- Key File Checksums ---" >> "$SNAPFILE"
for f in docs/UNIFIED_ROADMAP.md src/crab_daemon.py tests/test_daemon.py; do
    if [ -f "$f" ]; then
        md5sum "$f" >> "$SNAPFILE"
    fi
done
echo "" >> "$SNAPFILE"

echo "--- Test Status ---" >> "$SNAPFILE"
uv run pytest tests/ -q >> "$SNAPFILE" 2>&1 || echo "TESTS FAILED" >> "$SNAPFILE"

echo "Snapshot saved to: $SNAPFILE"
```

**Integration with session-close checklist:** Item [5/5] of the checklist calls `session-snapshot.sh` automatically. The snapshot is not committed; it lives in `_state/session-snapshots/` which is `.gitignore`d.

**Retention policy:** Keep snapshots for 90 days. After 90 days, archive to `_state/session-snapshots/archive/` or delete. The purpose is short-term recovery, not long-term audit.

---

## Implementation Status

| Recommendation | Convention / Artifact | Status | Owner |
|---|---|---|---|
| Rec 1: Session-close checklist | `CONVENTIONS.md` §1 + inline script | **Documented** | All agents |
| Rec 2: Human external auditor | `CONVENTIONS.md` §2 — pending operator | **Blocked on operator** | Operator |
| Rec 4: Redteam inclusion | `CONVENTIONS.md` §3A — 5-lens minimum | **Documented** | Review coordinator |
| Rec 5: Script pre-flight | `CONVENTIONS.md` §3B — pre-flight script | **Documented** | All agents |
| Rec 6: Session-state snapshot | `CONVENTIONS.md` §4 — snapshot script | **Documented** | All agents |

**Next action:** Operator designates a human external auditor. Until then, all Evidence Matrix grades are provisional.

---

**Documented by:** `codex`  
**Canonical repo:** `hummbl-dev/crab#main`  
**Source AAR:** `docs/peer_reviews/AAR_2026-05-11.md`
