# Source Notes

This repository formalizes CRAB as a portable methodology.

The initial extraction comes from HUMMBL's founder-mode operating practice,
where CRAB is used as a mandatory turn loop for multi-agent work.

Originating implementation references:

- `founder_mode/playbooks/CRAB.md`
- `.claude/rules/crab-protocol.md`
- `founder_mode/docs/operations/DOC_LAYER_CONVENTION.md`

Those source files include host-specific and repo-specific details. This repo
keeps the method portable and leaves machine paths, bus wrappers, agent rosters,
and local authority rules to each adopting project.

## Naming

CRAB expands to:

**CRAWL/Check -> Reason -> Act -> Bus**

`Check` is the original implementation term. `CRAWL` is the expanded
human-facing name for the same first phase: Context, Repo, Agents, Wire, and
Limits.

Earlier internal language described a related multi-session synchronization
workflow. CRAB is the agent-neutral form intended for broader reuse.
