# CRAB Unified Roadmap v2.0 — Measurement Audit
**Auditor:** The Metrologist (ARCANA Measurement Lens)
**Subject:** `docs/UNIFIED_ROADMAP.md` (440 lines, dated 2026-05-11)
**Frameworks applied:** Goodhart's Law; Campbell's Law; Porter's politics of quantification; measurement invariance; stop-rule analysis.

---

## 1. Inventory of Metrics, KPIs, Scores, and Quantitative Targets

The roadmap contains roughly **six classes** of quantitative artifact. I'm cataloguing each one — including the ones that present themselves as *qualitative* but smuggle in numeric claims.

| # | Metric / Quantitative Artifact | Where it appears | Type | Stated unit |
|---|---|---|---|---|
| M1 | **Effort estimates** ("2.5 hrs", "1 week", "3 days", "2–4 weeks") | Every track table | Time-to-complete | Hours / days / weeks |
| M2 | **Uncertainty ranges** on effort ("2–4 weeks", "1–2 weeks", "2x or 0.5x") | Phase headers, Tier 2 | Confidence band | Multiplicative |
| M3 | **Phase/version numbers** (v1.0, v1.1, v1.2, v1.3) | Track 1 | Ordinal release tag | Semver |
| M4 | **Status Legend** (Done / Ready / Planned / Open / Research-mentioned / Prototype) | Status Legend table | Categorical/ordinal | 6-level scale |
| M5 | **Evidence Grade** (Anecdotal / Theoretical / Speculative / Internal / Aesthetic / Uncertain / Opinion / No evidence / Arbitrary) | Evidence Matrix | Categorical, claims to be ordinal | 9 ad-hoc grades |
| M6 | **Priority labels** (P0, P1, P2, P3, P4, P5, P6) | Track 4 Tier 2 | Ordinal | 7-level scale |
| M7 | **Risk levels** (Low / Medium / High) | Cross-Track Collision table | Ordinal | 3-level scale |
| M8 | **Test counts** ("18 tests", "34 tests", "6 retrograde tests") | Track 1, Track 2 | Cardinal | Count |
| M9 | **Line counts** ("625 lines", "332 lines", "444 lines", "146 lines") | Throughout | Cardinal | LOC |
| M10 | **Citation count** ("36 citations") | Track 3 header | Cardinal | Count |
| M11 | **Lane/backend counts** ("3 lanes, 4 bus backends") | Track 1 header | Cardinal | Count |
| M12 | **Dissonance score / threshold** (`dissonance_threshold` config) | Track 1 Phase A | Continuous (implied) | Unspecified |
| M13 | **Scuttlebutt confidence** (0.0–1.0) | Track 6 sketch | Continuous | Probability |
| M14 | **Confidence decay function** (linear, exponential, step) | Track 6 | Functional form | — |
| M15 | **Provenance chain trust** (`trust = 1/len(chain)`) | Track 6 | Continuous | Inverse count |
| M16 | **TTL parameters** (24 hours, 1000 entries, ≤4KB tucked tail) | Track 6, Track 1 Phase B | Threshold | Time/size |
| M17 | **Acceptance rates as benchmark** ("AAAI/NeurIPS 15–25%") | Evidence Matrix | External base rate | Percent |
| M18 | **Evidence Matrix summary score** ("0/12 external, 8/12 internal, 4/12 speculative") | Evidence Matrix interpretation | Tally over M5 | Ratio |
| M19 | **Evidence inventory size** ("Sources synthesized: 8 documents, ~1,500 lines") | Receipt | Cardinal | Documents/LOC |
| M20 | **Hardening pass count** ("v1.0", "v2.0", "14 gaps", "5 additional gaps") | Receipt | Cardinal | Count |
| M21 | **Mascot expression count** ("14 expressions") | Track 6 brand | Cardinal | Count |
| M22 | **Latency / recovery / audit benchmarks** (planned, Track 1 Phase C) | Track 1 Phase C | Continuous | TBD |

That is **22 distinct measurement artifacts** in a document that is ostensibly a roadmap, not an evaluation. The density alone is a yellow flag: any plan dense with numbers attracts gaming pressure proportional to the stakes attached.

---

## 2. Goodhart Audit (per metric)

Goodhart: *the moment any of these is used to gate a decision, agents will optimize the proxy and abandon the underlying value.*

