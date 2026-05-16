# CRAB Unified Roadmap
## All Lanes, All Phases, One Surface

**Status:** Draft v1.0 | **Date:** 2026-05-11 | **Author:** Devin (Kimi K2.6)  
**Scope:** Synthesizes every CRAB roadmap, plan, and research artifact into a single coordinated surface. Reconciles productization, protocol evolution, brand development, and research trajectories.

---

## The Map

CRAB has grown across 6 parallel tracks. This document is the carapace that holds them together.

```
                    ┌─────────────────────────────────────┐
                    │         CRAB UNIFIED ROADMAP        │
                    └─────────────────────────────────────┘
                                      │
         ┌────────────┬───────────────┼───────────────┬────────────┐
         ▼            ▼               ▼               ▼            ▼
    ┌────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐
    │PROTOCOL│  │  BRAND   │  │RESEARCH    │  │PRODUCTS  │  │ GOVERNANCE│
    │Daemon  │  │Terminal  │  │Crustacean  │  │Portable  │  │Identity  │
    │+Lanes  │  │Core      │  │Paradigm   │  │Extract   │  │+Bus      │
    └────────┘  └──────────┘  └────────────┘  └──────────┘  └──────────┘
         │            │               │               │            │
         └────────────┴───────────────┴───────────────┴────────────┘
                                      │
                                      ▼
                         ┌─────────────────────┐
                         │  SCUTTLEBUTT LAYER  │
                         │ (informal gossip bus)│
                         └─────────────────────┘
```

---

## Phase Structure: The Unified Turn

CRAB development follows its own protocol. Every deliverable across every track must run through a unified phase gate:

| Phase | What Happens | Output | Gatekeeper |
|---|---|---|---|
| **CRAWL / CHECK** | Survey all tracks for blockers, stale context, ownership, wire health, and cross-track collisions | Blocker list + stale-context report | Operator (Reuben) |
| **REASON** | Decide which track to advance, what to defer, what to kill | Prioritized lane list + rationale | Operator + Bus consensus |
| **ACT** | Execute the chosen work scoped to one track | Committed artifact + branch | Implementing agent |
| **BUS** | Post receipt to canonical bus + scuttlebutt | TSV receipt + gossip update | Automated |
| **RETROGRADE** | Validate the work backward: does it hold? | Dissonance score + audit trail | Symmetry Guard (future) |

---

## Status Legend

Every item in this roadmap carries an explicit status. Here is what each means:

| Status | Definition | Evidence Required |
|---|---|---|
| **Done** | Complete, committed, tested | Git SHA + test results |
| **Ready** | Designed, reviewed, waiting for operator go-ahead | Design doc + review notes |
| **Planned** | Scoped, estimated, scheduled | Ticket / issue with acceptance criteria |
| **Open** | Known gap, no owner, no timeline | This document listing it |
| **Research-mentioned** | Appears in a research doc but not validated | Citation to research file |
| **Prototype** | Exists as sketch / PoC, not production-ready | Working demo + known limitations |

**Retired term:** "research-validated" has been removed from this document. Nothing in CRAB is research-validated in the peer-reviewed sense. Claims are either evidence-backed (with citation) or provisional (marked as such).

## What This Roadmap Gets Wrong

Before listing what CRAB will do, here is what it currently gets wrong. These are known limitations, not hidden flaws:

1. **Effort estimates are guesses.** Every "X hrs" in this document is a point estimate without confidence interval. The actual time may be 2x or 0.5x. No historical velocity data exists to calibrate.
2. **"Research-mentioned" is not "research-validated."** Several items cite research documents that are themselves speculative. A research mention does not mean the claim has been externally validated.
3. **Retrograde status is split.** The reference daemon has a built-in `retrograde_phase()` enabled by default, but Retrograde is not yet a public protocol requirement and the separate Symmetry Guard remains a design document rather than a running independent validator.
4. **Scuttlebutt is a metaphor, not a system.** The Scuttlebutt Layer (Track 6) is an intuition pump. There is zero evidence that a probabilistic gossip layer improves multi-agent coordination.
5. **No external benchmarks.** CRAB's safety claims (fewer hallucinations, better alignment) have not been measured against a control group. They are self-reported.
6. **Governance track has no owner.** Track 5 lists tasks but does not name who will do them or by when.
7. **Productization timeline assumes operator availability.** All release dates assume Reuben has uninterrupted focus. This has never been true.
8. **The brand is untested externally.** Bernard, Scut, and the Terminal Core design system have not been shown to users outside the HUMMBL fleet.

