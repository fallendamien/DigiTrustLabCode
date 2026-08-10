# Post #9 — Luna Execution Handoff

## Mission

Complete the DigiTrust Lab article mission for the **Prompt Engineering** category, from the current WriterZen outline state through publication and all post-publication gates.

## Handoff readiness

**READY FOR LUNA EXECUTION — RESUME AT THE FINAL POST-PUBLICATION GATES.**
Research, outline, WriterZen generation, editorial packaging, image preparation,
media upload, two-review naturalness evidence, WordPress editor checks,
publication, rendered checks, ClickRank tracking/pages, Google Search Console
request evidence, inbound-link review, and the Screpy Rank Tracker entry are
complete. Luna must continue with the still-running Screpy Pages crawl,
documentation parity, final validators, and the scoped commit/push. Do
not restart completed WriterZen research, create a second post, or republish
Post #9.

The only accepted completion state is the one defined at the end of this file:
every required gate has fresh evidence, every dashboard result is recorded, and
the live site and project documents agree. A missing dashboard snapshot, stale
hash, or unverified editor field is a stop condition, not a reason to mark a
phase complete.

## Current verified state (2026-08-10)

- Use only the authenticated WriterZen app at `https://app.writerzen.net/`.
- WriterZen Content Creator article: `https://app.writerzen.net/user/content-creator/report/243931`
- WriterZen Keyword Planner project: `Post 9 — Prompt Gemini AI Research`, ID `178604`.
- Winning focus keyword: `prompt gemini ai untuk edit foto`.
- Metrics: volume **140/month**, CPC **US$1.17**, Allintitle **0**, Golden Score **1.001**, Weak Spot **2** (passes the minimum gate).
- Supporting keywords in the selected cluster:
  - `prompt gemini ai gambar realistis` — volume 50, Golden Score 1.003, Weak Spot 0.
  - `prompt gemini ai terbaru` — volume 30, Golden Score 1.005, Weak Spot 3.
- The broader `prompt gemini ai` keyword was rejected as the focus keyword because Weak Spot was **1**.
- Rejected comparison: `contoh prompt gambar ai` has volume **10**, below the minimum threshold.
- Working title: `10 Prompt Gemini AI untuk Edit Foto dengan Mudah` (48/60 characters in WriterZen).
- Working description: `Gunakan 10 prompt Gemini AI untuk edit foto, ubah latar, baiki pencahayaan dan hasilkan gaya realistik dengan langkah yang mudah diikuti.` (137/160 characters).
- Proposed slug: `prompt-gemini-ai-untuk-edit-foto`.
- Proposed manual excerpt (160 characters): `Pelajari 10 prompt Gemini AI untuk edit foto, ubah latar, baiki pencahayaan dan hasilkan gaya realistik dengan arahan yang mudah disesuaikan mengikut keperluan.`
- Category: `Prompt Engineering`; tags are optional and must be justified by the final article.
- Content format: How-to guide.
- Tone: Friendly/Conversational, adapted during editing to DigiTrust Lab's natural formal–semi-formal Malay voice.
- WriterZen has generated and saved the outline into the keyword stage, then generated the Content Creator draft.
- The outline was expanded to ten prompt sections, including old-photo restoration, composition/cropping, product/profile cleanup, and creative style transformation.
- The controlled local editorial package is `content/drafts/10-prompt-gemini-ai-edit-foto.html` (1,732 words, within the useful 1,600–1,900-word target).
- Local and live link validation passes: 3 contextual internal links, 1 editorial external link, and 1 external dofollow link. Deterministic naturalness findings are empty, and the two-review artifact is hash-matched. The rendered Google-support link is confirmed `target="_self"` with `rel="dofollow noopener"`; the destination check uses a GET fallback because this host returns 404 to HEAD while serving the page to GET.
- All four planned images are generated, visually checked, copied to the project archive, and SHA-256 verified. WordPress Media upload is complete via Respira as Media 578–581 with the planned Malay alt text; the three in-content sources now pass a fresh rendered viewport check at 1672×941.
- WordPress post **ID 582** is published through Respira at `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/` (status `publish`, 2026-08-10), category `Prompt Engineering`, featured Media 578, three in-content image elements, excerpt, and Rank Math title/description/focus keyword.
- The authenticated WordPress editor was verified before publication: excerpt, slug, category, featured-image alt text, Article schema, and Rank Math sidebar score **85/100** were visible. Respira's essential audit remains **100/A (13/13)**; record both scores accurately rather than collapsing them into one number.
- The live page was verified for canonical URL, meta description, JSON-LD `BlogPosting`, headings, ToC, lists, code blocks, three branded blockquotes, internal links, visible article structure, and the three resolved in-content image sources.
- Respira Rank Math essential audit now passes **100/A (13/13)**: SEO title `10 Prompt Gemini AI untuk Edit Foto dengan Mudah: Panduan Praktikal` (67 characters), 1,732 words, keyword density 0.52%, 3 images with alt text, 3 internal links, and 1 external link.
- SERP View and AI Assistant toggles are OFF, as required.
- Post #11 (`https://digitrustlab.com/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi/`) has its exact URL visible in ClickRank Website Optimization / Pages with status **Not Optimized**; do not add a duplicate. The separate backfill is now recorded in `content/content-calendar.md`; no ClickRank copy change was applied.

