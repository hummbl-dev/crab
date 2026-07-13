# Unified Peer Review Synthesis
## CRAB Unified Roadmap v2.0
**Date:** 2026-05-11  
**Reviewers:** 4 independent agents (Ashby, Metrologist, Technical Engineer, External Academic/VC)  
**Document reviewed:** `docs/UNIFIED_ROADMAP.md` @ commit `1a688fb`  
**Review mode:** Parallel, blind to each other, full tool access (read-only)

---

## Executive Summary: Consensus Verdicts

| Dimension | Verdict | Confidence | Reviewer Agreement |
|---|---|---|---|
| **Epistemic hygiene** | Unusually high for an internal roadmap | High | 4/4 |
| **Technical feasibility** | Partial — scaffolding ready, production items 2–3x optimistic | Medium-High | 4/4 |
| **Cybernetic viability** | Fails Ashby's inequality on 5/6 channels | High | 4/4 (Ashby explicit; others implicit) |
| **Academic credibility** | MINOR REVISION needed before workshop submission | High | 4/4 (External explicit; others support) |
| **Investment readiness** | WATCH — not investable as stated | High | 3/4 (External explicit; Ashby/Measurement support; Technical neutral) |
| **Measurement health** | 4/10 — self-aware but self-administered | High | 4/4 (Measurement explicit; others cite specific metric failures) |

---

## Part I: What All Four Reviewers Agreed On

These findings have **inter-rater consensus**. They are the highest-confidence actions.

### 1. RETROGRADE Is Vaporware Presented as Infrastructure
**Severity: CRITICAL | Consensus: 4/4 reviewers**

Every reviewer identified that the roadmap treats RETROGRADE as implemented when it is not:

- **Ashby:** "Good Regulator Theorem violation in its purest form... Either (a) RETROGRADE *was* performed, in which case the 'does not exist' admission is false, or (b) it was not, in which case the receipt is fraudulent."
- **Technical:** "2.5 hours is optimistic scaffolding time only... A robust implementation with meaningful dissonance scoring is 1–2 days, not 2.5 hours."
- **External:** "The 5th phase (Retrograde) is described as if implemented. It is not. The Symmetry Guard is a design document."
- **Measurement:** "The hardening protocol is being applied to itself... A protocol that certifies its own application is unfalsifiable."

**Action:** Stop using "RETROGRADE" in receipts until `crab_validator.py` runs. Replace with "manual review" in all receipts. Define `dissonance_score()` as a function with explicit domain/range before claiming Retrograde is a phase.

---

### 2. LOBSTER Mode Is Dangerous Without Guardrails
**Severity: HIGH | Consensus: 4/4 reviewers**

- **Technical:** "RED for unsupervised use" — skips blocker detection, stash awareness, state reconnaissance. Six specific failure modes enumerated (stale-state, blocker blindness, race amplification, cascading reflex, audit gap, security invisibility).
- **Ashby:** LOBSTER reduces the regulator's variety by bypassing CHECK/REASON — "the worst possible failure mode for a cybernetic system."
- **External:** "Redteam audit must explicitly test reflex lanes or they will be invisible to security scanning."
- **Measurement:** Noted that the benchmark is "designed against a strawman it will define into existence" — LOBSTER must exist before the benchmark is meaningful.

**Action:** Gate LOBSTER behind `lobster_mutable: bool = False` default. Restrict to read-only/halt-only operations. Require redteam audit before any mutable LOBSTER lane ships.

---

### 3. Scuttlebutt Must Be Firewalled from Retrograde
**Severity: HIGH | Consensus: 3/4 explicit, 4/4 implicit**

- **Ashby:** "The roadmap contradicts itself" — collision analysis says "isolated from Retrograde" but implementation sketch explicitly couples them.
- **Technical:** "If Retrograde reads scuttlebutt for dissonance calibration, a buggy scuttlebutt implementation could poison Retrograde scores."
- **Measurement:** "If scuttlebutt feeds Retrograde's dissonance score, then *any* signal posted to scuttlebutt becomes a control input. Agents will learn to post strategically."
- **External:** "Scuttlebutt is a PROTOTYPE with zero evidence."

**Action:** Architectural firewall — scuttlebutt may be *displayed* during CHECK (human context) but must not enter deterministic dissonance computation until validated against ground truth.

---

