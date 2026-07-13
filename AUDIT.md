# Red Team Audit | CRAB Daemon (Portable)
**Date**: 2026-05-10
**Target**: `crab_daemon.py` (portable reference implementation)
**Classification**: Historical — pre-release security review (public release completed 2026-07-13)

**Scope caveat:** This audit was daemon-scoped and performed before the repo-wide public/private split audit (2026-07-13). Both audits are now complete. The repository was exported to a fresh public repo (`hummbl-dev/crab`) with no inherited history, issues, or PRs. All findings below are historical; current disposition is recorded per finding.

---

## Attack Surface

| Surface | Count | Notes |
|---------|-------|-------|
| Subprocess invocations | 1 (`subprocess.run`) | Used for git commands, curl probes, find |
| Bus writers | 4 backends | TSV append, JSONL append, stdout, callback shell |
| File reads | 2 | Bus tail, git status |
| File writes | 4 | Bus append (all backends), config JSON |
| Config inputs | 1 | JSON config file |

---

## Category D — Data Exfiltration

| # | Probe | Expected | Result |
|---|-------|----------|--------|
| D1 | Scan for secrets in source | No API keys, tokens, passwords | **PASS** — zero matches for common API-key, cloud-key, token, and password patterns |
| D2 | Scan for personal/operational details | No real names, emails, hostnames, IPs | **PASS** — zero matches for known internal org, host, tailnet, and personal-identity markers |
| D3 | Check for hardcoded paths that leak structure | No repo-specific paths | **PASS** — all paths are relative (`crab-daemon/`, `bus/`, `.`) or configurable |
| D4 | Check for env-controlled critical paths | No `os.environ.get` for paths | **PASS** — no env lookups in the module |

## Category E — Identity & Provenance

| # | Probe | Expected | Result |
|---|-------|----------|--------|
| E1 | Hardcoded identity borrowing | No `BUS_SENDER` or borrowed identity | **PASS** — identity comes from config JSON or `--identity` CLI flag |
| E2 | Default identity is generic | Default is `crab-daemon`, not a person or org | **PASS** |
| E3 | Bus posts distinguishable from human posts | TSV format includes `from` column | **PASS** — every post includes the configured identity |

## Category F — Supply / Env

| # | Probe | Expected | Result |
|---|-------|----------|--------|
| F1 | Env vars control critical paths | No env-controlled paths | **PASS** — all paths from config or defaults |
| F2 | Subprocess uses shell=True or env-injectable wrapper | `subprocess.run` with `shell=False` (implicit) and list args | **PASS** — all calls use `list[str]` args, no `shell=True` |
| F3 | Iterates untrusted directories with privileged ops | No directory iteration for privileged ops | **PASS** — `find` is scoped to `.git` only; no broad iteration |

## Static Analysis

| Tool | Result |
|------|--------|
| Bandit | Not available on this host (LibreOffice python conflict). Recommended to run on a host with bandit installed. |
| Semgrep | Not available on this host. Recommended to run periodically. |
| Manual review | **CLEAN** — no `eval`, `exec`, `compile`, `pickle`, `yaml.load`, or other deserialization risks. |

## Findings

