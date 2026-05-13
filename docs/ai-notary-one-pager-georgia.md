# AI Notary: Compliance Copilot for Georgia Notaries

## One-Pager

**Prepared by:** Reuben Bowlby, HUMMBL Research Institute  
**For:** [Notary Friend] — Joint Venture Discussion  
**State:** Georgia  
**Date:** May 11, 2026

---

## The Problem

Georgia notaries just got hit with the biggest regulatory change in a generation — and most are still using paper notebooks.

**House Bill 1292 took effect January 1, 2025.** Every Georgia notary must now:
- Complete **mandatory state training** to apply or renew a commission
- Maintain a **written or electronic journal** for notarizations requested by "self-filers"
- Record **6 specific fields** per entry: signer name, address, phone, date/time/location, ID type + number, signer signature, document type
- Use **stricter ID verification** guidelines

Here's the catch: **you cannot tell if someone is a "self-filer" until they hand you the document.** The National Notary Association's advice? *Journal every single notarization to avoid accidental non-compliance.*

That's a lot of handwriting for $2 per signature.

---

## The Georgia-Specific Reality

| Fact | Impact |
|------|--------|
| **$2 maximum per notarial act** (OCGA § 45-17-11) | Lowest fee in the country. Efficiency is everything. |
| **$4 total per service** (including attendance/certification) | You cannot make money on the act itself. You make it on volume, travel, and loan signings. |
| **HB 1292: mandatory journals effective Jan 2025** | Miss a journal entry for a self-filer = compliance violation. |
| **Georgia is an "attorney state" for real estate** | A licensed GA attorney must oversee real estate closings. Loan signing agents assist; they do not replace attorneys. |
| **RON is NOT yet legal for GA-commissioned notaries** | HB 289 passed the House Judiciary Committee (amended, implementation delayed to 2027) but has not been enacted. GA notaries must still appear in person. |
| **Self-filers must now e-file** (HB 1292) | Deeds, mortgages, liens filed electronically. The notary's journal is now part of a digital chain. |

**Translation:** Georgia notaries are legally required to keep better records than ever, for less money per act, in a state where real estate closings require attorney oversight and RON doesn't exist yet.

---

## The Market in Georgia

| Segment | Typical Income | Notes |
|---------|---------------|-------|
| Traditional in-person | $2,000–$7,500/year | Part-time, office-based |
| **Mobile notary** | **$8,000–$35,000/year** | Travel fees are unregulated — this is where the money is |
| **Loan signing agent** | **$30,000–$80,000+/year** | $75–$200 per closing in Atlanta metro; highest-margin segment |
| Hybrid mobile + signing | $40,000–$90,000+/year | Combinations of services drive the top end |

Atlanta metro is one of the fastest-growing real estate markets in the country. Loan signing agents are in constant demand. But a single missed journal entry on a self-filer deed — or a blank notary block in a 120-page closing package — can cost the notary their commission.

---

## The Solution: HUMMBL Notary Copilot (Georgia Edition)

An AI-native compliance layer designed specifically for Georgia's low-fee, high-regulation, attorney-state environment.

### Pre-Session Intelligence
- **Document pre-check (OCR):** Scan the full closing package before leaving the office. Flags blank notary blocks, missing signatures, incomplete fields. Prevents the costly "dry signing" return trip.
- **Self-filer detector:** Reads the document type (deed, mortgage, lien, plat) and auto-flags if journal entry is legally required under HB 1292.
- **GA certificate generator:** Auto-selects the correct acknowledgment/jurat wording for Georgia.
- **ID compliance check:** Verifies the presented ID meets Georgia's post-HB 1292 requirements before the notary arrives.

### During-Session Guardrails
- **Real-time journal auto-pop:** Pre-fills all 6 required HB 1292 fields from session data. Notary confirms with one tap — no handwriting, no missed entries.
- **Attorstate awareness:** Flags if the document is a real estate instrument requiring attorney oversight under Georgia law. Prevents accidental UPL (unauthorized practice of law).
- **Notary block navigator:** AI highlights exactly where each signature, initial, and notary stamp goes in a 100+ page package.
- **Recording compliance:** For applicable sessions, auto-starts/stops consent capture and timestamp alignment.

