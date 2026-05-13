# TECHNICAL FEASIBILITY REVIEW
## CRAB Unified Roadmap v2.0
### Reviewer: Technical Engineer (Subagent Assessment)
### Date: 2026-05-11
### Artifacts Examined:
- `docs/UNIFIED_ROADMAP.md` (440 lines)
- `crab_daemon.py` (625 lines)
- `tests/test_daemon.py` (207 lines, 18 tests)
- `docs/PRODUCTIZATION.md` (278 lines)
- `docs/research/2026-05-10_crustacean_paradigm_grounded.md` (332 lines)
- `docs/research/2026-05-11_crab_canon_symmetrical_runtime.md` (444 lines)

---

## 1. TRACK 1: PROTOCOL EVOLUTION — FEASIBILITY VERDICT

### Phase A: Core Hardening (v1.1)

| Item | Verdict | Assessment |
|------|---------|------------|
| **Retrograde Validator (5th phase)** | **YELLOW** | Implementable with current architecture. The phase separation in `crab_daemon.py` (lines 206, 247, 375, 451) is clean and the `CrabTurn` aggregate (line 93) can accept a new `retrograde` field. However, the 2.5-hour estimate is optimistic scaffolding time only. Each lane needs a domain-specific backward verifier; for `cleanup` you must capture or re-derive the `gone` list, for `git-audit` you must re-run `git status`, for `bus-audit` you must re-read and validate counts. A robust implementation with meaningful dissonance scoring and edge-case handling (partial failure, state changes between Act and Retrograde) is 1–2 days, not 2.5 hours. |
| **Config schema extensions** | **GREEN** | Trivial. `DaemonConfig`, `BusConfig`, and `LaneConfig` are extensible dataclasses with `from_json`/`to_json` (lines 139–173). Adding `dissonance_threshold` (float), `audit_backend` (str), and `retrograde_enabled` (bool) is minutes of work. |
| **6 Retrograde tests** | **YELLOW** | The existing test fixtures are well-structured and can be extended. Writing 6 meaningful tests (3 valid paths, 3 scuttle paths) that cover all 3 lanes with mocked git state and bus state is 2–3 hours, not 1 hour. The 1-hour claim assumes no fixture refactoring. |
| **`crab_validator.py` — decoupled Symmetry Guard** | **YELLOW** | Feasible but 1 week is tight. The bus backend architecture (lines 390–448) supports writing to a separate `bus/audit.tsv`. The hard part is not plumbing; it is defining what the decoupled validator actually *does*. The research doc (Sec 3.5) says it must not share weights/context with the executor to avoid confirmation bias. In this codebase, that means a separate process that reads `messages.tsv` and applies deterministic rules (Jaccard similarity over key-value pairs). Building a genuinely independent rule engine with useful coverage in 1 week is aggressive. |

### Phase B: Lateral Scuttle (v1.2)

| Item | Verdict | Assessment |
|------|---------|------------|
| **LOBSTER mode (reflex lane)** | **GREEN** | Straightforward. The `LANE_REGISTRY` (line 368) is a simple dict; you can add a reflex lane handler or a `LaneConfig.reflex: bool` flag that bypasses `check_phase`/`reason_phase` in `run_lane()` (lines 478–504). The 3-day estimate is generous; core implementation is hours. **Safety concerns are significant** (see Section 3). |
| **State compression (≤4KB tucked tail)** | **YELLOW** | Feasible as a mechanical file write, but "compression" implies semantic summarization. Without external dependencies, meaningful compression of arbitrary agent state into ≤4KB requires hand-written heuristics per lane. The portable daemon currently has no persistent memory between runs (only `_last_run` cooldown timestamps and the bus log). A naive `state.json` with raw field dumps is trivial; an intelligent "tucked tail" that actually improves performance is a research problem, not 2 days of engineering. |
| **Bus file locking (`flock`/`msvcrt.locking`)** | **GREEN** | Fully feasible stdlib-only. Unix: `fcntl.flock`. Windows: `msvcrt.locking`. The TSV backend (lines 390–398) and JSONL backend (lines 402–420) both use `open("a")`; wrapping the write in a lock is a localized change. 1 day is realistic. |
| **Simple retrieval (grep-based bus keyword filter)** | **GREEN** | Trivial. The bus is already read in `check_phase()` (lines 221–232) as a list of strings. Adding keyword filtering with Python's `in` operator or `re` module is minutes. The 2-day estimate is 5–10x too high unless "simple retrieval" secretly means a full BM25 index. |
| **Shadow / inversion lanes** | **YELLOW** | The registry supports it (lines 368–372). An inversion lane runs the opposite hypothesis. For `git-audit`, that means verifying nothing was missed. The challenge is defining the "negation" of each lane's intent in a computable way. 3 days is reasonable for 3 lanes. |

