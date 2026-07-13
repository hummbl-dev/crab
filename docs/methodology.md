# CRAB Methodology

## Definition

CRAB is a four-step execution loop for coordinated work:

**CRAWL/Check -> Reason -> Act -> Bus**

It is designed for environments where multiple agents, humans, or automation
surfaces can modify shared state.

CRAWL expands the first phase ("Check") into five live-state probes that every
consequential turn should consider: **C**ontext (what the requester asked and
recent coordination state), **R**epo (branch/worktree/stash/PR/CI state),
**A**gents (who is active, blocked, or owns dirty work), **W**ire (is the
coordination substrate current), and **L**imits (stop conditions, protected
surfaces, credentials). `Check` remains the short-form implementation name;
`CRAWL` is the expanded human-facing label for the same phase.

## Goals

- Prevent stale-context execution.
- Reduce branch, stash, and worktree collisions.
- Make blockers visible before work proceeds.
- Leave a durable coordination trail.
- Preserve human authority while reducing human copy-paste burden.

## Non-Goals

- CRAB is not a replacement for review, tests, or CI.
- CRAB is not a generic project-management framework.
- CRAB does not define one universal bus implementation.
- CRAB does not grant authority to override local governance rules.

## Step 1: CRAWL / Check

Before acting, read the live state that can invalidate the requested work.

CRAWL is the expanded human-facing name for the Check phase:

| Letter | Meaning | Required question |
|---|---|---|
| C | Context | What did the requester ask, and what recent coordination state changes the prompt? |
| R | Repo | What repository, branch, worktree, stash, PR, or CI state can invalidate the work? |
| A | Agents | Which humans, agents, sessions, lanes, or daemons are active, blocked, or owners of dirty work? |
| W | Wire | Is the coordination substrate current: bus, issue tracker, PR comments, queue, or other shared surface? |
| L | Limits | What stop conditions, approvals, protected surfaces, credentials, or irreversible actions constrain the next step? |

Minimum checks for a git-backed coordination surface:

- Current repository or workspace.
- Current branch.
- Dirty worktree state.
- Stash state.
- Recent coordination messages.
- Open blockers or unresolved proposals in scope.

The CRAWL/Check step must use live sources, not inherited summaries, when the state is
cheap to verify.

If there is no shared coordination surface, a git-only CRAWL may stop at repo
and limit checks. If a bus, issue queue, PR thread, deployment channel, or other
shared surface exists, recent coordination state is part of the minimum check.

## Step 2: Reason

Integrate:

- The requester instruction.
- The live state from CRAWL/Check.
- Local guardrails and authority boundaries.
- Known stop conditions.
- The message type that will be posted after Act.

Reasoning does not need to be verbose or externally posted by default. The
purpose is to prevent blind execution.

## Step 3: Act

Do the requested work on the verified surface.

During Act:

- Keep changes scoped to the lane.
- Stop if the checked assumptions become false.
- Verify edits or runtime behavior at a level proportional to risk.
- If work becomes blocked, post the blocker instead of improvising around it.

## Step 4: Bus

Before final closeout, publish a coordination receipt to the shared surface.

A bus receipt should include:

- Who acted.
- What changed or what was observed.
- Where it happened.
- Current state or next gate.
- Any blocker, risk, or review request.

The bus can be a TSV log, issue comment, chat channel, event stream, database
table, or other append-only coordination surface. The important property is that
the next worker can read it before acting.

## Stop Conditions

Stop and publish a blocker when:

- A live blocker affects the task scope.
- A cross-branch or shared-state operation would collide with dirty or stashed work.
- Required authority is missing.
- The requested action would modify a protected surface.
- Verification fails and there is no safe recovery path.
- The worker cannot distinguish current state from stale inherited state.

## Quality Bar

Good CRAB execution is:

- **Current**: based on live state.
- **Scoped**: limited to the requested work surface.
- **Auditable**: leaves a receipt another worker can use.
- **Honest**: distinguishes verified facts from assumptions.
- **Timely**: posts the receipt before final response or handoff.

## Operational Notes

### Preserving unrelated dirty work

If CRAWL/Check discovers dirty worktree state, stashes, or in-progress work
that is unrelated to the current lane, the worker must not touch it. Stash,
branch, or worktree state belonging to another agent or session should be
preserved as-is. Post a `BLOCKED` message if the unrelated dirty state
prevents safe progress.

### Shadow bus prohibition

When a canonical coordination bus exists, workers must post receipts to that
bus — not to a local shadow copy that diverges from the canonical surface.
Local-only bus writes are permitted only when no shared coordination surface
exists and the host-specific local-only exception conditions are met.

### WIP_START / WIP_END pairing

`WIP_START` and `WIP_END` messages must be paired. A worker that posts
`WIP_START` to claim a lane is responsible for posting `WIP_END` when it
releases that lane — whether the work completed successfully, was blocked,
or was abandoned. Unpaired `WIP_START` messages create stale ownership that
blocks other workers. If a worker crashes or loses context, the next CRAWL
should detect the orphaned `WIP_START` and post a corrective `WIP_END`.