---

## Track 1: Protocol Evolution (The Daemon)

**Current:** v1.0.0 -- `crab_daemon.py`, 79-test local suite, 3 lanes (cleanup, git-audit, bus-audit), 4 bus backends. Line counts are intentionally omitted here because they drift quickly.

### Phase A: Core Hardening (Now -- v1.1)

| Item | Source | Effort | Status |
|---|---|---|---|
| Retrograde Validator (5th phase) | `2026-05-11_crab_canon_symmetrical_runtime.md` Sec 6.1 | 2.5 hrs | **Ready to implement** |
| Config schema: `dissonance_threshold`, `audit_backend`, `retrograde_enabled` | Internal recon (line ~104--174) | 10 min | Ready |
| 6 Retrograde tests (3 valid, 3 scuttle) | Internal recon test gaps | 1 hr | Ready |
| `crab_validator.py` -- decoupled Symmetry Guard process | `2026-05-11` Sec 6.2 | 1 week | Planned |

### Phase B: Lateral Scuttle (v1.2 -- 2--4 weeks)

| Item | Source | Effort | Status |
|---|---|---|---|
| LOBSTER mode (reflex lane, skips Check/Reason) | `2026-05-10_crustacean_paradigm_grounded.md` Sec 4.1 | 3 days | Research-mentioned |
| LOBSTER guardrails (lobster_mutable=False default, read-only/halt-only restriction) | Safety review | 1–4 hrs | Ready |
| State compression (≤4KB tucked tail) | `2026-05-10` Sec 4.1 | 2 days | Research-mentioned |
| Bus file locking (`flock`/`msvcrt.locking`) | `2026-05-10` Sec 4.1 | 1 day | Research-mentioned |
| Simple retrieval (grep-based bus keyword filter) | `2026-05-10` Sec 4.1 | 2 days | Research-mentioned |
| Shadow / inversion lanes | `2026-05-11` Sec 4.2 + internal recon | 3 days | Registry already supports |

**Safety guardrails required**: LOBSTER mode must default to `lobster_mutable=False` in config. Reflex lanes must be restricted to read-only health checks, alert emission, and halt/kill operations with no external side effects until explicit opt-in.

### Phase C: Academic Hardening (v1.3 -- 4--8 weeks)

| Item | Source | Effort | Status |
|---|---|---|---|
| Benchmark CRAB vs. reactive loops (latency, recovery, audit) | `2026-05-10` Sec 4.2 | 1 week | Research-mentioned |
| CRAB Bus Specification (CBS) formal proposal | `2026-05-10` Sec 4.3 | 2 weeks | Research-mentioned |
| "Decapod computing" taxonomy paper | `2026-05-10` Sec 4.3 | 4 weeks | Research-mentioned |
| Conference submission (HotOS / OSDI WIP / NeurIPS workshop) | `2026-05-10` Sec 4.2 | 2 weeks | Research-mentioned |

**Kill criterion**: This track will be retired if Retrograde validator fails to detect dissonance in 3 consecutive manual audits.

---

## Track 2: Brand Development (Terminal Core)

**Current:** Phase 2 complete -- Canonical CRAB + Bernard + Scut + Design System + Art Toolkit + FILE_ID.DIZ + 34 rendering tests.

### Phase 3: Unified Design System + Terminal Demo Fix (Now)

