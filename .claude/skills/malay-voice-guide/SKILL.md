---
name: malay-voice-guide
description: "Natural formal-to-semi-formal Bahasa Melayu writing standard for DigiTrust Lab, plus the mechanical and naturalness gates that enforce it. Use on ANY task involving writing, editing, reviewing, or PUBLISHING Malay content (blog posts, pages, copy, CTA text, alt text, meta). Ships automated checkers at scripts/verify-malay-voice.py and scripts/verify-malay-naturalness.py. Enforces DBP-aligned spelling/grammar, blocks Bahasa Indonesia forms, anti-salesy tone, and red-phrase avoidance. Reference style: PandaiTech.my, Ecentral.my."
---

# Malay Voice Guide — Natural Formal–Semi-Formal Bahasa Melayu Standard

**Trigger:** ANY task involving writing, editing, or reviewing Malay content (blog posts, pages, copy, CTA text).

**Full voice rules:** See `AGENTS.md` § "DigiTrust Lab Writing Voice" for core voice characteristics, anti-salesy policy, and red flag phrases.

**Reference style:** PandaiTech.my, Ecentral.my — professional but accessible, not textbook-dry.

**Authoritative reference:** Dewan Bahasa dan Pustaka (DBP) — `dbp.gov.my/pedoman-dan-panduan-bahasa-melayu/` for spelling, grammar, and formal BM standards.

---

## 🚦 PUBLISH GATE — run both halves before any post goes live

### Naturalness evidence gate (hard block)

`scripts/verify-malay-naturalness.py` is the hard publication gate for wording
that may be grammatically valid but still sound translated, bureaucratic, or
unnatural to a Malaysian reader. It uses the rules in
`content/malay-naturalness-rules.json` and validates a review artifact in
`content/naturalness-reviews/<post-slug>.json`.

Two independent fresh reviews must cover the same final content: one
Claude/Anthropic review and one OpenAI review. Both must mark every
document-level and segment-level checklist item true with `confidence:
"high"`. Any finding, uncertainty, disagreement, missing segment, missing
required family, or content-hash mismatch blocks publication. Fix the copy,
create a new hash, and rerun both reviews from scratch.

```bash
# before publishing the final local HTML
python scripts/verify-malay-naturalness.py \
  --file content/drafts/<post-slug>.html \
  --review content/naturalness-reviews/<post-slug>.json
```

The review checklist covers natural usage, literal translations, bureaucratic
stiffness, technical-term choice, read-aloud clarity, and consistency. The
artifact protocol and JSON shape are documented in
`content/naturalness-reviews/README.md`. The confirmed regression
`alasan sopan` is an example of why a simple grammar or spelling pass is not
enough.

### Mechanical voice gate

**`scripts/verify-malay-voice.py` is the mechanical half of this skill.** Run it on every piece before the live verification step. It fails the build on defects that are countable, so your attention is free for the ones that are not. The naturalness evidence gate above is a separate hard requirement.

```bash
# after publishing to WordPress, before rank tracking:
python scripts/verify-malay-voice.py <post-id>

# whole site:
python scripts/verify-malay-voice.py
```

**Pass condition: 0 errors.** Exit code is 1 on any error, 0 on clean, so it can gate a pipeline. It reads the **live public REST API**, so a pass proves the fix is live — not merely saved. If a fix does not show, purge LiteSpeed Cache and re-run before investigating anything else.

### ⚠️ Register every new post, or it is silently never checked

The script only checks IDs listed in its `CONTENT` dict. **When a post publishes, add it:**

```python
CONTENT = {
    ...
    599: ("Post #7  <short title>", "posts"),   # <- add this line
}
```

A post that is not registered will never fail, which reads exactly like passing. This is the single easiest way for the gate to rot.

### What the script checks (so you don't re-check by hand)

em dashes (split by prose / `<li>` / alt-text) · banned contractions · non-baku loanwords · Bahasa Indonesia forms (§4f) · English where a BM word exists (§11c) · informal register, hard error on core pages (§11e) · brand capitalisation (§4d) · italic policy (§4c)

### What the mechanical checker CANNOT check

A clean mechanical run is **not** a naturalness pass. The two-model review
artifact above is mandatory; use this checklist to prepare the content before
creating that artifact and to investigate any reviewer disagreement. Read for:

- [ ] **Heading typos** (§11d) — character by character. `Berfungsa` survived three weeks live; no script catches a misspelling that is still a plausible word.
- [ ] **Tatabahasa completeness** (⚠️ CRITICAL section below) — every sentence has a proper verb with correct imbuhan.
- [ ] **Sentence fragments** — especially after removing punctuation. A `jika…` / `apabila…` clause ended with a full stop leaves a dangling subordinate clause. Found live on Tentang Kami, 2026-07-30: *"Jadi jika anda ingin… membayar designer mahal. Anda berada di tempat yang betul."* — grammatically broken, perfectly spelled, invisible to the script.
- [ ] **Comma splices** — the most likely regression from bulk em-dash removal.
- [ ] **Read-aloud flow** (§1) — if a rewritten sentence reads worse than what it replaced, use a full stop instead.
- [ ] **Register on core pages** (§11e) — Privasi / Disclaimer / Tentang Kami.

### Extending the checks

Mechanical defect patterns go into **both** the script's dicts **and** the relevant table in this file. Naturalness regressions go into `content/malay-naturalness-rules.json` and a test in `tests/`. Never add a naturalness phrase to only a document or only a prompt — the regression must be executable.

> **Do not ban a word without verifying it at `prpm.dbp.gov.my` first.** `efektif` was wrongly banned on 2026-07-30 and had to be un-banned across four files. Being wrong in this direction costs real rework.

---

## The Standard