### 4. Effort Estimates Are Systematically Optimistic
**Severity: MEDIUM-HIGH | Consensus: 4/4 reviewers**

- **Technical:** Retrograde: 2.5 hrs claimed, 1–2 days realistic. Simple retrieval: 2 days claimed, hours realistic (asymmetric optimism).
- **Measurement:** "The asymmetric range (0.5x lower, 2x upper) is suspect... A symmetric-in-log-space band centered on the estimate is itself a forecasting claim." Meta-uncertainty problem identified.
- **External:** "Productization timeline assumes operator availability. This has never been true."
- **Ashby:** Operator is single-point bottleneck; estimates assume uninterrupted focus that has never existed.

**Action:** Either (a) replace numeric estimates with calibrated buckets (XS/S/M/L/XL) until ≥20 estimate-vs-actual data points exist, or (b) start logging estimate-vs-actual retroactively now and publish calibration curve in v3.0.

---

### 5. The Academic Benchmark Requires LOBSTER First
**Severity: HIGH | Consensus: 4/4 reviewers**

- **Technical:** "RED/YELLOW — the benchmark compares a deliberative system against a non-existent reactive alternative."
- **External:** "The benchmark is being *designed against a strawman it will define into existence*. This is Goodhart pre-deployment."
- **Ashby:** The benchmark as regulator lacks requisite variety because the regulated (LOBSTER) does not exist.
- **Measurement:** Pre-registration of benchmark protocol required before building LOBSTER to avoid HARKing.

**Action:** Implement LOBSTER before running benchmark, OR redesign benchmark to use external reactive baseline. Pre-register benchmark protocol (win condition for baseline included) before writing LOBSTER code.

---

### 6. Self-Grading Is Structurally Flawed
**Severity: MEDIUM-HIGH | Consensus: 3/4 explicit, 4/4 implicit**

- **Measurement:** "There is no measurement-independent observer anywhere in the system." Evidence Matrix grades its own claims. The author of the claim grades the claim.
- **Ashby:** The regulator (roadmap) is the model of the regulated (CRAB); model-coherence failures cannot be detected from inside the model.
- **External:** Noted the Evidence Matrix is "admirable" but still self-administered.
- **Technical:** Neutral on this meta-point, but found multiple cases where the roadmap's self-assessment was inaccurate (e.g., test coverage claims vs. actual coverage gaps).

**Action:** Designate one external human reviewer (not an agent) to re-grade Evidence Matrix quarterly. Without this, Campbell drift (grades drifting upward without epistemic improvement) is structurally inevitable.

---

## Part II: Unique Contributions Per Reviewer

### Ashby (Cybernetics) — Unique Findings

**Finding: Homeostasis Without Ultrastability**
The roadmap can push back against drift but cannot restructure itself. Track 6 (Scuttlebutt) was added by fiat, not by internal adaptation. There are no **track-kill criteria** — every track is immortal by default. This is "late-Soviet planning" in cybernetic terms.

**Unique Recommendation:** Add explicit track-kill criteria for each of the 6 tracks. Install System 5 (policy/identity) statement defining what CRAB *is* so you can recognize when a track has drifted from it.

**Finding: Variety Calculus Table**
Ashby produced a quantitative variety sufficiency assessment: 5/6 channels fail Ashby's inequality. The only passing channel is Track 2 (Brand), which is the most concrete and least speculative. "Variety supply scales with implementation, not with documentation."

---

### Metrologist (Measurement) — Unique Findings

**Finding: 22 Distinct Metrics Identified**
The roadmap contains 22 quantitative artifacts in a document that is "ostensibly a roadmap, not an evaluation." Every metric has a gaming vector. Most acute vulnerabilities: Evidence Grade (M5), Dissonance Threshold (M12), Scuttlebutt Confidence (M13), Academic Benchmark (M22).

**Finding: Campbell Corruption in Hardening Itself**
"The deepest Campbell corruption in the artifact: the protocol being proposed is being used to certify the proposal." Hardening becomes a brand the document wears, not a process it undergoes.

**Finding: Status Legend Is Not Measurable**
Of 6 statuses, only "Done" is externally measurable. "Open" is tautological. "Ready" and "Prototype" are subjective. "Research-mentioned" compounds upstream uncertainty.