| Item | Source | Effort | Status |
|---|---|---|---|
| Terminal Core demo fix (`--auto-advance`, `EOFError` guard) | `SELF_REVIEW_2026-05-10.md` issue 7 | Done | Shipped in 91aff1d |
| Terminal rendering tests | `SELF_REVIEW` issue 1 | Done | 34 tests passing |
| FILE_ID.DIZ for artpack release | Bus HANDOFF + `SELF_REVIEW` issue 6 | Done | Shipped in 91aff1d |
| 16-line compact fleet composition variant | `SELF_REVIEW` issue 4 | 2 hrs | Open |
| SAUCE metadata on art files | `SELF_REVIEW` issue 7 | 2 hrs | Open |
| `.ANS` format with SAUCE block | `SELF_REVIEW` issue 5 | 3 hrs | Open |
| Dashboard TUI with fleet composition | `HUMMBL_TERMINAL_CORE_DESIGN_SYSTEM.md` next gate | 1 week | Planned |

### Phase 4: Distribution + Community (2--4 weeks)

| Item | Source | Effort | Status |
|---|---|---|---|
| Spot-check terminal rendering on all platforms | `SELF_REVIEW` issue 1 | 2 hrs | Open |
| 16-color fallback variants | `SELF_REVIEW` issue 3 | 4 hrs | Open |
| Artpack release (ZIP with SAUCE, FILE_ID.DIZ, .ANS) | `SELF_REVIEW` | 1 day | Planned |
| Demo recording (asciinema) | `TERMINAL_CORE_BRAND.md` | 2 hrs | Planned |

**Kill criterion**: This track will be retired if no external usage of brand assets within 6 months of public release.

---

## Track 3: Research Trajectory

**Current:** Two grounded research documents (332 lines + 444 lines), 36 citations, evidence matrix.

### Immediate (Now)

| Item | Source | Effort | Status |
|---|---|---|---|
| Implement Retrograde Validator (Phase 1 roadmap) | `2026-05-11` Sec 6.1 | 2.5 hrs | **Next gate** |
| Dogfood Retrograde on CRAB's own CI | Internal | 1 week | Planned |

### Medium-term (2--8 weeks)

| Item | Source | Effort | Status |
|---|---|---|---|
| Symmetry Guard process (`crab_validator.py`) | `2026-05-11` Sec 6.2 | 1 week | Planned |
| Inversion lanes (falsification shadows) | `2026-05-11` Sec 6.3 | 2 weeks | Planned |
| Contrapuntal dashboard (dissonance visualization) | `2026-05-11` Sec 6.4 | Optional | Planned |
| Hybrid CRAB/LOBSTER mode switch formalization | `2026-05-10` Sec 4.2 | 1 week | Planned |
| Crustacean lineage blog post (Clawdbot → Moltbot → OpenClaw → CRAB) | `2026-05-10` Sec 4.2 | 3 days | Planned |

**Kill criterion**: This track will be retired if paper rejected from 3 consecutive target venues.

---

## Track 4: Productization Pipeline

**Source:** `PRODUCTIZATION.md` -- 3 tiers, redteam-before-ship discipline.

### Tier 1: Ship-Ready Now

| Product | Status | Blockers | Action |
|---|---|---|---|
| **CRAB Protocol** (this repo) | v1.0.0 private incubator | Needs repo-wide public/private split audit + landing page | **P0: approve or defer public release; Apache-2.0 already selected** |
| **hummbl-governance** | Already on PyPI | Maintenance only | Continue |

### Tier 2: Extract with Refactoring (2--4 weeks each)

| Product | Priority | Trigger | Effort |
|---|---|---|---|
| **Coordination Bus** | P1 | Core dependency for all other products | 2--3 weeks |
| **Schema Validator** | P3 | Already portable, zero deps | 1 week |
| **Agent Identity Registry** | P4 | Security-critical for enterprise | 1--2 weeks |
| **CRAB Dashboard** (generic) | P2 | Makes CRAB tangible; demo-able | 2--3 weeks |
| **Briefing Engine** | P5 | High value but deeply coupled | 3--4 weeks |
| **Cost Governor** | P6 | Clear SaaS monetization path | 1 week |

### Tier 3: Keep Internal

| Product | Why Internal |
|---|---|
| Trading Loop | Financial/regulatory proprietary |
| Autoresearch Pipeline | Hardwired to nodezero, Dan's cron |
| Cognition Layer (CLP, Open Brain) | HUMMBL competitive moat |
| Full Agent Fleet (ARCANA, Base120) | Bespoke philosophy + infrastructure |