| # | Underlying value the metric purports to track | Gaming vector once the metric becomes a target |
|---|---|---|
| **M1 Effort estimates** | Actual cost-to-ship | Pad estimates so anything finished early looks heroic; or compress estimates to win prioritization, then absorb slippage into "scope changed." Either way, velocity becomes a story, not a measurement. |
| **M2 Uncertainty ranges (2x/0.5x)** | Calibration of estimator | The range itself becomes a get-out-of-jail-free card: any outcome inside [0.5x, 2x] is "expected." A 2x band over a 1-week task spans 3.5 days to 2 weeks — almost unfalsifiable. |
| **M3 Version numbers** | Real protocol maturity | Bump v1.0→v1.1→v1.2 by checking off table rows rather than improving capability. "Shipped v1.3" can mean "merged 4 PRs of varying quality." |
| **M4 Status Legend** | Actual readiness | Definitionally fluid — see §5. The cheapest gaming is reclassification: stuck items quietly migrate "Planned → Research-mentioned" to clear the visible backlog. |
| **M5 Evidence Grade** | Epistemic warrant | The grade scale itself is gameable: see §4 — the most dangerous metric in the document. |
| **M6 Priority labels (P0–P6)** | Strategic importance | Priority inflation: everything drifts toward P1. Or the inverse — items the operator dislikes get parked at P5/P6 and starve indefinitely under cover of an ordinal label. |
| **M7 Risk levels** | Probability × impact of cross-track failure | Three-bucket coarseness invites anchoring: every novel risk becomes "Medium" because Low feels dismissive and High triggers escalation. |
| **M8 Test counts** | Code correctness | The classic Goodhart of software: write trivial tests to inflate the count; coverage of *behaviors that matter* is uncorrelated with N. "34 rendering tests" is a number, not an assurance. |
| **M9 Line counts** | Substance / scope of artifact | LOC is anti-correlated with quality past a threshold. Citing "625 lines" of `crab_daemon.py` as evidence of maturity rewards verbosity. |
| **M10 Citation count (36)** | Research grounding | Citations become a coverage tax: pad with tangential references; self-cite the prior CRAB research docs (which the matrix already grades "Internal/Anecdotal"). |
| **M11 Lane/backend counts** | Protocol generality | Add empty-shell lanes/backends to bump the count. Already a risk: "Registry already supports" shadow/inversion lanes — i.e., the count includes lanes that have no implementation. |
| **M12 Dissonance threshold** | Drift between intended and actual behavior | Tune the threshold until the daemon stops complaining. Threshold-tuning is the canonical Goodhart move: when the alarm is annoying, raise the alarm level. |
| **M13 Scuttlebutt confidence (0–1)** | Actual reliability of a rumor | Agents will learn the confidence value that gets their RUMOR acted on and post that value regardless of true uncertainty. Self-reported confidence with no calibration loop is pure theater. |
| **M14 Confidence decay function** | How belief should age | The roadmap admits this is "ARBITRARY." Once a decay curve is chosen and any decision uses it, agents will time their posts to game the curve (post late so confidence stays high through the decision window). |
| **M15 Trust = 1 / len(chain)** | Telephone-game degradation | Trivially gamed: strip provenance, repost as if first-hand. The metric *rewards* provenance-laundering. |
| **M16 TTL / size thresholds (24h, 1000 entries, 4KB)** | Bounded ephemerality / state | Important messages timed to repost just before TTL; state compression to exactly 4096 bytes regardless of what fits. Hard thresholds invite right-at-the-line behavior. |
| **M17 Conference acceptance rate (15–25%)** | Probability of academic validation | Used as a base rate, this becomes the floor of credibility — "we're in the range" — independent of the actual paper. |
| **M18 Evidence Matrix summary (0/12, 8/12, 4/12)** | Distribution of warrant | Headline ratios become the *only* thing read. Move two claims from "Speculative" to "Internal" and the summary improves without any underlying epistemic change. |
| **M19 Sources synthesized count** | Synthesis breadth | Inflate by chunking source files, or by counting auto-generated docs. |
| **M20 Hardening passes (v1.0, v2.0; 14 gaps, 5 gaps)** | Document quality | Run more passes, find more "gaps," book the credit. Hardening becomes a ritual whose output is pass-count, not document quality. The decline from 14→5 gaps is *presented* as improvement; it could equally indicate gap-fatigue (fewer found because less looked for). |
| **M21 Mascot expression count (14)** | Brand expressiveness | Pure vanity metric. |
| **M22 Future benchmarks (latency/recovery/audit)** | CRAB's actual operational quality | The roadmap *itself flags* the most dangerous Goodhart in this document: the Track 3 benchmark "compares CRAB vs. reactive loops" but LOBSTER mode does not exist. The benchmark is being *designed against a strawman it will define into existence*. This is Goodhart pre-deployment. |