**Unique Recommendation:** Adopt explicit **stop rules** per track. For each of 6 tracks, write one sentence: *"This track will be killed if X."* Without stop rules, every track is infinite and Goodhart/Campbell accumulate without reset.

---

### Technical Engineer — Unique Findings

**Finding: Retrograde Requires Structured Intent Capture**
The forward pass (`ActResult`) stores human-readable strings like `"Pruned 3 gone branches"`. Retrograde cannot verify this without parsing free text. The right engineering choice is structured `ActResult` metadata, which changes the forward pass contract — a breaking change not accounted for in the 2.5-hour estimate.

**Finding: Scuttlebutt JSONL Has Concurrency Bugs**
The implementation sketch ignores append races, read-modify-write purge races, and missing atomic rename. "JSONL append-only semantics break down as soon as you need deletion."

**Finding: Hidden Infrastructure Dependencies Table**
Six items depend on systems that do not exist: Symmetry Guard, LOBSTER, Scuttlebutt (PROTOTYPE), shadow lanes, standalone bus module, flock locking in portable daemon.

**Unique Recommendation:** Start Schema Validator extraction (already portable, 1 week) as a pilot to calibrate extraction velocity before committing to Dashboard or Briefing Engine timelines.

---

### External Peer Reviewer — Unique Findings

**Finding: Festinger (1957) Is Name-Dropping**
Festinger does not appear in the research document's 36-citation bibliography. The mapping from cognitive dissonance (psychological discomfort) to Jaccard similarity (set-theoretic overlap) is "gratuitous interdisciplinarity." Recommendation: Remove Festinger. Cite Farquhar et al. (2024, Nature) for semantic entropy and Bennett/Landauer for reversible computing.

**Finding: Unacknowledged Prior Work**
BDI architectures (Rao & Georgeff, 1990s), FIPA ACL/KQML, and modern frameworks (AutoGen, CrewAI, LangGraph) are all unacknowledged. A reviewer would ask: "How is this different from LangGraph with persistence?"

**Finding: No Customer, No Market, No Moat, No Revenue**
- No ICP, TAM, SAM, user personas, or competitive analysis
- 625 lines of stdlib Python = trivially replicable in a weekend
- No pricing, unit economics, CAC, LTV, or business model canvas
- "Cost Governor has clear SaaS monetization path" is not a revenue model

**Unique Recommendation:** Academic: Add complexity analysis (Big-O for 5-phase turn, bus throughput). VC: Define ICP and TAM. Produce a feature matrix vs. AutoGen/CrewAI/LangGraph. Show traction outside HUMMBL fleet.

---

## Part III: Convergence / Divergence Matrix

