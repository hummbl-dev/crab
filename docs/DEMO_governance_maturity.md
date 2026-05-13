# Governance Maturity Demo Script
## CRAB + HUMMBL Primitives — 5 Minutes

---

## Setup (30 seconds)

```bash
cd PROJECTS/crab
uv run pytest tests/test_daemon.py::TestRetrogradePhase -v
```

Expected: 6/6 tests pass in ~2 seconds.

---

## Demo Narrative

### 1. The Forward Pass (30 seconds)

```bash
uv run crab_daemon.py --once --lane cleanup --dry-run
```

Show the 4-phase output:
```
CHECK: branch=main dirty=False stashes=0 blockers=0
REASON: should_act=True type=STATUS rationale=prune-gone
ACT: success=True actions=2 errors=0
BUS: posted=True
```

**Narrative:** "This is what every agent runtime does — check, decide, act, report."

---

### 2. The Backward Pass — RETROGRADE (1 minute)

Run the same command **without** `--dry-run` (on a test repo):

```bash
uv run crab_daemon.py --once --lane cleanup --config test-config.json
```

Show the 5th phase:
```
RETROGRADE: validated=True dissonance=0.00 scuttle=False findings=["OK: pruned == found"]
```

**Narrative:** "This is what no competitor does. After the agent reports success, Retrograde re-reads the system state and verifies the claim."

---

### 3. The Scuttle Condition (1 minute)

Show the test that triggers scuttle:

```python
# From tests/test_daemon.py
def test_retrograde_cleanup_orphaned_prune():
    # Agent claims it pruned "feat/phantom"
    # But "feat/phantom" was never in the found list
    # Dissonance: 0.8 → SCUTTLE
```

Run it:
```bash
uv run pytest tests/test_daemon.py::TestRetrogradePhase::test_retrograde_cleanup_orphaned_prune -v
```

Show output:
```
RETROGRADE: validated=False dissonance=0.80 scuttle=True findings=["Orphaned prune: feat/phantom not in found list"]
```

**Narrative:** "The agent tried to prune a branch it never found. Retrograde caught it. The lane is scuttled. No further action until human review."

---

### 4. Integration with HUMMBL Stack (1 minute)

Show the kill switch escalation table:

| Dissonance | Kill Switch Mode | Action |
|---|---|---|
| 0.0–0.3 | DISENGAGED | Normal operation |
| 0.3–0.5 | HALT_NONCRITICAL | Pause non-essential lanes |
| 0.5–0.8 | HALT_ALL | Stop all lanes, alert operator |
| 0.8–1.0 | EMERGENCY | Full shutdown, preserve audit trail |

**Narrative:** "Retrograde doesn't just log a number. It triggers the same kill switch that powers HUMMBL's production governance."

---

### 5. The Track-Kill Criteria (1 minute)

Show the roadmap excerpt:

```markdown
**Kill criterion**: This track will be retired if Retrograde validator
fails to detect dissonance in 3 consecutive manual audits.
```

**Narrative:** "This is not a promise to be careful. This is a mechanical commitment: if Retrograde stops working, Track 1 dies. No appeals."

---

### 6. The Peer-Review Pipeline (30 seconds)

Show the 4-lens review synthesis:

```bash
cat docs/peer_reviews/2026-05-11_unified_peer_review.md | head -20
```

**Narrative:** "Retrograde was not built in isolation. It was reviewed by 4 independent AI agents — cybernetics, metrology, engineering, external — before a single line of code was written."

---

## Closing Line

> "This is not a roadmap item. This is a running system. And it is the first time an AI agent runtime has verified its own outputs against ground truth with automatic scuttle."

---

## Fallback Plans

| Failure | Fallback |
|---|---|
| Tests fail | Show `git log --oneline -3` + `git show b79f4ee --stat` |
| No test repo | Use `--dry-run` for forward pass, show test code for Retrograde |
| Demo environment unavailable | Show `docs/peer_reviews/2026-05-11_unified_peer_review.md` as evidence of rigor |
