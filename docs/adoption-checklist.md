# Adoption Checklist

Use this checklist when introducing CRAB to a repo, team, or agent fleet.

## Baseline

- [ ] Name the canonical work surface.
- [ ] Name the canonical coordination surface.
- [ ] Define valid worker identities.
- [ ] Define valid message types.
- [ ] Define restricted message types.
- [ ] Define protected surfaces.
- [ ] Define who has approval and merge authority.

## Check

- [ ] Document the branch/status command.
- [ ] Document the dirty-worktree command.
- [ ] Document the stash or lock command.
- [ ] Document the bus-tail command.
- [ ] Document stop conditions.

## Reason

- [ ] Require workers to reconcile requester instruction with bus state.
- [ ] Require explicit distinction between verified facts and assumptions.
- [ ] Require authority checks before protected or consequential work.

## Act

- [ ] Require scoped edits.
- [ ] Require verification proportional to risk.
- [ ] Require immediate blocker publication when work cannot proceed safely.

## Bus

- [ ] Require a bus receipt before final closeout.
- [ ] Require message body to include artifact path, PR, commit, or next gate.
- [ ] Require canonical sender identity.
- [ ] Forbid local shadow writes when a canonical bus exists.

## Review

- [ ] Add CRAB to onboarding docs.
- [ ] Add CRAB to PR or handoff templates where useful.
- [ ] Run one AAR after the first real incident or missed check.
- [ ] Promote durable lessons back into the local implementation guide.