### Phase C: Academic Hardening (v1.3)

| Item | Verdict | Assessment |
|------|---------|------------|
| **Benchmark CRAB vs. reactive loops** | **RED/YELLOW** | The roadmap's own collision analysis admits this benchmark is meaningless without LOBSTER mode implemented first: "Without LOBSTER, the benchmark compares a deliberative system against a non-existent reactive alternative." The 1-week estimate is for execution; designing a fair benchmark is harder. Also, no external reactive baseline exists in the repo. |
| **CRAB Bus Specification (CBS) formal proposal** | **GREEN** | Documentation-only. No code blockers. 2 weeks is reasonable for a solid draft. |
| **"Decapod computing" taxonomy paper** | **YELLOW** | Writing a 4-week paper is feasible, but acceptance at listed venues (HotOS, OSDI WIP, NeurIPS workshop) is uncertain. The research docs themselves note that "Crab Canon" and "decapod computing" are neologisms with zero CS precedent. The paper would need strong empirical results to be competitive. |
| **Conference submission** | **YELLOW** | 2 weeks is realistic for formatting and submission, but contingent on the benchmark and paper being ready. |

---

## 2. TRACK 6: SCUTTLEBUTT LAYER — FEASIBILITY ASSESSMENT

### Verdict: YELLOW (prototype feasible, production risky)

**Is a stdlib-only gossip layer feasible?**
Yes, mechanically. It is an append-only JSONL file with a dataclass and a purge loop. The implementation sketch in the roadmap (lines 268–286) is sound Python.

**Concurrency issues with JSONL append:**
This is the critical flaw. The sketch ignores several concurrency hazards:

1. **Append races without locking:** Multiple processes opening `scuttlebutt.jsonl` in `"a"` mode and calling `f.write()` concurrently can produce interleaved lines on some filesystems. The roadmap says "stdlib-only," which means `fcntl.flock` or `msvcrt.locking` must be used — but the sketch does not mention locks.

2. **Purge is read-modify-write:** The purge rule states: "At every CHECK phase, the daemon purges entries where `expires_at` < now." This requires reading the entire file, filtering, and rewriting it. If two daemons purge simultaneously, the last writer wins and recent entries from the other daemon are lost. JSONL append-only semantics break down as soon as you need deletion.

3. **No atomic rename pattern:** A safe purge would write to a temp file and atomically replace (`os.replace`). The sketch does not show this.

4. **Provenance chain integrity:** The `provenance: list[str]` field assumes cooperative agents append correctly. A buggy or malicious agent can inject arbitrary provenance chains. The roadmap admits validation is "None — anyone can post anything," which is fine for a gossip layer but means scuttlebutt cannot feed into safety-critical paths.

**Confidence decay:**
The roadmap correctly flags this as "ARBITRARY — needs A/B test." Linear decay, exponential decay, and step decay are all modeling choices without empirical grounding. This is not an engineering blocker; it is a research question.

**Bottom line:** Scuttlebutt is feasible as a single-process prototype or low-traffic demo. As a multi-agent, multi-process gossip layer, it needs file locking, atomic purge, and careful isolation from the canonical bus. The roadmap itself admits: "There is zero evidence that a probabilistic gossip layer improves multi-agent coordination."

---

## 3. LOBSTER MODE SAFETY ANALYSIS

### Verdict: RED for unsupervised use; YELLOW for guarded kill-switch use

**Claim:** "LOBSTER mode (reflex lane, skips Check/Reason)"

**Is this safe?**
No. Skipping Check/Reason removes the three safety mechanisms that define CRAB:

1. **Blocker detection:** The Reason phase reads `check.blockers` (line 248) and halts if unresolved blockers exist. LOBSTER bypasses this.
2. **Stash awareness:** The Reason phase halts stash-sensitive lanes when stashes exist (line 256). LOBSTER bypasses this.
3. **State reconnaissance:** The Check phase reads git branch, dirty state, stash count, and bus tail (lines 210–234). LOBSTER acts without this context.

**Failure modes:**

