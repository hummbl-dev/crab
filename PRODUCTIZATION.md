# CRAB Productization Plan
## From Internal Ops to Marketable Products

**Status**: Brainstorm v0.1.1 — 2026-05-16 hygiene note
**Classification**: INTERNAL — operator eyes only
**Author**: Devin (Kimi K2.6)
**Context**: Commit `2e7ed48` just landed the portable CRAB Daemon in this repo. The next question is: what else from the HUMMBL internal ops platform (`founder-mode`) can and should become a standalone product?

---

## 1. Current State of `founder-mode` — The "Garage"

The `hummbl-dev/founder-mode` repo is a **production multi-agent operating system** with ~279 Python modules across services, integrations, cognition, and bus layers. It runs daily in production. It is also **deeply coupled to Dan and Reuben's specific infrastructure**:

| Coupling Type | Count | Examples |
|-------------|-------|----------|
| Machine profiles | 19 service files | Internal hostnames hardcoded as Ollama hosts, inference nodes, CI runners |
| VPN/tailnet IPs | 512 Python references | Internal tailnet addresses and host mappings |
| Hardcoded emails | 46 | Internal personal/work emails in configs, adapters, notifications |
| Bus paths | 36 files | `_state/coordination/messages.tsv` assumes specific repo layout |
| Agent identities | ~40 | `claude-code`, `codex`, `gemini`, `sov`, `echo`, `soma`, `devin`, `opencode` — all HUMMBL-specific roster |
| Windows paths | scattered | Hardcoded user paths, `.claude/rules/`, `.agents/rules/` in guardrails and launchers |
| External adapters | 7 live | GitHub, Google Calendar, Linear, Cost Tracker, Security, Ollama — wired to HUMMBL accounts |

**The garage is not a showroom.** You cannot open-source `founder-mode` as-is without exposing your operational topology, personal infrastructure, and security surface.

---

## 2. What Can Become a Product

### Tier 1: Already Extracted or Extractable Now

| Product | Status | What It Is | Portability Blockers | Action |
|---------|--------|-----------|----------------------|--------|
| **CRAB Protocol** | `DONE` — private incubator | 4-step coordination protocol + daemon | Repo-wide public/private split audit required | **Prepare public-core subset** |
| **hummbl-governance** | `DONE` — on PyPI | 7 safety primitives (kill switch, circuit breaker, delegation tokens, etc.) | Already stdlib-only, already on PyPI | **Continue maintaining** |
| **Coordination Bus** | `NEEDS WORK` | TSV append-only log with `flock` locking, identity validation, message type enforcement | Hardcoded paths, HUMMBL identity registry, HMAC signing secret schema | Extract bus core as `crab-bus` or `coordination-bus` |

### Tier 2: Extractable with Moderate Refactoring

| Product | What It Is | Why It Matters | Blockers | Effort |
|---------|-----------|---------------|----------|--------|
| **CRAB Dashboard** | Next.js + FastAPI Mission Control UI (system map, agent fleet, bus stream, kill switch) | Visualization layer makes CRAB tangible | Coupled to HUMMBL service endpoints, hardcoded agent list, HUMMBL branding | 2-3 weeks |
| **Agent Identity Registry** | HMAC-signed capability tokens, chain-depth enforcement, governance audit log | Who can do what, provably | Identity schema is HUMMBL-specific; needs generic role-based model | 1-2 weeks |
| **Cost Governor** | Per-agent budget tracking with automatic halt at ceiling | Prevents runaway API spend | Currency/provider-specific; needs pluggable cost backend | 1 week |
| **Schema Validator** | stdlib-only JSON Schema Draft 2020-12 subset | Validate configs, contracts, bus messages without external deps | None significant — already portable | **Low-hanging fruit** |
| **Briefing Engine** | Morning Briefing generator — aggregates git, calendar, issues, security scans into structured digest | The "daily pulse" product | Deeply coupled to HUMMBL adapters (GitHub org, Google Calendar, Linear team) | 3-4 weeks |

### Tier 3: Long-term / Requires Fundamental Rethink

