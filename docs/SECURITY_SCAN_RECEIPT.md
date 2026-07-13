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

| Category | Pattern | Matches |
|----------|---------|---------|
| Windows paths | `C:\Users`, `C:/Users`, `/c/Users`, `/Users/`, `/home/` | 0 |
| Internal hostnames | `Anvil`, `nodezero`, `Huxley` (case-insensitive) | 0 |
| VPN/tailnet | `Tailscale`, `tailscale`, `tail0ff7b3` | 0 |
| Personal names | `Reuben`, `Bowlby`, `Dan` (case-insensitive) | 0 |
| Personal emails | `reuben@` | 0 |
| GitHub usernames | `reubenbowlby` (case-insensitive) | 0 |
| Port numbers | `18790`, `11434`, `8081` | 0 |
| IP addresses | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | 0 |
| Visibility | `visibility.*private` (case-insensitive) | 0 |

## Gitleaks report

See `gitleaks-v1.0.0.json` (empty array = no findings).

## Notes

- This is a fresh repository with no inherited git history, issues, PRs, or Actions artifacts.
- The private incubator repo (`hummbl-dev/crab-incubator`) retains the full development history.
- All paths in code are configured via environment variables (`FM_REPO`, `BUS_GLOBAL_SCRIPT`).
- No hardcoded infrastructure references remain.