DigiTrust Lab uses **natural formal–semi-formal Bahasa Melayu** — proper baku (standard Malay), grammatically correct, polished, clear, and accessible. The register may move between formal and semi-formal according to context. Formal constructions are welcome when they sound natural aloud; semi-formal phrasing provides warmth and approachability. Avoid both casual slang and bureaucratic or academic stiffness. Think of a knowledgeable mentor who speaks carefully without sounding distant.

## ⚠️ CRITICAL — Tatabahasa & Sentence Completeness (MOST IMPORTANT RULE)

**Every Malay sentence MUST have complete tatabahasa (grammar) — especially a proper verb.** A sentence missing its verb sounds stagnant, broken, and unnatural when read aloud. This is the single most common quality issue in Malay content.

**The principle:** A sentence that is grammatically complete flows naturally. A sentence with missing verbs or loose structure sounds like casual speech transcribed — not polished writing.

| ❌ Incomplete (missing verb / loose structure) | ✅ Complete (proper tatabahasa) | What was missing |
|---|---|---|
| `Kerja yang banyak proses ulang-ulang` | `Kerja yang banyak melibatkan proses berulang` | Missing verb `melibatkan` + standard BM `berulang` |
| `Cuma anda tidak perasan` | `Cuma anda mungkin tidak menyedarinya` | `perasan` is colloquial; `menyedarinya` is proper verb form |
| `Soalan ini yang ramai orang risau` | `Soalan inilah yang menjadi kebimbangan ramai orang` | Missing verb `menjadi`; sentence was incomplete |
| `Ini yang ramai orang tidak perasan` | `Ini yang ramai orang tidak sedari` | `perasan` → `sedari` (proper verb form) |

**Checklist before publishing any Malay sentence:**
1. Does it have a clear subject and verb (subjek + kata kerja)?
2. Does it flow smoothly when read aloud, or does it feel stagnant?
3. Is the verb in the correct form (imbuhan: `meN-`, `ber-`, `di-`, etc.)?
4. Are there any colloquial words that should be standard BM?
5. Does the sentence connect naturally to the next one?

**Core rule:** If a sentence feels stagnant or choppy when read aloud, it likely has a missing verb or incorrect tatabahasa. Fix the grammar first, then check the register. Never sacrifice grammatical completeness for brevity.

### "Malaysia" Usage — Less Is More

**Do not insert "Malaysia", "rakyat Malaysia", or "warga Malaysia" into copy unless the context specifically requires it** (e.g., a keyword target like "AI tools Malaysia"). The audience is already Malaysian — repeatedly saying "Malaysia" sounds bombastic, unnatural, and like SEO padding.

| ❌ Avoid | ✅ Prefer |
|---|---|
| `Blog AI Malaysia - Artikel AI...` | `Blog AI - Artikel AI...` |
| `untuk rakyat Malaysia` | `untuk anda` or just drop it |
| `AI tools yang digunakan di Malaysia` | `AI tools yang anda guna setiap hari` |
| `Panduan AI untuk warga Malaysia` | `Panduan AI untuk pemula` |

**Rule:** If removing "Malaysia" doesn't change the meaning, remove it. The .my domain, Malay language, and local context already signal the audience.

### Strategic Comma Usage — Natural Breathing Pauses

**Use commas creatively to create natural stop points within longer sentences.** A sentence that runs straight from start to finish without a pause feels breathless and monotonous. A well-placed comma gives the reader (and the read-aloud voice) a moment to breathe, emphasises the pivot point, and makes the sentence feel more deliberate.

| ❌ No pause (flat, breathless) | ✅ With strategic comma (natural rhythm) | Why the comma works |
|---|---|---|
| `Jadi soalannya bukan "adakah AI akan menggantikan saya?"` | `Jadi persoalannya, bukan "adakah AI akan menggantikan saya?"` | Comma after `persoalannya` creates a dramatic pause before the contrast |
| `Tetapi kerja yang memerlukan human touch empati kreativiti pertimbangan AI masih jauh` | `Tetapi kerja yang memerlukan human touch, empati, kreativiti, pertimbangan, AI masih jauh` | Commas separate the list items and create rhythm |
| `Jawapan jujur AI akan mengubah cara kerja dilakukan` | `Jawapan jujur: AI akan mengubah cara kerja dilakukan` | Colon (or comma) creates a reveal pause after the label |

**Principle:** Read the sentence aloud. If you naturally pause mid-sentence, that's where a comma belongs. If the sentence runs flat without any pause point, find the natural break and add a comma there.

**Common comma opportunities in Malay:**
- After transitional words: `Jadi,`, `Tetapi,`, `Namun,`, `Sebenarnya,`
- Before contrast or pivot: `persoalannya, bukan...`
- After introductory phrases: `Dalam kehidupan harian, AI...`
- In lists: `empati, kreativiti, pertimbangan`
- Before explanatory clauses: `kerana ia, sebenarnya, hanya...`

**Core rule:** A sentence without any comma is often a sentence that needs one. Don't let sentences run flat — give them natural breathing room.

## 1. Natural Formal–Semi-Formal BM Standard — Definition & References

The standard is a spectrum, not a fixed midpoint. Choose the most natural register for each sentence while preserving correct grammar, clarity, and consistency. A fully formal sentence is not automatically too formal. Reject it only when it sounds bureaucratic, academic, translated, or unnatural in context.