## Non-negotiable operating rules

1. Reuse the user's authenticated Chrome tab through the Chrome control skill. Claim the exact tab and take a fresh DOM snapshot before each action sequence.
2. Never use `writerzen.net`; use `https://app.writerzen.net/` only.
3. Follow `.devin/skills/write-post/SKILL.md`, `.devin/skills/writerzen-keyword-research/SKILL.md`, and `.devin/skills/malay-voice-guide/SKILL.md`.
4. Do not publish if any required gate is missing, stale, uncertain, or failed.
5. Do not invent firsthand testing or results. If prompts are not tested, describe outcomes as expected results.
6. Use Respira MCP for WordPress writes; use the authenticated WordPress GUI only where the workflow explicitly requires it (for example Rank Math/editor checks).

## Execution plan

### 0. Previous-post and site-state gate — ✅ completed

- Open the authenticated WordPress and dashboard tabs and verify the prior
  article's live status before touching Post #9.
- In ClickRank Website Optimization / Pages, Post #11's exact URL is present
  with visible status **Not Optimized**. It was not duplicated, and the
  separate backfill is recorded in `content/content-calendar.md`.
- Confirm the Post #11 calendar entry, live URL, and tracking evidence remain
  intact. Do not overwrite that prior evidence while documenting Post #9.

### 1. Review and approve the WriterZen outline — ✅ completed

- Keep the winning focus keyword and the verified brief.
- Confirm the saved outline still matches the natural Malay brief. Fix any remaining Indonesian/awkward wording such as `efek`, `berbagai`, `tone`, `bayangbayang`, `tampak`, and `efektif` before using it as the source for the final article.
- The six-prompt outline was expanded to **10 distinct prompt sections** in WriterZen.
- Required structure:
  1. Short scenario-led introduction.
  2. What Gemini photo editing can and cannot do.
  3. How to prepare/upload a suitable photo, including privacy warning.
  4. Ten prompt sections: background replacement, lighting/contrast, unwanted-object removal, colour correction, realistic enhancement, old-photo restoration, crop/composition, clothing/style adjustment without identity deception, product-photo cleanup, and creative style transformation.
  5. Prompt-customisation formula and common mistakes.
  6. Limitations, consent, privacy and ethical use.
  7. FAQ.
  8. Calm conclusion with no sales pitch.
- Each prompt section must contain the prompt, editable variables, expected result, and one practical caution.
- The outline was saved and the keyword stage was completed. Do not redo clustering or spend credits unless a verification check shows the saved state is missing.

### 2. Configure WriterZen keywords and generate the draft — ✅ completed; editorial control remains

- Keep the focus keyword natural; do not stuff it.
- Review suggested NLP/secondary terms and remove irrelevant, unsafe, Indonesian-only, or sales-oriented terms.
- Target about **1,600–1,900 words**, subject to natural coverage rather than padding.
- Generate the article through WriterZen Content Creator; do not bypass the Content Creator pipeline.
- The generated draft was copied into `content/drafts/10-prompt-gemini-ai-edit-foto.html` for controlled editing. Use this local file as the editorial source of truth; do not publish the unreviewed WriterZen output directly.

### 3. Editorial and DigiTrust Lab formatting pass

- Rewrite directly into natural formal–semi-formal Bahasa Melayu using `anda` and complete grammar.
- Italicise retained English technical terms where required.
- Maximum one em dash in the whole article.
- Use short paragraphs, bold-label lists, before/after examples, contrast pairs, and at least three branded blockquotes.
- Remove hype, income claims, unverified claims, unsafe identity editing, and any suggestion that AI-generated passport/official-document photos are acceptable.
- Add descriptive internal links to relevant existing DigiTrust Lab posts and at least one editorial external dofollow source.
- Prepare excerpt, slug, category (`Prompt Engineering`), tags if justified, and Rank Math title/meta.
- Re-run the local word count and decide whether the article needs useful explanatory detail to reach the 1,600–1,900-word target. Do not add filler merely to hit a number.

