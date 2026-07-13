# Implementation Guide

CRAB is intentionally implementation-neutral. A team should bind it to local
commands, identities, and authority rules.

## 1. Define the Work Surface

For each repo or operation lane, document:

- Canonical repository or workspace path.
- Default branch and branch naming convention.
- Shared state surfaces: bus, issue tracker, PR comments, queue, ledger.
- Protected files or systems.
- Required peer-review gates.

## 2. Define the CRAWL / Check Command Set

For git-backed work with no shared coordination surface, a minimal CRAWL/Check
command set usually includes:

```bash
git branch --show-current
git status --short --branch
git stash list
```

Add the local bus read command for your environment.

If a shared coordination surface exists, the bus, issue tracker, PR thread, job
queue, or equivalent read is not optional. CRAWL must include the live source
that can reveal blockers, ownership, unresolved proposals, or recent handoffs.

For non-git work, replace these with the equivalent live-state checks:

- Deployment status.
- Job queue state.
- Lock ownership.
- Database migration state.
- Incident channel tail.
- CI or monitor state.

Keep CRAWL implementation-neutral. Mesh, SSH, VPN, host process, and disk
probes belong in local profiles only when those sources can change the next
safe action and the worker has authority to read them.

CRAWL sources should be documented with permission boundaries:

- Which sources are canonical.
- Which probes require credentials, SSH, or privileged access.
- Which probe failures are stop conditions.
- Which protected surfaces must not be inspected without approval.

## 3. Define Authority Boundaries

CRAB works only if workers know what they may and may not decide.

Document:

- Who can approve proposals.
- Who can merge.
- Who can delete branches.
- Who can post decisions.
- Which message types are restricted.
- Which actions require human approval.

## 4. Define Bus Semantics

The bus should be append-only or otherwise audit-preserving.

At minimum, each message should carry:

- Timestamp.
- Sender.
- Target or audience.
- Type.
- Message body.

Teams can add lane, host, model, repo, PR, commit, severity, or review metadata.

## 5. Define Closeout Rules

Every meaningful work item should end with:

- A bus receipt.
- A human-facing summary.
- Links or paths to changed artifacts.
- Verification performed.
- Remaining gates.

## 6. Automate Carefully

Automation can enforce CRAB, but should not fake it.

Useful automation:

- Pre-flight scripts that print branch/status/stash/bus tail.
- Commit hooks that reject protected-surface violations.
- PR templates that require bus receipt IDs.
- CI checks for forbidden message types or identity drift.

Risky automation:

- Auto-posting success without verifying the operation.
- Hiding dirty worktree state behind truncated output.
- Using local shadow buses that diverge from the canonical coordination surface.
