# CLAUDE.local.md — Project Imports + Machine-Specific Overrides (gitignored)

> This file is **per-device** and gitignored. It does two things:
> 1. **Loads project doctrine** via `@import` (repo-relative paths — see below)
> 2. **Documents env vars, machine paths, and setup steps** for this device
>
> Recreate on each device. The `@import` block uses repo-relative paths, so
> the same content works on any device that has the repo cloned.
>
> This TSOT copy is a seed. The setup script copies it into the repo as a real
> `CLAUDE.local.md`; replace any machine-specific values if the device differs.

---

## Project Doctrine + Always-On Rules (loaded every session)

These imports use **repo-relative paths**, which resolve relative to this
file's location (the repo root). They work on any device with the repo
cloned, regardless of the absolute path.

@AGENTS.md
@.claude/rules/bricks-standard-guide.md
@.claude/rules/bricks-mcp-absolute.md
@.claude/rules/content-planning.md
@.claude/rules/browser-preview.md
@.claude/rules/malay-skill-sync.md
@.windsurf/rules/verification-protocol.md
@.windsurf/rules/self-improvement-loader.md
@.windsurf/rules/change-summary-rule.md
@.windsurf/rules/context7-default.md

> **Why imports live here, not in `CLAUDE.md`:** Claude Code's `@import`
> parser breaks on spaces in absolute paths (e.g. `G:/Zamzam Biznez/...`),
> and relative paths in the symlinked `CLAUDE.md` resolve relative to the
> TSOT, not the repo. This file is a real file in the repo root, so
> repo-relative paths resolve correctly.

---

## First Session — Approval Dialog

When you start Claude Code in this repo for the first time, you'll see a
**one-time approval dialog** listing external files that `CLAUDE.md` imports
(the TSOT lessons files via `~/.codeium/windsurf/...`).

**Approve it.** This flips `hasClaudeMdExternalIncludesApproved` to `true` in
`~/.claude.json` and the imports load silently every session after.

If you decline by accident, run:
```powershell
$projectPath = (Get-Location).Path -replace '\\','/'
$env:CLAUDE_PROJECT_PATH = $projectPath
python -c "import json, os; p=os.path.expanduser('~/.claude.json'); d=json.load(open(p,'r',encoding='utf-8')); project=os.environ['CLAUDE_PROJECT_PATH']; d.setdefault('projects',{}).setdefault(project,{})['hasClaudeMdExternalIncludesApproved']=True; json.dump(d,open(p,'w',encoding='utf-8'),indent=2,ensure_ascii=False)"
Remove-Item Env:CLAUDE_PROJECT_PATH
```

---

## MCP Servers — Connectors UI Only (no per-project config)

Claude Code's **Connectors UI** (Settings → Connectors) is the canonical place
to install MCP servers. Connectors are installed at the user level, so they
apply to **every project** automatically — no per-project `mcpServers` block
in `~/.claude.json` is needed.

### 🚨 `claude mcp list` LIES about OAuth'd Web connectors (learned 2026-08-01)

**Do not diagnose a connector as broken from `claude mcp list` output.** That
command health-checks remote connectors by probing their raw URL **without the
OAuth token**, so a perfectly working authenticated connector reports a failure.

Observed 2026-08-01 for Screpy:

| Probe | Result | Reality |
|---|---|---|
| `claude mcp list` | `✘ Failed to connect — HTTP 405` | misleading |
| `curl -X POST https://mcp.screpy.com` | `401` | misleading (no token) |
| **Actual tool call** (`list_projects`) | ✅ `digitrustlab.com`, owner, 3 crawls | **truth** |

A `401` on a well-formed request means "no credential on *this* probe" — not
"the connector is unauthenticated." The Connectors UI holds the token; `curl`
and the CLI health check do not.

**The only reliable test is calling one of the connector's tools.** Web
connectors surface under a UUID namespace (`mcp__<uuid>__*`), which is normal —
see the Context7 note further down. If you can't find the tools, use ToolSearch
with the connector's subject matter before concluding anything is wrong.