### 4. Images and prompt archive

- Define the featured image plus useful instructional images in `content/image-prompts.md`.
- Generate/obtain images, verify them visually, optimise filenames and Malay alt text, and archive final originals in `G:\Zamzam Biznez\DigiTrustLab\Blog images` using the exact prompt filenames.
- Current state: generation, visual inspection, archive copy, source/destination hash checks, and WordPress Media upload are complete for all four assets. Continue with post placement and rendered-image verification.
- Never upload an unverified image or claim that an example is an actual Gemini result unless it was genuinely produced and checked.

### 5. Pre-publication mechanical gates — ✅ completed

- Run `python scripts/verify-links.py --file <draft.html>`.
- Run the deterministic Malay voice/naturalness checks required by the write-post workflow.
- Produce two fresh independent naturalness reviews: one Claude/Anthropic and one OpenAI, following `content/naturalness-reviews/README.md`.
- Block publication on any finding, uncertainty, disagreement, stale hash, missing required review family, or unresolved link issue.

**Current review packet:** the final-package file is `content/drafts/10-prompt-gemini-ai-edit-foto.html` and includes the title, exact body, three image alt texts, and manual excerpt. Its current hash is `264ae912dcee181fca28747daa2295f8e25884ee8281b314ec47c220c1bf0afa` across 80 segments; deterministic findings are 0. The body-only comparison copy is in ignored `tmp/10-prompt-gemini-ai-edit-foto-body.html`. The review artifact is `content/naturalness-reviews/post-9-prompt-gemini-ai.json` and contains fresh Claude/Anthropic and OpenAI records with all six checks true, high confidence, empty findings, and the same hash. Re-run the live hash check after any content edit; never reuse an older hash or copy Post #11's artifact.

The local and live naturalness checks both pass against hash `264ae912...1bf0afa`; the repository artifact is complete. `python -m pytest` is unavailable in this environment, so use the repository's `unittest` command for the regression test instead of installing a new dependency.

### 6. Create and optimise the WordPress post — ✅ completed

- Create the post through Respira MCP using Gutenberg content and keep the snapshot UUID.
- Set featured image, excerpt, slug, Prompt Engineering category, internal/external links, and Article/BlogPosting schema requirements.
- In the authenticated WordPress editor, complete Rank Math:
  - focus keyword;
  - SEO title and meta description;
  - schema and featured image;
  - pillar-content decision (expected: not pillar unless the final scope becomes foundational);
  - keyword density 0.5%–2.5%;
  - at least one external dofollow link;
  - valid H2/H3 hierarchy and ToC coverage;
  - target score 80+.
- Click the WordPress Save/Update button after every editor or Rank Math change.

### 7. Publish and live revalidation — ✅ completed

- Publish only after every pre-publication gate passes.
- Run:
  - `python scripts/verify-malay-naturalness.py --post-id <id> --review <artifact>`
  - `python scripts/verify-malay-voice.py <id>`
  - `python scripts/verify-links.py --post-id <id> --inbound-review content/link-reviews/<slug>.json --check-destinations`
- Verify the live post visually on desktop and mobile, including images, blockquotes, ToC, links, spacing, and metadata.
- Fresh rendered verification confirms the three in-content images resolve to Media 579–581 URLs at 1672×941, and the editorial external link is `rel="dofollow noopener"` with `target="_self"`. No article HTML changed during verification.

### 8. Mandatory post-publication tracking — ClickRank/GSC ✅; Screpy partial ⏳

- ClickRank Keyword Tracker: ✅ primary focus keyword only with the exact post URL, country Malaysia, device All; visible row verified.
- ClickRank Website Optimization / Pages: ✅ exact post URL added; crawl completed; status **Not Optimized** visible; approved title/meta reviewed and no copy changes applied. Post #11's exact URL was already present and was not duplicated.
- ClickRank AI Overview Tracker: ✅ same focus keyword + URL, Malaysia, Malay; visible row verified (current result Not Found, 0% visibility).
- Screpy Rank Tracker: ✅ added the primary focus keyword only with Malaysia,
  Malay, and **Device: Both** in one action; fresh snapshots showed the row in
  both Desktop and Mobile views.
- Screpy Pages: ✅ **Analyze** was clicked at 2026-08-10 03:14 (+08:00).
  Current fresh snapshots still show **Analyzing...**, crawler `18151`, the old
  2026-08-08 06:13 AM result, and no Post #9 URL yet. Do not record the crawl
  as complete until the new URL and result are visible.
