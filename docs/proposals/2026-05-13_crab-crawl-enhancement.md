# Proposal: CRAB CRAWL Enhancement

**Status:** Draft
**Date:** 2026-05-13
**Author:** codex
**Scope:** Enhance CRAB by introducing CRAWL as the expanded human-facing name for Step 1 "Check" while preserving the CRAB acronym, the existing Reason -> Act -> Bus contract, and current daemon compatibility.

---

## Executive Summary

Keep CRAB as the parent protocol:

> **CRAB = CRAWL/Check -> Reason -> Act -> Bus**

The change is not a rename of the whole protocol. It is a precision upgrade to Step 1. "Check" is semantically broad in the existing docs, but the required discovery surface is scattered across methodology, implementation, bus, host-specific, and founder-mode guidance. "CRAWL" makes the first phase explicitly memorable enough to cover context, repo state, agent ownership, wire/mesh state, and operational limits.

This is additive and backward-compatible:

- Existing daemon code can keep `CheckResult` and `check_phase()` as internal names for v1.x.
- Public docs should introduce CRAWL as the canonical human-facing expansion of Step 1.
- Implementations can add richer fields over time without breaking old lanes.
- Retrograde is implemented in the reference daemon and enabled by default, but it remains outside the public four-step protocol contract unless/until the public protocol version explicitly promotes it.

---

## Evidence Reviewed

Primary CRAB repo (`hummbl-dev/crab`, local checkout `<WORK_SURFACE>`):

- `README.md` defines CRAB as "Check -> Reason -> Act -> Bus" and advertises a four-step protocol.
- `docs/methodology.md` defines Step 1 as "Check" and lists minimum git-backed checks: repository/workspace, branch, dirty worktree, stash, recent coordination messages, blockers/proposals.
- `docs/implementation-guide.md` tells adopters to define a "Check command set" and gives git branch/status/stash plus local bus read as the baseline.
- `docs/adoption-checklist.md` has a dedicated "Check" section for branch/status, dirty-worktree, stash/lock, bus-tail, and stop conditions.
- `crab_daemon.py` still names the first-phase data structure `CheckResult`, but the implementation already includes extensibility fields (`health_status`, `extra`) suitable for CRAWL.
- `crab_daemon.py` has already grown `RetrogradeResult`, `retrograde_phase()`, and retrograde tests. Docs are therefore behind code on protocol evolution; CRAWL should be documented carefully as part of a v1.x-compatible doc/code alignment pass.
- `docs/BUS_ALIGNMENT_founder_mode.md` identifies founder-mode bus alignment concerns. Some entries are stale relative to current daemon code: current TSV writes already include `to=all`. Real remaining concerns include locking, identity validation, path resolution, and vocabulary drift.
- `docs/UNIFIED_ROADMAP.md` already frames "CHECK" as surveying all tracks for blockers, stale context, and cross-track collisions.

Founder-mode / machine-local CRAB surfaces:

- `founder_mode/playbooks/CRAB.md` requires branch, stash, and bus tail before acting, with host-specific bus-global commands.
- `.claude/rules/crab-protocol.md` adds CWD verification, unresolved proposal reading, verify-before-claim, and host-specific command forms.
- `.claude/rules/crab-protocol-host-specific.md` preserves Bus as mandatory for shared state but allows a narrow local-only exception.
- Machine-global guidance adds mesh surfaces: a bus authority host, peer hosts, mesh/VPN reachability, and no local bus fallback.

Observed live trigger for this proposal:

- On 2026-05-13, the label "Check" did not naturally pull agents toward the full discovery surface needed for coordination. The useful preflight had to include active work surface, branch/stash/status, canonical bus status/tail, mesh/VPN reachability, SSH peer probes, process inventory, disk pressure, dirty worktree ownership, and active peer agent role assignment.

---

## Problem

"Check" is too weak as the canonical label.

The existing CRAB docs already allow broad live-state discovery, including blockers, proposals, protected systems, review gates, deployment status, queues, locks, and CI state. The problem is not that the method forbids those checks. The problem is that the word "Check" lets agents collapse Step 1 into a minimal git/bus preflight and miss broader operating truth:

- Which machine am I on?
- Is this the correct checkout or just a launch directory?
- Are other agents active, exhausted, or claiming ownership?
- Is the bus canonical path healthy or a stale mirror?
- Is there a mesh/SSH/VPN problem?
- Are host limits, disk pressure, usage caps, or protected surfaces relevant?
- Did a human assign a temporary leadership or coordination role?

CRAWL gives the first phase a mnemonic that matches the real operating requirement without changing the core turn loop.

---

## Proposed Semantics

Expand the Step 1 heading:

> **Check**

to:

> **CRAWL / Check**

Define CRAWL as:

| Letter | Meaning | Required Question |
|---|---|---|
| **C** | Context | What is the operator asking, what role/authority was assigned, and what prior bus state changes the prompt? |
| **R** | Repo | What branch/worktree/stash/PR/CI state can invalidate the requested work? |
| **A** | Agents | Which humans, agents, sessions, lanes, or daemons are active, blocked, exhausted, or owners of dirty work? |
| **W** | Wire | Is the coordination substrate current: bus, mirror, SSH, VPN, bridge, queue, issue tracker, or PR comments? |
| **L** | Limits | What stop conditions, disk pressure, usage caps, protected surfaces, credentials, permissions, or irreversible actions constrain the next step? |