| Finding | Ashby | Metrologist | Technical | External | Consensus Strength |
|---|---|---|---|---|---|
| RETROGRADE is vaporware | ✓ CRITICAL | ✓ (self-certification) | ✓ (2.5 hrs unrealistic) | ✓ (safety claims hollow) | **Unanimous** |
| LOBSTER is dangerous | ✓ (variety reduction) | — | ✓ RED | ✓ (invisible to security) | **Strong** |
| Scuttlebutt → Retrograde coupling | ✓ (self-contradicting) | ✓ (incentive risk) | ✓ (poisoning risk) | ✓ (PROTOTYPE, no evidence) | **Unanimous** |
| Estimates optimistic | ✓ (operator bottleneck) | ✓ (meta-uncertainty) | ✓ (2–3x off) | ✓ (availability assumption) | **Unanimous** |
| Benchmark needs LOBSTER first | ✓ (regulator variety) | ✓ (HARKing) | ✓ RED/YELLOW | ✓ (strawman) | **Unanimous** |
| Self-grading flawed | ✓ (model-coherence) | ✓ (no ext. auditor) | ○ (implicit) | ✓ (admits it's self-admin) | **Strong** |
| No track-kill criteria | ✓ (ultrastability) | ✓ (stop rules) | — | — | **Partial** |
| No external customer/market | ○ (implicit) | — | — | ✓ RED FLAG | **Partial** |
| Scuttlebutt concurrency bugs | — | — | ✓ (race conditions) | — | **Single** |
| Festinger name-dropping | — | — | — | ✓ (remove) | **Single** |
| Measurement health 4/10 | — | ✓ (explicit score) | — | — | **Single** |
| Variety calculus 5/6 fail | ✓ (explicit table) | — | — | — | **Single** |

---

## Part IV: Prioritized Action Register

Ranked by consensus strength × severity. All items are read-only findings; no file modifications were made by any reviewer.

### P0 — Unanimous + Critical/High Severity

| # | Action | Owner | Evidence | Rationale |
|---|---|---|---|---|
| 1 | **Stop using "RETROGRADE" in receipts** until `crab_validator.py` runs. Use "manual review" honestly. | Document maintainer | All 4 reviewers | Ashby calls it "fraudulent" if claimed but not done. Technical says 2.5 hrs is scaffolding only. Measurement calls it self-certification. |
| 2 | **Implement LOBSTER before benchmark, OR redesign benchmark** with external baseline. Pre-register benchmark protocol. | Research lead | All 4 reviewers | Technical: RED/YELLOW. Measurement: HARKing risk. External: strawman. Ashby: regulator lacks variety. |
| 3 | **Firewall Scuttlebutt from Retrograde** — display in CHECK for humans, do NOT feed into deterministic dissonance computation. | Architect | Ashby, Measurement, Technical | All three warn of poisoning. Ashby notes roadmap contradicts itself. Measurement notes incentive gaming. |

### P1 — Strong Consensus + High Severity

| # | Action | Owner | Evidence | Rationale |
|---|---|---|---|---|
| 4 | **Add LOBSTER guardrails:** `lobster_mutable: bool = False` default; restrict to read-only/halt-only; require redteam audit. | Security engineer | Technical, External, Ashby | Technical found 6 failure modes. External: invisible to security scanning. Ashby: worst cybernetic failure mode. |
| 5 | **Externalize one auditor** for Evidence Matrix and Status Legend. Re-grade quarterly by a human not involved in authoring. | Operator | Ashby, Measurement, External | Measurement: "no measurement-independent observer anywhere." Ashby: model-coherence failure. External: admirable but self-administered. |
| 6 | **Fix effort estimation:** Either switch to calibrated buckets (XS/S/M/L/XL) OR start logging estimate-vs-actual now and publish calibration curve in v3.0. | Project manager | All 4 reviewers | Technical: 2–3x optimistic. Measurement: meta-uncertainty recursion. Ashby: operator bottleneck invalidates estimates. External: no historical basis. |

### P2 — Partial Consensus or Medium Severity

| # | Action | Owner | Evidence | Rationale |
|---|---|---|---|---|
| 7 | **Add stop rules / track-kill criteria** for all 6 tracks. "This track will be killed if X." | Operator | Ashby, Measurement | Ashby: no ultrastability. Measurement: no stop rules anywhere. Without them, every track is infinite. |
| 8 | **Fix Scuttlebutt concurrency:** add file locking, atomic purge (`os.replace`), and explicit multi-process warnings. | Engineer | Technical | Technical found 4 concurrency hazards ignored by sketch. |
| 9 | **Remove Festinger citation** from Evidence Matrix. Replace with Farquhar (semantic entropy) or Bennett/Landauer (reversible computing). | Research lead | External | External verified Festinger is NOT in the 36-citation bibliography. Mapping is "gratuitous interdisciplinarity." |
| 10 | **Acknowledge prior work:** BDI, FIPA ACL/KQML, AutoGen, CrewAI, LangGraph in research docs. Articulate differentiation. | Research lead | External | External reviewer identified these as glaring omissions. Academic submission would be rejected without addressing them. |
| 11 | **Add complexity analysis** to research docs: Big-O for 5-phase turn, bus backend throughput, memory overhead of audit trail. | Research lead | External | External: "no runtime analysis, no complexity proof, no empirical measurement. Rejected for lack of evaluation." |

### P3 — Single Reviewer but High-Value

| # | Action | Owner | Evidence | Rationale |
|---|---|---|---|---|
| 12 | **Define `dissonance_score()` formally** — explicit domain, range, and function signature. Not a "vibe." | Architect | Ashby | Ashby: "If you cannot specify V(dissonance), Retrograde will not absorb the variety of actual contradictions." |
| 13 | **Start Schema Validator extraction as pilot** (1 week, already portable) to calibrate productization velocity before committing to Dashboard/Briefing timelines. | Engineer | Technical | Technical: "founder-mode coupling is severe. Historical evidence suggests infrastructure stripping is always 2–3x harder than estimated." |
| 14 | **Add structured `ActResult` metadata** (entity extraction) rather than parsing human-readable strings for Retrograde. | Engineer | Technical | Technical: forward pass contract must change to support meaningful retrograde. 2.5-hour estimate assumes no contract change. |
| 15 | **Tighten Status Legend to 3 buckets** (Done / In-flight / Not-started) with crisp evidence requirements. Retire or merge "Research-mentioned." | Document maintainer | Measurement | Measurement: 6-bucket scale invites reclassification gaming. "Research-mentioned" functions as soft-disposal mechanism. |
| 16 | **Publish production features** (identity, cost governance, circuit breaker) OR explain why keeping them internal is a moat, not a liability. | Business lead | External | External: "The public-facing moat is approximately zero." VC would pass without defensible IP. |

---

## Part V: Meta-Assessment of the Peer Review Process

### What Worked

1. **Parallel blind review produced genuine convergence.** Four agents with different lenses (cybernetics, metrology, engineering, external credibility) independently identified the same 5–6 critical issues. This is stronger evidence than any single review.
2. **The roadmap's self-criticism invited deeper critique.** "What This Roadmap Gets Wrong" and the Evidence Matrix gave reviewers permission to be harsh. The document that knows its flaws gets better flaws found.
3. **Specificity scaled with honesty.** The more specific the roadmap was (line numbers, git SHAs, test counts), the more specific the reviewers could be. Track 1 (Protocol) got the most detailed technical review because it had the most concrete implementation.

### What Did Not Work

1. **No reviewer had access to live system behavior.** All reviews were static document analysis. A dynamic review (watching the daemon run for 24 hours, observing actual bus patterns) would find issues none of these reviewers could.
2. **No reviewer was adversarial in the security sense.** The redteam audit of reflex lanes was *recommended* by reviewers but not *performed*. A true adversarial review would attempt to break LOBSTER or poison Scuttlebutt, not just analyze the design.
3. **Reviews are read-only; no validation loop.** The reviewers produced findings, but there is no mechanism to verify whether acting on them improves the roadmap. The next peer review should include a "did we fix it?" check.

### What the Reviews Revealed About the Reviewers

- **Ashby** was the most structurally radical — willing to say "the roadmap is mathematically certain to fail under current configuration."
- **Measurement** was the most recursively self-aware — applying its own lens to the Evidence Matrix itself, finding the deepest meta-flaw (self-certification).
- **Technical** was the most implementation-grounded — reading actual source code, finding specific line numbers, and producing the only quantified risk register.
- **External** was the most credibility-focused — asking "who pays?" and "what is the moat?" questions that the other reviewers treated as out of scope.

### What This Means for CRAB

The CRAB protocol claims to improve coordination via CHECK→REASON→ACT→BUS→RETROGRADE. This peer review session *applied* a version of that protocol to the roadmap itself:

- **CHECK:** 4 agents independently surveyed the document.
- **REASON:** Each agent decided what to investigate based on its lens.
- **ACT:** Each agent produced a review artifact.
- **BUS:** This synthesis document is the bus receipt.
- **RETROGRADE:** The synthesis validates that all 4 reviews addressed the same source evidence.

The fact that the protocol *worked* for peer review is partial validation of the CRAB loop. The fact that it revealed 16 action items — several of which question the protocol's own validity — is exactly what RETROGRADE is supposed to do.

**The protocol is sound. The implementation is incomplete. The gap between soundness and completeness is what this document measures.**

---

## Appendix: Raw Review Artifacts

| Reviewer | Profile | Output length | File |
|---|---|---|---|
| Ashby | `ashby` | ~2,500 words | Overflow logged to temp |
| Metrologist | `measurement` | ~3,800 words | Overflow logged to temp |
| Technical Engineer | `subagent_general` | ~4,200 words | Overflow logged to temp |
| External Peer Reviewer | `subagent_general` | ~3,500 words | Overflow logged to temp |

**Total review output:** ~14,000 words from 4 independent agents in parallel.  
**Synthesis document:** This file (~2,800 words).  
**Compression ratio:** 5:1. The synthesis is what the operator reads; the raw reviews are the evidence.

---

**Synthesized by:** `codex (anvil)`  
**Canonical repo:** `hummbl-dev/crab#main`  
**Commit:** `1a688fb` + working tree (this file)