- Google Search Console: ✅ authenticated URL Inspection showed **URL is not on
  Google / URL is unknown to Google**, no referring sitemap, and the request was
  submitted successfully at **2026-08-10 02:42 (+08:00)**. The visible dialog
  said **Indexing requested** and that the URL was added to a priority crawl
  queue. This is not proof of indexing; re-inspect later.
- The authenticated Screpy tab is available and claimed at
  `https://app.screpy.com/wgspvb7lc3/pages`; leave the crawl running or resume
  from that exact tab. A pending **Analyzing...** state is not completion
  evidence.
- Do not mark Phase 7 complete if any of these six dashboard/indexing gates is
  missing or represented only by a generic “done” note.

### 9. Internal linking and documentation — inbound scan ✅; docs/final checks ⏳ Luna

- The internal-link-builder scan is complete. No safe contextual inbound link was
  found in published posts/pages, so no link was forced. The auditable artifact
  is `content/link-reviews/prompt-gemini-ai-untuk-edit-foto.json` and records
  `no_safe_context` with the live link hash.
- The complete local/live validator set was rerun at 2026-08-10 03:26 (+08:00)
  while Screpy was still analyzing: content-status, imports, 29 unit tests,
  both naturalness gates, Malay voice, both link gates, and `git diff --check`
  all passed. Rerun it once more after the fresh Screpy result is recorded,
  immediately before commit/push.
- Update `content/content-calendar.md`, `content/image-prompts.md`, `STATE.json`, and `NEXT.md` with the final title, URL, post ID, metrics, Rank Math score, tracking status, and verification results.
- After Screpy/GSC, run the full final gate set:
  - `python scripts/verify-content-status.py`
  - `python scripts/verify-imports.py`
  - `python -m unittest tests.test_verify_malay_naturalness -v`
  - `python -m unittest tests.test_verify_links -v`
  - `python scripts/verify-malay-naturalness.py --file content/drafts/10-prompt-gemini-ai-edit-foto.html --review content/naturalness-reviews/post-9-prompt-gemini-ai.json`
  - `python scripts/verify-malay-naturalness.py --post-id 582 --review content/naturalness-reviews/post-9-prompt-gemini-ai.json`
  - `python scripts/verify-malay-voice.py 582`
  - `python scripts/verify-links.py --file content/drafts/10-prompt-gemini-ai-edit-foto.html`
  - `python scripts/verify-links.py --post-id 582 --inbound-review content/link-reviews/prompt-gemini-ai-untuk-edit-foto.json --check-destinations`
  - `git diff --check`
- Commit and push only the scoped article/workflow/documentation changes after
  the gates pass; preserve unrelated user changes and inspect the final diff
  before committing.
- Preserve and include the existing uncommitted workflow fix in `.devin/skills/write-post/SKILL.md` and the Post #11 ClickRank Pages update in `content/content-calendar.md`; do not overwrite them.

## Completion definition

The mission is complete only when the post is live, all live checks pass, Rank
Math is recorded, ClickRank Keyword Tracker + AI Overview + Pages, Screpy
Both-device + fresh crawl, and Google Search Console inspection/request result
are recorded, inbound-link review is complete, project documents match the live
site, every final validator passes, and the final scoped diff is committed and
pushed. A request to index must never be recorded as proof of indexing.

## Resume point for Luna

Use the authenticated WriterZen tab only for source verification at
`https://app.writerzen.net/user/content-creator/report/243931`; the research,
outline, keyword gates, WriterZen generation, editorial pass, two-review
artifact, WordPress publication, and initial live checks are already complete.
Resume in this order:

1. Confirm the running Screpy Pages Analyze crawl finishes and record the fresh
   discovery/HTTP/page-health result for Post #9. Rank Tracker is already
   complete for Malaysia, Malay, **Device: Both**, verified in Desktop and
   Mobile.
2. Confirm the Google Search Console request evidence remains recorded; a later
   re-inspection may verify indexing, but do not equate “indexing requested”
   with “indexed”.
3. Confirm the inbound artifact remains hash-matched; do not add a speculative
   link without an explicit safe-context finding.
4. Update `content/content-calendar.md`, `content/image-prompts.md`,
   `STATE.json`, `NEXT.md`, and `ROADMAP.md`; run all final validators, inspect
   the scoped diff, then commit and push only the article/workflow/docs changes.

The mission is not complete until the six dashboard/indexing gates, inbound-link
artifact, documentation parity, final repository checks, and commit/push all
have fresh evidence. The exact WriterZen URL for any source verification is
`https://app.writerzen.net/`; never substitute `https://writerzen.net/`.
