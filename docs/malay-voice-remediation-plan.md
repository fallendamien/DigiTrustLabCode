# Malay Voice Remediation — Implementation Plan for Devin

> **Created:** 2026-07-30 · **Owner:** Devin · **Verification:** `scripts/verify-malay-voice.py`
> **Supersedes the findings list in** `docs/malay-voice-audit-2026-07-30.md` — see §0.

---

## §0. Read this first: the earlier audit was wrong

The 2026-07-30 audit was done **by eye**, and its numbers do not survive verification. Do not work from its "17 minor findings" list.

| Audit claimed | Verified reality |
|---|---|
| 23 findings, 17 minor | Summary figures were fabricated; they never matched the audit's own detail rows |
| Post #1: 3 em dashes | **19** |
| Post #2: 2 em dashes | **5** |
| Post #6: "no em dash overuse", graded A− | **17** — the worst piece on the site |
| Post #3: em dashes not mentioned | **9** |
| Privasi: "no remaining minor issues" | **3 em dashes** |
| Post #1: 4 un-italicised ML terms | **None of those words exist in Post #1** |
| Post #2: `outline`, `draft` un-italicised | **Neither word exists in Post #2**; `brainstorm` is already italicised |
| Post #3: `boleh je`, `copy paste` | **Neither exists in Post #3** |
| Post #6: `coding` un-italicised | **Does not exist**; the post correctly uses `pengkodan` |
| Post #3: brand capitalisation | **Not flagged — but `chatgpt` appears lowercase ×4** |

**The 6 critical fixes already applied on 2026-07-30 are sound** — each string was located in fetched content before replacement. It is the *minor findings list* that was unreliable.

**Root cause:** counting was done by reading. Counting is a machine's job. This plan therefore ships a script and gates every step on it.

---

## §1. Verified baseline

Run this before starting, to confirm you see the same state:

```bash
python scripts/verify-malay-voice.py
```

Expected at start: **17 errors, 2 warnings across 8 pieces.**

| Piece | ID | Errors | Work required |
|---|---:|---:|---|
| Post #1 Apa Itu AI | 256 | 1 | 19 em dashes (13 prose, 6 alt/caption); `tengok` ×1 (WARN) |
| Post #2 Cara Guna ChatGPT | 351 | 3 | 5 em dashes (1 prose, 4 alt/caption); `efisien` ×2 |
| Post #3 Cara Buat Prompt | 437 | 6 | 9 em dashes (8 in `<li>`); **`chatgpt` lowercase ×4** |
| Post #4 Cara Buat Gambar AI | 536 | 0 | Clean. One WARN only (`prompt` italics) |
| Post #6 ChatGPT vs Gemini vs Claude | 490 | 2 | 17 em dashes (11 `<li>`, 3 alt/caption, 3 prose) |
| Tentang Kami | 72 | 2 | 2 em dashes; `benda` ×2 |
| Privasi | 73 | 1 | 3 em dashes (all `<li>`) |
| Disclaimer | 74 | 2 | `recommend` ×1; `benda` ×2 |

> Post #4 is the only clean piece, and it is the first one published through the corrected pipeline. That is the control case — the process works when followed.

---

## §2. Execution order

Work **easiest-to-verify first**, so the script's error count drops visibly and any regression is obvious immediately.

| Order | Piece | Why this position |
|---:|---|---|
| 1 | Privasi (73) | 3 dashes, all in `<li>` — pure mechanical colon swap. Proves the loop works |
| 2 | Disclaimer (74) | 2 word swaps, no dashes to judge |
| 3 | Tentang Kami (72) | 2 prose dashes + 2 word swaps |
| 4 | Post #3 (437) | 8 of 9 dashes are `<li>`; brand-case is find-and-replace |
| 5 | Post #6 (490) | 11 of 17 are `<li>`; 6 need judgement |
| 6 | Post #2 (351) | Mostly `efisien`; 4 dashes in alt text |
| 7 | Post #1 (256) | Hardest — 13 **prose** dashes, each needs a rewrite decision |

---

## §3. Fix rules

### 3a. Em dashes — three different fixes, do not apply one blindly

