# CRAB Methodology

## Definition

CRAB is a four-step execution loop for coordinated work:

**Check -> Reason -> Act -> Bus**

It is designed for environments where multiple agents, humans, or automation
surfaces can modify shared state.

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

## Step 1: Check

Before acting, read the live state that can invalidate the requested work.

Minimum checks for a git-backed coordination surface:

- Current repository or workspace.
- Current branch.
- Dirty worktree state.
- Stash state.
- Recent coordination messages.
- Open blockers or unresolved proposals in scope.

The Check step must use live sources, not inherited summaries, when the state is
cheap to verify.

## Step 2: Reason

Integrate:

- The requester instruction.
- The live state from Check.
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