| Trait | Casual (do NOT use) | Natural formal–semi-formal (use) | Bureaucratic/academic (do NOT use) |
|------|----------------------|----------------------------------|------------------------------------|
| Pronoun | `korang`, `kau` | `anda`, `kami`, `beliau` | Impersonal references where direct address is clearer |
| Negation | `tak`, `takleh` | `tidak`, `bukan` | Unnecessarily emphatic or legalistic negatives |
| Filler | `confirm`, `gila`, `je` | Remove or use a precise equivalent | Empty formal padding |
| Sentence | Short, slangy, incomplete | Complete and polished; formal where natural, semi-formal where warmer | Long clauses, nominalisation, and official-sounding padding |
| Tone | Like an unedited chat message | Like a knowledgeable Malaysian mentor | Like a government circular or academic paper |

### Register Selection — The Read-Aloud Rule

Read every sentence aloud before simplifying it. Prefer the version that is grammatically correct, precise, immediately clear, and natural in the surrounding paragraph.

**Decision order:**
1. Preserve the intended meaning accurately.
2. Follow standard DBP spelling and grammar.
3. Choose the version that sounds most natural when read aloud by a Malaysian speaker.
4. Keep it clear to a general reader on the first reading.
5. Match the rhythm and register of the surrounding paragraph.

| Preferred | Avoid mechanically flattening to | Why |
|---|---|---|
| `Tanpa memerlukan kefahaman konsep matematik yang rumit` | `Tanpa perlu faham matematik yang rumit` | The formal construction is precise, smooth, and natural aloud; the shorter version is not automatically better. |

**Core rule:** Simplify bureaucratic or academic wording, not good formal Malay. Never downgrade a natural formal sentence merely to make it “more semi-formal.”

### Concrete Before → After Examples (from Post #1 editing session)

These real edits show the pattern: elevate casual phrasing to natural formal when it sounds more complete aloud, but leave intentionally punchy or humorous sentences as-is.

| ❌ Casual (before) | ✅ Natural formal (after) | Pattern |
|---|---|---|
| `Cuma anda tidak perasan.` | `Cuma anda mungkin tidak menyedarinya.` | `tidak perasan` → `tidak menyedarinya` |
| `Lama-lama dia akan kenal mana gambar kucing` | `Lama-lama dia akan dapat mengenal pasti mana gambar kucing` | `kenal` → `mengenal pasti` |
| `Kita tidak perasan kerana ia melakukan kerja` | `Kita tidak menyedarinya kerana ia melakukan kerja` | `tidak perasan` → `tidak menyedarinya` |
| `Filem sains fiksyen membuat kita berasa takut` | `Filem sains fiksyen sering menimbulkan rasa takut` | `membuat kita berasa` → `menimbulkan rasa` |
| `AI sekarang tidak ada "kesedaran"` | `AI sekarang tidak mempunyai "kesedaran"` | `tidak ada` → `tidak mempunyai` |
| `Ia tidak ada perasaan.` | `Ia tidak mempunyai perasaan.` | `tidak ada` → `tidak mempunyai` |
| `Ia hanya ikut arahan dengan sangat pantas.` | `Ia hanya mengikut arahan dengan sangat pantas.` | `ikut` → `mengikut` |
| `Soalan ini yang ramai orang risau.` | `Soalan inilah yang menjadi kebimbangan ramai orang.` | Incomplete → complete sentence |
| `Tengok bagaimana ia menjawab.` | `Lihat bagaimana ia menjawab.` | `Tengok` → `Lihat` |
| `anda akan jumpa cara guna AI` | `anda akan menemui cara guna AI` | `jumpa` → `menemui` |
| `Apabila anda buka YouTube` | `Apabila anda membuka YouTube` | `buka` → `membuka` |
| `Ini yang ramai orang tidak perasan` | `Ini yang ramai orang tidak sedari` | `tidak perasan` → `tidak sedari` |

**Leave as-is (intentionally casual for humour/punchiness):**
- `Jangan expect definisi textbook di sini.` — humour
- `Itu sahaja.` — punchy, deliberate
- `Netflix mencadangkan drama? AI. Spotify mencadangkan playlist? AI juga.` — staccato rhythm
- `(Seperti intern yang cekap sangat tetapi tidak pernah meminta naik gaji.)` — humour
- `Tidak perlu kursus mahal. Tidak perlu background IT. Cuma perlu curiosity dan keinginan untuk mencuba.` — parallel punchy structure

**Reference sites (studied for style patterns):**

| Site | Style | Why it's a good reference | URL |
|------|-------|--------------------------|-----|
| **TrueNetLab.com** (Malay section) | Formal-but-natural tech writing | Best match for DigiTrust Lab's target style. Polished BM with complete tatabahasa, strategic commas, engaging openers, and natural flow. Writes about deep tech (ASML, semiconductors) in accessible formal Malay. | `truenetlab.com/ms/blog/` |
| **BarakahDigital.com.my** | Natural formal–semi-formal mix | Good example of mixing registers naturally. Uses dashes and commas for rhythm. Formal BM with conversational warmth — exactly the spectrum DigiTrust Lab targets. | `barakahdigital.com.my` |
| **Exabytes.my/blog** (BM section) | Formal business tech writing | Clean, grammatically complete BM for business/tech audience. Good reference for how to write about products and services in formal Malay without sounding like a press release. | `exabytes.my/blog/` (filter BM) |
| **PandaiTech.my** | Semi-formal AI tech blog | Closest to DigiTrust Lab's niche (AI/tech). Leans more casual than our standard — use as a comparison reference, not a style target. Good for seeing how English tech terms are integrated in BM. | `pandaitech.my/blog/` |
| **Ecentral.my** | Formal educational BM | Good reference for grammar structure and formal BM conventions. More textbook-oriented than our target, but useful for tatabahasa patterns. | `ecentral.my` |
| **Dewan Bahasa dan Pustaka** | Authoritative BM reference | Not a style reference — use for spelling, grammar, and formal BM standards verification. | `dbp.gov.my/pedoman-dan-panduan-bahasa-melayu/` |