| Failure Mode | Scenario | Impact |
|--------------|----------|--------|
| **Stale-state action** | Reflex lane triggers based on old signal; git state has changed | Incorrect pruning, wrong audit conclusions |
| **Blocker blindness** | Another agent posted BLOCKED; reflex lane ignores it and mutates state | Violates coordination invariant, causes merge conflicts or data corruption |
| **Race condition amplification** | Two reflex lanes on two agents fire simultaneously on the same resource | Double mutation, lost updates, corrupted bus |
| **Cascading reflex** | One reflex lane's action triggers another reflex condition | Uncontrolled chain reaction, potential infinite loop without cooldown |
| **Audit gap** | No rationale recorded for why action was taken | Debugging becomes impossible; "who deleted this branch and why?" has no answer |
| **Security invisibility** | The roadmap's own collision analysis flags this: "Redteam audit must explicitly test reflex lanes or they will be invisible to security scanning" | Unaudited execution path is an attack surface |

**Mitigation:**
The research document correctly frames LOBSTER as "kill switch, circuit breaker" — emergency-only reflexes that halt or signal, not mutate. If LOBSTER lanes are restricted to:
- Read-only health checks
- Emitting alerts (not acting)
- Halt/kill operations with no external side effects

…then the risk drops to YELLOW. But the roadmap does not explicitly restrict LOBSTER to read-only/halt actions. If LOBSTER runs `cleanup` (branch deletion) without Check/Reason, it is dangerous.

**Recommendation:** LOBSTER mode must be gated behind a `lobster_mutable: bool = False` config default, with loud warnings in docs and CLI.

---

## 4. RETROGRADE VALIDATOR — TIME ESTIMATE REALISM

### Claimed: 2.5 hours (Track 1, Phase A) / 2–8 hours (Track 3, Immediate)

### Verdict: YELLOW (scaffolding is 2.5 hrs; production-ready is 1–2 days)

**What the research doc breaks down:**
- `RetrogradeResult` dataclass: 1 min
- `CrabTurn.retrograde` field: 1 min
- `RetrogradeValidator` class: 30 min
- `RETROGRADE_REGISTRY` + 3 handlers: 45 min
- `run_lane()` integration: 10 min
- Config schema: 5 min
- Serialization: 5 min
- `default_config()`: 5 min
- 6 tests: 60 min
- **Total: ~2.5 hours**

**Why this is optimistic:**

1. **The forward pass doesn't capture enough state for meaningful retrograde.**
   - `ActResult` (line 83) stores `actions_taken: list[str]` as human-readable strings like `"Found 3 stale [gone] branches"` and `"Pruned 3 gone branches"`. To retrograde "verify pruned branches were in `gone` list," you must either:
     - (a) Parse these human-readable strings (fragile), or
     - (b) Add structured data to `ActResult` (changes forward pass contract), or
     - (c) Re-run `git branch -vv` during retrograde (wasteful, and state may have changed).
   - Option (b) is the right engineering choice but it changes `ActResult` and all existing lanes.

2. **Dissonance scoring is harder than Jaccard over strings.**
   - The research doc proposes `dissonance = 1 - J(intent_reconstructed, intent_original)` using Jaccard similarity.
   - For `cleanup`: intent = "prune stale branches"; outcome = "pruned 3 branches". What is the set intersection? You need to extract structured entities from both intent and outcome. This requires NLP or at least regex parsing of `actions_taken` strings.
   - For `bus-audit`: intent = "verify bus integrity"; outcome = "Bus has 47 messages". Reconstructing intent from `ReasonResult.rationale` (a free-text string) is not deterministic.

3. **Edge cases multiply quickly:**
   - Forward action fails → retrograde should detect failure (easy)
   - Forward action partially succeeds → retrograde must score partial dissonance (hard)
   - World state changes between Act and Retrograde → retrograde compares against stale expected state (requires snapshotting)
   - Bus file is locked or corrupted during retrograde → needs error handling

4. **The 6 tests claim assumes perfect fixtures.**
   - Writing a test for "scuttle on dissonance" requires controlling both the forward action outcome and the retrograde verifier's view of it. This means either heavy mocking or a full git repo + bus file per test case. The existing tests use `tmp_path` git repos, so this is doable, but 60 minutes for 6 robust tests is tight.

**Realistic estimate:**
- **2.5 hours:** Skeleton compiles; `RetrogradeValidator` dispatches to no-op handlers; tests pass with mocks.
- **1 day:** Meaningful retrograde handlers for all 3 built-in lanes with basic dissonance scoring.
- **2 days:** Robust edge-case handling, structured `ActResult` metadata, proper test coverage, and integration with config-driven `dissonance_threshold`.

**What would a REAL retrograde validator need to do?**