| Product | What It Is | Why It Matters | Blockers | Effort |
|---------|-----------|---------------|----------|--------|
| **Autoresearch Pipeline** | Overnight batch: intake → distill → synthesize → propagate | AI-powered research automation | Hardwired to a specific inference host, operator's cron schedule, HUMMBL research topics | 4-6 weeks |
| **Trading Loop** | Alpaca-integrated algorithmic trading with circuit breakers | Revenue-generating subsystem | Financial logic is proprietary; infrastructure is HUMMBL-specific | **Keep internal** |
| **Cognition Layer** | CLP (Cognitive Ledger Protocol), BM25 index, Open Brain server | Shared memory for agents | Tied to HUMMBL memory layout, embedding model choices, disk paths | 4-6 weeks |
| **Full Agent Fleet** | 10+ agents with guardrails, personas, multi-lens synthesis (ARCANA, Base120, etc.) | The "HUMMBL OS" | Entire framework is bespoke philosophy + custom infrastructure; not a product, it's the *platform* | **Keep internal** |

---

## 3. The Productization Pipeline

```
HUMMBL Internal (founder-mode)
        |
        v
[REFACTOR] Strip hostnames, IPs, emails, hardcoded paths
        |
        v
[EXTRACT] Move to standalone repo (e.g., hummbl-dev/<product>)
        |
        v
[TEST] Verify zero third-party deps (stdlib-only policy)
        |
        v
[REDTEAM] Audit for secrets, leakage, injection, identity borrowing
        |
        v
[DOCUMENT] Write README with worked examples, no HUMMBL context required
        |
        v
[ALPHA] Dogfood inside HUMMBL for 30+ days on real workloads
        |
        v
[PUBLIC DECISION] Operator (Reuben) decides: ship as OSS, sell as SaaS, or keep internal
        |
        v
[if OSS] Clean commit history, choose license, create fresh public repo
```

---

## 4. What Must Occur

### Before ANY product ships

1. **Complete redteam audit** — secrets, hostnames, operational details, identity leakage
2. **Replace all hardcoded infrastructure** with configuration:
   - VPN/tailnet IPs → `MESH_HOSTS` env var or config JSON
   - Machine names → `INFERENCE_NODES` config
   - Emails → `NOTIFICATION_RECIPIENTS` config
   - Bus paths → `BUS_PATH` config with sensible default
3. **Write documentation that assumes zero HUMMBL context** — a stranger should understand it
4. **Add CI/tests** that run in isolation (no HUMMBL services required)
5. **Operator approval** — Reuben must explicitly greenlight each product for external visibility

### For each product tier

| Tier | Must Occur |
|------|-----------|
| Tier 1 (CRAB, governance) | Document, test, license, ship |
| Tier 2 (Dashboard, Identity, Cost Gov, Schema, Briefing) | Extract → refactor → dogfood → decide |
| Tier 3 (Autoresearch, Trading, Cognition, Full Fleet) | Keep internal; productize sub-components only |

### Commercialization paths

| Product | OSS | SaaS | Consulting |
|---------|-----|------|------------|
| CRAB Protocol | Yes (MIT/Apache-2.0) | No (protocol, not service) | Training/implementation |
| CRAB Dashboard | Yes (front-end) | Hosted version possible | Custom dashboards |
| hummbl-governance | Already PyPI | No (library) | Integration support |
| Coordination Bus | Yes | Hosted bus with webhooks | Enterprise on-prem |
| Briefing Engine | Core engine OSS | Hosted briefing service | Custom adapters |
| Agent Identity | Yes | Identity-as-a-service | Enterprise SSO integration |

---

## 5. What Must NOT Occur

### Absolute Red Lines