| Severity | Finding | Remediation |
|----------|---------|-------------|
| **LOW** | Callback backend uses `_run_shell(["sh", "-c", cb])` which invokes a shell | Document that callback backend is UNSAFE for untrusted config sources. Config file must be write-protected. |
| **LOW** | TSV backend appends to a file without file locking (unlike HUMMBL's `bus_writer` which uses `fcntl.flock`) | Document limitation: TSV backend is not safe for concurrent writers. Recommend JSONL or external locking for multi-process use. |
| **INFO** | No HMAC signing or verification of bus messages | Out of scope for reference implementation. HUMMBL's `bus_writer_signing` module handles this in production. |

## Overall Score

| Category | Score |
|----------|-------|
| D — Data Exfiltration | 4/4 PASS |
| E — Identity & Provenance | 3/3 PASS |
| F — Supply / Env | 3/3 PASS |
| **Overall** | **10/10 PASS** |

## Recommendations (historical — pre-release)

The following recommendations were made before public release. Current disposition recorded inline.

1. Run `bandit -r crab_daemon.py` and `semgrep --config auto` on a machine with these tools installed. **Status: addressed — static analysis completed; no HIGH/CRITICAL findings.**
2. Add a test that verifies no `os.environ.get` appears in future revisions. **Status: deferred — tracked as Medium finding #13 below.**
3. Add a CONTRIBUTING.md note: "Never commit real hostnames, IPs, or tokens". **Status: addressed — CONTRIBUTING.md includes security reporting guidance.**
4. Consider adding file locking to the TSV backend using `fcntl` / `msvcrt` (platform-specific). **Status: deferred — tracked as Medium finding #4 below. Documented as a known limitation.**
5. Run a repo-wide public/private split audit covering docs, bridge modules, examples, generated artifacts, and git history. **Status: addressed — completed 2026-07-13. Fresh public repo created with no inherited history.**

## Next action

Public release completed 2026-07-13. The two LOW findings are documentation/operational, not code defects. No further action required for the public release gate. Medium findings are tracked below with disposition.

---

## 2026-06-25 Cyber Deep Scan — Follow-up

A follow-up cyber deep scan identified 14 findings across the repository.
Summary:

### High (3) — Fixed in PR #17

1. **Hardcoded infrastructure paths in bridge module** — `bridge_crab_fm.py`
   contained hardcoded Windows paths to the founder-mode repo. Replaced with
   `FM_REPO` / `FM_BUS_PATH` environment variables with sensible defaults.
2. **Hardcoded global bus script path** — `bus/crab_bus.py` contained a
   hardcoded path to a bus-global script. Replaced with `BUS_GLOBAL_SCRIPT`
   env var; returns `False` when unset.
3. **Internal hostnames in docs** — Multiple docs referenced internal fleet
   hostnames and VPN/tailnet references. Replaced with generic
   terms ("a host", "bus authority host", "peer hosts", "VPN/tailnet").

### Medium (9) — Post-release disposition

4. TSV backend lacks file locking (documented; `flock`/`msvcrt` not yet added). **Disposition: accepted as known limitation. Documented in daemon docstring. Safe for single-process use; multi-process users should use JSONL or external locking.**
5. Callback backend uses `sh -c` (documented as unsafe for untrusted config). **Disposition: accepted as known limitation. Documented in callback backend docstring. Config file must be write-protected.**
6. No HMAC signing in portable daemon (deferred to `hummbl-governance`). **Disposition: deferred — signing lives in the `hummbl-governance` library for production use. Reference daemon intentionally omits it.**
7. No identity validation in portable daemon (deferred). **Disposition: deferred — identity validation is a governance primitive in `hummbl-governance`. Reference daemon accepts any identity from config.**
8. No concurrent-writer test for TSV backend. **Disposition: deferred — tracked for future test coverage improvement.**
9. No corruption-recovery test for bus files. **Disposition: deferred — tracked for future test coverage improvement.**
10. No config schema migration test. **Disposition: deferred — tracked for future test coverage improvement.**
11. Scuttlebutt layer is prototype-only with no concurrency safety. **Disposition: accepted — scuttlebutt is documented as prototype/experimental.**
12. Productization timeline estimates are 2–3× optimistic per technical review. **Disposition: accepted — estimates are advisory, not commitments.**

### Low (2) — Accepted

13. No `os.environ.get` guard test for future revisions. **Disposition: accepted — recommend adding in future test coverage expansion.**
14. No CONTRIBUTING.md note about committing hostnames/IPs/tokens. **Disposition: addressed — CONTRIBUTING.md includes security reporting guidance.**

**Post-release status:** Public release completed 2026-07-13. All High findings fixed. Medium findings accepted as documented limitations or deferred to `hummbl-governance`. Low findings accepted or addressed. No blocking issues remain.
