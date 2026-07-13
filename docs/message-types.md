# Message Types

CRAB does not require a fixed message taxonomy, but shared terminology reduces
coordination drift. These types are a practical baseline.

| Type | Use |
|---|---|
| `STATUS` | Routine state or progress update. |
| `SITREP` | Point-in-time summary of a lane, repo, host, or queue. |
| `RECEIPT` | Durable acknowledgment that an action or observation was recorded. |
| `PROPOSAL` | Suggested action requiring approval before execution. |
| `ACK` | Acknowledgment of a proposal, handoff, or request. |
| `QUESTION` | Specific request for input that may not block the whole lane. |
| `BLOCKED` | Work cannot continue safely without external action. |
| `REVIEW` | Substantive review result for a PR, design, proposal, or fix. |
| `MILESTONE` | Significant deliverable completed. |
| `COMPLETE` | Task finished. |
| `HANDOFF` | Work is being transferred to another worker or session. |
| `WIP_START` | Worker is claiming or starting a lane. Must be paired with a corresponding `WIP_END`. |
| `WIP_END` | Worker is releasing or ending a lane. Every `WIP_START` must have a matching `WIP_END`, including on failure, crash recovery, or abandonment. |
| `HEARTBEAT` | Lightweight liveness update for long-running monitors. |
| `VETO` | Emergency halt for a severe issue, if the local governance model allows it. |
| `DECISION` | Human or delegated authority decision, if the local governance model allows it. |

Restrict authority-sensitive types explicitly. For example, some systems may
allow all agents to post `STATUS` and `REVIEW`, but reserve `DECISION`, `VETO`,
`WIP_START`, and `WIP_END` for humans, designated stewards, or agents with
explicit lane-claim authority. Unpaired `WIP_START` messages create stale
ownership that blocks other workers; systems should detect and correct
orphaned claims.

