# Release Notes

## v1.1 draft: CRAWL/Check terminology

Status: draft, not released.

Packaging note: `pyproject.toml` remains pre-1.0 for package metadata in this hygiene pass. Historical git tags and draft protocol labels do not by themselves authorize a public release or package version bump.

This draft keeps CRAB as a four-step public protocol:

```text
CRAWL/Check -> Reason -> Act -> Bus
```

`Check` remains the implementation-compatible name used by existing code,
tests, and older integrations. `CRAWL` is the expanded human-facing meaning of
that first phase: Context, Repo, Agents, Wire, and Limits.

This draft does not rename `CheckResult`, `check_phase()`, or any public daemon
API. It does not add `crawl_profile` or any other config key.

The reference daemon includes Retrograde validation behavior, but Retrograde is
not promoted to a required public protocol phase in this draft. Any future
five-phase public protocol requires a separate release decision.

Founder-mode or host-specific guardrail changes are out of scope for this CRAB repo
draft and require explicit operator/steward approval.
