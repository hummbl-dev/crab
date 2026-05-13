# AI Notary: Compliance Copilot for Independent Notaries

## One-Pager

**Prepared by:** Reuben Bowlby, HUMMBL Research Institute  
**For:** [Notary Friend] — Joint Venture Discussion  
**Date:** May 11, 2026

---

## The Problem

Notaries are drowning in administrative risk. In 2025 alone:

- **Texas made notary misconduct a criminal offense** — up to 1 year in jail, $4,000 fines, state jail felony for real property fraud (SB 693, effective Sept 2025)
- **Ohio raised RON fees to $30 + $10 tech fee** — but notaries need defensible audit trails to justify charging technology costs (HB 315, effective April 2025)
- **45 states + DC now allow Remote Online Notarization (RON)** — but independent notaries lack the enterprise-grade compliance tools that platforms like Notarize keep for themselves

Every missed journal entry, every blank notary block, every incomplete ID check is now a potential liability. Notaries are legal officers with paper notebooks and Excel spreadsheets.

---

## The Market

| Metric | Value |
|--------|-------|
| RON market (2025) | **$1.5–1.8 billion** |
| Projected (2032–33) | **$6–13 billion** |
| CAGR | **18–25%** |
| US notaries (active) | **~4.4 million** |
| Title companies using online notarization | **~69%** |

The market is shifting from "employed notary platforms" (Notarize) to **embedded notarization** — enterprises want notarization as a capability, not a separate vendor. Independent notaries need tools to compete.

---

## The Solution: HUMMBL Notary Copilot

An AI-native compliance layer for independent notaries — before, during, and after every notarial act.

### Pre-Session Intelligence
- **Document pre-check:** OCR scan detects blank notary blocks, missing signatures, incomplete fields before the notary leaves the office
- **ID pre-validation:** Signer uploads ID; AI checks expiration, readability, state validity
- **State certificate generator:** Auto-selects the correct jurat/acknowledgment wording for the notary's commissioning state
- **Compliance briefing:** "This signer is out-of-state — RON reciprocity rules apply"

### During-Session Guardrails
- **Real-time checklist:** "Verify signer matches ID photo" — AI watches for behavioral red flags (duress cues on video)
- **Recording automation:** Start/stop A/V recording, timestamp alignment, consent capture
- **Notary journal auto-pop:** Fields pre-filled from session data; notary confirms with one tap

### Post-Session Evidence
- **Hash-chain receipt:** SHA-256 tamper-evident audit trail stored for state-mandated retention (5–10 years)
- **Compliance score:** "3/3 checks passed — this notarization is defensible"
- **Auto-invoice:** Fee calculation including RON tech fee, travel fee, per-signature fee

---

## Why Us

### Foundational Infrastructure (Already Built)

HUMMBL Research Institute has spent 18 months building **governance infrastructure for legal AI**:

| Asset | What It Is | How It Maps to Notary Copilot |
|-------|-----------|-------------------------------|
| **Receipt Store** | SHA-256 hash-chain, append-only, content-free audit logging | Notary journal + long-term retention compliance |
| **Forward-Only State Machine** | AI output can only progress to review or rejection — never backward | Prevents tampering with notarial records |
| **Conflict-Check Middleware** | Real-time filtering for ethical conflicts | Notary commission validation, recusal flags |
| **Kill Switch + Circuit Breaker** | Automatic halt on anomaly detection | Session abort if ID verification fails or duress detected |
| **Compliance Mappings** | ABA Model Rules, EU AI Act, ISO 42001, NIST AI RMF | Extend to state notary laws + UETA/ESIGN |
| **hummbl-governance (PyPI)** | 19 modules, 400 tests, stdlib-only Python, Apache-2.0 | Reuse for notary-specific governance layer |

**We are not starting from zero. We are adapting proven legal AI infrastructure to a new vertical.**

---

## Competitive Landscape

| Player | Their Model | The Gap We Fill |
|--------|------------|-----------------|
| **Notarize / Proof** | Employs notaries on a platform | Notaries work *for* them, not independently |
| **OneNotary** | RON platform + third-party network | Tech-heavy, no AI-native compliance layer |
| **Snapdocs** | Mobile signing-agent dispatch | Signing-agent only, no RON, no compliance audit |
| **Dewx** | Scheduling + route optimization | Narrow ops tool — no document intelligence, no RON |
| **AgentZap** | AI phone receptionist | Single feature; no session intelligence |

**No competitor offers tamper-evident audit trails designed for criminal defense.**

---

## Business Model

### Phase 0: Validation (0–30 days)
- Interview 5 notaries in [friend]'s network
- Build notary journal schema + state certificate engine
- Demo to 3 notaries, collect feedback

### Phase 1: MVP Launch (1–3 months)
- **SaaS pricing:** $49–79/month per notary
- **Per-session fee:** $2–5 for RON sessions (mirrors Ohio's new $10 tech fee structure)
- **Target:** 50 paying notaries = $29,400–47,400 MRR

### Phase 2: Scale (3–12 months)
- **Signing agent tier:** $79–129/month with loan package OCR + route optimization
- **API tier:** $10–25 per embedded notarization call for proptech/fintech platforms
- **Target:** 500 notaries + 5 API customers = $300K+ MRR

---

## Joint Venture Structure

```
AI Notary JV LLC
├── HUMMBL Research Institute: 60%
│   └── Governance infrastructure (receipts, compliance, kill switch)
│   └── Technical execution + product development
│   └── Capital for Phase 0–1
├── [Notary Partner]: 40%
│   └── Notary commission + RON authority
│   └── Industry expertise, state compliance navigation
│   └── Notarial act template content + first clients
│   └── Notary network access for validation
└── Revenue: Split pro-rata after HUMMBL recovers dev costs
```

**Phase gate:** If MVP does not acquire 3 paying notaries in 60 days, pivot or wind down — low-risk, high-learning.

---

## Why Now

1. **Regulatory urgency:** Texas criminalized notary misconduct. Notaries need defensive tools.
2. **Fee expansion:** Ohio now allows explicit tech fees — notaries want to capture this revenue.
3. **RON normalization:** 45 states permit it. The infrastructure exists; the notary tools don't.
4. **AI readiness:** GPT-class models can now reliably parse documents, verify IDs, and generate state-specific certificates.
5. **Our readiness:** We have production governance infrastructure that no notary-tech competitor has built.

---

## The Ask

**For [Notary Friend]:**
- 2–3 hours/week for 30 days: interview notaries in your network, review state-specific certificate templates, validate compliance workflows
- Your commission as the first test notary for RON sessions
- Industry credibility and first-client introductions

**For HUMMBL:**
- Adapt existing governance infrastructure to notary-specific workflows
- Build MVP in 4–6 weeks
- Capital for API integrations (ID verification, e-signature)

**Next step:** 30-minute call to walk through the Dewx homepage (what exists) vs. our receipt store (what we have) and decide if the gap is worth building into.

---

## Appendix: Evidence

- **Texas SB693:** https://notaryhub.com/articles/tx-ron-law-changes-2025
- **Ohio HB315:** https://notaryhub.com/articles/ohio-ron-law-changes-2025
- **RON market data:** Global RON market $1.8B (2024) → $13.6B (2033), 24.7% CAGR
- **HUMMBL governance library:** `hummbl-governance` v0.1.0 on PyPI, 19 modules, 400 tests
- **Christine Schneider term sheet:** `hummbl-legal/engagements/christine/B25-partnership-term-sheet.md` — template for JV structure

---

*Prepared by HUMMBL Research Institute. Not legal advice. All market figures from public research reports cited in appendix.*