Cost of ignoring this: on 2026-08-01 Screpy was reported broken and "needs OAuth
setup" for an entire session, and was queued for a pointless re-auth, while it
had been working the whole time.

### Installed Connectors (verify in Settings → Connectors)

| Connector | Type | Auth | Status | Purpose |
|-----------|------|------|--------|---------|
| `fetch` | Desktop (local, `mcp-fetch-server`) | None | ✅ Connected | Web page fetching |
| `Context7` | Web (Anthropic-hosted remote) | None | ✅ Connected | Up-to-date library docs |
| `Respira for WordPress` | Desktop | OAuth / API key (set in connector) | ✅ Connected | WordPress + Bricks editing |
| `Screpy` | Web (custom remote) | OAuth (browser sign-in) | ✅ Connected | SEO monitoring |

> **`fetch` is NOT built-in/hosted — it is a local Desktop extension with no
> Web equivalent.** It only works in Claude Desktop and Claude Code (not on
> web/mobile/Cowork). Do NOT remove its entry from `claude_desktop_config.json`
> (see below) — doing so disables it entirely, since there is no remote
> fallback.

> **Screpy update (2026-07-29):** Screpy is now connected via Connectors UI.
> It authenticated automatically — no manual OAuth browser sign-in was needed.
> If it disconnects after a Claude Code update, re-add it via Settings →
> Connectors → Add custom remote MCP connector → URL: `https://mcp.screpy.com`.

### Respira MCP server version

> ⚠️ **Corrected 2026-07-30 — the previous note here was wrong.** It claimed
> `npm i -g @respira/wordpress-mcp-server@latest` plus an npx-cache clear would
> make the connector pick up 8.0.2. **It does not, and cannot.** The connector is
> a self-contained `.mcpb` extension that bundles its own copy of the server and
> never consults the global install or npx. The global 8.0.2 has been sitting
> unused; the connector has been running **7.1.2** the whole time.

**Verified state (2026-07-30):**