1. **NEVER leak operational topology** — VPN/tailnet IPs, machine hostnames, network layout, VPN details
2. **NEVER leak personal identities** — Real names, emails, home addresses, personal GitHub accounts
3. **NEVER leak credentials or tokens** — API keys, PATs, OAuth tokens, signing secrets, even in test fixtures
4. **NEVER make public before audit** — The `redteam` skill must run clean before any repo visibility changes
5. **NEVER ship half-extracted products** — A "ported" module that still imports from `founder_mode.services.*` is not a product
6. **NEVER commit to public repo with dirty history** — The public repo must have clean history; use `git-filter-repo` or start fresh
7. **NEVER violate the "no secrets in code" rule** — Even in private repos; secrets belong in env vars, Keychain, or vaults

### Strategic Must-Nots

8. **NEVER open-source the Trading Loop** — Financial logic is proprietary and regulated; keep internal
9. **NEVER open-source the full Agent Fleet** — ARCANA, Base120, and the multi-lens synthesis framework are HUMMBL's competitive moat. The *primitives* (CRAB, governance) can be OSS. The *orchestration layer* stays internal.
10. **NEVER ship without a license** — Every public repo needs a LICENSE file before first commit. Choose before shipping.
11. **NEVER ship without a Code of Conduct and CONTRIBUTING.md** — OSS projects need community guardrails
12. **NEVER use the public repo as the incubator** — The private `hummbl-dev/*` repos are for trial and error. The public repo is for polished artifacts only.

---

## 6. Recommended Priority Order

| Priority | Action | Why First |
|----------|--------|-----------|
| **P0** | Finish CRAB public artifact (docs, website, examples) | Most viral-ready, lowest risk, highest external value |
| **P1** | Extract Coordination Bus as standalone module | Core dependency for CRAB; other products need it |
| **P2** | Port CRAB Dashboard to generic form | Makes CRAB tangible; demo-able; sells the vision |
| **P3** | Productize Schema Validator (already portable) | Zero deps, immediately useful, builds credibility |
| **P4** | Extract Agent Identity / Delegation Token system | Security-critical; enterprises will want this |
| **P5** | Refactor Briefing Engine for generic adapters | High-value daily-use product; requires adapter abstraction |
| **P6** | Evaluate Cost Governor for SaaS potential | Clear monetization path: "pay for what you use" |
| **P7** | Keep everything else internal | Trading, autoresearch, cognition, full fleet — HUMMBL's moat |

---

## 7. The Viral Question

> "What makes CRAB (or any HUMMBL product) spread?"

CRAB spreads because:
- It solves a problem everyone in multi-agent systems has (coordination)
- It requires zero infrastructure (stdlib-only, any bus)
- It's memorable (4 letters, 4 steps, crustacean branding)
- It's already battle-tested (50+ AAR cycles, 5+ agent types)

Other products spread if they:
- Solve a *specific* pain (not a platform promise)
- Work in 5 minutes (not 5 hours of setup)
- Have a clear before/after ("before: agents race each other; after: every turn leaves a receipt")
- Don't require buying into the HUMMBL philosophy to get value

**The moat is not the code.** The moat is the *operating system* — the way 10+ agents, 3 humans, and 5 machines coordinate daily without chaos. The code is the *demonstration* of the OS. The OSS products are the *on-ramp*.

---

## 6. License Status — Apache-2.0 Selected

CRAB now has a repository `LICENSE` file using Apache-2.0. The remaining gate is not license selection; it is whether and when Reuben approves a public release after the repo-wide public/private split audit.

Historical options considered:

| License | Permissiveness | Patent Protection | Commercial Use | Best For |
|---------|---------------|-------------------|----------------|----------|
| **MIT** | Maximum | None | Unlimited | Fastest adoption, widest distribution |
| **Apache-2.0** | High | Yes (explicit patent grant) | Unlimited | Corporate adoption (legal departments prefer patent clauses) |
| **PolyForm Noncommercial 1.0.0** | Restricted | None | Prohibited without separate agreement | Delayed monetization — keeps commercial rights reserved |
| **AGPL-3.0** | Copyleft | Yes | Allowed, but modifications must be shared | If you want to force contributions back (risk: scares companies away) |

### Selected: Apache-2.0

