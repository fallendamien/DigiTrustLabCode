# Handoff for Devin — `.devin/` symlink migration broke project doctrine

> ✅ **RESOLVED** — 2026-07-30 · Commit `e3588a2` · Rules restored, write-post rebuilt as skill, AGENTS.md references fixed, verify-imports passed. Do NOT re-execute.

> **Raised:** 2026-07-30 by Claude Code · **Severity:** high, silent · **All findings verified, commands included**

---

## TL;DR

Commit `ae550c3` replaced `.devin/rules` and `.devin/workflows` with **symlinks to the global Devin agent-templates**. The project-specific files that used to live there are no longer on the active path. Nothing errors — the doctrine just stops loading, silently.

**Three of the four rules `CLAUDE.local.md` `@import`s no longer resolve.** Sessions have been running without them.

---

## Verified evidence

### 1. What the symlinks now point at

```
.devin/rules      ->  %APPDATA%\devin\agent-templates\workspace\rules
.devin/workflows  ->  %APPDATA%\devin\agent-templates\global-workflows
```

Both are **global**, shared by every project.

### 2. Broken `@import`s in `CLAUDE.local.md`

`CLAUDE.local.md` imports four rules by exact path. Current state:

| Import | Resolves? |
|---|---|
| `.devin/rules/bricks-mcp-absolute.md` | ✅ (happens to exist in the global set) |
| `.devin/rules/bricks-standard-guide.md` | ❌ **MISSING** |
| `.devin/rules/content-planning.md` | ❌ **MISSING** |
| `.devin/rules/browser-preview.md` | ❌ **MISSING** |

An `@import` to a missing file fails quietly. There is no warning.

### 3. The publish pipeline is off the active path

`.devin/workflows/write-post.md` — the full Option C pipeline (quota check, Topic Discovery, Golden Filter, Weak Spot gate, publish, Rank Math, rank tracking) — is not in the symlinked global folder. The global folder holds only the 31 generic workflows (`commit`, `deploy`, `plan`, …).

### 4. The `.bak` folders are gone

`ae550c3` created `.devin/rules.bak_20260730_144544/` and `.devin/workflows.bak_20260730_144543/`. **Both have since been deleted.** Recovery must come from git.

### 5. `AGENTS.md` has dead references

Three point at the now-unreachable path:

- line 510 — `**Full workflow:** See .devin/workflows/write-post.md …`
- line 624 — `See .devin/workflows/write-post.md → Key Rules → "Content formatting" …`
- line 595 — `run /write-post for the full end-to-end pipeline`

---

## What is recoverable, and from where

All content is retrievable from **`ae550c3^`** (the parent of the migration commit):

| File | Lines at `ae550c3^` |
|---|---|
| `.devin/rules/bricks-standard-guide.md` | 37 |
| `.devin/rules/content-planning.md` | 41 |
| `.devin/rules/browser-preview.md` | 19 |
| `.devin/workflows/write-post.md` | 525 |

### ⚠️ One caveat on `write-post.md`

The 525-line version in git is **pre-deduplication**. On 2026-07-30 it was slimmed to ~399 lines by moving reference material into its proper homes. That slimming was never committed and is now lost.

**The destinations survived and ARE committed** — verified at `HEAD`:

| Content | Now lives in | In git? |
|---|---|---|
| Image prompt template, design system, anatomy fix, worked examples | `content/image-prompts.md` | ✅ |
| Rich Formatting Toolkit, blockquote/callout templates, Formatting Checklist | `.devin/skills/readability-pass/SKILL.md` | ✅ |
| Malay voice + publish gate | `.devin/skills/malay-voice-guide/SKILL.md` | ✅ |

So restoring the 525-line version would **re-introduce duplicates** of content that already lives in those three files. Do not restore it verbatim — see the task below.

---

## 🚨 The trap — read before touching anything

`.devin/rules` and `.devin/workflows` are **symlinks to global, shared templates**. Writing a file into them writes it into **every project on this machine**, and the target is not a git repo, so mistakes are unrecoverable.

**Always remove the symlink before restoring files into that path.** Use `rmdir`, which deletes the link only, never the target:

```powershell
# INSPECT FIRST — confirm it is a symlink and see the target
Get-Item .devin\rules | Select-Object LinkType, Target

# Remove the LINK only (rmdir on a symlink does not touch the target)
cmd /c rmdir "G:\Zamzam Biznez\DigiTrustLabCode\.devin\rules"
```

Do **not** use `Remove-Item -Recurse` on a symlinked directory.