**What to study from each site:**
- **TrueNetLab**: How they open articles with engaging hooks in formal BM; how complex tech concepts are explained without dumbing down the language
- **BarakahDigital**: How they mix formal and semi-formal within the same article; how dashes and commas create rhythm
- **Exabytes**: How product/business content stays formal without becoming a press release
- **PandaiTech**: How English tech terms are naturally integrated (italicized in BM sentences)
- **Ecentral**: How to structure formal BM sentences with complete tatabahasa

**Academic backing:** A UPM study (NEMD v2.0) found that blogs using "bahasa Melayu yang sempurna dan kurang menggunakan unsur bahasa kasar/slanga, campur kod, alih kod dan singkatan" are significantly more engaging to readers than blogs using casual/colloquial Malay. This confirms that proper BM with complete grammar is not just correct — it's what readers actually prefer.

## 2. Pronoun & Address

| ❌ Casual (do NOT use) | ✅ Approved formal–semi-formal | Context |
|---|---|---|
| `korang` | `anda` | Addressing the reader |
| `kita` (inclusive) | `kami` (company voice) | When DigiTrust Lab speaks as a brand |
| `dia` (for people) | `beliau` | Referencing professionals/experts |
| `dia` (for things) | `ia` | Referencing objects/concepts |
| `korang semua` | `anda semua` or just `anda` | Addressing multiple readers |

**Rule:** Always use `anda` for the reader. Use `kami` when DigiTrust Lab speaks collectively. Use `beliau` for named professionals. Never use `korang`, `kau`, `awak` in any content.

## 3. Full Forms vs Contractions

Natural formal–semi-formal BM uses full forms. Contractions are a casual register marker and should not appear in DigiTrust Lab content.

| ❌ Casual contraction | ✅ Standard full form | Notes |
|---|---|---|
| `tak` | `tidak` | Always use full form |
| `takleh` | `tidak boleh` | Always use full form |
| `dah` | `sudah` or `telah` | Use the form that best matches the sentence and intended time reference |
| `tu` | `tersebut` or `itu` | `tersebut` for specific references, `itu` for general |
| `ni` | `ini` | Always use full form |
| `sebab` | `kerana` or `sebab` | `kerana` in formal sections, `sebab` acceptable in conversational passages |
| `macam` | `seperti` or `macam` | `seperti` in formal sections, `macam` acceptable in examples |
| `bila` | `apabila` | Use `apabila` in polished prose |
| `nak` | `akan` or `hendak` | Use `akan` for future, `hendak` for intention |

**Rule:** Default to full forms. `sebab` and `macam` may appear in deliberately conversational passages, but prefer `kerana` and `seperti` when they read more smoothly. Always use full forms such as `tidak`, `sudah`, `ini`, `itu`, and `apabila`.

## 4. Code-Switching Rules

English tech terms stay in English. Common nouns and verbs use BM. No slang code-switching.

### 4a. Tech Terms — Keep in English

| ✅ Keep in English | ✅ Use BM | ❌ Slang code-switching (do NOT use) |
|---|---|---|
| AI, ChatGPT, API, tools | kandungan (content) | `confirm` |
| prompt, template, dashboard | perniagaan (business) | `gila` |
| login, download, upload | pemasaran (marketing) | `je` (as filler) |
| software, hardware | pengguna (user) | `kat sini` |
| email, website, blog | tetapan (settings) | `macam mana` (use `bagaimana`) |

**Rule:** Established tech terms (AI, ChatGPT, API, prompt, tools) stay in English — do not translate them. Common nouns that have standard BM equivalents should use BM (`kandungan`, `perniagaan`, `pemasaran`). Slang English words used as Malay fillers (`confirm`, `gila`, `je`, `kat sini`) must be replaced with proper BM equivalents.

### 4b. English Retention — Awkward BM Translations

Some English terms have BM translations that sound unnatural, funny, or awkward in context. For these, **retain the English term** — it reads more naturally to a Malaysian audience.

| ✅ Keep in English | ❌ Awkward BM translation | Why |
|---|---|---|
| copy & paste | salin & tampal | Sounds comical — Malaysians universally say "copy & paste" |
| drag & drop | seret & lepas | Sounds unnatural — no Malaysian uses this in practice |
| brainstorm | ribut otak / sumbang saran | "Sumbang saran" is formal and stiff; "brainstorm" is universally understood |
| shopping | membeli-belah | OK in formal writing, but "shopping" is natural in conversational blog posts |
| install | pasang | "Pasang" is ambiguous (could mean "set up"); "install" is clearer for tech context |
| background (design) | latar belakang | "Latar belakang" is fine for people's backgrounds, but for UI/design context, "background" is clearer |
| feedback | maklum balas | "Maklum balas" is formal; "feedback" is natural in blog context |
| deadline | tarikh akhir | "Tarikh akhir" is stiff; "deadline" is universally used in Malaysian workplaces |
| request | permintaan | "Permintaan" can mean demand; "request" is clearer for asking someone to do something |
| draft | draf | Both acceptable — "draf" is fine, but "draft" is also natural |

**Rule:** When a BM translation sounds awkward, funny, or less clear than the English original, retain the English term. Malaysian readers are accustomed to English tech terms mixed into BM — this is natural code-switching, not slang. The goal is clarity and natural reading flow, not forced translation.

### 4c. Italic Policy for English Terms

When using English terms within BM sentences, **italicize them** so readers can visually distinguish code-switching. This signals intentionality — the English term is a deliberate choice, not a mistake.

| ✅ Correct (italicized) | ❌ Incorrect (not italicized) |
|---|---|
| Anda boleh _brainstorm_ idea menggunakan ChatGPT. | Anda boleh brainstorm idea menggunakan ChatGPT. |
| Jangan _copy & paste_ maklumat peribadi. | Jangan copy & paste maklumat peribadi. |
| _Deadline_ untuk projek ini esok. | Deadline untuk projek ini esok. |
| Kami perlukan _feedback_ anda. | Kami perlukan feedback anda. |

