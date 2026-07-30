# Plan — migrate DigiTrust Lab rules out of the global TSOT

> **Written:** 2026-07-30 by Claude Code
> **Supersedes the file list in** `docs/claude-handoff-malay-skill-sync.md` § "Other DigiTrust Lab-specific files"

---

## ✅ RESOLVED 2026-07-30 — no migration performed, by design

**§2 was answered: Windsurf runs in parallel with Devin.** Deleting the global copies would have blinded Windsurf, so **nothing was deleted**. The plan below is kept for the scope analysis in §0, which stands.

**What was done instead — sync + automated drift detection:**

1. Backed up `workspace\rules\` (35 files) and `project-memories\` (2 files) to
   `%USERPROFILE%\.tsot-backup\20260730-213542\`, byte-verified.
2. **Found both duplicated rules had already drifted**, silently:
   - `bricks-mcp-absolute.md` — the global copy still described the **Bricks MCP endpoint decommissioned on 2026-07-05**. Windsurf had been reading a dead-endpoint rule for over three weeks.
   - `malay-skill-sync.md` — global said "13 semi-formal sections" against an actual 14.
3. Copied the authoritative `.devin/rules/` versions over the global ones. Both now byte-identical. Global folder still 35 files.
4. **Added drift detection to `scripts/verify-imports.py`** — it now compares every duplicated rule byte-for-byte and fails if the two trees disagree. Red-green verified.

**The duplicate is now permanent and intentional**, because both tools need their own path. What changed is that drift can no longer happen unnoticed: the check runs with the rest of the doctrine verification.

> **Revisit only if** Windsurf stops being used against this project. Until then, deleting the global copies is the wrong move, and §5 of this plan explains why.

---

## §0. The scope is 2 files, not 8

The handoff named 8 files as "DigiTrust Lab-specific files stuck in global TSOT". Tested against content, **4 have zero DigiTrust markers** and 2 more are global rules that merely *reference* project lesson files.

Measured by counting DigiTrust-specific terms (`digitrust|bricks|respira|malay|wordpress|writerzen`) versus other-project terms (`psp-emi|onewaysms|vue|laravel|pinia`):

| File | DTL markers | Verdict | Action |
|---|---:|---|---|
| `bricks-mcp-absolute.md` | **11** | Purely Bricks/Respira. Already duplicated in `.devin/rules/` | **MIGRATE** |
| `malay-skill-sync.md` | **7** | Purely Malay voice. Corrected copy already in `.devin/rules/` | **MIGRATE** |
| `self-improvement-loop.md` | 8 | Generic "how to write a lesson" rule. Its 8 hits are a **routing table** listing where each project's lessons file lives — it serves every project | KEEP GLOBAL |
| `self-improvement-loader.md` | 2 | Generic "load lessons at session start". Its 2 hits are just the path to `lessons-digitrustlab.md`. ⚠️ **Also `@import`ed by `CLAUDE.local.md`** | KEEP GLOBAL |
| `continuous-improvement.md` | 0 | Generic | KEEP GLOBAL |
| `general-advisor.md` | 0 | Generic | KEEP GLOBAL |
| `visual-communication.md` | 0 | Generic | KEEP GLOBAL |
| `deployment.md` | 0 | Cloudflare Pages + Render + TiDB. That is the **psp-emi / onewaysms** stack. DigiTrust Lab is WordPress on Hostinger — this rule does not even apply here | KEEP GLOBAL |

### ⚠️ The one that would have broken things

`self-improvement-loader.md` is on the handoff's move-list **and** is `@import`ed by `CLAUDE.local.md`:

```
@.windsurf/rules/self-improvement-loader.md
```

Removing it from the global folder breaks that import — recreating the exact silent-doctrine-loss failure of 2026-07-30. It stays.

---

## §1. Blast radius — read before touching anything

```
.windsurf/rules  ->  E:\My Drive\windsurf\.agent-templates\workspace\rules   (35 files)
```

This folder is:

- **shared by every project** on this machine
- **synced via Google Drive** to every other machine
- **not a git repository** — there is no history and no undo

A deletion here propagates to all machines on the next sync and cannot be recovered from version control.

**Therefore: back up before deleting, and verify the backup, before any `rm`.**

---

## §2. Which tool reads which tree — resolve this first

This is the one thing I cannot determine from the filesystem, and it decides whether §3 is safe.

| Tool | Reads | Would it lose the rule after migration? |
|---|---|---|
| **Claude Code** | `CLAUDE.local.md` `@import`s (both trees, explicit paths) | No, provided §3 step 4 is done |
| **Devin** | `.devin/rules/` | No — the files already live there |
| **Windsurf (if used standalone on this project)** | `.windsurf/rules/` → global | **Yes** — it would stop seeing both rules |

**Question for the owner:** do you still run Windsurf directly against DigiTrust Lab, separately from Devin? Recent reports are headed *"Executed by: Devin (Windsurf)"*, which suggests one tool, but that is an assumption I should not act on.

- **If Devin only** → §3 proceeds as written.
- **If Windsurf too** → do not delete from global. Instead do §3 steps 1–4 and leave the global copies as-is, accepting a known duplicate, and revisit when the tooling consolidates. A knowingly-tracked duplicate is safer than a silently missing rule.

---

## §3. Migration steps

### Step 1 — back up the global rules folder (mandatory, do this first)

```powershell
$src = "E:\My Drive\windsurf\.agent-templates\workspace\rules"
$dst = "$env:USERPROFILE\.tsot-backup\workspace-rules_$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item "$src\*" -Destination $dst -Recurse -Force