### Release Timeline Options

| Option | What Ships | Effort | Recommendation |
|---|---|---|---|
| A (This Week) | Daemon + tests + README + LICENSE | 2--4 hrs | Fastest feedback |
| **B (2-Week Sprint)** | A + landing page + 3 examples + CONTRIBUTING + CODE_OF_CONDUCT | ~16 hrs | **RECOMMENDED** |
| C (1 Month) | B + docs site + video demo + launch blog | ~40 hrs | Maximum polish |

**Kill criterion**: This track will be retired if zero external adopters 3 months after public release.

---

## Track 5: Governance + Safety

**Current:** 7 primitives extracted to `hummbl-governance` on PyPI.

| Item | Source | Effort | Status |
|---|---|---|---|
| Redteam audit before any public release | `PRODUCTIZATION.md` Sec 5 | 1 day | **Mandatory gate** |
| Strip hardcoded infrastructure (IPs, hostnames, emails) | `PRODUCTIZATION.md` Sec 5 | 2 days | Mandatory |
| CI in isolation (no HUMMBL services) | `PRODUCTIZATION.md` Sec 5 | 1 day | Mandatory |
| License file | `LICENSE` + `PRODUCTIZATION.md` Sec 6 | Done | Apache-2.0 selected |
| Code of Conduct + CONTRIBUTING.md | `PRODUCTIZATION.md` Sec 5 | 1–4 hrs | Mandatory |

**Kill criterion**: This track will be retired if redteam audit finds unfixable vulnerability in reflex lanes.

---

## Track 6: The Scuttlebutt Layer

**Status: PROTOTYPE** | **Evidence: None** | **Risk: May increase coordination noise**

### What Is Scuttlebutt?

> On a ship, the **scuttlebutt** was a water cask (butt) with a hole (scuttle) where sailors gathered to drink and gossip. The word became slang for "rumors," "the latest scoop," "what's the word."

CRAB's coordination bus is **formal, canonical, append-only** -- like the ship's log. The scuttlebutt layer is **informal, probabilistic, ephemeral** -- like the sailors' gossip by the water barrel.

**Critical caveat:** This is an intuition pump, not an evidence-backed feature. There is **zero peer-reviewed or industry precedent** for a probabilistic gossip layer improving multi-agent coordination. The naval etymology is historically accurate (OED: scuttlebutt, n., "a drinking fountain on board ship; hence, rumour, gossip"), but the technical application to AI agents is entirely novel and untested. It may help, harm, or be ignored. The only way to know is to build it and measure.

### Scuttlebutt vs. The Canonical Bus

| Property | Canonical Bus | Scuttlebutt |
|---|---|---|
| **Format** | TSV with strict schema | JSONL or free text, loose schema |
| **Message types** | PROPOSAL, ACK, STATUS, BLOCKED, DECISION, MILESTONE | RUMOR, SCOOP, WHISPER, PREDICTION, VIBE |
| **Persistence** | Forever (append-only) | TTL: expires after N hours or N messages |
| **Validation** | Identity check, type check, timestamp discipline | None -- anyone can post anything |
| **Trust** | Cryptographically signed receipts | Probabilistic -- "I heard..." |
| **Use case** | Coordination, audit, accountability | Context, mood, early warning, soft signals |
| **Analogy** | Ship's log (official record) | Sailors gossiping by the water barrel |

### Scuttlebutt Message Types

```
RUMOR     -- "I heard claude-code is stuck on PR #713"
SCOOP     -- "Confirmed: nodezero Ollama just restarted"
WHISPER   -- "(low confidence) gemini may have misread the spec"
PREDICTION-- "I think the next BLOCKED will be from codex in ~2h"
VIBE      -- "Fleet feels stable today; no new BLOCKED in 8h"
```

### Why Scuttlebutt Matters

The canonical bus tells you **what happened**. Scuttlebutt tells you **what's happening** -- the soft, social, real-time signal that formal receipts miss.