**Exceptions — do NOT italicize:**
- Established tech proper nouns: AI, ChatGPT, Claude, API, Google Maps, Waze, Netflix, Spotify, WhatsApp, YouTube, Lazada, Shopee — these are brand/product names, not code-switching
- Acronyms that are universally used: AI, API, URL, HTML, CSS
- Words that have been fully absorbed into Malaysian BM usage and no longer feel "foreign": _online_, _download_, _upload_, _login_, _email_, _blog_, _website_, _post_, _link_, _hashtag_, _viral_ — italicizing these would be excessive

**Rule:** Italicize English verbs, adjectives, and informal terms that are code-switched into BM sentences (_brainstorm_, _copy & paste_, _drag & drop_, _shopping_, _feedback_, _deadline_, _request_, _install_, _draft_). Do NOT italicize brand names, acronyms, or fully absorbed loan words.

### 4d. Brand Name Capitalization (MANDATORY)

Brand names and product names must ALWAYS use their official capitalization in body text. Never write them in lowercase — even when the focus keyword is lowercase for SEO purposes. The Rank Math focus keyword field stays lowercase (matching search queries), but the actual content text must use proper brand capitalization.

| Brand | ✅ Correct | ❌ Wrong |
|-------|-----------|----------|
| ChatGPT | ChatGPT | chatgpt, Chatgpt |
| Gemini | Gemini | gemini |
| Claude | Claude | claude |
| OpenAI | OpenAI | openai |
| Google | Google | google |
| Microsoft | Microsoft | microsoft |
| Canva | Canva | canva |
| Notion | Notion | notion |
| Midjourney | Midjourney | midjourney |
| DALL-E | DALL-E | dall-e |
| Netflix | Netflix | netflix |
| Spotify | Spotify | spotify |
| WhatsApp | WhatsApp | whatsapp |
| YouTube | YouTube | youtube |
| Shopee | Shopee | shopee |
| Lazada | Lazada | lazada |

**Rule:** ALWAYS capitalize brand names in content. The only place brand names appear lowercase is in: (1) URL slugs, (2) image filenames, (3) Rank Math focus keyword field. Everywhere else in the article body, headings, captions, and alt text — use official brand capitalization.

### 4e. Word Choice — "Jika" not "Kalau" (MANDATORY)

Use **Jika** (formal/semi-formal) instead of **Kalau** (informal/colloquial) for conditional sentences. DigiTrust Lab uses a semi-formal register — "Kalau" is too casual for written content.

| ✅ Correct | ❌ Wrong |
|-----------|----------|
| Jika anda perlukan AI... | Kalau anda perlukan AI... |
| Jika anda pelajar... | Kalau anda pelajar... |
| Jika anda baru bermula... | Kalau anda baru bermula... |

**Rule:** ALWAYS use "Jika" in all written content. "Kalau" is spoken/informal Malay and does not match the DigiTrust Lab semi-formal register. Scan for "Kalau" during proofreading and replace with "Jika".

### 4f. Bahasa Indonesia vs Bahasa Melayu (MANDATORY — added 2026-07-30)

**AI models routinely emit Indonesian forms when asked for Malay.** The two languages share most vocabulary, so an Indonesian word inside Malay prose does not look like an error — it looks like a slightly odd word choice. That is what makes this class of defect dangerous: it survives proofreading.

This was found live on 2026-07-30: `mencoba` had been sitting in Post #1 since publication, and **this very skill file was teaching `menyadarinya` in three separate example tables** — an Indonesian form presented as the correct target.

#### Systematic pattern 1 — the `-tas` / `-ti` suffix

Indonesian takes `-tas`; Malay takes `-ti`. This is the single highest-yield check.

| ❌ Indonesian | ✅ Malay |
|---|---|
| aktivitas | aktiviti |
| kualitas | kualiti |
| komunitas | komuniti |
| identitas | identiti |
| realitas | realiti |
| universitas | universiti |
| fasilitas | fasiliti / kemudahan |
| prioritas | prioriti / keutamaan |
| kreativitas | kreativiti |
| produktivitas | produktiviti |

#### Systematic pattern 2 — root-vowel families

| ❌ Indonesian root | ✅ Malay root | Derived forms |
|---|---|---|
| sadar | **sedar** | menyedari, kesedaran, menyedarinya |
| coba | **cuba** | mencuba, dicuba, percubaan |
| pikir | **fikir** | fikiran, memikirkan, pemikiran |

#### Common Indonesian-only words

| ❌ Indonesian | ✅ Malay |
|---|---|
| bisa | boleh |
| butuh / membutuhkan | perlu / memerlukan |
| karena | kerana |
| kayak | seperti |
| gimana | bagaimana |
| nggak / enggak / gak | tidak |
| banget | sangat |
| bikin / membikin | buat / membuat |
| mobil | kereta |
| kantor | pejabat |

> ⚠️ **`bisa` is a real Malay word** — it means *venom* (`bisa ular`). Flagging it assumes the AI-writing sense of "can", which is Indonesian. Check the sentence before replacing; do not blind-swap.

#### Spelling variants

| ❌ Indonesian | ✅ Malay |
|---|---|
| resiko | risiko |
| praktek | praktik |
| silahkan | sila |
| ijin | izin |
| nasehat | nasihat |
| merubah | mengubah |

**Rule:** treat any Indonesian form as a hard error, not a stylistic preference. `scripts/verify-malay-voice.py` checks the list above automatically — but it can only catch words already in the list. When you meet a new one, add it to **both** the script's `INDONESIAN` dict and this table.