**Most acute Goodhart vulnerabilities:** M5 (Evidence Grade), M12 (dissonance threshold), M13 (scuttlebutt confidence), M22 (the academic benchmark).

---

## 3. Campbell Corruption Map

Campbell extends Goodhart from "metric breaks" to "the social process being measured is corrupted." Where in CRAB do the *practices* — not just the numbers — get distorted?

| Metric cluster | Social process at risk | Predicted Campbell corruption |
|---|---|---|
| **Effort estimates (M1, M2)** | Estimation discipline; honest scoping | Estimators learn that ranges are non-binding → estimation atrophies. The "no historical velocity data" admission means there is *no feedback loop closing on M1*, which is precisely the condition under which estimation becomes performative. |
| **Status Legend (M4)** | Backlog hygiene; admission of "Open" | High-stakes statuses ("Done", "Ready") get awarded prematurely; "Open" items migrate to "Research-mentioned" to disappear from the visible queue. The legend distinguishes "Open" from "Research-mentioned" in a way that *invites* this migration: Open is "known gap, no owner"; Research-mentioned is "appears in a research doc." Anything Open can be made Research-mentioned by writing a research doc. |
| **Evidence Grade (M5)** | Epistemic discipline; honest self-assessment | The grades become a *defensive vocabulary*: any criticism is met with "we already graded that Anecdotal." The matrix transforms epistemic humility into a shield. (See §4.) |
| **Priority labels (M6)** | Strategic decisions about what to ship | Priority becomes a political settlement, not a strategic call. Tracks with louder advocates get P1/P2. The Cost Governor is P6 *despite* being labeled "clear SaaS monetization path" — a label-priority mismatch that is a Campbell tell. |
| **Risk levels (M7)** | Cross-track coordination | Risk becomes a routing label rather than an intervention trigger. "High" risks (productization × governance double-count; benchmark × LOBSTER) sit in the table without owners or deadlines. |
| **Test counts (M8)** | Engineering discipline | Test theater: tests written to keep the count rising rather than to surface defects. The roadmap quotes "18 tests" and "34 tests" as standalone evidence — a Campbell pressure already visible. |
| **Hardening passes (M20)** | Self-review culture | "Hardening" becomes a brand the document wears, not a process the document undergoes. The receipt section reads as ritual: CHECK→REASON→ACT→BUS→RETROGRADE applied to the document itself, with the document as both subject and judge. **This is the deepest Campbell corruption in the artifact**: the protocol being proposed is being used to certify the proposal. |
| **Scuttlebutt confidence (M13–M15)** | Inter-agent honesty | If scuttlebutt feeds Retrograde's dissonance score (as Track 6 proposes), then *any* signal posted to scuttlebutt becomes a control input. Agents will learn to post strategically. The roadmap's own collision analysis flags this ("buggy scuttlebutt could poison Retrograde") but treats it as a *bug* risk rather than an *incentive* risk. The incentive risk is worse: even a correct implementation will be gamed. |
| **Academic benchmark (M22)** | Research integrity | Already pre-corrupted: the comparison baseline (LOBSTER) doesn't exist, so the benchmark will be designed *after* CRAB's behavior is known. This is the publication-bias / HARKing pathway in microcosm. |

