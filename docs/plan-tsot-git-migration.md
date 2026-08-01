# Plan — Move the TSOT from Google Drive to a Private Git Repo

**Status:** planned, not started
**Written:** 2026-08-01
**Estimated effort:** one focused session (~45–60 min), both laptops

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
| `<repo>\CLAUDE.md` | `…\agent-templates\project-memories\DigiTrustLab-CLAUDE.md` |
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

### Phase 4 — office laptop

1. `git clone` the repo to the same relative location.
2. Re-run the symlink setup pointing at the clone.
3. `startup-integrity-check.ps1` + confirm 31 commands.

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

| Script | Line |
|--------|------|
| `bootstrap-new-device.ps1` | 39 |
| `setup-global-rules-symlink.ps1` | 27 |
| `sync-memories.ps1` | 16 |
| `update_breadcrumbs.ps1` | 44 |
| `startup-integrity-check.ps1` | 21 (also still uses a hardcoded letter list — fix while here) |

Simplification: with a fixed clone path, drive-scanning can be dropped entirely.

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
3. **`memories/` and `mcp_config.json`** live in `windsurf\` (the parent), not in
   `.agent-templates`. Devin symlinks to them. If Devin is fully retired they can
   be folded into the repo; otherwise leave them on Drive.

## Rollback

Until Phase 5 deletes it, the Drive copy is untouched and authoritative. Rollback
is repointing the symlinks back at `<drive>:\My Drive\windsurf\.agent-templates`.