> **Do not over-extend this list.** Many words are valid in both languages (`paham`/`faham`, `kamu`, `sekarang`, `jam`), and `efektif` was wrongly banned on 2026-07-30 before DBP confirmed it is valid Malay. Verify against `prpm.dbp.gov.my` before adding anything here.

## 5. Sentence Structure — Complete Every Thought

Every general statement needs concrete examples. No hanging claims. No vague promises.

| ❌ Hanging / vague | ✅ Complete with examples |
|---|---|
| `AI telah mengubah banyak perkara.` (then moves on) | `AI telah mengubah banyak perkara — cara kita bekerja, cara kita menghasilkan kandungan, cara kita mencari maklumat.` |
| `Anda boleh guna AI untuk banyak benda.` | `Anda boleh guna AI untuk banyak perkara — menulis emel, membuat ringkasan, mencari idea, dan pelbagai lagi.` |
| `Ini akan membantu anda.` | `Ini sangat membantu jika anda sering menghadapi kesukaran untuk memulakan penulisan.` |

**Rule:** After any general statement, ask "seperti apa?" or "contohnya?" — if the answer isn't in the next sentence, add it.

## 6. Opening Lines — Hook Without Textbook Intros

Never start with a formal definition or "dalam artikel ini". Hook with a relatable scenario, question, or observation — but in proper BM.

| ❌ Textbook opener | ✅ Natural formal–semi-formal hook |
|---|---|
| `AI bermaksud Artificial Intelligence, atau dalam Bahasa Melayu, Kecerdasan Buatan.` | `Pernahkah anda tertanya-tanya apa sebenarnya AI dan bagaimana ia berfungsi?` |
| `Dalam artikel ini, kami akan membincangkan...` | `Mari kita lihat bagaimana AI boleh membantu kerja harian anda.` |
| `Terdapat banyak tools AI yang tersedia...` | `Banyak alat AI tersedia hari ini, tetapi ini yang paling berguna untuk bermula:` |

**Rule:** Start with a question, a relatable scenario, or jump straight into the point. Never start with a dictionary definition or a "dalam artikel ini" preamble.

## 7. Transitions — Clear and Professional

Natural formal–semi-formal BM uses transitions according to context. Prefer polished formal transitions in explanatory sections; conversational transitions may be used selectively where they improve warmth without becoming slang.

| Formal transition (use in formal sections) | Conversational transition (OK in blog posts) | ❌ Slang (do NOT use) |
|---|---|---|
| `Selain itu,` | `Selain itu,` or `Jadi,` | `Lagi satu,` (too casual) |
| `Walau bagaimanapun,` | `Walau bagaimanapun,` or `Tetapi,` | `Tapi jujur cakap,` |
| `Oleh itu,` | `Oleh itu,` or `Jadi,` | `Sebab tu,` |
| `Kesimpulannya,` | `Kesimpulannya,` or `Intinya,` | `So,` |
| `Pertama sekali,` | `Pertama,` | `Benda pertama,` |

**Rule:** Default to formal transitions (`Selain itu`, `Walau bagaimanapun`, `Oleh itu`). `Jadi` and `Tetapi` are acceptable in conversational blog passages. Never use `pasal tu`, `sebab tu`, `So` as transitions.

## 8. Emphasis — Professional Intensifiers

| ❌ Casual emphasis (do NOT use) | ✅ Approved formal–semi-formal emphasis |
|---|---|
| `confirm berguna` | `sangat berguna` or `pasti berguna` |
| `memang jadi` | `berkesan` or `terbukti` |
| `wajib tahu` (slang tone) | `perlu diketahui` or `penting untuk diketahui` |
| `tak boleh nafikan` | `tidak dapat dinafikan` |
| `betul-betul jadi` | `benar-benar berkesan` |

**Note:** `memang` is acceptable in a conversational passage as a natural emphasis marker (`memang penting`, `memang berguna`). Use it moderately and prefer a more precise formal intensifier when it sounds better in context.

**Rule:** Replace casual emphatic words (`confirm`, `gila`, `wajib` as slang) with proper intensifiers (`sangat`, `amat`, `penting`, `pasti`, `terbukti`). `memang` is acceptable in moderation.

## 9. Humour — Light Wit Without Slang

DigiTrust Lab content should have a light sense of humour — not forced jokes, but dry wit that makes someone smile while reading. Think: a knowledgeable mentor who occasionally adds a human touch.

**How to add humour in natural formal–semi-formal BM:**
- Self-deprecating honesty: *"Kami juga pernah melakukan kesilapan ini — jangan tertawa."*
- Relatable exaggeration: *"Membuka laptop, membuka 47 tab, akhirnya menutup semula semuanya."*
- Gentle sarcasm about obvious things: *"Kami tahu polisi privasi bukan bacaan paling menarik..."*
- Unexpected honest admissions: *"Jujur, kami juga tidak menjangka ia akan berjaya."*
- Lighthearted aside in brackets: *"(percaya atau tidak, memang boleh)"*

**Rules for humour:**
- Never punch down or mock the reader
- Keep it relevant — don't force a joke where none fits
- One or two light moments per page/post is enough
- Humour works best in openers, transitions, and asides — not in conclusions or CTAs
- All humour must use proper BM — no slang-based humour

## 10. Punctuation — Write Properly, Not Like AI

**Em dash (`—`) rule:** Use sparingly. Maximum 1 per post/page, only when genuinely needed. Malay prose flows naturally with commas, `iaitu`, `memandangkan`, `kerana`, `jadi`, or a new sentence entirely.