| Component | Version | Actually used? | Location |
|-----------|---------|----------------|----------|
| WordPress plugin | Updated 2026-07-29 | ✅ yes | WP Admin → Plugins (`digitrustlab.com`) |
| **`.mcpb` extension (the live one)** | wrapper **7.1.3** / server **7.1.2** | ✅ **this is what runs** | `%APPDATA%\Claude\Claude Extensions\local.mcpb.mihai-dragomirescu.respira-wordpress\` |
| Global npm install | ~~8.0.2~~ **removed 2026-07-30** | ❌ never loaded | was `%APPDATA%\npm` |
| npx cache | (empty) | ❌ not used | `%LOCALAPPDATA%\npm-cache\_npx` |
| Latest on registry | 8.1.4 *(2026-08-01)* | — | npm — moves independently, irrelevant to the connector |

**Why the global install is inert:** the extension manifest declares its entry as
`node ${__dirname}/server/index.js`, and `server/node_modules/` contains its own
`@respira/wordpress-mcp-server@7.1.2`. There is no `npx` call and no reference to
the global path anywhere in the server entry point. It is fully self-contained by
design.

**The only real upgrade path:** replace the extension itself — download a newer
`.mcpb` from Respira and install it through Claude Desktop (Settings →
Extensions), or check for an in-app update there. `npm -g` is not an upgrade path
and running it again will not help.

**Do NOT** hand-edit files inside the extension's `node_modules` to force a
version. The wrapper (7.1.3) is pinned to that server build, and any extension
update would silently overwrite the edit.

**Do NOT reinstall globally.** The stale global 8.0.2 was removed on 2026-07-30
(`npm rm -g @respira/wordpress-mcp-server`, 140 packages) precisely because its
presence made this file's old note look correct and hid the fact that the
connector runs 7.1.2. Connector verified working immediately after removal. If a
future session sees a version mismatch, the answer is the `.mcpb` extension —
never `npm -g`.

### ⚠️ THREE separate Respira version lines — do not conflate them

This caused a wasted upgrade attempt on 2026-07-30. They move independently:

There are **four**. Bundle re-checked **2026-08-01**; the rest measured 2026-07-30:

| Version line | Current | Where you see it | Relevance |
|---|---|---|---|
| **Platform (marketing)** | 8.1.8 | footer stats block on respira.press | site-wide counter, ticks often — **not a software version you can install** |
| **WordPress plugin** | **8.0.5** | `respira_diagnose_connection` → `plugin_diagnostic.plugin_version` | server side, updates via WP Admin → Plugins |
| **npm library** | **8.1.4** *(was 8.0.6 on 07-30)* | `npm view @respira/wordpress-mcp-server version` | NOT used by the connector (proven — see below) |
| **`.mcpb` bundle** | **7.1.3** (server 7.1.2) | `manifest.json` inside the `.mcpb` zip | ✅ **the only one that governs Claude Desktop / Claude Code** |

**The `.mcpb` bundle lags all the others, and that is normal.** Seeing "v8.1.8"
on respira.press, or 8.1.4 on npm, does NOT mean an 8.x bundle exists.

### Re-verified 2026-08-01 — still 7.1.3, no 8.x bundle

Downloaded the bundle and read the manifest **without installing**:

```bash
curl -sL -o respira.mcpb https://respira.press/downloads/respira-wordpress-latest.mcpb
unzip -p respira.mcpb manifest.json | grep '"version"'
unzip -p respira.mcpb "server/node_modules/@respira/wordpress-mcp-server/package.json" | grep '"version"'
```

Result: wrapper **7.1.3**, bundled server **7.1.2** — identical to 07-30. Bundle
size 6,957,887 bytes (that is the *zip*; the 21.18 MB figure from 07-30 was the
*extracted* extension folder — do not compare the two).

**The `Last-Modified` trap fired again.** The header read `Fri, 31 Jul 2026
04:17:50 GMT`, i.e. "yesterday", yet the bundled `package.json` inside is still
dated **2026-06-06**. Re-upload, not a release. That header has now been
misleading on two separate occasions — **never treat it as a version signal.**

**The cheap check (use this, it needs no install):** `curl` the bundle to a temp
folder and `unzip -p manifest.json`. Read `version`. Delete the file. Confirms
in seconds whether an upgrade even exists, with zero risk to the working
connector. Never infer the bundle version from a number on the website, from
npm, or from `Last-Modified`.

**What an 8.x bundle would eventually gain:** Respira 8.0 "Canopy" adds WordPress
Site Editor (FSE) support and fixes two safety bugs (Divi serialiser + Theme
Builder rollback). Neither affects Bricks workflows, so this is **low priority** —
7.1.2 is working correctly for everything this project does.

### Health check — one command

```
respira_diagnose_connection
```

Run this first whenever Respira misbehaves. It combines the plugin's server-side
report with outside-in HTTP probes and returns concrete remediation steps.

**Known-good baseline (2026-07-30 18:29):** `success: true` · all 5 probes 200 +
`application/json` · `html_instead_of_json: false` · 258 REST routes · all 3 DB
tables present (`api_keys`, `audit_log`, **`snapshots`**) · `write_method_blocked:
false` · auth via `x_respira_api_key_present: true`.

Environment at that check: WordPress 7.0.2 · PHP 8.3.30 · theme `bricks` ·
LiteSpeed Cache · Cloudflare (cache status `DYNAMIC`, so REST is not cached).

**The `runtime` block in the response is the authoritative answer to "which copy
is running":**

```
version           : 7.1.2
binary_path       : ...\Claude Extensions\local.mcpb...\server\index.js
is_global_install : false
```

This is the server reporting on itself — use it instead of guessing from npm or
the website.

**Two standing advisories** (both benign as of the baseline, neither actioned):

1. Cloudflare — the diagnostic suggests a WAF Skip / Page Rule for
   `/wp-json/respira/*` so requests are never challenged or cached. Only needed
   if "html instead of json" errors ever appear.
2. Limit Login Attempts Reloaded — generic warning that some security plugins
   redirect to the homepage rather than returning 403, which the MCP server reads
   as `200 + HTML`. Not occurring.

### Extension backup

A verified rollback copy lives at
`%USERPROFILE%\.respira\ext-backup\respira-wordpress-7.1.3_<timestamp>\`
with a `RESTORE.md` alongside it. Currently identical to the live extension, so
it can be pruned; keep one whenever a real version change does land.

### Claude's second config file: `claude_desktop_config.json` (NOT the same as `~/.claude.json`)

> There are **four** MCP config surfaces on this machine, and they are independent:
> `~/.claude.json` (now empty of MCP), the Connectors UI, `claude_desktop_config.json`,
> and **Devin's own `%APPDATA%\devin\mcp_config.json`** (see the section below it).

Claude Desktop (the unified app hosting chat, Cowork, and Claude Code) has its
**own** MCP config file, separate from Claude Code CLI's `~/.claude.json`:

```
%APPDATA%\Claude\claude_desktop_config.json
```

> This used to be written as `C:\Users\Zamri\AppData\Roaming\...`, which is the
> **home PC's** username and resolves to nothing on any other device. Use
> `%APPDATA%` (or `$env:APPDATA`) — this file is per-device, so hardcoded
> usernames are a silent-staleness trap.

This file's `mcpServers` block is where `Desktop`-type local extensions
(tagged `Local dev` in the Connectors UI) actually come from — it's not
managed by the Connectors UI "Add" button for Web connectors.

**Current state (as of 2026-07-29):** Only `fetch` remains here, a genuinely
local-only extension with no Web equivalent. `Context7` was removed
from this file (it also exists as a `Web` connector, so it was a true
duplicate). Verified end-to-end after restart: Claude Code now shows exactly
**one** Context7 tool namespace — `mcp__105f132a-5af6-41e0-aeca-3779cae338ff__*`
(the UUID form, which is the normal shape for a Web/remote connector). The
old `mcp__context7__*` namespace (the local Desktop entry) is gone, confirming
the right one was removed.

```json
{
  "mcpServers": {
    "fetch": { "command": "cmd.exe", "args": ["/d","/c","npx.cmd","-y","mcp-fetch-server"] }
  }
}
```

**Before removing anything from this file:** check whether the entry has a
`Web`-type duplicate in Settings → Connectors first. If it doesn't (like
`fetch`), removing it disables that capability entirely in both
Claude Desktop and Claude Code — there's no fallback.

---

## 🚨 Devin has its OWN MCP config — never edit it to manage Claude's servers

**These are completely separate files. Changing one has zero effect on the other.**

| Tool | MCP config |
|------|-----------|
| Claude Desktop / Claude Code | Connectors UI + `%APPDATA%\Claude\claude_desktop_config.json` |
| **Devin** | `%APPDATA%\devin\mcp_config.json` |
| Windsurf | its own, under `~/.codeium/windsurf/` |

On 2026-07-30, three servers in **Devin's** config (`devin/fetch`, `respira-wordpress`,
`github-remote`) ended up `disabled: true` during a config migration and stayed that way.
Devin lost those tools until it was noticed. Whatever the cause, the rule is simple:
**do not touch `%APPDATA%\devin\mcp_config.json` for the purpose of managing Claude's MCP
servers.** Claude's servers live in the Connectors UI and `claude_desktop_config.json`.

### ⚠️ Devin's config is a symlink onto Google Drive

```
%APPDATA%\devin\mcp_config.json  ->  <TSOT>\mcp_config.json
%APPDATA%\devin\memories         ->  <TSOT>\memories
```

Two consequences that cost real time on 2026-07-30:

1. **`Get-Item` reports the LINK, not the target.** `FileInfo.Length` reads **0** and the
   mtime is the link's, not the file's. Reading those and concluding "the file is empty /
   hasn't changed" is wrong. Always resolve first:
   ```powershell
   $i = Get-Item "$env:APPDATA\devin\mcp_config.json" -Force
   $i.LinkType; $i.Target                    # -> SymbolicLink, <TSOT>\...
   (Get-Item $i.Target).LastWriteTime        # the REAL last-write
   ```
2. **The file has three writers:** Devin, Google Drive sync, and any editor.

### The write-race — edit only with Devin closed

**Devin rewrites this file on startup.** It holds its own in-memory copy, re-applies its own
`disabled` flags, and re-serialises the JSON (its serializer escapes `<` as `\u003c` — a
useful fingerprint for "Devin wrote this, not a human or Drive").

Verified sequence on 2026-07-30:

```
23:49  manual edit  -> command/args changed, disabled:false, literal '<'
23:57  Devin starts
23:58  Devin writes -> KEPT command/args, RE-APPLIED disabled:true, escaped '<'
```

So a `disabled` flag set while Devin is running **will be clobbered**.

**Correct procedure:**
1. Quit Devin **fully** (many processes — check Task Manager, not just the window)
2. Back up the Drive target, then edit
3. Start Devin

**Do NOT pause Google Drive for this.** Drive was not the culprit (it restores bytes
verbatim; it does not re-encode JSON). Pausing leaves the edit unsynced, risks a conflict
copy on resume, and stops backing up the TSOT meanwhile. Prefer Devin's own UI toggle if it
has one — the app owns that state, so it cannot overwrite you afterwards.

### `devin/fetch` — the `mcp<2` pin (fixed 2026-07-31)

`mcp-server-fetch` declares `mcp>=1.1.3` with **no upper bound**. The `mcp` SDK 2.0 renamed
`McpError` → `MCPError`, so an unpinned install breaks itself:

```
ImportError: cannot import name 'McpError' from 'mcp.shared.exceptions'
```

Measured resolutions:

| Pin | Resolves to | Result |
|-----|-------------|--------|
| *(none)* | mcp 2.0.0 + fetch 2026.7.10 | ❌ ImportError |
| `mcp<1.0` | mcp 0.9.1 + fetch **0.1.0** | ⚠️ starts, but silently rolls the server back ~2 years |
| **`mcp<2`** | mcp 1.29.0 + fetch 2026.7.10 | ✅ correct |

`mcp<1.0` is a trap: uv satisfies the impossible constraint by downgrading *the other*
package. It looks fixed while running ancient code.

**Working entry:**

```json
"devin/fetch": {
  "args": ["--with", "mcp<2", "mcp-server-fetch"],
  "command": "uvx",
  "disabled": false,
  "registry": "devin/fetch"
}
```

A `docker run -i --rm mcp/fetch` variant also exists but needs Docker Desktop's daemon
running; it failed with `transport closed` purely because the daemon was down. `uvx` has no
daemon dependency, so it survives reboots.

### ⚠️ Devin and Claude drive WordPress through DIFFERENT Respira versions

| Agent | Respira source | Version |
|-------|----------------|---------|
| Claude | `.mcpb` extension, self-contained | **7.1.2** (pinned by the bundle) |
| Devin | `npx -y @respira/wordpress-mcp-server`, unpinned | **8.1.4** as of 2026-08-01 — floats to whatever npm serves |
| Codex | `npx -y @respira/wordpress-mcp-server`, unpinned (`~/.codex/config.toml`) | same as Devin — floats |

Same site, same tools, two different server builds. **If Devin and Claude ever disagree about
a Respira behaviour, check this first.** Devin's entry is unpinned, so its version moves on its
own whenever npx refreshes.

Config backups from this work: `%USERPROFILE%\.devin-config-backup\`.

---

### Why no per-project `mcpServers` in `~/.claude.json`

We previously mirrored Devin's TSOT `mcp_config.json` into
`~/.claude.json` per-project (`respira-wordpress`,
`devin/mcp-playwright`, `devin/fetch`). All four were **redundant** with
Connectors that were already installed at the user level. Duplicating them
just created maintenance burden and breakage surface area (e.g. `devin/fetch`
had a `McpError`/`MCPError` import bug that the built-in `fetch` connector
doesn't have).

The per-project `mcpServers` key was removed entirely. The top-level
`mcpServers` key was also removed (it only held `context7` as a redundant
backup of the Connector). **`~/.claude.json` now has zero MCP config** —
every MCP server is provided exclusively via the Connectors UI. This is the
cleanest possible state: one source of truth (Settings → Connectors), no
duplicate entries, no config-file maintenance.

### Environment variables (still useful, even with Connectors)

Some Connectors read env vars for auth. Set these as **user environment
variables** (persists across reboots):

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `RESPIRA_API_KEY` | Respira WordPress auth (if connector uses env var) | `respira_xxxx-xxxx-xxxx-xxxx` |
| `WORDPRESS_URL` | WordPress site URL | `https://digitrustlab.com` |

```powershell
[Environment]::SetEnvironmentVariable("RESPIRA_API_KEY", "respira_xxxx-xxxx", "User")
[Environment]::SetEnvironmentVariable("WORDPRESS_URL", "https://digitrustlab.com", "User")
```

> **Note:** The `Respira for WordPress` connector may store its API key in the
> connector config itself (via OAuth or input field in Settings → Connectors).
> If so, `RESPIRA_API_KEY` is unused for MCP and only useful for direct REST
> calls. Verify in the connector's settings UI.

### Screpy — Connected via Connectors UI (2026-07-29)

Screpy MCP is now connected. It uses **OAuth** (browser sign-in), not a bearer
token. The `SCREPY_TOKEN` env var is for Screpy's REST API only — it does NOT
work for MCP connections.

**Setup was:**
1. Settings → Connectors → Add custom remote MCP connector
2. URL: `https://mcp.screpy.com`
3. Authenticated automatically (no manual browser sign-in needed)

**If it disconnects after a Claude Code update:**
Re-add it via Settings → Connectors → Add custom remote MCP connector →
URL: `https://mcp.screpy.com`. This is a UI action — it cannot be automated
via config files.

**Test:** "Use Screpy to show my active projects."

⚠️ **Before ever re-adding it, run that test first.** `claude mcp list` and
`curl` both report Screpy as failed even when it is fully working — see
"`claude mcp list` LIES about OAuth'd Web connectors" near the top of this file.
Verified working 2026-08-01: `list_projects` returned `digitrustlab.com`
(uid `wgspvb7lc3`, owner, 3 crawls) under namespace `mcp__d4c2fdac-…__*`.
There is no `screpy` entry in `~/.claude.json` or `claude_desktop_config.json`,
and there should not be — the Connectors UI owns it.

---

## Machine-Specific Paths

**This device: OFFICE LAPTOP** — filled in and verified 2026-08-03.

| What | Value on this device |
|------|----------------------|
| Home | `C:\Users\zamrirosli.HEITECH` |
| Repo | `C:\my_Projektz\DigiTrustLabCode` |
| TSOT (use this — drive-letter-free) | `~\.codeium\windsurf\agent-templates` |
| TSOT resolves to | `C:\my_Projektz\agent-templates` (**git clone**, not Drive) |
| Google Drive mount | `G:\` — retained for `memories\` only |

> 🔒 **Drive is retained for `memories/` + `mcp_config.json` BY DESIGN — do not
> "finish the migration" by moving them.** Decided 2026-08-04: `memories/` holds
> HEITECH work product (`lessons-psp-emi.md`, `psp-staging-parking-tables.md`,
> `psp-emi-breadcrumbs/`) plus 43 opaque Devin `.pb` blobs. The clone auto-pushes
> to a personal GitHub remote, so folding them in would publish employer data
> irreversibly. Claude and Codex do not need any of it. Full rationale:
> `docs/plan-tsot-git-migration.md` § "Why `memories/` will never move into the repo".
>
> ⚠️ **The TSOT is a git repo now, not a Drive folder** (migration Phase 4
> completed on this laptop 2026-08-03). Sync is no longer automatic: `git pull`
> when starting on a machine, `git push` after changing a skill. The auto-push
> hook is enabled here (`core.hooksPath = scripts/hooks`), so committing in the
> TSOT pushes for you.
>
> `startup-integrity-check.ps1` reports drift under **🔄 TSOT Git Sync** — an
> uncommitted change there means the other machine is running stale doctrine.

The `@import` block above uses repo-relative paths, so it works on any device
regardless of the absolute repo path. No path adjustments needed when moving
devices — just recreate this file in the repo root.

**Always prefer `$env:USERPROFILE` / `%APPDATA%` over a literal path.** This file
is per-device and gitignored, so a hardcoded username survives indefinitely and
fails silently on the other machine — nothing validates it.

---

## Recreating the CLAUDE.md Symlinks (for a new device)

Two symlinks to recreate — the global memory and the project memory:

```powershell
$repo = (Get-Location).Path
$tsot = (Resolve-Path "$env:USERPROFILE\.codeium\windsurf\agent-templates").Path

# Global memory: ~/.claude/CLAUDE.md -> TSOT
cmd /c mklink "$env:USERPROFILE\.claude\CLAUDE.md" (Join-Path $tsot "global-memories\Claude-CLAUDE.md")

# Project memory: <repo>/CLAUDE.md -> TSOT
cmd /c mklink (Join-Path $repo "CLAUDE.md") (Join-Path $tsot "project-memories\DigiTrustLabCode\CLAUDE.md")
```
(Adjust the repo path if different on this device.)

---

## Recreating the Commands Symlinks (for a new device)

If `~/.claude/commands/` is empty or pointing at the stale antigravity tree:
```powershell
$cmds = "$env:USERPROFILE\.claude\commands"
$tsot = Join-Path (Resolve-Path "$env:USERPROFILE\.codeium\windsurf\agent-templates") "global-workflows"
Get-ChildItem $cmds -Filter "*.md" | Remove-Item -Force
Get-ChildItem $tsot -Filter "*.md" | ForEach-Object { cmd /c mklink (Join-Path $cmds $_.Name) $_.FullName }
```

---

## Recreating This File (for a new device)

This file is gitignored and per-device. On a new device, either:
1. Copy this file from the old device (the `@import` block is repo-relative, so
   it works without modification)
2. Or recreate it from the TSOT template at
   `<TSOT>\project-memories\DigiTrustLabCode\CLAUDE.local.template.md`

`CLAUDE.local.md` must remain a real local file. Do not symlink it to TSOT.

---

## Pre-Session Checklist

1. ~~Google Drive running? (TSOT must be reachable)~~ **No longer true as of
   2026-08-03.** The TSOT is a git clone at `C:\my_Projektz\agent-templates`;
   doctrine loads with Drive offline. Drive is still needed for Devin's
   `memories\` and `mcp_config.json`, which stayed behind — but not for Claude.
   Instead run: `& C:\my_Projektz\agent-templates\scripts\startup-integrity-check.ps1`
   (expect **all checks passed, exit 0** — 23/23 on this laptop as of 2026-08-04;
   the count grows as checks are added, so judge by "All N checks passed" + exit 0,
   not by a fixed number) and `git -C C:\my_Projektz\agent-templates pull`.
2. Confirm all imports loaded — ask Claude to list what's in its context
3. Check MCP connectors in Settings → Connectors:
   - `fetch`, `Context7`, `Respira for WordPress`, `Screpy` — all 4 should be connected
   - If any are missing, see the relevant section above for setup steps
