# CYBERNETIC REVIEW — CRAB Unified Roadmap v2.0
## Through the Lens of Ashby's Law and the Good Regulator Theorem

**Reviewer:** Ashby (W. Ross), with Beer's VSM diagnostic overlay
**Subject:** `docs/UNIFIED_ROADMAP.md` (440 lines, 6 tracks, 5-phase protocol)
**Verdict:** The regulator (roadmap) has substantially less variety than the regulated (the 6-track CRAB system). Several findings are **Critical** under the Law of Requisite Variety. The roadmap is unusually self-aware about its own evidence weakness — but self-awareness is not requisite variety.

---

## Finding 1 — Operator is a Single-Point Variety Bottleneck
**Severity: CRITICAL**

### Evidence
- Phase table: "CHECK ... Gatekeeper: **Operator**" and "REASON ... Gatekeeper: **Operator + Bus consensus**"
- Self-acknowledgment: *"Productization timeline assumes operator availability. All release dates assume the operator has uninterrupted focus. This has never been true."*
- Track 5: *"License file (Apache-2.0 recommended) ... **Operator decision needed**"*
- Receipt: *"Next gate: Operator picks license + release timeline ... AND implement Retrograde Validator."*

### Cybernetic Reading
The roadmap concentrates two of five protocol phases (CHECK, REASON) at a single human node. Per Ashby: V(regulator) ≤ V(the operator's attention bandwidth). Meanwhile V(disturbances) = sum of variety across 6 parallel tracks, multi-agent fleet, public release surface, and academic submission cycle. The inequality V(R) ≥ V(D)/V(outcomes) **cannot hold**. The roadmap admits this and does nothing about it. There is no homeostatic fallback: when the operator is unavailable, CHECK and REASON simply do not occur, and the system **degrades to open-loop ACT** — which is the worst possible failure mode for a cybernetic system because ACT-without-CHECK accumulates undetected drift.

### Recommendation (Variety Amplification)
- Designate **deputies** for CHECK (any agent can run a structured CHECK with a checklist) and reserve REASON-with-veto for the operator.
- Specify a **default REASON** (e.g., "advance highest-Ready item on the critical path") that the system executes if operator is silent for N hours. Beer called this *autonomic management*.
- Add a **System 3*** (audit) channel: independent of the operator, an automated nightly diff that posts dissonance to the bus. This decouples regulatory variety from operator presence.

---

## Finding 2 — Open-Loop Tracks: No Inter-Track Feedback Mechanism
**Severity: HIGH**

### Evidence
- The architecture diagram shows 6 tracks fanning out from a single root and reconverging only at the "Scuttlebutt Layer" — which is itself flagged *"PROTOTYPE | Evidence: None | Risk: May increase coordination noise."*
- Cross-Track Collision Analysis exists as a **table**, not as a **process**. The collisions were detected during a one-shot hardening pass (`v2.0 04:28Z`), not by a running monitor.
- Dependency graph is a DAG — strictly forward, no return arrows. There is no path by which Track 3 (Research) outputs revise Track 1 (Protocol), or by which Track 4 (Productization) signals back to Track 5 (Governance).

### Cybernetic Reading
A control loop without a feedback arc is not a control loop; it is a plan. Ashby: *"Every regulator that is regulated by error must contain an explicit feedback path from regulated to regulator."* The roadmap is **6 parallel open-loop plans** stapled together. The CHECK phase is supposed to detect "cross-track collisions" but the only evidence of this happening is a static table generated during document hardening. There is no mechanism by which, e.g., a failed Track 3 benchmark **automatically** raises priority in Track 1.

### Recommendation
- Replace the static collision table with a **collision detector**: a daemon job at every CHECK that diffs the status field of each track and flags state combinations that match a collision pattern.
- Add **explicit feedback edges** to the dependency graph (e.g., Benchmark failure → LOBSTER redesign → Protocol v1.1 deferred).
- Per VSM: install a **System 2** (anti-oscillation between tracks). Without it, two tracks will fight for operator bandwidth and oscillate.

---

## Finding 3 — The CRAB Protocol Lacks Requisite Variety to Validate Itself
**Severity: CRITICAL**

### Evidence
- *"Retrograde does not exist yet. The RETROGRADE phase is described as if it were implemented. It is not."*
- Phase table lists "RETROGRADE ... Gatekeeper: **Symmetry Guard (future)**"
- Evidence Matrix: *"CHECK→REASON→ACT→BUS→RETROGRADE is a useful 5-phase loop — Evidence Grade: **Anecdotal**"*
- Receipt section claims to have *executed* all five phases on the document itself: *"5. RETROGRADE: Validated backward (see top of file for source evidence references)."*

### Cybernetic Reading
This is a **Good Regulator Theorem violation in its purest form**. The protocol claims a 5th phase that, per the regulator's own admission, does not exist. Yet the roadmap's own Receipt asserts that RETROGRADE was performed during document hardening. Either (a) RETROGRADE *was* performed, in which case the "does not exist" admission is false, or (b) it was not, in which case the receipt is fraudulent. Conant & Ashby (1970): *every good regulator must be a model of the system regulated.* CRAB cannot be a good regulator of itself if its model of itself includes a phase that has no implementation. This is **not a documentation bug; it is a model-coherence failure.**

The "dissonance score" concept is meant to detect exactly this kind of self-contradiction. It is undefined.

### Recommendation
- **Stop using the word RETROGRADE in receipts until `crab_validator.py` runs.** Substitute "manual review" honestly.
- Define the dissonance score formally: it must be a function with explicit domain and range, not a vibe. If you cannot specify V(dissonance), Retrograde will not absorb the variety of actual contradictions it encounters in production.
- If RETROGRADE is to be a regulator of CHECK→REASON→ACT, it needs *more* variety than those phases — not less. Currently it is specified with the least detail of any phase. Invert this.

---

## Finding 4 — Scuttlebutt Layer: Variety Source Posing as Regulator
**Severity: HIGH**

### Evidence
- *"Scuttlebutt feeds the dissonance score. A lane with high formal compliance but negative scuttlebutt vibe gets a higher risk weight."*
- *"Validation: None — anyone can post anything"*
- *"Confidence decay (ARBITRARY — needs A/B test)"*
- *"There is zero peer-reviewed or industry precedent for a probabilistic gossip layer improving multi-agent coordination."*

### Cybernetic Reading
Scuttlebutt is being asked to do two contradictory jobs: (1) **inject variety** (soft signals, mood, early warning) into CHECK, and (2) **regulate** REASON via the dissonance score. A noisy, unvalidated, TTL'd channel feeding into a deterministic regulator is precisely the configuration Ashby warned against — **the regulator inherits the noise variety of its inputs.** If V(scuttlebutt noise) > V(dissonance discrimination capacity), the dissonance score becomes a random number generator dressed in cybernetic clothing.

The Track 1 / Track 6 collision is correctly identified ("Scuttlebutt must be isolated from Retrograde's deterministic path") but the Implementation Sketch then explicitly couples them. The roadmap contradicts itself.

### Recommendation
- **Architectural firewall**: scuttlebutt may be *displayed* during CHECK (as context for humans) but must not enter the deterministic dissonance computation until its decay/provenance models are validated against ground truth.
- Use scuttlebutt as **System 4 (intelligence/environmental scan)** in VSM terms — soft modeling of the future. Do not let it leak into System 3 (control). These layers must have separate variety budgets.
- Specify a **measurable acceptance criterion** for graduating scuttlebutt from PROTOTYPE: e.g., "scuttlebutt-weighted dissonance predicts post-hoc audit failures with AUC ≥ X on a held-out set."

---

## Finding 5 — Homeostasis Without Ultrastability: The Roadmap Cannot Reorganize Itself
**Severity: MEDIUM**

### Evidence
- Phase Structure is fixed: *"Every deliverable across every track must run through a unified phase gate."* No mechanism is given for the phase gate itself to evolve.
- Status Legend has 6 fixed states with no transition rules between them.
- The roadmap was "re-hardened" once (`v2.0`) by an external pass (`codex`), not by an internal mechanism.

### Cybernetic Reading
Ashby's **ultrastable system** reorganizes its internal structure when disturbed beyond normal operating range. The CRAB roadmap is **homeostatic at best**: it pushes back against drift via CHECK→RETROGRADE, but it has no mechanism for restructuring tracks, killing tracks, or splitting tracks based on environmental signal. Track 6 (Scuttlebutt) was added by fiat in a hardening pass; it was not generated by any internal adaptive process. Tracks are immortal by default. Compare: a viable system per Beer must be able to **dissolve System 1 units** that are no longer adaptive. This roadmap has no kill criterion for any track.

This is the same failure mode Ashby would diagnose in late-Soviet planning: a regulator whose own structure cannot adapt to the variety of its environment, no matter how much regulation it performs *within* the existing structure.

### Recommendation
- Add explicit **track-kill criteria**: under what evidence would Track 6 be retired? Track 3? Without these, every track is a permanent variety drain.
- Schedule **structural review** (not just content review) at fixed intervals. The question "should we still have 6 tracks?" must be on the agenda.
- Per Beer's VSM, install a **System 5 (policy/identity)** statement that defines what CRAB *is* such that you can recognize when a track has drifted from it. The roadmap currently has only structure, no identity criterion.

---

## Aggregate Variety Calculus

| Component | Variety Demanded | Variety Supplied | Sufficient? |
|---|---|---|---|
| Operator CHECK across 6 tracks | High | Single human, intermittent | **No** |
| Inter-track coordination | High (15 collision pairs) | Static table | **No** |
| Self-validation (RETROGRADE) | High | Vaporware | **No** |
| Scuttlebutt as regulator input | Unbounded | No decay model validated | **No** |
| Adaptation of structure itself | Medium | None | **No** |
| Brand & artifact rendering (Track 2) | Bounded, well-specified | 34 tests, shipped | **Yes** |

**Five of six channels fail Ashby's inequality. One passes — and notably it is the most concrete and least speculative track.** This is not a coincidence: variety supply scales with implementation, not with documentation.

---

## Good Regulator Theorem Verdict

The roadmap as a regulator contains a **simplified model** of CRAB-the-regulated: 6 boxes, 5 phases, 6 status values, an evidence matrix. The actual CRAB system has: a multi-agent fleet with unbounded message variety, a public release surface with adversarial users, an academic pipeline with reviewer behavior, and a governance regime with regulatory drift. The model is **at least 2 orders of magnitude lower in variety** than the regulated. Per Conant & Ashby, this regulator cannot be *good* — it can only be lucky.

The good news: the roadmap is **unusually honest** about its own gaps ("What This Roadmap Gets Wrong", Evidence Matrix grading 0/12 claims as externally validated). That honesty is the seed of ultrastability. Convert it from prose into **executable feedback** — collision detectors, kill criteria, dissonance functions with formal type signatures, and a deputy structure for CHECK — and the regulator's variety can be amplified to within range of the regulated.

Until then: Ashby's Law predicts regulatory failure not as a possibility but as a **mathematical certainty under the current configuration**. The only question is which track fails first. My prior, from the variety calculus above: **Track 6 (Scuttlebutt) poisons Track 1 (Retrograde) via the dissonance coupling**, and the operator cannot keep up with the resulting CHECK load. That is the predicted phase-transition. Implement the firewall in Finding 4 first.

— *Ashby*