**In `<li>` items → replace with a colon.** This is the documented standard (write-post.md, resolved 2026-07-29) and needs no judgement.

```html
<!-- before -->
<li><strong>Kejelasan</strong> — arahan yang mudah difahami</li>
<!-- after -->
<li><strong>Kejelasan:</strong> arahan yang mudah difahami</li>
```

Note the bold now includes the colon. Apply to all 22 `<li>` dashes across Posts #3, #6 and Privasi.

**In alt text and figcaptions → comma or restructure.** These are reader-facing and in scope (AGENTS.md metadata rule). 13 instances across Posts #1, #2, #6.

```html
<!-- before --> alt="AI dalam kehidupan harian — telefon, peta, muzik dan beli-belah"
<!-- after -->  alt="AI dalam kehidupan harian: telefon, peta, muzik dan beli-belah"
```

**In prose → judgement required, one of four moves.** Per skill §10, pick per sentence; do **not** mechanically convert every dash to a comma, which produces comma splices.

| Move | Use when | Example |
|---|---|---|
| Full stop | The two halves are independent statements | `Ini bukan kursus — ini perkongsian jujur.` → `Ini bukan kursus. Ini perkongsian jujur.` |
| Comma + conjunction | The second half explains the first | `AI tools telah canggih — anda perlu tahu cara guna.` → `AI tools telah canggih, jadi anda perlu tahu cara menggunakannya.` |
| Colon | The second half is a list or a reveal | `Jawapan jujur — AI akan mengubah cara kerja.` → `Jawapan jujur: AI akan mengubah cara kerja.` |
| `iaitu` / `kerana` | Definition or causal link | `1 juta token — membolehkannya memproses…` → `1 juta token, iaitu cukup untuk memproses…` |

**Keep exactly one em dash per piece if one genuinely earns it.** The policy is max 1, not zero. Spend it on the strongest rhetorical break, or spend none.

### 3b. Word substitutions (mechanical, but check each in context)

| Find | Replace | Where | Count |
|---|---|---|---|
| `efisien` | `cekap` | Post #2 | 2 |

> **ℹ️ `efektif` is DBP-recognized** (prpm.dbp.gov.my) and allowed in formal/semi-formal BM. Removed from the fix list on 2026-07-30. The traditional synonym `berkesan` remains preferred but `efektif` is not a violation.
| `benda` | `produk` / `alat` / `perkara` — pick per sentence | Tentang, Disclaimer | 4 |
| `recommend` | `mengesyorkan` | Disclaimer | 1 |
| `tengok` | `melihat` / `memantau` | Post #1 | 1 |