1. **Intent capture:** Store structured intent from `ReasonResult` (not just free-text rationale) — e.g., `intent_entities: {"lane": "cleanup", "target_branches": ["feat/old"], "expected_action": "prune"}`.
2. **Effect capture:** Store structured effects in `ActResult` — e.g., `effect_entities: {"branches_pruned": 3, "branches_list": ["feat/old", "feat/older"]}`.
3. **World snapshot:** Capture relevant world state at the end of Act (or beginning of Retrograde) so comparison is temporally grounded.
4. **Backward lens per lane:** A deterministic function `retrograde(lane, intent, effect, world_state) -> dissonance` that knows how to reconstruct expected state from intent and compare to actual effect + world snapshot.
5. **Threshold enforcement:** If `dissonance > threshold`, trigger scuttle (lateral recovery to another lane or halt).
6. **Audit trail:** Append structured retrograde results to `bus/audit.tsv` for human inspection.
7. **Independence guarantee:** For true Symmetry Guard, run in separate process with no shared memory (the 1-week `crab_validator.py` item).

This is essentially an **assertion framework for agent actions** — useful, but not 2.5 hours of work for 3 lanes.

---

## 5. HIDDEN INFRASTRUCTURE DEPENDENCIES

### Verdict: Multiple items depend on systems that do not exist

| Missing Infrastructure | Dependent Items | Risk |
|------------------------|-----------------|------|
| **Symmetry Guard (`crab_validator.py`)** | Retrograde phase (listed as "1 week"), Track 3 "Symmetry Guard process" | MEDIUM. The decoupled validator is a prerequisite for meaningful retrograde in production. Without it, retrograde is just self-critique, which research warns "can degrade planning performance" (arXiv:2310.08118). |
| **LOBSTER mode implementation** | Academic benchmark ("Benchmark CRAB vs. reactive loops") | HIGH. The roadmap's own collision analysis states: "Without LOBSTER, the benchmark compares a deliberative system against a non-existent reactive alternative." The benchmark *requires* LOBSTER to be meaningful. |
| **Scuttlebutt Layer** | Track 1 collision: "If Retrograde reads scuttlebutt for dissonance calibration, a buggy scuttlebutt implementation could poison Retrograde scores." | MEDIUM. The dependency graph shows Scuttlebutt below Public Release, but the collision analysis reveals a hidden coupling. |
| **Shadow / inversion lanes** | "Contrapuntal dashboard" (optional), Track 3 "Inversion lanes" | LOW. Registry supports them, but no handlers exist. |
| **Coordination Bus as standalone module** | Tier 2 Productization (P1), CRAB Dashboard | MEDIUM. The portable daemon has a bus backend, but a standalone `crab-bus` product needs HUMMBL-specific code extracted and refactored. |
| **flock-based locking (production)** | "Bus file locking" in portable daemon | LOW. The research doc notes HUMMBL production has `flock` via `bus_writer_core.py`, but the portable daemon does not. The portable version must implement its own. |

**Critical path issue:** The dependency graph (lines 316–340) shows `[Retrograde] [Brand] [Bus Spec]` in parallel, then `[LOBSTER] [Dashboard] [Coordination Bus]`, then `[Scuttlebutt]`, then `[Public Release]`. But the collision analysis reveals that **Academic benchmark → LOBSTER** is a hidden hard dependency. If LOBSTER is deferred, the benchmark must be redesigned or deferred too.

---

## 6. TEST COUNT CLAIMS — CONSISTENCY CHECK

### Claim: "625 lines, 18 tests, 3 lanes (cleanup, git-audit, bus-audit), 4 bus backends."

### Verdict: GREEN (counts are accurate; coverage is thin)

**Test count verification:**

| Test Class | Tests | Description |
|------------|-------|-------------|
| `TestDataStructures` | 2 | Config roundtrip, bus pluggability |
| `TestCheckPhase` | 3 | Branch detection, stash counting, blocker detection |
| `TestReasonPhase` | 3 | Clean proceed, blocker halt, stash-sensitive halt |
| `TestActPhase` | 4 | Cleanup lane, git-audit lane, bus-audit lane, unknown lane failure |
| `TestBusPhase` | 2 | Dry-run no-op, stdout backend capture |
| `TestCrabDaemon` | 2 | Run once, cooldown skip |
| `TestCLI` | 2 | `--init` writes config, `--once --dry-run` |
| **TOTAL** | **18** | ✓ Matches claim |

**Coverage gaps noted by the research doc itself:**
- No integration test for callback backend (shell invocation is environment-dependent).
- No test for concurrent lane execution.
- No test for bus file corruption recovery.
- No test for JSONL backend (only TSV and stdout are exercised).
- All mutation tests run in `dry_run=True` mode; no test verifies actual git branch pruning or actual TSV append.

