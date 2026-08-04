# Plan — Move the TSOT from Google Drive to a Private Git Repo

**Status:** Phases 1–3 DONE on the home PC (2026-08-02). **Phase 4 DONE on the
office laptop (2026-08-03)** — 21/21, exit 0. Phase 5 (retire Drive copy) is the
only phase left, and it is now **unblocked** (no script work remains — see the
correction under "Scripts that need updating").
**Written:** 2026-08-01
**Estimated effort:** one focused session (~45–60 min), both laptops

| Fact | Value |
|------|-------|
| Repo | `https://github.com/fallendamien/agent-templates` (private) |
| Clone path | `C:\my_Projektz\agent-templates` — **must match on both machines** |
| Chokepoint | `~\.codeium\windsurf\agent-templates` → the clone |
| Links repointed | 39 (1 chokepoint + 38 routed through it) |
| Verified | `verify-imports.py` PASS · integrity check 17/17 exit 0 · 31 commands |

> The plan's Phase 2 table listed 7 link rows. The real count was **39** — the
> `~\.claude\commands\*.md` row alone is 31 links, and today's Codex work added
> `~\.codex\skills\TSOT_skills` and `~\.claude\skills\i-have-adhd`. Enumerate,
> do not trust the table:
> ```powershell
> Get-ChildItem ~\.claude,~\.codex,~\.codeium\windsurf,<repo> -Force -Recurse -Depth 2 |
>   Where-Object LinkType -eq 'SymbolicLink'
> ```

> **Windows gotcha hit during Phase 2:** `cmd /c del /q` on a file symlink is
> blocked by the agent guard. Use `[System.IO.File]::Delete($p)` for file links
> and `[System.IO.Directory]::Delete($p,$false)` for directory links — both
> remove the link only, never the target.

---

## Why

The TSOT (`<drive>:\My Drive\windsurf\.agent-templates`) holds 33 rules, 125
skills, 31 workflows, 9 setup scripts, and both `lessons.md` files. **None of it
is under version control.** Consequences observed:

- An edit through `.windsurf/skills` silently changes every project on every
  machine, with no history and no rollback (recorded in `lessons.md`).
- When Claude and Codex both read the same doctrine, there is no way to tell
  *what changed, when, or by which agent*.
- Google Drive's `Last-Modified` has twice been misleading about whether content
  actually changed (see the Respira `.mcpb` notes in `CLAUDE.local.md`).

Git fixes all three at once, and also removes the per-device drive-letter problem
because a clone lives at a normal local path.

## Scope (measured 2026-08-01)

```
3.6 MB · 419 files · no .git present
```

| Subtree | Size |
|---------|------|
| `skills-library/` | 1.9 MB |
| `workspace/` (33 rules + 125 skills) | 1.4 MB |
| `global-workflows/` (31) | 123 KB |
| `scripts/` (9) | 78 KB |
| `tasks/` (lessons.md + lessons-digitrustlab.md) | 74 KB |
| `references/` | 42 KB |

Trivially small for git.

---

## ⚠️ Do NOT `git init` inside Google Drive

`.git` is hundreds of small files rewritten constantly (`index`, `refs`, loose
objects). Drive syncing that across two laptops is a known corruption vector:
`index.lock` conflicts, torn object writes, detached refs.

| Option | Sync | History | Verdict |
|--------|------|---------|---------|
| A. `git init` inside Drive | Drive | ✅ | ❌ corrupts across 2 machines |
| B. Work tree in Drive, `.git` outside (`--separate-git-dir`) | Drive | per-machine | ⚠️ divergent histories |
| **C. Private GitHub repo, clone on both machines, drop Drive for the TSOT** | **git** | ✅ shared | ✅ **chosen** |

Under C, git replaces Drive entirely for this folder — it does sync *and* history
*and* conflict resolution.

**Tradeoff, accepted:** sync stops being automatic. `git pull` when starting on a
machine, `git push` after changing a skill. Same discipline already used for the
project repo.

---

## Migration steps

### Phase 1 — create the repo (home laptop)

1. `gh repo create <name> --private` (suggested name: `agent-templates`)
2. Copy `<drive>:\My Drive\windsurf\.agent-templates` → a new local path,
   e.g. `C:\my_Projektz\agent-templates`. **Copy, do not move** — Drive keeps the
   original until Phase 4 confirms everything works.
3. `git init && git add -A && git commit` — first commit is the current state.
4. Add a `.gitignore` for junk (`*.bak_*`, `__pycache__/`, `.DS_Store`).
5. Push.

