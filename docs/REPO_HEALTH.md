# CRAB Repository Health

## Identity

- **Repository**: `hummbl-dev/crab`
- **Canonical host**: `https://github.com/hummbl-dev/crab`
- **Gitea mirror**: `https://<GITEA_HOST>/hummbl-dev/crab`
- **Visibility**: Private/incubator upstream; Gitea mirror is local-only.
- **Default branch**: `main`
- **Owner**: HUMMBL

## Lifecycle

- **Status**: Active private coordination protocol repo
- **Purpose**: Standardize agent workflow observability through bus receipts and protocol traces.

## Canonical Relationship

- Source-of-truth for CRAB runtime and protocol docs is GitHub (`hummbl-dev/crab`).
- Gitea (`hummbl-dev/crab`) is a pull mirror for local-only visibility and continuity.
- Do not open Gitea-only PRs for CRAB runtime or protocol docs while the repo is configured as a mirror.

## Validation Contract

From repository root:

```bash
python -m pytest tests/ -v
```

Recommended pre-submit:

- `python -m pytest tests/ -q`
- If runtime cannot resolve external bus backends, run `python -m pytest tests/ -q -k "not TestBusBridge"`.

## Branch Protection Expectation

- Keep `main` PR-driven for runtime and protocol changes.
- Require at least one review and green `python -m pytest tests -q` for non-trivial lane updates.
- Verify Gitea mirror integrity after GitHub merges with `git ls-remote` or the org mirror-health checker.