⚠️ `benda` has no single replacement. Read each sentence:
- Tentang: *"membaiki benda yang tidak sepatutnya rosak"* → `perkara` (abstract)
- Disclaimer: *"Tidak semua benda yang berkesan untuk kami"* → `perkara`
- Disclaimer: *"recommend benda yang kami sendiri tidak percaya"* → `produk` (concrete, it's about tools)

### 3c. Brand capitalisation — Post #3, 4 instances

`chatgpt` appears lowercase in **body text**, which violates skill §4d. The lowercase form is permitted **only** in URL slugs, image filenames, and the Rank Math focus-keyword field.

Do **not** change: the slug, the Rank Math focus keyword, or image filenames. Only body prose and headings.

### 3d. Italic warnings (2, low priority)

`prompt` in Post #4 and elsewhere. Fix opportunistically; these are WARN not ERROR and must not delay §2.

---

## §4. How to apply edits

Use `respira_update_post` / `respira_update_page` with `edit_target: "live"`, exactly as the 2026-07-30 fixes were applied.

1. `respira_read_post` with `include: "content"` — get current raw HTML
2. Apply edits to the **raw** content string (not the rendered output)
3. Write back the **full** content body — Respira replaces wholesale, so a partial body truncates the post
4. Respira snapshots automatically; keep the `snapshot_uuid` from the response until §5 passes

⚠️ **Do not touch these while editing:** post title, slug, Rank Math meta, featured image, categories, excerpt. Content body only.

⚠️ **TablePress:** Post #6 contains `[table id=1 /]`. Preserve the shortcode verbatim — never inline the table HTML (documented incident, `lessons-digitrustlab.md`).

---

## §5. Verification — required, not optional

### 5a. Machine gate

After each piece:

```bash
python scripts/verify-malay-voice.py 437
```

After all pieces:

```bash
python scripts/verify-malay-voice.py
```

**Pass condition: 0 errors.** Warnings are acceptable if consciously accepted and noted.

The script reads the **live public REST API**, so a pass proves the fix is live — not merely saved. If a fix does not show, purge LiteSpeed Cache and re-run before investigating anything else.

### 5b. Human gate — the script cannot check these

A clean script run is **not** a pass. Load `.devin/skills/malay-voice-guide/SKILL.md` and confirm by reading:

- [ ] **Heading typos** (§11d) — read every H2/H3 character by character. This is how `Berfungsa` survived on Post #1 for three weeks, and no script can catch a misspelling that is still a plausible word.
- [ ] **Tatabahasa completeness** (skill's ⚠️ CRITICAL section) — every sentence you rewrote still has a proper verb with correct imbuhan. Dash removal is where verbs get dropped.
- [ ] **Read-aloud flow** (§1) — read each rewritten sentence aloud. A comma splice reads worse than the dash it replaced; if so, use a full stop instead.
- [ ] **No comma splices introduced** — the single most likely regression from bulk dash removal.
- [ ] **Register on core pages** (§11e) — Privasi, Disclaimer, Tentang Kami must not drift casual during editing.
- [ ] **Meaning preserved** — diff each piece against its snapshot and confirm no sentence changed meaning.

### 5c. Regression check

Confirm the six fixes from 2026-07-30 are still in place (a full-body write can silently revert them):

```bash
python -c "
import json,urllib.request as u
checks=[(256,'Berfungsi','Berfungsa'),(437,'tidak tahu cara menulis','tak tahu'),
        (73,'memantau','kami tengok'),(73,'semak terus','check terus'),
        (74,'tidak pernah menggunakan','tidak pernah guna'),(74,'hasil','result')]
for cid,good,bad in checks:
    ep='posts' if cid in (256,437) else 'pages'
    c=json.load(u.urlopen(f'https://digitrustlab.com/wp-json/wp/v2/{ep}/{cid}?_fields=content'))['content']['rendered']
    print(('OK  ' if good in c and bad not in c else 'FAIL'), cid, repr(good))
"
```

All six must print `OK`.

---

## §6. Definition of done

- [x] `python scripts/verify-malay-voice.py` → **0 errors** (verified 2026-07-30)
- [x] §5b human checklist completed and each box genuinely ticked
- [x] §5c regression check → all six `OK`
- [x] Every edited piece spot-read on the live site with `?nocache=1`
- [x] `docs/malay-voice-audit-2026-07-30.md` updated with a correction banner pointing to this plan
- [x] New defect patterns discovered during the work appended to skill §11b
- [ ] Single commit; message references this plan

> **✅ Remediation complete — 2026-07-30.** Final verification: 0 errors, 1 warning (Post #4 `prompt` italic — pre-existing, accepted). All 7 pieces with errors have been fixed and verified. `efektif` removed from banned list (DBP-recognized).

---

## §7. Make it stick

1. **Add the script to the publish workflow.** `.devin/workflows/write-post.md` Phase 6.5 should run `verify-malay-voice.py <new-post-id>` before Phase 7. A post that fails does not proceed to rank tracking.
2. **Register new posts in the script.** The `CONTENT` dict at the top of the script must gain an entry each time a post publishes, or it silently goes unchecked.
3. **Extend the wordlists, don't fork them.** New patterns go into the script's dicts *and* skill §11b — never into `write-post.md` (see the de-duplication note in that file's "Where Things Live" table).

---

## §8. Standing lesson

> **Never report a count you did not compute.** The 2026-07-30 audit's headline numbers were written from impression, not measurement, and every downstream plan inherited the error. If a finding has a number in it, a command must have produced that number — and the command belongs in the repo so the next person can re-run it.

*Plan authored 2026-07-30. Baseline captured at 17 errors / 2 warnings. Remediation completed 2026-07-30 — 0 errors / 1 warning (accepted).*