| Instead of `—` | Use this |
|---|---|
| `AI tools telah canggih — anda perlu tahu cara guna.` | `AI tools telah canggih, jadi anda perlu tahu cara menggunakannya.` |
| `Kami tulis dari pengalaman — bukan teori semata.` | `Kami tulis dari pengalaman sebenar, bukan teori semata.` |
| `Ini bukan kursus — ini perkongsian jujur.` | `Ini bukan kursus. Ini perkongsian jujur.` |

**Other AI punctuation patterns to avoid:**
- ❌ Stacking em dashes within the same sentence
- ❌ Starting bullets with em dashes
- ❌ Using `—` as a substitute for a full stop
- ❌ Overusing `...` (ellipsis) for dramatic pauses — one or two per post max

### Blockquote Policy — Notes, Heads-Up, and Callouts

**Always use `<blockquote>` for any reader-facing note, heads-up, info, disclaimer, or callout.** This includes:

- Language/style notes (e.g., "Nota bahasa" on Tentang Kami)
- Closing notes/sign-offs at the end of blog posts
- Privacy or safety reminders within articles
- Any meta-content where the author steps back to address the reader directly

| ✅ Use blockquote | ❌ Don't use blockquote |
|---|---|
| Closing sign-off note at end of a post | Regular body paragraphs |
| "Nota bahasa" or language policy notes | Headings or subheadings |
| Safety/privacy callouts within content | Navigation or menu text |
| Author's personal note to readers | Product descriptions or CTAs |

**Rule:** If the content is a "step back from the article to speak directly to the reader" — it goes in a `<blockquote>`. This visually distinguishes meta-content from article body text.

**Brand blockquote style (always match this exactly):**
```css
blockquote {
  border-left: 3px solid #e8621a;
  background-color: #fff8f5;
  padding: 12px 16px;
  margin: 20px 0;
  border-radius: 0 6px 6px 0;
  font-style: italic;
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #3a3a3a;
}
```

**Rule:** Blog posts automatically inherit this style from the single post template. For Bricks pages or other templates where the default browser blockquote appears (grey left border, no italic, wrong font), add this exact CSS to the container element's `_cssCustom` so the visual treatment stays consistent across the site.

## 11. Red Flag Phrases — Always Rewrite These

### Salesy / Corporate red flags (existing)
- ❌ `"Privasi anda penting bagi kami"` → sounds like a copy-paste template
- ❌ `"Anda berhak untuk"` → translated legalese
- ❌ `"Kami sentiasa terbuka"` → press release language
- ❌ `"Kunjungi link external pada risiko anda sendiri"` → sounds threatening
- ❌ `"Untuk pertanyaan umum, kerjasama, atau sokongan"` → call center language
- ❌ Any sentence that starts with `"Maklumat di blog ini adalah untuk tujuan..."` → textbook opening

### Casual slang red flags (NEW — do NOT use)
- ❌ `korang` → use `anda`
- ❌ `tak` → use `tidak`
- ❌ `je` (as filler) → remove or use proper equivalent
- ❌ `confirm` (as emphasis) → use `pasti`, `sangat`, `terbukti`
- ❌ `gila` (as intensifier) → use `sangat`, `amat`
- ❌ `kat sini` → use `di sini`
- ❌ `macam mana` → use `bagaimana`
- ❌ `boleh je` → use `anda boleh`
- ❌ `senang je` → use `mudah` or `senang`
- ❌ `takleh` → use `tidak boleh`
- ❌ `dah` → use `sudah` or `telah`
- ❌ `nak` (as future marker) → use `akan` or `hendak`

## 11b. Audit Pattern Library — Real Mistakes Found in Published Content

These are actual defects found on the live site during the 2026-07-30 audit of Posts #1–#6 and the core pages. AI drafts and WriterZen output keep reproducing these patterns — scan for them specifically.

| Pattern | ❌ Wrong | ✅ Correct | Found in |
|---------|---------|-----------|----------|
| Missing verb prefix | `tidak pernah guna` | `tidak pernah menggunakan` | Disclaimer |
| Informal observation verb | `kami tengok` | `kami memantau` / `kami melihat` | Privasi |
| English where BM exists | `boleh check terus` | `boleh semak terus` | Privasi |
| English noun with BM equivalent | `result` (×3) | `hasil` | Disclaimer |
| English noun with BM equivalent | `effort` | `usaha` | Disclaimer |
| Banned contraction in opening line | `tak tahu nak tulis` | `tidak tahu cara menulis` | Post #3 |
| **Typo in an H2 heading** | `Bagaimana AI Berfungsa` | `Bagaimana AI Berfungsi` | Post #1 |
| Non-baku loanword | `efisien` | `cekap` | Post #2 |
| Informal noun | `benda` | `produk`, `alat`, `perkara` | Disclaimer |

> **ℹ️ `efektif` note (updated 2026-07-30):** DBP-recognized (prpm.dbp.gov.my) and allowed in formal/semi-formal BM. `berkesan` is the traditional synonym and remains preferred, but `efektif` is **not a violation**. Only `efisien` is flagged as non-baku.

### 11c. English Words That DO Have Natural BM Equivalents

§4b lists English terms to **retain** because their BM translations are awkward. This is the inverse list — English words that were used in published content where a perfectly natural BM word already exists. There is no excuse for these.

| ❌ Don't retain | ✅ Use BM |
|---|---|
| `check` | `semak` |
| `result` | `hasil` / `keputusan` |
| `effort` | `usaha` |
| `benda` (informal, not English but same problem) | `produk`, `alat`, `perkara` |

**Test:** before keeping an English word, ask *"is the BM version awkward, or am I just being lazy?"* §4b is for genuinely awkward translations (`copy & paste`, `deadline`). It is not a licence to leave any English word untranslated.

### 11d. Heading Typo Scan (MANDATORY)

