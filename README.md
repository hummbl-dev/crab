# CRAB

CRAB is a lightweight operating methodology for multi-agent work:

**Check -> Reason -> Act -> Bus**

It exists to keep autonomous or semi-autonomous workers synchronized when more
than one session, host, model, or human can touch the same work surface.

CRAB is not a chat ritual. It is a coordination contract:

1. **Check** the live state before acting.
2. **Reason** against the current state, instructions, and stop conditions.
3. **Act** only after the work surface is understood.
4. **Bus** the result before closing the loop with the requester.

## Why It Exists

Multi-agent systems fail when agents inherit stale state, act on the wrong
branch, miss another worker's blocker, or rely on a human to relay context
between sessions. CRAB makes the state check and the coordination receipt part
of every meaningful turn.

## Repository Contents

- [Methodology](docs/methodology.md) - the canonical CRAB method.
- [Implementation Guide](docs/implementation-guide.md) - how to adapt CRAB to a repo, team, or agent fleet.
- [Adoption Checklist](docs/adoption-checklist.md) - practical rollout checklist.
- [Message Types](docs/message-types.md) - common bus message taxonomy.
- [Source Notes](docs/source-notes.md) - origin and relation to HUMMBL founder-mode.

## Status

Initial extraction from HUMMBL's founder-mode operating practice. This repo is
the portable methodology home; project-specific rules should keep their local
host paths, command wrappers, identities, and guardrails in their own repos.

