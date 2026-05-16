# Red Team Audit | CRAB Daemon (Portable)
**Date**: 2026-05-10
**Target**: `crab_daemon.py` (portable reference implementation)
**Classification**: INTERNAL — pre-commit security review

**Scope caveat:** This audit is daemon-scoped. It is not a repo-wide public-release audit. The repository also contains HUMMBL-internal bridge, roadmap, productization, and research artifacts that require a separate public/private split review before any external release.

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
| Bandit | Not available on this host (LibreOffice python conflict). Recommend running on Huxley/nodezero before public release. |
| Semgrep | Not available on this host. Recommend running before public release. |
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

## Recommendations before public release

1. Run `bandit -r crab_daemon.py` and `semgrep --config auto` on a machine with these tools installed.
2. Add a test that verifies no `os.environ.get` appears in future revisions.
3. Add a CONTRIBUTING.md note: "Never commit real hostnames, IPs, or tokens".
4. Consider adding file locking to the TSV backend using `fcntl` / `msvcrt` (platform-specific).
5. Run a repo-wide public/private split audit covering docs, bridge modules, examples, generated artifacts, and git history.

## Next action

The portable daemon is **clean for commit to the private repo**. The two LOW findings are documentation/operational, not code defects. Run formal bandit/semgrep and a repo-wide public/private split audit before any public release.