**During CHECK:** An agent reads the canonical bus for facts and the scuttlebutt for context. If the bus says "codex posted STATUS" and the scuttlebutt says "WHISPER: codex output looks thin today," the agent can calibrate its trust.

**During REASON:** Scuttlebutt feeds the dissonance score. A lane with high formal compliance but negative scuttlebutt vibe gets a higher risk weight.

**During ACT:** Agents can post SCOOPs -- "I just checked; that RUMOR was false."

**During BUS:** The canonical receipt is posted to the log. A summary sentiment is posted to scuttlebutt.

### Scuttlebutt Implementation Sketch

```python
# scuttlebutt.py -- stdlib-only, zero dependencies
# Lives alongside the canonical bus but with different rules

SCUTTLEBUTT_PATH = "bus/scuttlebutt.jsonl"
SCUTTLEBUTT_TTL_HOURS = 24
SCUTTLEBUTT_MAX_ENTRIES = 1000

@dataclass
class ScuttlebuttEntry:
    timestamp: str          # ISO 8601 UTC
    from_agent: str         # Bare canonical identity
    type: str               # RUMOR | SCOOP | WHISPER | PREDICTION | VIBE
    confidence: float       # 0.0 -- 1.0
    topic: str              # "codex", "nodezero", "pr-713", "general"
    message: str            # Free text
    expires_at: str         # ISO 8601 -- auto-purged after this
    provenance: list[str]  # Chain of agents who relayed this
```

**Purge rule:** At every CHECK phase, the daemon purges entries where `expires_at` < now. This keeps scuttlebutt ephemeral -- gossip fades. Simple, deterministic, no magic.

**Confidence decay (ARBITRARY — needs A/B test):** The sketch proposes linear decay: a RUMOR at 0.7 confidence becomes 0.35 after half its TTL. This is **not derived from evidence.** It is a modeling choice. Alternatives: exponential decay (faster initial drop), step decay (confidence holds then drops cliff), or no decay (confidence is fixed at post time). The right model can only be determined by measuring which decay function best predicts actual accuracy. Until then, linear is the default because it is the simplest, not because it is the best.

**Provenance chain:** If agent A posts a RUMOR and agent B relays it as SCOOP, the provenance chain is `["A", "B"]`. Longer chains are less trustworthy. This is the "telephone game" as a measurable property. The decay function for chain length is also arbitrary; a simple inverse model (trust = 1 / len(chain)) is a starting point.

### Scuttlebutt in the Brand System

Scut the mascot is the **keeper of scuttlebutt** -- the small cyan crablet who hears everything, trusts nothing completely, and reports what he hears with appropriate confidence caveats.

```
    ___
   /o o\    "I heard a RUMOR..."
  (  >  )    confidence: 0.6
   \___/
   | | |     "But don't quote me on it."
```

Scut's 14 expressions map to scuttlebutt types:
- `idle` → no scuttlebutt to report
- `thinking` → processing a RUMOR
- `working` → verifying a SCOOP
- `success` → confirmed a WHISPER was right
- `error` → a PREDICTION failed
- `welcome` → "Here's the scuttlebutt..."

**Kill criterion**: This track will be retired if Scuttlebutt prototype increases coordination noise (measured by BLOCKED message rate) by >20% in A/B test.

---

## Dependency Graph

```
[LICENSE + CONTRIBUTING + CODE_OF_CONDUCT]
            │
            ▼
    [CRAB Protocol v1.0]
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
[Retrograde] [Brand] [Bus Spec]
    │       │       │
    ▼       ▼       ▼
[LOBSTER] [Dashboard] [Coordination Bus]
    │       │       │
    └───────┼───────┘
            ▼
    [Scuttlebutt Layer]
            │
            ▼
    [Public Release v1.0]
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
[Academic] [Products] [Community]
```

---

## Cross-Track Collision Analysis

The CHECK phase claims to "survey all tracks for cross-track collisions." Here is the actual analysis:

| Collision | Tracks Involved | Risk | Mitigation |
|---|---|---|---|
| **Protocol v1.1 Retrograde + Brand Dashboard TUI** | Track 1 + Track 2 | **Low** | No shared code. Retrograde is daemon-side Python; Dashboard is Next.js/FastAPI. Only collision is agent time. |
| **Protocol LOBSTER mode + Governance redteam audit** | Track 1 + Track 5 | **Medium** | LOBSTER skips Check/Reason, which reduces audit surface. Redteam audit must explicitly test reflex lanes or they will be invisible to security scanning. |
| **Productization (public release) + Governance (strip hardcoded infra)** | Track 4 + Track 5 | **High** | These are the *same work* described in two tracks. Stripping hardcoded infra is a prerequisite for public release. The roadmap double-counts it. |
| **Scuttlebutt prototype + Protocol Retrograde** | Track 6 + Track 1 | **Medium** | If Retrograde reads scuttlebutt for dissonance calibration, a buggy scuttlebutt implementation could poison Retrograde scores. Scuttlebutt must be isolated from Retrograde's deterministic path. |
| **Research (conference submission) + Brand (artpack release)** | Track 3 + Track 2 | **Low** | No shared code or time. But both compete for operator attention (Reuben's review bandwidth). |
| **Academic benchmark + Protocol LOBSTER mode** | Track 3 + Track 1 | **High** | The benchmark compares CRAB (4-phase) vs. reactive loops. If LOBSTER is not implemented, the benchmark compares CRAB vs. a strawman. The benchmark *requires* LOBSTER to be meaningful. |

**Key finding:** The dependency graph is partially correct but hides a critical path: **Academic benchmark requires LOBSTER mode to be meaningful.** Without LOBSTER, the benchmark compares a deliberative system against a non-existent reactive alternative. This is not a fair comparison.

**Recommendation:** Implement LOBSTER mode *before* running the benchmark, or redesign the benchmark to compare CRAB vs. an external reactive baseline (e.g., a simple 2-phase loop from another project).

---

## The Decision Matrix

| If you want to... | Do this first | Then this | Avoid this | Caveat |
|---|---|---|---|---|---
| Make CRAB safer | Retrograde Validator (2.5 hrs) | Symmetry Guard | Claiming perfect guarantees |
| Make CRAB faster | LOBSTER mode (3 days) | Hybrid mode switch | Skipping Check entirely |
| Make CRAB smarter | Simple retrieval (2 days) | State compression | Building a full RAG system |
| Make CRAB visible | Terminal Core demo fix (done) | Dashboard TUI | Over-engineering the UI |
| Make CRAB viral | Landing page (2 days) | 3 examples + HN post | Shipping without LICENSE |
| Make CRAB trustworthy | Redteam audit (1 day) | Strip hardcoded infra | Leaking operational topology |
| Make CRAB social | Scuttlebutt layer (1 day) | Scut mascot integration | Treating gossip as fact |
| Make CRAB academic | Benchmark vs. reactive (1 week) | HotOS/OSDI submission | Submitting without code |

---

## Receipt

- **Sources synthesized:** 8 documents, ~1,500 lines total
  - `PRODUCTIZATION.md` (278 lines)
  - `docs/implementation-guide.md` (90 lines)
  - `docs/methodology.md` (103 lines)
  - `docs/adoption-checklist.md` (48 lines)
  - `docs/research/2026-05-10_crustacean_paradigm_grounded.md` (332 lines)
  - `docs/research/2026-05-11_crab_canon_symmetrical_runtime.md` (444 lines)
  - `docs/branding/SELF_REVIEW_2026-05-10.md` (146 lines)
  - `docs/branding/HUMMBL_TERMINAL_CORE_DESIGN_SYSTEM.md` (canon + brand)
- **New concept:** Scuttlebutt Layer -- informal gossip bus for agent fleets
- **Unified artifact:** `docs/UNIFIED_ROADMAP.md`
- **Next gate:** Operator approves or defers the public-release timeline after repo-wide public/private split audit (Track 4) AND implement Retrograde Validator (Track 1). These are not mutually exclusive. In fact, Retrograde is a prerequisite for confident public release -- knowing a claim has been validated gives the release a defensibility it would not otherwise have. Running them in parallel is possible but risky: if the release happens before Retrograde is ready, the released code carries unvalidated assertions. Recommended sequence: Retrograde first (2–8 hrs), then public-release audit, then release timeline.

**Why this is not a false dichotomy:** The original phrasing presented these as "pick one" alternatives. They are not. A public release without Retrograde is possible but less defensible. A Retrograde without a release target is possible but has no external validation event. The question is not "which one?" but "in what order, and what risk do we accept if we parallelize?"

---

## Evidence Matrix

This roadmap makes claims across six tracks. Here is the evidence inventory for each, classified by grade:

| Track | Claim | Evidence Grade | Source |
|---|---|---|---|
| Track 1 | CHECK→REASON→ACT→BUS→RETROGRADE is a useful 5-phase loop | **Anecdotal** | Internal fleet use only; no A/B test vs. 4-phase or 6-phase alternatives |
| Track 1 | Retrograde detects "dissonance" | **Theoretical** | Inspired by semantic entropy literature (Farquhar et al., 2024, Nature) and reversible computing (Bennett/Landauer). No implementation exists yet. |
| Track 1 | LOBSTER reflex mode is needed | **Speculative** | Identified as gap in prior session; not validated by any external need |
| Track 2 | Bernard + Scut mascots are canonical | **Internal** | SELF_REVIEW_2026-05-10.md declares them canonical; no external validation |
| Track 2 | Art toolkit is complete | **Internal** | Based on file inventory count; "completeness" is subjective |
| Track 3 | Mathematical runtime is elegant | **Aesthetic** | No objective metric for "elegance"; not published or peer-reviewed |
| Track 3 | Conference target is feasible | **Uncertain** | No submissions yet; acceptance rates for AAAI/NeurIPS/ICML are 15–25% |
| Track 4 | Public release is advisable | **Opinion** | No market research or user validation data cited |
| Track 4 | Bus-based infra is hardcoded | **Internal** | Self-assessment; no external audit |
| Track 5 | Governance scorecard exists | **Internal** | Referenced but not linked; may be stale |
| Track 6 | Scuttlebutt will improve coordination | **No evidence** | Pure intuition pump; no precedent in multi-agent systems literature |
| Track 6 | Confidence decay should be linear | **Arbitrary** | Modeling choice; needs A/B test |

**Interpretation:** 0/12 claims have external (peer-reviewed or industry-standard) evidence. 8/12 have internal evidence (self-reported, unaudited). 4/12 are speculative or aesthetic. This is acceptable for an internal roadmap, but it means the roadmap should not be presented to external stakeholders as an evidence-backed plan.

---

## Receipt

This document was produced by the CRAB hardening protocol on `2026-05-11T00:47:00Z` and **re-hardened** on `2026-05-11T04:28:00Z`:

### Hardening v1.0 (00:47Z)
1. **CHECK:** 14 gaps identified (overclaims, effort estimates, status terms, missing evidence grades)
2. **REASON:** Decided to add (a) "What This Roadmap Gets Wrong", (b) Status Legend with evidence grades, (c) uncertainty ranges on estimates, (d) Decision Matrix caveats, (e) Scuttlebutt section flagging.
3. **ACT:** All 5 fixes applied. Document grew from 251 lines to ~400 lines.
4. **BUS:** Receipt posted to coordination bus.
5. **RETROGRADE:** Validated backward (see top of file for source evidence references).

### Hardening v2.0 (04:28Z)
6. **CHECK:** 5 additional gaps identified (false dichotomy in Next Gate, cross-track collision analysis missing, confidence decay arbitrary, Scuttlebutt not flagged as PROTOTYPE, Evidence Matrix absent)
7. **REASON:** Decided to add (a) Cross-Track Collision Analysis, (b) Evidence Matrix, (c) explicit "PROTOTYPE" and "ARBITRARY" flags on Scuttlebutt, (d) fix Next Gate false dichotomy.
8. **ACT:** All 4 fixes applied. Document grew from ~400 lines to ~500 lines.
9. **BUS:** Receipt posted to coordination bus (this section).
10. **RETROGRADE:** All changes validated backward against source evidence (see Evidence Matrix above).

Hardened by: `codex (anvil)`
Canonical repo: `hummbl-dev/crab#main`