**Resource asymmetry note (Campbell's actual mechanism):** Campbell's law says the actors with resources to game the metric will game it. In CRAB, the operator and the document-producing agents (Devin, codex, etc.) have *complete control* over every metric in this table — there is no external auditor. The Evidence Matrix grades its own claims. The hardening protocol audits its own output. **There is no measurement-independent observer anywhere in the system.** This is not a flaw the roadmap can fix internally; it is a structural property of the current setup.

---

## 4. Audit of the Evidence Matrix Itself

The Evidence Matrix is the most metrologically interesting artifact in the document, because it claims to be a *measurement of measurements*. Let me apply the lens recursively.

**What it does well:**
- Names its categories explicitly (Anecdotal, Theoretical, Speculative, Internal, Aesthetic, Uncertain, Opinion, No evidence, Arbitrary).
- Refuses the term "research-validated" — a real epistemic concession.
- Produces a summary tally (0/12 external, 8/12 internal, 4/12 speculative) that is unflattering to itself, which is an honesty signal.

**Goodhart problems with Evidence Grade as a metric:**

1. **The grade scale is not ordinal.** "Anecdotal," "Theoretical," "Aesthetic," "Opinion" are not ranked on a single dimension. Is "Theoretical" stronger than "Anecdotal"? The matrix doesn't say. The summary tally collapses them into "internal vs. external vs. speculative" — a *post-hoc* re-grouping that the original grades don't license.
2. **Grading is self-administered.** The author of the claim grades the claim. There is no inter-rater reliability check, no external auditor, no calibration set.
3. **The grades are sticky downward but not upward.** It is socially easy to *upgrade* a claim later ("we ran a benchmark, now it's Empirical") and socially hard to *downgrade* ("on reflection, Internal was generous; this is actually Aesthetic"). Over time the matrix will drift toward higher grades without epistemic improvement.
4. **The matrix is incomplete.** 12 claims are graded. The roadmap contains far more than 12 claims. *Which 12* is itself an unmeasured choice — selection bias by the grader. (E.g., "Effort estimates are guesses" is admitted in §"What This Roadmap Gets Wrong" but no row in the matrix grades the estimate quality.)
5. **The summary ratio (0/12, 8/12, 4/12) will be the only thing remembered.** Once cited, this becomes the headline number. Future readers will see "0/12 external" as a fact about CRAB rather than a fact about *this matrix at this time about these 12 chosen claims*.

**Campbell prediction for the Evidence Matrix at 6–12 months:** the matrix will grow, grades will drift upward, and the summary tally will improve — *not because CRAB's evidence base improved* but because the social pressure of looking unrigorous selects for upgrades. Watch for the first claim graded "Empirical" or "Validated" with an internal benchmark as its sole warrant. That is the Campbell breach.

**Recommendation:** if the matrix is to be retained, it needs (a) an explicit ordinal scale with anchored definitions, (b) a separate column for *who graded it* and *when*, (c) a rule that grade upgrades require a citation external to CRAB, (d) a rule that no claim can be removed from the matrix once added (only re-graded), and (e) a periodic external review.

---

## 5. Status Legend Audit

The six statuses (Done, Ready, Planned, Open, Research-mentioned, Prototype) are presented as if measurable. Are they?

| Status | "Evidence Required" (per legend) | Actually measurable? | Subjective slippage |
|---|---|---|---|
| **Done** | Git SHA + test results | **Mostly yes.** SHA is verifiable; "tested" is a coverage claim that hides under M8. | "Done" can mean "the SHA exists" without functional validation. |
| **Ready** | Design doc + review notes | **No.** "Reviewed" by whom? "Design doc" of what completeness? | High slippage. Anything the author wrote and re-read can be Ready. |
| **Planned** | Ticket / issue with acceptance criteria | **Partially.** Ticket existence is checkable; acceptance criteria quality is not. | Acceptance criteria can be vacuous ("works as expected"). |
| **Open** | "This document listing it" | **Tautological.** The evidence for Open is that it's listed as Open. | Pure social construction. |
| **Research-mentioned** | Citation to research file | **Yes, weakly.** Citation existence is checkable. | But the *research file itself* may be Anecdotal/Speculative per the Evidence Matrix. So this status compounds prior weak evidence. |
| **Prototype** | Working demo + known limitations | **Partially.** "Working demo" is binary-ish; "known limitations" is open-ended. | Limitations list can be exhaustive (honest) or thin (concealing). |

**Verdict:** Of the six statuses, only **Done** is measurable in any external sense, and even Done relies on M8 (test counts) which is itself Goodhart-vulnerable. **Open is tautological**, **Ready and Prototype are subjective**, and **Research-mentioned compounds upstream uncertainty**.

**Measurement-invariance failure:** The same status word means different things across tracks. "Ready" for a 10-minute config schema item means something very different from "Ready" for a 1-week validator process. The legend implies a uniform meaning that the table rows do not honor.

**Recommendation:** Distinguish *deliverable readiness* (designed/scoped) from *operator readiness* (decision made, slot allocated). Conflating them is what makes "Ready" functionally subjective.

---

## 6. Effort Estimates and Uncertainty Ranges — the Meta-Measurement Problem

The roadmap admits at the top: *"Every 'X hrs' in this document is a point estimate without confidence interval. The actual time may be 2x or 0.5x. No historical velocity data exists to calibrate."*

This admission is unusually honest, and it creates the meta-measurement problem.

**The problem:** A 2x/0.5x band is itself a measurement claim — a claim about the *distribution of estimation error*. Where does it come from?

- Not from historical data (admitted absent).
- Not from a domain prior (none cited).
- Not from a calibration exercise (none described).

So the "2x/0.5x" range is a **point estimate of the uncertainty** without its own confidence interval. We have an unmeasured measurement of the uncertainty of an unmeasured measurement. This is the recursion that Hand (*The Improbability Principle*) and any serious treatment of forecast calibration warns against.

**Concrete consequences:**

1. **Mixed-unit estimates are not commensurable.** "2.5 hrs", "10 min", "2 days", "1 week", "2 weeks", "Optional" all sit in the same column. Summing them or comparing them across tracks assumes a common scale that doesn't exist. (What is "Optional" × 0.5? × 2?)
2. **The asymmetric range (0.5x lower, 2x upper) is suspect.** In software estimation literature (Buehler & Griffin, planning fallacy work), realized times are *systematically* longer than estimates, with right-skewed distributions where the upper tail is much longer than 2x. A symmetric-in-log-space band centered on the estimate is itself a forecasting claim that implies calibration that the roadmap denies having.
3. **No stop rule on estimation error.** What estimate-vs-actual ratio would cause CRAB to abandon a track? To re-plan the roadmap? To declare the estimation process broken? Without a falsification rule, estimates cannot be *learned from*; they can only be *narrated about*.
4. **Range-as-shield.** Once "2x or 0.5x" is normalized, every overrun within that band is "expected" and every undershoot is heroic. The asymmetry of social consequences (overruns absorbed; undershoots celebrated) means the *reported* distribution will not match the *actual* distribution.

**Recommendation:** Either (a) drop numeric estimates entirely until calibration data exists, replacing them with categorical effort buckets (XS / S / M / L / XL with fixed week-ranges), or (b) start logging estimate-vs-actual on every shipped item *now*, even retroactively, and publish the calibration curve. The current state — point estimates plus a hand-waved 2x band plus a disclaimer — is the worst of all worlds: it has the *appearance* of quantitative planning without the *substance* of calibration.

---

## 7. What Is *Not* Being Measured (Politics of Quantification)

Porter: *the choice of what to measure is a political act.* What does CRAB choose not to measure?

- **Operator bandwidth as a hard constraint.** The roadmap admits "all release dates assume the operator has uninterrupted focus. This has never been true." Yet no metric tracks operator availability, attention budget, or context-switching cost. The operator's time is the binding constraint and the unmeasured variable.
- **External user reception.** Brand, mascots, design system have "34 rendering tests" but zero user studies. The numerator of users-who-saw-it is unmeasured.
- **Cost.** No dollar figures, compute costs, API costs, or maintenance costs anywhere.
- **Failure modes in production.** No metric for "incidents," "rollbacks," "agents that misbehaved." The bus is append-only; failures are events that *should* leave receipts but no receipt-of-failure metric is defined.
- **Whether anyone outside HUMMBL would adopt this.** Track 4 ("Productization") is entirely supply-side. Demand is unmeasured.
- **Disagreement / dissonance among the agents themselves.** Ironically, given the centrality of the "dissonance score," the roadmap has no record of inter-agent disagreement about the roadmap's own claims.

**Who benefits from these absences?** The same actors who would be embarrassed by the measurements: the operator (whose bandwidth is the bottleneck), the agents (whose disagreements would surface), and the project itself (whose external demand is unverified). This is a normal pattern, not a uniquely CRAB pathology, but it is the political shape of the metric set.

---

## 8. Stop Rules / Kill Criteria

I find **zero explicit stop rules** in the roadmap. Specifically:

- No criterion for declaring a track *failed* and shutting it down.
- No criterion for declaring the Scuttlebutt prototype a *bad idea* and killing it. (The roadmap says "the only way to know is to build it and measure" — but specifies no measurement that would falsify it.)
- No criterion for declaring Retrograde *not worth the complexity*.
- No criterion for declaring CRAB itself *worse than a simpler reactive loop*. The planned benchmark is the closest thing, but it is structurally rigged (see §3, M22).

**Without stop rules, every track is in principle infinite.** Goodhart and Campbell will accumulate without any natural reset. This is the most important measurement-hygiene gap in the document.

---

## 9. Overall Measurement Health Score

**Score: 4 / 10.**

Reasoning:
- **+1** for explicitly listing what the roadmap "gets wrong" — meta-honesty is rare and worth crediting.
- **+1** for retiring the term "research-validated."
- **+1** for the Evidence Matrix existing at all (most plans don't include one).
- **+1** for the cross-track collision section catching the LOBSTER-vs-benchmark Goodhart pre-emptively.
- **−1** because the Evidence Matrix grades itself with no external auditor and an unprincipled scale.
- **−1** because the Status Legend conflates measurable and subjective categories under a uniform vocabulary.
- **−1** because effort estimates have a meta-uncertainty problem with no calibration plan.
- **−1** because there are no stop rules anywhere.
- **−1** because the hardening protocol is being applied to itself (recursive self-certification).
- **−1** because "dissonance score," "scuttlebutt confidence," and "trust = 1/len(chain)" are introduced as numeric without definition or validation, exactly the conditions for downstream Goodhart.

Net: **4/10.** This is a roadmap that is *aware* of measurement pathologies and partially defended against them, but whose defenses are themselves self-administered. It is roughly an order of magnitude more measurement-conscious than typical engineering roadmaps, and roughly an order of magnitude less rigorous than what the metrics would need to support the decisions they will be used for.

---

## 10. Recommendations for Measurement Hygiene

Ranked by leverage:

1. **Adopt explicit stop rules per track.** For each of the six tracks, write one sentence: *"This track will be killed if X."* If you cannot write such a sentence, you cannot honestly claim the track is being managed; you can only claim it is being narrated.

2. **Externalize at least one auditor.** The Evidence Matrix and Status Legend are self-graded. Pick one outside reviewer (a person, not an agent) to re-grade quarterly. Without this, Campbell drift is structurally inevitable.

3. **Replace numeric effort estimates with calibrated buckets** until you have ≥20 data points of estimate-vs-actual. Start logging that data *now*, retroactively where possible. Publish the calibration curve in v3.0.

4. **Define every numeric scuttlebutt parameter operationally before implementation, or do not ship it.** "Confidence 0.0–1.0" without a calibration procedure is meaningless. "Trust = 1/len(chain)" without a validation set is decorative arithmetic. Either build the calibration loop first or strip the numbers and use categorical labels (LOW/MED/HIGH).

5. **Decouple the hardening protocol from the document being hardened.** A protocol that certifies its own application is unfalsifiable. Either run RETROGRADE on this roadmap *from a different agent* with no access to the prior hardening receipts, or stop calling self-review "RETROGRADE."

6. **Tighten the Status Legend to a 3-bucket scale.** Done / In-flight / Not-started, with crisp evidence requirements. The current 6-bucket scale invites reclassification gaming. "Research-mentioned" especially should be retired or merged with "Open"; the distinction currently functions as a soft-disposal mechanism.

7. **Add a "What is unmeasured?" section to each track.** Force the politics of quantification into the open. Ask, per track: *what would change our minds about this track that we are currently not collecting?*

8. **Decommission vanity metrics.** "14 expressions," "36 citations," "625 lines" — these are not measurements of anything that matters. Keep counts only when they gate decisions.

9. **Commit to a benchmark protocol *before* building LOBSTER.** The existing plan (build LOBSTER, then benchmark CRAB-vs-LOBSTER) is a textbook HARKing setup. Pre-register the benchmark — including the win condition for the *reactive baseline* — and submit the protocol to an outside reader before writing the LOBSTER code.

10. **Watch the Evidence Matrix summary ratio over time.** If 0/12 external becomes 2/12 within 6 months, ask whether the new "external" claims really are external or whether the bar moved. Track the bar, not just the score.

---

**Final note from the lens.** The CRAB roadmap is unusual among engineering plans in that it acknowledges several of its own measurement problems openly. That honesty is real. But honesty about a measurement problem is not the same as a fix for the measurement problem, and several of the document's "fixes" (the Evidence Matrix, the hardening protocol, the uncertainty ranges) are themselves unaudited measurements that will, on a Goodhart/Campbell trajectory, become the next layer of theatre. The path forward is not more meta-self-review. It is one outside auditor, one stop rule per track, and one calibration data point per estimate. Three small things, structurally distinct from anything currently in the document.
