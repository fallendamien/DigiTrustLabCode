---
trigger: model_decision
description: Keep AGENTS.md, verify-malay-voice.py and malay-voice-guide/SKILL.md in sync. Activates whenever a section, pattern table or banned-word entry is added, renamed or renumbered in the Malay voice guide (natural formal–semi-formal BM standard).
---

# Malay Skill Sync

**Priority:** MEDIUM — activates when `.devin/skills/malay-voice-guide/SKILL.md` is modified.

## Rule

The Malay voice standard lives in three places that must agree:

| File | Holds |
|------|-------|
| `.devin/skills/malay-voice-guide/SKILL.md` | the full standard (authoritative) |
| `AGENTS.md` | a one-line-per-section quick summary + section count |
| `scripts/verify-malay-voice.py` | the machine-checkable subset (wordlists) |

Change one, sync the others in the same session. A pattern that exists in only one place drifts out of sync within weeks.

## Sync Checklist

### 1. Count the sections — do not eyeball it

Only top-level `## N.` headings count. Lettered `###` subsections (4a–4f, 11c–11e) do **not** add to the total; `## 11b` does, because it is a top-level heading.

```bash
grep -cE "^## [0-9]+[a-z]?\. " .devin/skills/malay-voice-guide/SKILL.md
```

**Current count: 14** (sections 1–13 plus 11b).

> This ambiguity is what caused the count to go stale before. `## 11b` looks like a subsection but is not one. Run the command; do not count by reading.

### 2. Update the header line in AGENTS.md

Search for `Quick summary of the` and set:

```
Quick summary of the N sections (natural formal–semi-formal BM standard):
```

The register phrase is **"natural formal–semi-formal"**, not "semi-formal". The standard is a spectrum: formal wording is preferred where it reads naturally aloud, semi-formal where warmth helps. See SKILL.md §1 "Register Selection — The Read-Aloud Rule".

### 3. Add a one-line summary for each new section

Append after the existing numbered items in AGENTS.md. One line only.

### 4. Sync the verification script

If the change added or removed a **checkable pattern** (a banned word, an Indonesian form, a brand name, a non-baku spelling), update the matching dict in `scripts/verify-malay-voice.py`:

| Skill section | Script dict |
|---|---|
| §3, §11 contractions and slang | `BANNED` |
| §4d brand capitalisation | `BRANDS` |
| §4c italic policy | `NEEDS_ITALIC` |
| §4f Bahasa Indonesia forms | `INDONESIAN` / `INDONESIAN_AMBIGUOUS` |
| §11c English with BM equivalents | `ENGLISH_WITH_BM` |
| non-baku loanwords | `NON_BAKU` |
| §11e informal register | `INFORMAL` |

Then re-run and confirm the site still passes:

```bash
python scripts/verify-malay-voice.py
```

> ⚠️ **Never ban a word without checking `prpm.dbp.gov.my` first.** `efektif` was wrongly banned on 2026-07-30 and had to be un-banned across four files. Being wrong in this direction costs real rework.

### 5. Update the Sources list

If a new reference site was added, update both the §1 reference table and the Sources list at the bottom of SKILL.md.

Current reference sites: **TrueNetLab.com** (closest style match), **BarakahDigital.com.my**, **Exabytes.my/blog**, **PandaiTech.my** (comparison only, leans casual), **Ecentral.my**, and **DBP** (`prpm.dbp.gov.my`, authoritative, not a style reference).

### 6. Verify

The numbered list in AGENTS.md must match the section count in SKILL.md, and the script must still pass.

## Trigger Conditions

- A new `## N.` section is added to `malay-voice-guide/SKILL.md`
- Sections are renamed or renumbered
- A new pattern table, banned word, or Indonesian form is added
- A new Malaysian reference site is scraped and its patterns recorded

## What NOT to Change

- Do **not** modify the natural formal–semi-formal core patterns (sections 1–8) unless they are explicitly being edited
- Do **not** duplicate full pattern details into AGENTS.md — one-line summaries only
- Do **not** touch the Voice Characteristics table or the Humour section in AGENTS.md
- Do **not** add casual Malay sources; the skill uses natural formal–semi-formal references only
- Do **not** paste the skill's tables into `write-post/SKILL.md` or any workflow. The voice guide is the single home. See the "Where Things Live" table in `.devin/skills/write-post/SKILL.md`.

---

*Corrected 2026-07-30: register phrase updated from "semi-formal" to "natural formal–semi-formal", section count 13 → 14, counting method made explicit, script-sync and DBP-verification steps added. Relocated from the global TSOT rules folder to `.devin/rules/` because this rule is DigiTrust Lab-specific and Devin loads project rules from here.*