**Additional gaps observed:**
- No test for config schema migration (adding new fields to old configs).
- No test for `poll_interval` or long-running daemon loop behavior.
- No test for invalid bus path handling (permissions, nonexistent parent dirs beyond `mkdir(parents=True, exist_ok=True)`).
- No test for `DaemonConfig.from_json` with missing fields.

**Conclusion:** The "18 tests" claim is factually correct. However, the test suite is not production-hardened. Adding Retrograde tests (6 claimed), LOBSTER tests, locking tests, and corruption recovery tests would bring the total to 30+ tests for v1.1 stability.

---

## 7. TECHNICAL RISK REGISTER (TOP 5)

| Rank | Risk | Likelihood | Impact | Mitigation |
|------|------|------------|--------|------------|
| **1** | **LOBSTER mode creates invisible, un-auditable execution paths.** If reflex lanes perform mutable operations without Check/Reason, blockers are ignored and audit trails are thin. The roadmap's own collision analysis rates this MEDIUM, but the safety impact is severe if LOBSTER touches production data. | Medium | High | Restrict LOBSTER to read-only / halt-only operations by default. Require explicit `lobster_mutable=true` config with warning. Redteam must explicitly test reflex lanes. |
| **2** | **Retrograde dissonance scoring is ill-defined for free-text rationales.** The Jaccard formula over `actions_taken` strings is fragile. A "2.5 hour" implementation will likely produce false positives (scuttle on valid actions) or false negatives (pass on erroneous actions), undermining trust in the safety mechanism. | High | Medium | Invest 1–2 days in structured `ActResult` metadata (entity extraction) rather than parsing human-readable strings. |
| **3** | **Scuttlebutt JSONL purge creates read-modify-write race conditions.** Multi-process purge without atomic rename or file locking will cause data loss. The "gossip layer" intuition is sound; the concurrent file I/O is not. | High | Medium | Implement atomic purge: read → filter → write temp → `os.replace`. Add advisory locking. Single-process deployments are safe; multi-process is not. |
| **4** | **Academic benchmark is methodologically flawed without LOBSTER.** The benchmark compares CRAB (4-phase) vs. reactive loops, but LOBSTER does not exist. This produces a strawman comparison that would not survive peer review. | Medium | High | Implement LOBSTER *before* running benchmark, or redesign the benchmark to compare against an external reactive baseline (e.g., a simple 2-phase loop). |
| **5** | **Productization timeline assumes clean extraction from deeply coupled founder-mode.** `PRODUCTIZATION.md` documents 512 Tailscale IP references, 46 hardcoded emails, 19 machine profiles, and 36 hardcoded bus paths. The "2–4 weeks per Tier 2 product" estimate assumes this coupling is superficial. Historical evidence suggests infrastructure stripping is always 2–3x harder than estimated. | High | Medium | Start with Schema Validator (already portable, 1 week). Use it as a pilot to calibrate extraction velocity before committing to Dashboard or Briefing Engine timelines. |

---

## 8. SUMMARY

**What is genuinely ready:**
- Config schema extensions (minutes)
- LOBSTER mode scaffolding (hours, but safety review needed)
- Bus file locking (1 day, stdlib-only)
- Simple grep retrieval (hours)
- Test count claims (accurate, though coverage is thin)

**What is optimistic:**
- Retrograde Validator at 2.5 hours (realistic: 1–2 days for robustness)
- "Simple retrieval" at 2 days (realistic: hours)
- Scuttlebutt as a production-grade gossip layer (prototype only; needs locking and atomic purge)
- Productization timelines for Tier 2 items (founder-mode coupling is severe)

**What is unsafe as specified:**
- LOBSTER mode performing mutable operations without Check/Reason
- Retrograde feeding from Scuttlebutt (probabilistic gossip poisoning deterministic validation)
- Academic benchmark without an implemented reactive baseline

**What depends on missing infrastructure:**
- Symmetry Guard (`crab_validator.py`) — not built
- Shadow/inversion lanes — registry supports, but no handlers
- LOBSTER mode — required for meaningful benchmark
- Scuttlebutt — explicitly marked PROTOTYPE with zero evidence of utility

**Overall assessment:** The CRAB Unified Roadmap v2.0 is a coherent strategic document with honest self-criticism (Section: "What This Roadmap Gets Wrong"). The technical architecture of `crab_daemon.py` is clean enough to support the proposed evolution. However, time estimates for Retrograde and Tier 2 productization are 2–3x optimistic. The highest-risk item is LOBSTER mode safety, followed by Scuttlebutt concurrency. The roadmap should be treated as a vision document with phased gates; each gate needs a separate technical design review before execution.

---

*No files were modified during this review.*