**Rationale:**
- CRAB is a *protocol* — protocols need network effects to be valuable
- Apache-2.0 provides the patent protection that enterprise legal teams require
- It's permissive enough for startups, big tech, and individual developers
- It does NOT force contributors to share modifications (unlike GPL/AGPL)
- It aligns with how other coordination protocols have succeeded (e.g., NATS, etcd, Kubernetes are all Apache-2.0)

**If you choose PolyForm Noncommercial:** You retain the right to sell commercial licenses later, but you sacrifice network effects now. This only makes sense if you have a specific commercial licensing strategy ready.

**If you choose MIT:** Simpler, but you lose patent protection. Fine for a hobby project; risky for something you might patent-protect later.

**Remaining decision needed:** approve or defer public release after the public-core subset is audited. Do not treat this private incubator repo as the public artifact by default.

---

## 7. Public Release Timeline — Three Options

### Option A: Ship This Week (Minimal Viable Release)
**What ships:** `crab_daemon.py`, `tests/`, `README.md`, `AUDIT.md`, `LICENSE`
**What doesn't:** Website, examples, blog post, community docs
**Pros:** Fastest feedback loop, lowest overhead
**Cons:** First impression is thin; harder to build momentum
**Effort:** 2-4 hours after repo-wide public/private split audit (verify LICENSE, cut v1.0 tag, write release notes)

### Option B: Two-Week Sprint (Recommended)
**What ships:** Everything in Option A + website landing page + 3 examples + `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md`
**What doesn't:** Full docs site, video demo, conference talk
**Pros:** Professional enough for HN/Reddit launch, examples prove value
**Cons:** 2 weeks of focused work
**Effort:** ~16 hours spread over 2 weeks

### Option C: One-Month Runway (Maximum Polish)
**What ships:** Everything in Option B + full docs site (MkDocs) + video demo + launch blog post + first community call
**Pros:** Best chance of sustained adoption, press coverage, conference CFP submissions
**Cons:** Longest time to market, highest opportunity cost
**Effort:** ~40 hours over 4 weeks

### Recommended: Option B (Two-Week Sprint)

If public release is approved after audit, a two-week sprint gives you:
- A landing page that explains CRAB in 60 seconds
- 3 working examples (Python script, shell script, Docker compose)
- A contribution guide that signals you're open to external contributors
- A v1.0 tag that signals stability after the public-core subset is verified

**Sprint breakdown:**

| Day | Task |
|-----|------|
| 1-2 | Verify LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md and public/private boundaries |
| 3-4 | Build landing page (single HTML, no framework, hosted on GitHub Pages) |
| 5-6 | Write 3 examples: basic Python, bus backend plugin, Docker compose |
| 7-8 | Write "Getting Started" guide + API reference |
| 9-10 | Cut v1.0.0 tag, write release notes, post to HN / r/selfhosted / relevant Discords |
| 11-14 | Respond to feedback, fix issues, update docs |

---

## 8. Tier 2 Priority — After CRAB OSS Ships

Once CRAB OSS v1.0 is live, the next extraction target depends on what feedback you get:

| If users ask for... | Extract first |
|---------------------|---------------|
| "How do I visualize my agent mesh?" | **CRAB Dashboard** (generic form) |
| "How do I track costs across agents?" | **Cost Governor** |
| "How do I validate bus messages?" | **Schema Validator** (low-hanging fruit) |
| "How do I authenticate agents?" | **Agent Identity Registry** |
| "How do I generate daily briefings?" | **Briefing Engine** (hardest, save for last) |

**My recommendation:** Start with **Schema Validator** (1 week effort, already portable) while gauging demand for the others. It gives you a quick win and proves the extraction pipeline works.

---

## Receipt

- Brainstorm artifact: this file
- Audit: `AUDIT.md` (10/10 PASS)
- Portable daemon: `crab_daemon.py` + `tests/test_daemon.py`
- Issue tracking: GitHub Issue #1 + #2 in `hummbl-dev/crab`
- Peer review: Issue #2 awaiting external sign-off
- **Next gate: Operator approves or defers public release after repo-wide public/private split audit (Section 6 & 7)**