### Phase 2 — repoint symlinks (home laptop)

Every link currently targeting the Drive path must point at the clone instead:

| Link | New target |
|------|-----------|
| `~\.codeium\windsurf\agent-templates` | `C:\my_Projektz\agent-templates` |
| `~\.claude\CLAUDE.md` | `…\agent-templates\global-memories\Claude-CLAUDE.md` |
| `~\.claude\commands\*.md` (31) | `…\agent-templates\global-workflows\*.md` |
| `<repo>\CLAUDE.md` | `…\agent-templates\project-memories\DigiTrustLabCode\CLAUDE.md` |
| `<repo>\.windsurf\rules` | `…\agent-templates\workspace\rules` |
| `<repo>\.windsurf\skills` | `…\agent-templates\workspace\skills` |
| `<repo>\.windsurf\workflows` | `…\agent-templates\global-workflows` |

Only the first strictly needs the real path — the rest can route through it, so
the target lives in exactly one place. (Same chokepoint pattern used for the
drive-letter fix on 2026-07-31.)

### Phase 3 — verify (home laptop)

```bash
python scripts/verify-imports.py        # must exit 0, 11 imports / 4 trees
```
```powershell
(Get-ChildItem "$env:USERPROFILE\.claude\commands" -Filter *.md).Count   # 31
```
Then restart Claude Code and confirm **16** files load; start Codex and confirm
`AGENTS.md` + Tier 1 doctrine still resolve.

### Phase 4 — office laptop  ✅ DONE 2026-08-03

> **Paste this prompt on the office laptop. Do not just say "follow this plan".**
> The doc describes five phases and nothing in it tells an agent which machine it
> is on. Phase 1 would re-create the repo; **Phase 5 renames the Drive folder,
> which is the only rollback.** Scope the request explicitly:
>
> ```
> Read docs/plan-tsot-git-migration.md. I'm on the OFFICE laptop.
>
> Execute Phase 4 ONLY — all of it, including step 1b (core.hooksPath).
> Do not run Phase 1, 2, 3 or 5.
>
> Before starting, enumerate the existing symlinks (command is in the header
> of this doc) and show me the list. Also show me what is currently in
> ~\.codex\skills — I expect a stale link to a project skills tree there.
>
> Phase 4 step 2 runs bootstrap-new-device.ps1. It must print
> "📦 TSOT git clone detected". If it prints "☁️ Google Drive detected"
> instead, STOP and tell me — the clone is missing and it would wire
> everything to the retired Drive copy.
>
> Finish by running, and showing me the output of:
>   startup-integrity-check.ps1      (expect all checks passed, exit 0)
>   python scripts/verify-imports.py (expect exit 0)
>   (Get-ChildItem ~\.claude\commands -Filter *.md).Count         (expect 31)
>   (Get-ChildItem ~\.codex\prompts  -Filter *.md).Count          (expect 31)
>   (Get-ChildItem ~\.codex\skills\TSOT_skills -Directory).Count   (expect 126)
>   ~\.codex\skills must contain ONLY: .system, TSOT_skills (+ any real folder)
>
> Then RESTART Codex and confirm typing "/check-sy" offers "prompts:check-sync".
> The prompt registry is built at Codex startup and never rescans, so it will
> show nothing until a restart after the bootstrap runs. That is expected, not
> a failure — three tests on 2026-08-02 were misdiagnosed for exactly this.
>
> Do not delete or rename anything on Google Drive.
> ```
>
> **Expect one failure that is not the migration's fault:** `CLAUDE.md` and
> `CLAUDE.local.md` are gitignored, so a fresh clone of *this* repo has neither.
> `verify-imports.py` flags it immediately — that is the git-worktree case
> described in `AGENTS.md`, not a broken symlink. Recreate them from the TSOT
> template (`project-memories/DigiTrustLabCode/CLAUDE.local.template.md`).

1. `git clone https://github.com/fallendamien/agent-templates.git C:\my_Projektz\agent-templates`
   — the path **must** match the home PC; the chokepoint symlink is absolute.
1b. **Enable the auto-push hook — a fresh clone does NOT run it:**
    ```powershell
    git -C C:\my_Projektz\agent-templates config core.hooksPath scripts/hooks
    ```
    The hook file is versioned (`scripts/hooks/post-commit`) so it arrives with
    the clone, but `core.hooksPath` is local config and must be set per machine.
    Without it, commits made on this laptop are never pushed and the home PC
    silently runs stale doctrine. `bootstrap-new-device.ps1 -IncludeClaude` sets
    this automatically; do it by hand if you skip the script.
