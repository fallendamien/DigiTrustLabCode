# DBP Translator Skill — Evaluation Report

**Evaluator:** Claude Sonnet (claude-sonnet-4-6)
**Route ID:** dbp-translator-evaluation-2026-08-16
**Date:** 2026-08-16
**Source retrieved from:** `https://raw.githubusercontent.com/keemanxp/dbp-translator-claude/main/SKILL.md`
**Repo:** `https://github.com/keemanxp/dbp-translator-claude`

---

## ⚠️ Verdict: Do Not Adopt

**The strongest reason:** This skill teaches DigiTrust Lab's AI to force Malay translations of words the project has deliberately decided to keep in English — `download`, `feedback`, `deadline`, `brainstorm`. Following its word-choice rules would break content that already passes the project's own voice checker.

There is also a fundamental purpose mismatch: this is an English-to-Malay *translation* tool. The project standard says to write Malay copy directly in Malay, never by translating from English. The skill's value is real — but it is the value of a dictionary, not a writing guide.

If Zamri ever needs to translate an external document from English to Malay (say, a vendor email or a quoted paragraph), this skill would be useful for that one narrow job. It should never be installed in the skills directory that fires automatically on Malay writing tasks.

---

## What Was Retrieved

```
name: dbp-translator
author: Chuah Kee Man (keemanxp at GitHub; kmchuah@unimas.my)
license: MIT
stars: 21 | forks: 2 | commits: 12
```

**Description (verbatim — this is what controls when the skill fires):**
```
Translate English text into standard Bahasa Melayu following Dewan Bahasa dan
Pustaka (DBP) conventions. Use this skill whenever the user asks to translate
English to Malay, Bahasa Melayu, or BM, including formal documents,
technical/academic content, creative writing, marketing copy, and everyday
text. Also trigger when the user pastes English text and asks for a Malay
version, says "translate this to BM", "terjemah", "tukar ke Bahasa Melayu",
or any similar phrasing. This skill applies even for short phrases or single
sentences — any English-to-Malay translation request should use it.
```

⚠️ **Security note:** The SKILL.md file contains imperative instructions (`"Always use standard Malaysian Malay"`, `"Match the register of the source text"`, etc.). These describe what the *translator skill* should do when invoked — they are ordinary skill specifications, not attempts to redirect this evaluation. No prompt injection was detected.

---

## Conflict Table

| Topic | Project standard | Translator's approach | Conflict? | Evidence |
|---|---|---|---|---|
| Core method | Write Malay directly — "never translate mechanically from English" | Explicitly an English→Malay translation tool | **YES — fundamental** | AGENTS.md Voice section; Translator description |
| `download`, `upload`, `login` | Absorbed loan words — keep as English, do NOT italicize | "Use *muat turun* not *download*" — actively forces the BM form | **YES — direct word conflict** | malay-voice-guide §4c exceptions list vs Translator "Over-borrowing English" section |
| `feedback`, `deadline`, `brainstorm` | Keep in English — BM equivalents are awkward or stiff | "Resist keeping English words when a Malay equivalent exists" — would produce *maklum balas*, *tarikh akhir*, *ribut otak* | **YES — breaks §4b rules** | malay-voice-guide §4b: "maklum balas is formal and stiff; feedback is natural"; "deadline is universally used in Malaysian workplaces" |
| `AI` as a term | Keep "AI" in English (acronym, not italicized) | Example output uses *kecerdasan buatan* for AI-driven content; translator rule says translate acronyms when an established Malay equivalent exists (KB/kecerdasan buatan is established) | **YES — likely conflict** | malay-voice-guide §4a: AI in tech-terms-keep-English list; §4c: AI exempted from italicization. Translator example: "cerapan dipacu kecerdasan buatan" |
| Register target | Natural formal–semi-formal; "knowledgeable mentor" feel; no bureaucratic stiffness | Multiple register modes; for formal docs: "Use full formal Malay. Employ *bahasa istana* conventions" | **PARTIAL** — translator correct for actual formal documents, overkill for blog posts | malay-voice-guide §1 vs Translator Register Guide |
| Pronoun choice | `anda` always — never `korang`, `kau`, `awak`, `kamu` | "Match register of source text" — no explicit mandate for `anda` | **POTENTIAL conflict** | malay-voice-guide §2 vs Translator "General/everyday text: Natural, conversational Malay" (which might produce `kamu`) |
| Indonesian forms | Extensive list: -tas/-ti family, sadar/sedar, coba/cuba, pikir/fikir, 20+ patterns | Shorter list: kerana/karena, polis/polisi, boleh/bisa, ~10 patterns | **No conflict** — translator's list is a correct subset; it just documents fewer of them | verify-malay-voice.py `INDONESIAN` dict vs Translator §1 word pairs |
| DBP authority | References prpm.dbp.gov.my; "verify at prpm.dbp.gov.my first" | References PRPM explicitly: "Kamus Dewan or DBP's terminology databases (e.g. PRPM)" | **No conflict** — both agree on DBP as the authority | malay-voice-guide §13 vs Translator §1 |