Canonical v1.1 protocol line:

```text
CRAB = CRAWL/Check -> Reason -> Act -> Bus
```

Compatibility note: existing code, tests, and older docs may continue to use `Check`, `CheckResult`, and `check_phase()` as implementation names. CRAWL is the expanded operator-facing semantics of that phase, not a breaking API rename.

Reference daemon note: current daemon code includes a post-Bus Retrograde validation phase and enables it by default. This proposal does not decide whether public CRAB v1.1 should become a five-phase protocol. It only upgrades the first-phase semantics. Public docs should say: "CRAB v1.1 remains a four-step public protocol; the reference daemon includes Retrograde as an implementation extension pending a separate protocol decision."

Short operator-facing card:

```text
CRAWL: Context, Repo, Agents, Wire, Limits.
Reason: integrate CRAWL state and choose the message type.
Act: execute the smallest correct step.
Bus: post the receipt, blocker, review, or handoff before final closeout.
```

---

## Minimal CRAWL Profiles

CRAWL must be profile-based. A public OSS repo should not require HUMMBL-specific mesh probes, but a HUMMBL mesh session must.

### Profile 1: Git-Only

For a single repo with one worker and no shared coordination surface:

```bash
git branch --show-current
git status --short --branch
git stash list
```

CRAWL fields covered: Repo, Limits.

Boundary: Git-only CRAWL is invalid when a bus, issue queue, PR thread, deployment channel, or other shared coordination surface exists. In those environments, Wire and Agents checks remain part of the minimum stop-condition contract.

### Profile 2: Coordinated Repo

For a team using a bus, issue queue, or PR comments:

```bash
git branch --show-current
git status --short --branch
git stash list
# plus local bus/queue/PR tail command
```

CRAWL fields covered: Context, Repo, Agents, Wire, Limits.

### Profile 3: HUMMBL Mesh

For host-specific mesh work:

```powershell
git -C <WORK_SURFACE> branch --show-current
git -C <WORK_SURFACE> status --short --branch
git -C <WORK_SURFACE> stash list
<FOUNDER_MODE_REPO>\bin\python.cmd <FOUNDER_MODE_REPO>\bin\bus-global.py tail 5
<FOUNDER_MODE_REPO>\bin\python.cmd <FOUNDER_MODE_REPO>\bin\bus-global.py status
<MESH_STATUS>
```

Use `<FOUNDER_MODE_REPO>` only when founder-mode is the actual work surface or bus authority context. For CRAB repo work, `<WORK_SURFACE>` is the CRAB repo path. Add SSH/process/disk probes only when cross-machine ownership or host health can change the action.

---

## Implementation Plan

### Phase 1: Documentation Alignment

Target files:

- `README.md`
- `docs/methodology.md`
- `docs/implementation-guide.md`
- `docs/adoption-checklist.md`
- `docs/source-notes.md` if present

Changes:

- Replace or annotate public protocol phrase with `CRAWL/Check -> Reason -> Act -> Bus`.
- Add one "Why CRAWL?" section explaining that this is the expanded Step 1, not a fifth phase.
- Rename "Check" headings to "CRAWL / Check" in docs while preserving "Check" as compatibility terminology.
- Add the C/R/A/W/L table.
- Add profile-based examples so public users are not forced into HUMMBL-specific mesh checks.
- Mention Retrograde as an optional implementation extension until a separate protocol-version decision promotes it.

### Phase 2: Daemon Compatibility Layer

Target files:

- `crab_daemon.py`
- `tests/test_daemon.py`

Recommended v1.x approach:

- Keep `CheckResult` and `check_phase()` to avoid churn.
- Add docstrings that define them as the implementation object for the CRAWL phase.
- Update rendered summary text from `CHECK` to `CRAWL` for human-facing output.

Avoid a broad rename in the first pass. Renaming `CheckResult` to `CrawlResult` is a v2 cleanup, not necessary for behavior.

### Phase 3: Deferred CRAWL Profile Config

Do not publish new config keys until parser compatibility and tests exist. Current `DaemonConfig.from_json()` passes unknown top-level keys into the dataclass constructor, so a copied example containing `crawl_profile` or `crawl` would fail before the schema lands.

When ready, add config without forcing all probes:

```json
{
  "crawl_profile": "git-only",
  "crawl": {
    "include_status": true,
    "include_bus_status": false,
    "include_agent_processes": false,
    "include_mesh": false,
    "include_limits": true
  }
}
```

This block is pseudocode only. Do not copy it into `crab-daemon/config.json` until parser support and tests exist.

Profiles:

- `git-only`
- `coordinated-repo`
- `mesh`
- `custom`

Required implementation work before documenting this as usable config:

- Add dataclass fields or a nested config object.
- Update `from_json()` and `to_json()`.
- Decide whether unknown keys should be tolerated or rejected with a clearer error.
- Add config serialization/deserialization tests.