# verify before trusting it
$a=(Get-ChildItem $src -Recurse -File); $b=(Get-ChildItem $dst -Recurse -File)
"src: $($a.Count) files / $(($a|Measure-Object Length -Sum).Sum) bytes"
"bak: $($b.Count) files / $(($b|Measure-Object Length -Sum).Sum) bytes"
```

Counts and byte totals must match exactly. Do not continue otherwise.

### Step 2 — confirm the project-local copies are complete and current

```bash
cd "G:/Zamzam Biznez/DigiTrustLabCode"
ls -l .devin/rules/bricks-mcp-absolute.md .devin/rules/malay-skill-sync.md
diff <(git show HEAD:.devin/rules/bricks-mcp-absolute.md) .devin/rules/bricks-mcp-absolute.md
```

`malay-skill-sync.md` in `.devin/rules/` is the **corrected** version (14 sections, "natural formal–semi-formal", script-sync step). It is intentionally *not* identical to the global copy — the global one is stale. Do not "resolve" that difference by copying the global version over it.

### Step 3 — commit the project-local copies first

Nothing gets deleted from a non-git folder until its replacement is safely in git.

```bash
git add .devin/rules/malay-skill-sync.md
git commit -m "feat(rules): add corrected malay-skill-sync as a project rule"
```

### Step 4 — repoint the on-demand table in `CLAUDE.md`

`CLAUDE.md` routes agents to rules by path. One row points at the global copy:

```
| Malay voice sync | `.windsurf/rules/malay-skill-sync.md` |
```

Change to:

```
| Malay voice sync | `.devin/rules/malay-skill-sync.md` |
```

`bricks-mcp-absolute.md` is **not** in that table, so it needs no row change.

⚠️ `CLAUDE.md` is itself a symlink to
`E:\My Drive\windsurf\.agent-templates\project-memories\DigiTrustLab-CLAUDE.md`.
That file is DigiTrust-specific by name, so editing it is in scope — but it is still on Google Drive and still not in git. It is covered by the Step 1 backup only if you also back up `project-memories\`. **Do that too.**

### Step 5 — delete the two global copies (only after §2 is answered "Devin only")

```powershell
Remove-Item "E:\My Drive\windsurf\.agent-templates\workspace\rules\malay-skill-sync.md"
Remove-Item "E:\My Drive\windsurf\.agent-templates\workspace\rules\bricks-mcp-absolute.md"
```

Expect the folder to drop from 35 files to 33.

### Step 6 — verify

```bash
python scripts/verify-imports.py          # must PASS: all 11 imports still resolve
git status --short                        # expect clean
```

Plus, manually:

- `.windsurf/rules/` no longer lists the two files
- `.devin/rules/` still has all six (4 original + bricks-mcp-absolute + malay-skill-sync)
- Start a fresh session and ask the agent to state the Bricks-Only Policy unprompted

---

## §4. Definition of done

- [ ] §2 answered: Windsurf standalone, yes or no
- [ ] Global rules folder backed up and byte-verified
- [ ] `project-memories\` backed up as well (Step 4 edits it)
- [ ] `.devin/rules/malay-skill-sync.md` committed
- [ ] `CLAUDE.md` on-demand table points at `.devin/rules/`
- [ ] Two files removed from global (35 → 33) — **only if "Devin only"**
- [ ] `verify-imports.py` PASS
- [ ] Fresh session loads project doctrine

---

## §5. What this deliberately does not do

**The other 6 files stay in global.** They are genuinely shared, and two are load-bearing for imports. Moving them would be motion, not progress — and one of them would have broken the session.

**No consolidation of `.devin/rules` and `.windsurf/rules`.** They serve different tools with different loading mechanisms. Merging them is a larger decision that should follow the answer to §2, not precede it.

---

## §6. Why the handoff's list was wrong, and the general lesson

The handoff listed 8 files. It appears to have classified by *where a file was noticed* rather than by *what the file contains*. Four of the eight contain zero DigiTrust-specific content; one is imported by name and would have broken.

Same shape as the em-dash miscount earlier today: a list produced by impression rather than measurement. The check that resolves it takes one command:

```bash
grep -ciE "digitrust|bricks|respira|malay|wordpress|writerzen" <file>
```

**Before migrating a file because it "feels project-specific", measure it.**

---

*Plan only. Nothing in §3 has been executed. Every file count, marker count, symlink target and import dependency above was verified against the live filesystem on 2026-07-30.*
