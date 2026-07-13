# Security Scan Receipt — v1.0.0

**Date:** 2026-07-13
**Scanner:** Gitleaks 8.x
**Scope:** Full working tree (68 files, ~906 KB)
**Result:** 0 findings

## Patterns scanned

- API keys (AWS, GitHub, Google, Slack, Stripe, etc.)
- Generic high-entropy secrets
- Private keys (RSA, EC, OpenSSH)
- Tokens (JWT, OAuth, Bearer)
- Passwords in config files
- Database connection strings

## Manual verification scans

| Category | Pattern class | Matches |
|----------|--------------|---------|
| Windows paths | All 3 forms (backslash, forward-slash, MSYS) + Unix home paths | 0 |
| Internal hostnames | 3 specific internal hostnames (case-insensitive) | 0 |
| VPN/tailnet | VPN product name + tailnet identifier | 0 |
| Personal names | Operator + collaborator names (case-insensitive) | 0 |
| Personal emails | Personal email prefix | 0 |
| GitHub usernames | Personal GitHub username (case-insensitive) | 0 |
| Port numbers | 3 specific internal service ports | 0 |
| IP addresses | IPv4 dotted-quad pattern | 0 |
| Visibility | `visibility.*private` (case-insensitive) | 0 |

## Gitleaks report

See `gitleaks-v1.0.0.json` (empty array = no findings).

## Notes

- This is a fresh repository with no inherited git history, issues, PRs, or Actions artifacts.
- The private incubator repo (`hummbl-dev/crab-incubator`) retains the full development history.
- All paths in code are configured via environment variables (`FM_REPO`, `BUS_GLOBAL_SCRIPT`).
- No hardcoded infrastructure references remain.