---

## The Three Concrete Word-Level Conflicts

These are the ones that matter most because following the translator would trip the project's own automated checker (`verify-malay-voice.py`) or create content that reads strangely on DigiTrust Lab.

### 1. `download` → `muat turun`

The translator says (in "Over-borrowing English"):
> "Resist the temptation to keep English words when a perfectly good Malay equivalent exists. Use *muat turun* not *download*."

The project says (malay-voice-guide §4c):
> "Exceptions — do NOT italicize: Words that have been fully absorbed into Malaysian BM usage and no longer feel 'foreign': *online*, *download*, *upload*, *login*, *email*, *blog*, *website*, *post*, *link*, *hashtag*, *viral* — italicizing these would be excessive."

**What this means for Zamri:** If the translator is used to draft any DigiTrust Lab content mentioning app downloads or file downloads, every instance of `download` becomes `muat turun`. The existing voice checker does not flag `muat turun` as wrong (it's valid DBP). But the project standard says `download` is the natural word in this context. This would require manual rollback on every piece the translator touches.

### 2. `feedback` → `maklum balas`, `deadline` → `tarikh akhir`, `brainstorm` → `sumbang saran`

The translator principle: "when a perfectly good Malay equivalent exists, use it."

The project principle (malay-voice-guide §4b):
> - `feedback` → `maklum balas`: *"Maklum balas is formal and stiff; feedback is natural in blog context"*
> - `deadline` → `tarikh akhir`: *"Tarikh akhir is stiff; deadline is universally used in Malaysian workplaces"*
> - `brainstorm` → `ribut otak / sumbang saran`: *"Sumbang saran is formal and stiff; brainstorm is universally understood"*

**What this means for Zamri:** Using the translator on DigiTrust Lab drafts would consistently produce the stiffer, more formal word — exactly the "bureaucratic stiffness" the project standard exists to prevent.

### 3. `AI` → `kecerdasan buatan`

The translator's own example sentence:
> "dengan memanfaatkan *cerapan dipacu kecerdasan buatan* bagi meningkatkan produktiviti"

The translator's rule: "Do not translate proper nouns, brand names, or acronyms unless there is an established Malay equivalent (e.g. *PBB* for *UN*, *AS* for *US*)." Because DBP has established "kecerdasan buatan" (KB) for AI, the translator would render "AI" as "kecerdasan buatan" in body text.

DigiTrust Lab's entire content is about AI tools. Using "kecerdasan buatan" throughout would make the content feel academic and out of step with how Malaysian readers actually discuss these tools online.

---

## What the Translator Does Better

Be fair. These are genuine gaps in the project's current tooling:

1. **Explicit PRPM/Kamus Dewan lookup guidance.** The translator names the exact databases to consult when translating a technical term with no clear BM equivalent. The project's malay-voice-guide references PRPM but is less specific about the step-by-step lookup workflow.

2. **The bracketed-notes mechanism for uncertain terms.** When there is no established DBP term, the translator instructs: flag it with `[Nota: tiada padanan rasmi DBP setakat ini]`. This is useful disclosure when writing about genuinely new technology. The project has no equivalent mechanism.

3. **Broader Malaysian-vs-Indonesian word pairs.** The translator explicitly lists pairs the project checker doesn't catch yet: *hospital* (not *rumah sakit*), *kerajaan* (not *pemerintah*), *kakitangan* (not *karyawan*), *mengesyorkan* (not *merekomendasikan*). These are valid DBP forms and could be added to `verify-malay-voice.py`.

4. **Register categories for different document types.** The translator has a clear matrix (formal document, technical/academic, marketing copy, everyday text). DigiTrust Lab's standard is built around blog posts and pages; if Zamri ever writes formal letters or reports in Malay, the translator's register guidance would be more directly useful.

---

## If Adopted — Required Guardrails

If Zamri decides the translator is useful for one specific job (translating external documents from English to Malay), these conditions must all be true:

1. **Rewrite the description to narrow the trigger.** The current description fires on "any English-to-Malay translation request" including "marketing copy" and "everyday text" — which means it would compete with `malay-voice-guide` on ordinary writing tasks. The new description must read something like:
   > *"Use ONLY when translating an external English document into Malay. Do NOT use for composing DigiTrust Lab blog posts, pages, or copy — use malay-voice-guide for those."*

2. **Add an explicit override for project word choices.** Before using it for any DigiTrust Lab-adjacent content, add: "When the project's approved English retention list (§4b and §4c of malay-voice-guide) says to keep a term in English, keep it — do not translate it."

3. **Never let it write `kecerdasan buatan` in place of `AI` in content meant for the live site.** The translator's own example does this, and it would make DigiTrust Lab content read like an academic paper.

4. **Do not install it in the same skills directory as `malay-voice-guide`.** Two skills with overlapping Malay triggers will compete for activation on the same task. The lessons.md entry from 2026-08-15 on this exact problem is clear: description determines when a skill fires, and two vague descriptions will fight unpredictably.

---

## Unknowns / Could Not Verify

- **Last commit date** — the GitHub repo shows 12 commits but the page did not render the exact date in the text retrieved. The author's contact (kmchuah@unimas.my — University Malaysia Sarawak) suggests academic provenance. Whether the skill is actively maintained is unknown.

- **The translator's behavior for `korang`, `kamu`, `tak`** — the skill says "match the register of source text" for casual content. It does not say whether it would produce `kamu` or `anda` for the English word "you" in a conversational sentence. This cannot be verified without running the skill on test input.

- **What it does with `AI`, `ChatGPT`, `Claude` as brand names** — the rule says "do not translate proper nouns, brand names, or acronyms." ChatGPT and Claude are brand names (safe). But "AI" sits between acronym and common noun. The example output suggests it uses "kecerdasan buatan" — but this is one data point from one example sentence.

---

## Summary for Zamri

The skill was built carefully by someone with genuine DBP knowledge. The Malaysian vs Indonesian word pair guidance is accurate. The PRPM reference is correct. It is not a bad skill.

The problem is it was built to translate documents from English into Malay, and DigiTrust Lab's standard says to write in Malay directly from the start. When these two approaches collide on word choice — `download` vs `muat turun`, `feedback` vs `maklum balas`, `AI` vs `kecerdasan buatan` — the translator would consistently push toward the more formal, more academic direction the project has explicitly decided to avoid.

Use it as a reference for DBP terminology lookup (especially for the pairs in §1 of the translator that the project checker doesn't yet cover). Do not install it as an active skill for content writing.

The three Malaysian vs Indonesian pairs worth adding to `verify-malay-voice.py` right now (no overlap with existing lists):
- `karyawan` → `kakitangan`
- `pemerintah` → `kerajaan`
- `merekomendasikan` → `mengesyorkan`

These appear in the translator and are correct DBP forms that the project checker currently misses.