### Phase 4: Version and Governance Boundary

Before any public adoption beyond this proposal:

- Add a v1.1 release note or changelog entry that states CRAWL/Check is a terminology and documentation update, not an API rename.
- Keep `CheckResult` and `check_phase()` stable.
- State that CRAB v1.1 remains a four-step public protocol while the reference daemon's Retrograde behavior is an implementation extension.
- Require explicit operator/steward approval before changing founder-mode or host-specific operating guardrails.
- Keep HUMMBL mesh commands out of core OSS docs; put them in source notes or founder-mode-specific guidance.

### Phase 5: Bus Receipt Shape

Bus receipts should optionally expose CRAWL evidence in compressed form:

```text
[lane] OK - action summary | crawl=branch:main dirty:false stash:0 bus:ok agents:2 limits:none
```

For founder-mode bridge posts:

```text
CRAWL branch=<branch> dirty=<n> stash=<n> wire=<ok|degraded> agents=<summary> limits=<summary>
```

Do not dump long process lists into the bus. CRAWL should preserve signal, not create telemetry noise.

---

## Acceptance Criteria

Documentation:

- Public docs consistently define CRAB as `CRAWL/Check -> Reason -> Act -> Bus` for v1.1.
- The first phase is explicitly "CRAWL / Check", with CRAWL documented as the expanded human-facing semantics.
- The C/R/A/W/L table appears in methodology and adoption guidance.
- Examples distinguish git-only, coordinated-repo, and mesh profiles.
- Public docs mention Retrograde as optional implementation behavior, not silently absent protocol reality.
- Public docs distinguish public protocol requirement from reference-daemon default Retrograde behavior.
- A v1.1 release note or status marker states whether CRAWL/Check is draft, stable, or pending release.

Daemon:

- Existing tests still pass.
- Human-facing summary uses `CRAWL` or `CRAWL/CHECK` during the transition.
- `check_phase()` remains backward-compatible.
- No new runtime dependency is introduced.
- No public config example uses `crawl_profile` or `crawl` until parser support and tests land.

HUMMBL/founder-mode:

- The host-specific CRAB rule can be updated to say "CRAWL" while preserving current bus-global commands.
- CRAWL does not weaken the host-specific local-only bus exception.
- Mesh CRAWL includes canonical bus status and avoids local shadow bus writes.
- Limits explicitly include a `bus-required` vs. `local-only-eligible` determination using the host-specific exception's five conditions.
- Founder-mode/host-specific guardrail edits require explicit operator/steward approval and must not be bundled into the OSS docs-only pass.

---

## Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Acronym confusion: "CRAB CRAWL" sounds like a new protocol | Medium | State repeatedly: CRAB remains the protocol; CRAWL is Step 1. |
| Over-probing slows every turn | Medium | Use profiles and proportionality. Mesh probes only when mesh state matters. |
| Public OSS docs become too HUMMBL-specific | High | Keep HUMMBL commands in examples or source notes, not the core method. |
| Code churn from renaming `CheckResult` | Medium | Do not rename internals in v1.x. Add compatibility docstrings first. |
| Bus receipts become noisy | Medium | Summarize CRAWL evidence, link/path detailed artifacts only when needed. |
| Retrograde docs/code drift gets worse | Medium | Fold CRAWL doc update into a broader doc alignment pass acknowledging Retrograde state. |
| Config examples crash adopters | High | Defer `crawl_profile` documentation until schema support and tests land. |

---

## Recommended Decision

Adopt CRAWL as the canonical expansion of Step 1 for a docs-only v1.1 draft.

Do it as a documentation-first v1.1 protocol enhancement:

1. Update public CRAB docs.
2. Update human-facing daemon strings.
3. Keep `CheckResult` and `check_phase()` stable internally.
4. Defer profile-based CRAWL configuration until parser support and tests exist.
5. Separately reconcile Retrograde docs/code drift so the protocol surface is coherent.
6. Add release/status wording before treating CRAWL/Check as stable public v1.1.
7. Include this proposal in the repo as a draft process artifact under `docs/proposals/` so reviewers can inspect the full decision trail.

This gives CRAB a first phase that matches the actual operational burden of multi-agent systems without destabilizing the implementation.

---

## Peer Review Notes

Peer review by `Singer` on 2026-05-13 required these revisions before adoption:

- Treat CRAWL as the expanded human-facing name for Check, not an immediate breaking protocol/API rename.
- Defer `crawl_profile` config until schema support and tests exist.
- Acknowledge current Retrograde implementation rather than publishing a misleading four-phase-only protocol surface.
- Remove stale `missing to` bus-gap evidence because current TSV writes include `to=all`.
- Parameterize HUMMBL mesh work surface instead of hardcoding founder-mode for every mesh use.
- Add bus-required vs. local-only-eligible as an explicit Limits check.
- Red/blue/purple review later blocked adoption as written until Retrograde default behavior, git-only boundaries, founder-mode guardrail approval, v1.1 release boundary, config pseudocode, and Wire/Agents permission limits were clarified; this revision incorporates those gates.