### Post-Session Evidence
- **HB 1292-compliant journal export:** Written or electronic format, ready for GSCCCA inspection.
- **Hash-chain receipt:** SHA-256 tamper-evident audit trail stored for state-mandated retention. If a deed is challenged, the notary has defensible proof of every step.
- **Auto-invoice:** $2 notarial act + travel fee + printing + scanback — calculated and itemized per Georgia law.
- **Compliance score:** "All HB 1292 fields captured — this notarization is inspection-ready."

---

## Why This Is Urgent for Georgia Right Now

**January 2025 was not a drill.** HB 1292 is in effect. The Georgia Superior Court Clerks' Cooperative Authority (GSCCCA) is now enforcing:
- Training completion before commission renewal
- Journal maintenance for self-filer transactions
- Standardized ID acceptance rules

**Notaries who fail to comply risk:**
- Commission suspension or revocation (GSCCCA has authority)
- Liability in real estate fraud disputes
- Inability to renew their commission without re-training

**There is no Georgia-specific compliance tool on the market.** National platforms (Notarize, OneNotary) are built for RON states. Dewx does scheduling. Snapdocs does loan dispatch. **No one is building AI that understands Georgia's $2 fee cap, attorney-state real estate rules, and HB 1292 journal requirements.**

---

## Your Competitive Moat: Governance Infrastructure

HUMMBL Research Institute has spent 18 months building **tamper-evident compliance infrastructure for legal AI** — and it maps directly to Georgia notary requirements.

| HUMMBL Asset | How It Serves Georgia Notaries |
|-------------|-------------------------------|
| **Receipt Store** (SHA-256 hash-chain, append-only) | HB 1292 journal + long-term retention compliance. Tamper-evident if GSCCCA audits. |
| **Forward-Only State Machine** | AI output can only progress — never backward. Prevents accidental journal alteration. |
| **Conflict-Check Middleware** | Flags if a signer appears in fraud databases; recusal alerts for known conflicts. |
| **Kill Switch + Circuit Breaker** | Auto-halts session if ID verification fails or duress is detected. Protects the notary from liability. |
| **Compliance Mappings** | ABA, EU AI Act, ISO 42001, NIST AI RMF frameworks already mapped. Extend to GSCCCA rules. |
| **hummbl-governance (PyPI)** | 19 modules, 400 tests, stdlib-only Python, Apache-2.0. Reuse as the Georgia notary compliance engine. |

**We are not building from scratch. We are adapting proven legal AI governance to the notary vertical.**

---

## Competitive Landscape

| Player | Their Strength | Why They Fail in Georgia |
|--------|---------------|------------------------|
| **Notarize / Proof** | Enterprise RON platform | RON is illegal for GA-commissioned notaries |
| **OneNotary** | RON + third-party network | No GA-specific compliance; no journal automation |
| **Snapdocs** | Loan signing dispatch | Scheduling only — no document intelligence, no HB 1292 compliance |
| **Dewx** | Scheduling + route optimization | Narrow ops tool; no OCR, no journal auto-pop, no attorney-state awareness |
| **AgentZap** | AI phone receptionist | Single feature; no session intelligence |
| **Notary journal vendors** (NNA, etc.) | Paper/electronic journals | Static forms; no AI pre-check, no document analysis, no compliance scoring |

**No competitor offers:**
- HB 1292 journal auto-population from session data
- Document deficiency detection for Georgia loan packages
- Attorney-state real estate awareness
- Hash-chain audit trails for GSCCCA inspection defense

---

## Business Model

### Phase 0: Validation (0–30 days)
- Interview 5 Georgia mobile notaries / loan signing agents in your network
- Map 6 HB 1292 journal fields to auto-pop workflow
- Demo to 3 notaries, collect feedback

### Phase 1: MVP Launch (1–3 months)
- **Georgia Notary Copilot:** $39–59/month per notary
- **Loan Signing Agent tier:** $79–129/month with OCR package analysis + route optimization
- **Target:** 50 paying Georgia notaries = $1,950–6,450 MRR