---

## Tasks

### Task 1 — restore the rules (required, do this first)

`CLAUDE.local.md` hardcodes `.devin/rules/*.md`, so these must exist at exactly that path.

```powershell
cd "G:\Zamzam Biznez\DigiTrustLabCode"
Get-Item .devin\rules | Select-Object LinkType, Target      # confirm symlink
cmd /c rmdir ".devin\rules"                                  # remove link only
```

```bash
git checkout ae550c3^ -- .devin/rules/
```

**Verify all four resolve:**

```bash
for f in bricks-mcp-absolute bricks-standard-guide content-planning browser-preview; do
  [ -e ".devin/rules/$f.md" ] && echo "OK   $f" || echo "FAIL $f"
done
```

All four must print `OK`.

### Task 2 — rebuild the publish pipeline as a **skill**, not a workflow

The owner's stated preference: **skills carry the load; workflows stay thin.** So do not simply restore `write-post.md` into `.devin/workflows/`.

Create `.devin/skills/write-post/SKILL.md`:

1. Start from `git show ae550c3^:.devin/workflows/write-post.md` (525 lines)
2. **Delete** the sections that now live elsewhere, replacing each with a one-line pointer:
   - Image Prompt Template / design system / variation guide / worked examples → `content/image-prompts.md`
   - Rich Formatting Toolkit / blockquote + callout templates / Formatting Checklist → `.devin/skills/readability-pass/SKILL.md`
   - Malay voice checks and the publish gate → `.devin/skills/malay-voice-guide/SKILL.md`
   - Keyword research detail (Phases 0a–1.5) → `.devin/skills/writerzen-keyword-research/SKILL.md`
3. **Keep** the sequential phases: −1 (quota), 0a (Topic Discovery), 0b (Golden Filter), 1 (cluster), 1.5 (Weak Spot gate), 2–5 (brief → outline → keywords → write), 6 (publish via Respira, **including the `wp.data` excerpt method** — that was hard-won), 6.5 (Rank Math essential-vs-cosmetic), 7 (ClickRank + Screpy + internal links + docs)
4. Add a **"Where Things Live"** table at the end recording which file owns which topic, plus the rule: *if you are about to paste a table or template into this skill, it belongs in one of those files — add a pointer instead*
5. Valid frontmatter — `name: write-post`, matching the directory, kebab-case
6. Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate-skills.ps1` — must report 0 violations

**Add the Malay publish gate to Phase 6.5**, since that is where it belongs in sequence:

```bash
python scripts/verify-malay-voice.py <post-id>   # must be 0 errors before Phase 7
```

…and note that the new post ID must be added to the script's `CONTENT` dict, or it is silently never checked.

### Task 3 — fix the `AGENTS.md` references

Update lines 510, 595, 624 to point at `.devin/skills/write-post/SKILL.md` instead of `.devin/workflows/write-post.md`. Check for others with:

```bash
grep -n "write-post" AGENTS.md
```

### Task 4 — decide the `.devin/workflows` symlink

With the pipeline living as a skill, the symlink to the global 31 workflows can stay. **Confirm nothing else project-specific was in the old folder** before accepting that:

```bash
git show ae550c3^ --stat -- .devin/workflows | head -40
```

Anything project-specific that appears there and is not in the global set needs a home too.

---

## Definition of done

- [ ] All four `.devin/rules/*.md` imports resolve
- [ ] `.devin/rules` is a real directory, not a symlink; the global template folder is unmodified
- [ ] `.devin/skills/write-post/SKILL.md` exists, carries the sequential phases, and duplicates nothing
- [ ] `validate-skills.ps1` → 0 violations
- [ ] `grep -n "write-post" AGENTS.md` → no dead paths
- [ ] `python scripts/verify-malay-voice.py` → still 0 errors
- [ ] A session started fresh loads the project doctrine (spot-check: ask the agent to state the Bricks-Only Policy without being told)

---

## Why this matters

The failure mode is silence. A missing `@import` does not warn; a missing workflow does not warn. The first symptom is an agent publishing a post without the Weak Spot gate or the Bricks-Only Policy, and nobody noticing until the damage is live.

That is exactly what happened on Post #4, before the gates were added.

**Recommended follow-up:** add a startup check that asserts every `@import` target in `CLAUDE.local.md` exists, so this class of breakage announces itself instead of degrading quietly.

---

*Prepared by Claude Code, 2026-07-30. Every path, line count, and symlink target above was verified against the live filesystem and git history at the time of writing.*