**Scan every H2 and H3 character-by-character before publishing.** Heading typos are the highest-cost defect in the entire content pipeline because they surface in:

- Google search results (SERP snippets pull headings)
- The browser tab and page title
- The auto-generated Table of Contents
- Internal link anchor text

A body-paragraph typo is embarrassing. A heading typo is embarrassing **in public, at scale, indefinitely**. `Berfungsa` sat live on Post #1 from 2026-07-09 to 2026-07-30.

### 11e. Core Pages Need a Higher Register

Privasi, Disclaimer, Tentang Kami, and Hubungi Kami sit at a **higher register than blog posts**. Blog posts may use conversational warmth; core pages are quasi-institutional and readers judge credibility from them.

| On core pages, avoid | Use instead |
|---|---|
| `benda` | `produk`, `alat`, `perkara` |
| `tengok` | `melihat`, `memantau` |
| `guna` (bare verb) | `menggunakan` |
| Any contraction | Full form, always |

The warmth stays — `"Kami tahu halaman ini biasanya membosankan"` is still the right opener. What changes is that **every verb carries its full imbuhan** and no informal nouns slip through.

## 12. Green Light Patterns — Use These

Natural formal–semi-formal BM examples that hit the right tone — polished, professional, and accessible:

- ✅ `"Kami tahu halaman ini biasanya membosankan, tetapi kami akan menerangkan dengan cara yang mudah difahami."`
- ✅ `"Kami tidak menjual data sesiapa kepada sesiapa."` — direct, reassuring
- ✅ `"Itu janji kami."` — personal, accountable
- ✅ `"Biasanya dalam masa 48 jam pada hari bekerja."` — plain, no jargon
- ✅ `"Jika anda ingin mengetahui tentang...anda berada di tempat yang betul."` — warm, inclusive
- ✅ `"Pernahkah anda tertanya-tanya bagaimana AI berfungsi di sebalik skrin?"` — engaging question hook
- ✅ `"Mari kita mulakan dengan asasnya."` — conversational but proper
- ✅ `"Kami juga pernah menghadapi masalah yang sama."` — empathetic, honest

## 13. DBP Reference — Authoritative BM Guidance

When uncertain about spelling, grammar, or word choice, consult **Dewan Bahasa dan Pustaka (DBP)**:

- **Pedoman dan Panduan Bahasa Melayu:** `dbp.gov.my/pedoman-dan-panduan-bahasa-melayu/`
- **Khidmat Nasihat DBP:** `kndbp.dbp.gov.my` — for specific grammar questions
- **Pusat Rujukan Persuratan Melayu:** `prpmv1.dbp.gov.my` — for terminology and references

### Key DBP Rules to Remember

| Rule | Correct | Incorrect |
|------|---------|-----------|
| `ialah` for noun predicates | `AI ialah teknologi...` | `AI adalah teknologi...` |
| `adalah` for adjective/sendiri predicates | `Ini adalah penting.` | `Ini ialah penting.` |
| Use `ia` not `ianya` | `ia boleh membantu` | `ianya boleh membantu` |
| `dalam kalangan` not `di kalangan` | `dalam kalangan pengguna` | `di kalangan pengguna` |
| `daripada` for origin/member | `daripada Malaysia` | `dari Malaysia` (when meaning origin) |
| `dari` for direction/time | `dari Kuala Lumpur ke Johor` | `daripada KL ke Johor` (when meaning direction) |
| `berbahaya` not `merbahaya` | `berbahaya` | `merbahaya` |
| `istirahat` not `istirehat` | `istirahat` | `istirehat` |

**Rule:** When in doubt about a word, check DBP first. Consistent use of DBP-standard spelling and grammar builds authority and trust with readers and search engines.

## Content Authenticity Rules (added 2026-07-25)

**Core principle:** The blog is a practitioner sharing knowledge — not a business guru teaching success. Content must be authentic and educational first.

### Banned Phrases (NEVER use anywhere — titles, body, UI copy)

| ❌ Banned | ✅ Use Instead |
|---|---|
| `jana pendapatan` / `menjana pendapatan` | Focus on the skill: `buat kerja`, `jimat masa`, `mudahkan hidup` |
| `buat duit` / `buat duit mudah` / `dapatkan duit` | Focus on the tool: `guna AI untuk...`, `cara buat...` |
| `untuk perniagaan anda` / `untuk bisnes anda` | Focus on the user: `untuk anda`, `untuk kerja harian` |
| `jual digital products` / `mula jual di Etsy` | Focus on the creation: `buat digital products`, `cara design...` |

### Positioning

- **You are:** A practitioner sharing what you learn — not a success story or business guru
- **Tone:** "Here's how to use this tool well" — not "Here's how to make money"
- **Affiliate links:** Natural tool mentions, not sales pitches
- **Business/income posts:** ONLY when you have real results to share honestly
- **Prompt gallery posts:** Show the prompt + the result + the tool used. No income promises.

### Content Categories (updated 2026-07-25)

- AI Tools — reviews, tutorials, comparisons
- Canva & Design — tutorials, templates, design tips
- Prompt Engineering — prompt gallery posts, AI art showcases
- Digital Skills — Notion, WordPress, productivity tools

**Deleted categories:** Digital Side Hustle (implied income claims), AI untuk Perniagaan Kecil (business advice without results)

## Sources

- **PandaiTech.my** — semi-formal AI tech blog, closest reference for DigiTrust Lab
- **Ecentral.my** — semi-formal tech info blog
- **Jobstreet Malaysia** (my.jobstreet.com) — formal career advice articles
- **Dewan Bahasa dan Pustaka** (dbp.gov.my) — authoritative BM reference for spelling, grammar, and standards
- **Hashmeta** (hashmeta.com) — Malaysian content marketing research and trends