### Phase 2: Scale + RON Readiness (3–12 months)
- **Multi-state expansion** as RON rolls out (track HB 289 — if enacted, Georgia notaries will need RON tools immediately)
- **API tier** for proptech/fintech platforms embedding notarization
- **Target:** 500 notaries across Southeast + 5 API customers

### Phase 3: RON Launch (contingent on Georgia legislation)
- When HB 289 or successor passes, add RON video sessions + ID verification
- GA notaries who already use our copilot become first adopters of the RON module
- **First-mover advantage in a state with 4.4M notaries' worth of pent-up demand**

---

## Joint Venture Structure

```
AI Notary JV LLC (Georgia)
├── HUMMBL Research Institute: 60%
│   └── Governance infrastructure (receipts, compliance, kill switch)
│   └── Technical execution + product development
│   └── Capital for Phase 0–1
├── [Notary Partner]: 40%
│   └── Georgia notary commission + HB 1292 expertise
│   └── Industry knowledge, GSCCCA relationship navigation
│   └── Notarial act template content + first clients
│   └── Loan signing agent network access (Atlanta metro)
└── Revenue: Split pro-rata after HUMMBL recovers dev costs
```

**Phase gate:** If MVP does not acquire 3 paying Georgia notaries in 60 days, pivot or wind down — low-risk, high-learning.

**Scope separation from HUMMBL Paralegal:** The attorney-facing product (Christine Schneider engagement) handles legal practice AI. This JV handles notary compliance. No overlap, shared infrastructure.

---

## Why Now

1. **HB 1292 is live.** Georgia notaries need compliance tools *today*, not when RON arrives.
2. **Lowest fees in America.** At $2 per signature, notaries survive on volume and efficiency. AI is the only lever left.
3. **Atlanta real estate boom.** Loan signing agents are the highest-paid notary segment and the most document-heavy. They need AI pre-checks the most.
4. **Attorney-state complexity.** Georgia's real estate rules are stricter than RON states. Generic national tools break here.
5. **RON is coming.** HB 289 passed committee (amended, delayed to 2027). When it hits, notaries who already have our compliance layer will upgrade to RON instantly. **We capture the transition, not just the current state.**

---

## The Ask

**For [Notary Friend]:**
- 2–3 hours/week for 30 days:
  - Introduce us to 3–5 Georgia mobile notaries / loan signing agents for interviews
  - Review GA-specific certificate templates and HB 1292 journal workflows
  - Validate attorney-state real estate rules in our document classifier
- Your commission as the first test notary for the platform
- Industry credibility and first-client introductions in Atlanta metro

**For HUMMBL:**
- Adapt existing governance infrastructure to Georgia notary workflows
- Build MVP in 4–6 weeks (reuse PyPI library, build GA-specific UI layer)
- Capital for API integrations (OCR, route optimization)

**Next step:** 30-minute call to walk through HB 1292's journal requirements and show how our receipt store already solves the tamper-evident retention problem.

---

## Appendix: Evidence

- **Georgia HB 1292 (signed May 2, 2024, effective Jan 1, 2025):** OCGA § 45-17-8, § 44-2-39 — mandatory training, journal requirements, ID guidelines, self-filer e-filing
- **Georgia HB 289 (introduced Feb 5, 2025):** Remote online notarization framework — passed House Judiciary Committee with amendments, implementation delayed to 2027
- **Georgia notary fees:** OCGA § 45-17-11 — $2 per notarial act, $4 total per service
- **HB 1292 journal fields:** Signer name, address, phone, date/time/location, ID type + number, signer signature, document type
- **Self-filer definition:** Party to a deed, mortgage, lien, map/plat, or state tax execution who is NOT an attorney, real estate agent, insurance agent, or government official
- **HUMMBL governance library:** `hummbl-governance` v0.1.0 on PyPI, 19 modules, 400 tests
- **NNA guidance on HB 1292:** https://nationalnotary.org/notary-bulletin/blog/2024/12/new-training-journal-and-id-requirements-for-georgia-notaries-start-on-january-1-2025

---

*Prepared by HUMMBL Research Institute. Not legal advice. All statutory citations from the Official Code of Georgia Annotated and publicly available legislative records.*
