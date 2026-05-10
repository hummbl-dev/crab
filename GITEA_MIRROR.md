# Gitea Mirror Setup for `hummbl-dev/crab`

## Current State

| Repo | GitHub | Gitea |
|------|--------|-------|
| `hummbl-dev/founder-mode` | PRIVATE | Not verified (AGENTS.md claims mirror every 8h) |
| `hummbl-dev/crab` | PRIVATE | **Does not exist** |

## Recommendation

Set up Gitea as a **pull mirror** of the GitHub private repo. This gives you:
- Local backup on Anvil (your hardware, your data)
- Fallback git server if GitHub is unreachable
- Fast local clones for Anvil-only work

## Setup Steps

### 1. Create the repo on Gitea

```bash
# Via Gitea API (requires GITEA_TOKEN)
curl -X POST "https://<GITEA_HOST>/api/v1/user/repos" \
  -H "Content-Type: application/json" \
  -H "Authorization: token $GITEA_TOKEN" \
  -d '{
    "name": "crab",
    "private": true,
    "description": "CRAB protocol — mirror of hummbl-dev/crab",
    "mirror": true
  }'
```

### 2. Configure the mirror

```bash
# Set the GitHub repo as the remote to mirror from
curl -X PATCH "https://<GITEA_HOST>/api/v1/repos/hummbl/crab" \
  -H "Content-Type: application/json" \
  -H "Authorization: token $GITEA_TOKEN" \
  -d '{
    "mirror": true,
    "clone_addr": "https://github.com/hummbl-dev/crab.git",
    "repo_name": "crab",
    "private": true
  }'
```

### 3. Add GitHub credentials for private repo access

Gitea needs a GitHub PAT with `repo` scope to pull from a private repo:

```bash
# In Gitea web UI: Site Administration → Authentication Sources
# Or via API:
curl -X POST "https://<GITEA_HOST>/api/v1/user/repos" \
  -H "Authorization: token $GITEA_TOKEN" \
  -d '{
    "service": "github",
    "auth_token": "$GITHUB_PAT"
  }'
```

### 4. Windows Task Scheduler job for manual sync fallback

If Gitea's built-in mirror sync is unreliable, add a scheduled task:

```powershell
# As Administrator
schtasks /Create /TN "GiteaMirror-Crab" /TR "powershell -Command curl -s -H 'Authorization: token TOKEN' 'https://<GITEA_HOST>/api/v1/repos/hummbl/crab/mirror-sync'" /SC HOURLY /ST 00:00
```

## Policy Note

Your current AGENTS.md states:
> "Solo HUMMBL repos on Gitea; `hummbl-dev/founder-mode` stays on GitHub, mirrors to Gitea every 8h"

The `crab` repo fits the "Solo HUMMBL repos on Gitea" category since it is a HUMMBL project. However, since it's intended for eventual public release, keeping the canonical on GitHub (with Gitea as mirror) is the right architecture.

## Action Required

- [ ] Create Gitea repo via API or web UI
- [ ] Configure mirror with GitHub PAT
- [ ] Test sync: push to GitHub, verify Gitea reflects the commit within minutes
- [ ] Document in this repo's README: "Gitea mirror: `https://<GITEA_HOST>/hummbl/crab`"