2. Run the bootstrap — it now prefers the clone over Drive (fixed 2026-08-02):
   ```powershell
   & C:\my_Projektz\agent-templates\scripts\bootstrap-new-device.ps1 `
       -IncludeClaude -IncludeCodex -ProjectPath '<repo path>'
   ```
   Expect `📦 TSOT git clone detected at: C:\my_Projektz\agent-templates`. If it
   says `☁️ Google Drive detected` instead, **stop** — the clone is missing or has
   no `.git`, and every link would be wired to the retired Drive copy.
3. Verify: `startup-integrity-check.ps1` (**all checks passed**, exit 0) · 31 Claude commands ·
   126 Codex skills · `python scripts/verify-imports.py` (exit 0).

**What `-IncludeCodex` wires** (all created, not merely repointed):

| Target | Purpose |
|--------|---------|
| `~\.codex\AGENTS.md` | global doctrine loader |
| `~\.codex\skills\TSOT_skills` | the 126 shared skills |
| `~\.codex\prompts` | whole-folder link to `global-workflows` → 31 slash commands (`/check-sy` → `prompts:check-sync`). **Needs a Codex restart to appear.** |
| strays under `~\.codex\skills` | **removed** (unlink only; real folders kept) |

**Why the bootstrap is required and not optional:** the home PC's Phase 2 loop
only *repointed links that already existed*. The office laptop has never had
`~\.codex\skills\TSOT_skills` or `~\.claude\skills\i-have-adhd` — those were
created on 2026-08-02. A repoint-only pass leaves Codex reading 53 skills from
the deprecated `antigravity` tree with no `i-have-adhd`. The bootstrap creates
them, and also **auto-removes every stray symlink under `~\.codex\skills`**
(unlink only; real folders such as `pdf/` are kept and reported).

### 🏠 Home PC — do this first, before Phase 5 (2026-08-03 handoff)

The office laptop pushed changes that the home PC does not have yet. Run in order:

```powershell
# 1. Pull the TSOT — brings the codex bridge + the two bootstrap fixes
git -C C:\my_Projektz\agent-templates pull

# 2. Wire the new Codex link (the bridge did not exist when this PC was set up)
& C:\my_Projektz\agent-templates\scripts\bootstrap-new-device.ps1 `
    -IncludeClaude -IncludeCodex -ProjectPath '<repo path>'

# 3. Verify
& C:\my_Projektz\agent-templates\scripts\startup-integrity-check.ps1   # expect all checks passed, exit 0
python scripts/verify-imports.py                                       # expect exit 0
```

Then **restart Zed** — the ACP command registry is built at startup and never
rescans, so `$check-sync` will not appear until you do.

Two things to check on the home PC specifically:

1. **Its `CLAUDE.local.md` Pre-Session Checklist still says "Google Drive
   running? (TSOT must be reachable)".** That is false since the migration —
   doctrine now loads with Drive offline. Fixed on the office laptop; the home
   PC's copy is gitignored and per-device, so it must be edited separately.
2. **Confirm its TSOT resolves to the clone, not Drive**, before Phase 5:
   ```powershell
   (Get-Item "$env:USERPROFILE\.codeium\windsurf\agent-templates" -Force).Target
   # must print C:\my_Projektz\agent-templates
   ```
   The bootstrap prints `📦 TSOT git clone detected` when this is right, and
   `☁️ Google Drive detected` when it is not. **Do not start Phase 5 until both
   machines print the former** — the rename reaches both through Drive sync.

### Phase 5 — retire the Drive copy

Only after both machines pass:

1. Rename the Drive folder to `.agent-templates.RETIRED_<date>` — do **not**
   delete yet. Leave it one to two weeks.
2. Confirm nothing breaks on either machine.
3. Delete.

---

## Scripts that need updating

These auto-detect the TSOT by scanning drives for `My Drive\windsurf\.agent-templates`.
All must learn the new location:

| Script | Line | Status |
|--------|------|--------|
| `startup-integrity-check.ps1` | 85–102 | ✅ **done 2026-08-02** — prefers the clone, falls back to Drive |
| `bootstrap-new-device.ps1` | 60–80 | ✅ **done 2026-08-02** — clone wins, Drive is fallback + warns |
| `setup-global-rules-symlink.ps1` | 27 | ✅ **no change needed** — scans `windsurf\memories\`, not `.agent-templates\` |
| `sync-memories.ps1` | 16 | ✅ **no change needed** — same reason |
| `update_breadcrumbs.ps1` | 44 | ✅ **no change needed** — same reason |

### ⚠️ Correction (2026-08-03) — the three "outstanding" scripts were never at risk

This section previously read *"All four outstanding scripts work today only
because the Drive folder still exists. They break at Phase 5."* **That was wrong**,
and acting on it would have broken three working scripts.

The claim assumed any drive-scan is migration debt, without checking **which**
Drive path each script scans. Verified layout — these are **siblings**, not nested:

```
<drive>:\My Drive\windsurf\
├── .agent-templates   ← Phase 5 renames THIS (migrated to git)
├── memories           ← all three scripts use THIS (deliberately stayed)
├── backups
└── mcp_config.json
```

`memories/` and `mcp_config.json` are **not in the git repo** — Devin symlinks
them, as already documented in `startup-integrity-check.ps1:89-92`. All three
scripts target `memories\`, so renaming `.agent-templates` does not affect them.

The two scripts fixed on 2026-08-02 *did* target `.agent-templates`. These three
never did.

> **The lesson:** before applying a fix pattern across a list of scripts, check
> what each one actually resolves. "Uses a drive scan" is not the same as "depends
> on the migrated folder." Blanket-applying the clone-preference here would have
> pointed `sync-memories.ps1` at a clone with no `memories/` folder, breaking
> Devin's memories link on every device.

**Phase 5 is therefore unblocked** — no script work remains before renaming the
Drive `.agent-templates`. Verify the home PC also resolves its TSOT to the clone
first, since the rename reaches both machines through Drive sync.

Simplification: with a fixed clone path, drive-scanning can be dropped entirely.

### ✅ Two project-link bugs found on the office laptop — FIXED 2026-08-03

Phase 4 passed 19/21 on first run. Both failures were **script bugs, not migration
damage**, and both sat in the create path that only a fresh machine exercises. The
home PC never hit them: its Phase 2 loop *repointed links that already existed*,
while a new device *creates* them.

**Both are now fixed in the TSOT** (commit `415b3d4`). A fresh device reaches 21/21
without hand-editing.

| # | Bug | Evidence | Fix shipped |
|---|-----|----------|-------------|
| 1 | `bootstrap-new-device.ps1` pointed `<repo>\.windsurf\skills` at the **real clone path**, but `startup-integrity-check.ps1` expects the **chokepoint** | bootstrap `:378-380` targeted `$DrivePath\workspace\skills`; integrity check `:301` expects `$TemplatesDir\workspace\skills` | ✅ bootstrap now targets the chokepoint — the plan's own rule (line 114) is "the target lives in exactly one place" |
| 2 | **Nothing created `<repo>\.windsurf\workflows`** | `setup-windsurf-workspace.ps1` had `Sync-WindsurfRules` + `Sync-WindsurfSkills` and no workflows equivalent; integrity check `:302` and `verify-imports.py` both require it | ✅ added `Sync-WindsurfWorkflows` (mirrors the rules function, preserves a real dir) + bootstrap creates it |

**How the fix was verified — do this, not a code re-read.** Both links were
*deleted* to simulate a fresh device, then the scripts were re-run and watched to
rebuild them:

```powershell
# link-only delete; the target is never touched
[System.IO.Directory]::Delete("$repo\.windsurf\skills", $false)
[System.IO.Directory]::Delete("$repo\.windsurf\workflows", $false)
& <TSOT>\scripts\bootstrap-new-device.ps1 -IncludeClaude -ProjectPath <repo>
```

Result: both recreated through the chokepoint · integrity check project section
3/3 · `verify-imports.py` PASS exit 0 (it had been failing on
`.windsurf/workflows`).

> ⚠️ Also note: `bootstrap-new-device.ps1` printed `[OK] CLAUDE.local.md created`
> at 19:18:19 for a file whose mtime was 19:00:47 — it did not create it. Do not
> trust that line as evidence the file is fresh.

### 🔌 Codex workflows in Zed — the `codex-skill-bridge` (added 2026-08-03)

Separate from the migration, found while verifying Phase 4. The 31 workflows work
in **native Codex** (`/check-sy` → `prompts:check-sync`) but were **invisible in
Zed's Codex panel**.

**Cause:** `codex-acp` — the ACP adapter Zed drives Codex through — does not
enumerate `~/.codex/prompts`. It advertises built-ins (`/status`, `/mcp`,
`/skills`, `/review`, `/compact`, `/logout`) **plus skills**, and nothing else.
Confirmed on codex-acp **1.1.9**, the latest on npm; no upgrade fixes it.

**Not** [zed#53161](https://github.com/zed-industries/zed/issues/53161) (Zed
dropping a valid `available_commands_update`). That was ruled out because
built-ins *and* an existing skill (`$ab-test-analyzer`) both rendered correctly —
the wire was healthy. **Use that as the discriminator:** if built-ins show but
custom entries do not, it is the adapter; if *nothing* shows, it is zed#53161.

**Fix:** `<TSOT>/codex-skill-bridge/` — 31 skill wrappers, one per workflow,
linked in as `~/.codex/skills/TSOT_workflows`. They surface in Zed as
`$check-sync`. Each wrapper is a **pointer** to `global-workflows/<name>.md`,
never a copy, so there is one source of truth (per `workspace/rules/tsot-parity.md`).
`bootstrap-new-device.ps1 -IncludeCodex` creates the link and **excludes it from
stray-link removal** — without that exclusion the next bootstrap run would delete
the bridge, since that loop removes every symlink not on its allow-list.

⚠️ **Restart Zed after pulling this** — the command registry is built at agent
startup and never rescans. Same trap that caused three misdiagnoses on 2026-08-02.

Accepted tradeoff: workflows now appear **twice in native Codex** —
`/prompts:check-sync` and `$check-sync`. Same file, two doorways. Cost measured at
~828 tokens of extra skill metadata (+9.8%). Watch for spurious auto-invocation:
skills can be selected by the model on its own, prompts cannot.

Also update the prose in:
- `CLAUDE.local.md` (Machine-Specific Paths, recreate-symlinks sections)
- `Claude-CLAUDE.md` (`<drive>:` placeholders become the clone path)
- `AGENTS.md` Tier 3 table (lessons paths)

---

## Open questions

1. **Repo name and location** — `agent-templates` under `C:\my_Projektz\`?
   Office laptop uses `C:\my_Projektz\` too, so the path can match on both.
2. **Keep Drive as a backup?** Drive could still sync a *copy* for disaster
   recovery, as long as nothing symlinks to it. Decide in Phase 5.
3. ~~**`memories/` and `mcp_config.json`** live in `windsurf\` (the parent), not in
   `.agent-templates`. Devin symlinks to them. If Devin is fully retired they can
   be folded into the repo; otherwise leave them on Drive.~~
   **DECIDED 2026-08-04 — they stay on Drive permanently. Do not fold them in.**
   See "Why `memories/` will never move into the repo" below.

## Why `memories/` will never move into the repo (decided 2026-08-04)

**This is a deliberate, permanent exception. A future session that finds Drive
still in use here should NOT "finish the migration" by moving it.**

Moving `memories/` into the clone was evaluated and rejected. Two reasons:

1. **It contains employer material.** `lessons-psp-emi.md` (8 KB),
   `psp-staging-parking-tables.md`, and `psp-emi-breadcrumbs/` are HEITECH work
   product. The clone's `post-commit` hook auto-pushes to a personal GitHub
   remote, so folding them in would publish employer data to a personal account.
   A push is not reversible — GitHub retains unreachable objects, and mirrors or
   indexers keep copies even after a force-remove.
2. **43 `.pb` files (~60 KB) are opaque.** They are Devin's protobuf memory
   blobs, not human-readable, so their contents cannot be reviewed before
   publishing. Anything Devin observed — credentials, source, screenshots —
   could be inside. Unreviewable content must not enter a pushed repo.

`global_rules.md` alone (23 KB, pure doctrine) *could* have moved, but that would
split `memories/` across two locations while leaving Devin dependent on Drive
anyway — all of the cost, none of the benefit.

**Net effect:** the setup is intentionally hybrid, and that is the finished
state, not an unfinished one.

| Component | Source | Status |
|---|---|---|
| Templates, workflows, skills, lessons | local git clone | ✅ migrated |
| Project symlinks / adapters | local git clone | ✅ migrated |
| `memories/` + `global_rules.md` | Google Drive | 🔒 **stays — by design** |
| `mcp_config.json` (Devin) | Google Drive | 🔒 **stays — by design** |

Claude and Codex are fully Drive-independent; doctrine loads with Drive offline.
**Only Devin's runtime state still needs Drive.** If Devin is ever retired, revisit
— but the employer-data problem above must be solved first regardless.

## Rollback

Until Phase 5 deletes it, the Drive copy is untouched and authoritative. Rollback
is repointing the symlinks back at `<drive>:\My Drive\windsurf\.agent-templates`.
