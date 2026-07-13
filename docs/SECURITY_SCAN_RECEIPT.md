# Security Scan Receipt — v1.0.1

**Date:** 2026-07-13
**Scanner:** Gitleaks 8.30.1
**Command:** `gitleaks detect --source . --no-git --report-format json --report-path docs/gitleaks-v1.0.1.json`
**Scope:** Full working tree, 70 tracked files, ~909 KB
**Scan base:** v1.0.0 (`6138eda`) — the initial public release commit
**Patch:** v1.0.1 post-release governance patch (CODEOWNERS, AUDIT.md, this receipt)
**Result:** 0 findings

## Patterns scanned (Gitleaks built-in rules)

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
| Visibility | Non-public visibility declarations in governance YAML | 0 |

## Gitleaks report

- File: `docs/gitleaks-v1.0.1.json`
- Content: `[]` (empty array = no findings)
- Checksum (SHA-256): `37517E5F3DC66819F61F5A7BB8ACE1921282415F10551D2DEFA5C3EB0985B570`

## Notes

- This is a fresh repository with no inherited git history, issues, PRs, or Actions artifacts.
- The private incubator repo (`hummbl-dev/crab-incubator`) retains the full development history.
- All paths in code are configured via environment variables (`FM_REPO`, `BUS_GLOBAL_SCRIPT`).
- No hardcoded infrastructure references remain.
- v1.0.0 tag preserved at commit `6138eda` (initial public release).
- v1.0.1 is a post-release governance patch (CODEOWNERS fix, AUDIT.md historical language, scan receipt refresh). No code changes.
