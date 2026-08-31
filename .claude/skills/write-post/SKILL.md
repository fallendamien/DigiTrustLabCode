---
name: write-post
description: "Write and publish a blog post using the WriterZen Option C pipeline. Quota check → Topic Discovery → Golden Filter → Keyword List → cluster → Weak Spot gate → Content Brief → Content Creator → publish via Respira MCP → Rank Math → Malay voice gate → ClickRank/Screpy tracking → Google Search Console indexing request. Includes the hard-won wp.data excerpt method."
---

# Write & Publish a Blog Post (Option C Pipeline)

This is the standard workflow for every DigiTrust Lab blog post. Follow these steps in order.

## Prerequisites

- WriterZen account active (app.writerzen.net)
- Respira MCP connected to digitrustlab.com
- Existing Content Creator project: "DigiTrust Lab" (reuse — never create new)
- Existing Keyword List: "DigiTrust Lab Blog Posts" (ID: 68708) — the one permanent list for all posts
- Keyword Planner: a **new project per post topic** is created during Phase 1. Legacy project 178201 exists but is NOT a reuse target
- WriterZen quota headroom — verify in Phase -1 before starting

## Goal, Plan, and Token-Efficient Delegation

For a full end-to-end request, use one Goal only when the user explicitly selects
or requests Goal mode. Use this objective:

> Research, write, publish, optimize, and track the next DigiTrust Lab article.

Maintain a Plan inside that Goal for phases -2 through 7. A planning-only request
does not need a Goal. The coordinator owns the objective, phase transitions,
publication authorization, synthesis, final decisions, and evaluation of worker
evidence. Substantive tools, browser actions, edits, external writes, and
verification commands are executed by bounded workers dispatched by the
coordinator.

Use the configured default worker without passing model or reasoning overrides.
The intended setup is **Sol Light as coordinator** and **Luna High as the
default worker**. Delegate to Luna whenever a bounded task can be completed to the
same standard more efficiently; do not spend Sol tokens redoing completed worker
work. Sol reviews the evidence and makes only the integrated decision.

| Work | Default owner | Parallel? |
|------|---------------|-----------|
| Calendar/status inventory, content-gap scan, source pack, immutable-file review | Luna High | Yes, only with independent inputs and disjoint scopes |
| WriterZen → Content Creator stateful chain | One owner; prefer Luna when it has the authenticated Chrome binding | No |
| Image prompt/filename preparation and deterministic local checks | Luna High | Yes, when they do not mutate the same artifact |
| WordPress writes, publishing, ClickRank, Screpy, GSC, canonical status files | One bounded worker under Sol's phase control | No |
| Final gate decisions, ambiguity, synthesis, evidence evaluation, and completion claim | Sol Light | No |

Token and context rules:

1. Spawn the minimum number of workers needed; task size alone is not a reason to parallelize.
2. Give each worker exact inputs, one bounded output, and a non-overlapping write scope. Use a fresh context unless prior context is essential.
3. Keep one worker for a tightly connected chain. Never let multiple agents operate the authenticated Chrome session, the same WriterZen project, the same WordPress post, or the same documentation file concurrently.
4. Subagents may execute explicitly assigned bounded edits, external writes, tests,
   and verification commands, but they may not approve their own gate or mark the
   article complete. Sol authorizes the phase; the worker performs the action.
5. Collect each result, evaluate the returned evidence once, and close the worker
   immediately. Sol must not rerun the worker's command or repeat its browser
   action inline. See `docs/knowledge-library/delegation-patterns.md` for the
   human-readable explanation.

The required Claude/Anthropic and OpenAI naturalness reviewers are independent
review roles, not ordinary workflow delegation. The Anthropic lane must use
Claude Sonnet (actual model ID recorded in the artifact); do not use Claude
Opus for this review unless the user explicitly changes the preference. A
fresh Luna High session may serve as the OpenAI-family reviewer when it
receives only the frozen final content and none of the other review. The
Claude/Anthropic review must still come from that separate family.

### Remy-style parallel article pattern

The coordinator may route one article into content, creative, and SEO/operations
workstreams, then set a barrier before staging. Parallelize only independent,
bounded tasks with disjoint inputs and write scopes, such as per-asset image
generation or batches, read-only SEO/source checks, and visual QA on completed
assets. Each worker result must identify the actual `gpt-5.6-luna` model,
`high` effort, scope, and evidence. One worker owns each asset or file; never
concurrently edit the same image, prompt library, WordPress post, browser tab,
or canonical documentation. After the barrier, the coordinator reconciles and
chooses assets; one sequential bounded worker performs upload, staging,
publication, tracking, and documentation under Sol's authorization. If the work
is tightly coupled or concurrency is not useful, use one worker.

## Browser Automation Standard — Existing Authenticated Chrome Session (FIRST GATE)

This gate must pass before any Phase -2 dashboard verification, Phase -1, or
other browser action. All WriterZen, WordPress-admin, ClickRank, Screpy, Google
Search Console, and visual-verification interactions use the user's already-open
Chrome extension session through `chrome:control-chrome` — **explicitly the real
signed-in browser, not a blank or private one**. The incident and prevention
sequence are documented in `docs/browser-session-hardening.md`.

1. Connect to the Chrome extension browser and reuse its persistent browser binding. Name the session before opening or claiming a tab.
2. Inspect the user's open tabs and claim the exact target tab by its current title and URL. Never assume a numeric tab ID or claim a guessed tab.
3. Take a fresh DOM snapshot and verify the expected authenticated dashboard/site state before entering data or changing anything. A login page from another browser connection is not evidence that this Chrome session is unauthenticated.
4. After every navigation or meaningful UI change, take a fresh DOM snapshot and use only locators from the current state. Never reuse stale locators.
5. Use the claimed tab's semantic controls for clicks, fills and waits. The in-skill `tab.playwright` API is available once the existing Chrome tab has been claimed, and operates inside that claimed tab.
6. Use DOM/CUA interaction only for documented UI workarounds such as a label intercepting a checkbox click. After a workaround, take a fresh snapshot and verify the visible state.
7. If the exact authenticated Chrome tab is unavailable, stop and ask the user to open/sign in to it, so the work continues in their real session.

## WriterZen Tool Hierarchy (CRITICAL — know this before starting)

| Tool | Purpose | Persistence | When to use |
|------|---------|-------------|-------------|
| **Keyword Explorer** | Discover keywords + metrics | Session-only | Research phase |
| **Keyword List** | Permanent keyword storage | ✅ Permanent | Save keywords from Explorer |
| **Keyword Group** | Temporary scratchpad | ❌ Session-only | NEVER use — disappears after session |
| **Keyword Planner** | Cluster keywords into topics | Project-based | Planning phase |
| **Content Creator** | Generate outline + write article | Project-based | Writing phase |

### ⚠️ Keyword List vs Keyword Group

- **ALWAYS use "Add keyword to LIST"** (permanent) — NEVER "Add keyword to GROUP" (temporary, disappears after session)
- Keyword List is the bridge between Explorer and Planner

### ⚠️ Project Structure

- **ONE Keyword List** for all blog posts: "DigiTrust Lab Blog Posts" (ID: 68708) — single source of truth
- **ONE Keyword Planner project PER blog post topic** — WriterZen clustering is one-time, cannot append to existing
- **ONE Content Creator project**: "DigiTrust Lab" (existing) — all articles under this project

> **Full keyword research detail:** See `.claude/skills/writerzen-keyword-research/SKILL.md` for WriterZen tool walkthrough, Golden Filter thresholds, and Weak Spot gate methodology.

## Steps

### Phase -2: Start or Resume Gate (MANDATORY)

1. Run `python scripts/verify-imports.py` before trusting the workflow loaders.
2. Run `python scripts/verify-content-status.py` and compare
   `content/content-calendar.md`, `STATE.json`, and `NEXT.md` with the live
   WordPress result. Do not infer completion from documentation alone.
3. Verify the previous article's required post-publish work before selecting the
   next topic. ClickRank and Screpy have no reliable API, so use their recorded
   evidence or verify their authenticated dashboards when completion is unclear.
4. Resume an existing active Goal and Plan when they already cover this article.
   Create a new Goal only when the user explicitly selected or requested one.
5. Record the current scope: planning-only, draft-only, or complete publication.
   Do not start drafting until Topic Discovery and the Weak Spot gate validate
   the topic.
6. For topic selection, Sol may delegate independent read-only analysis to Luna:
   one worker for the calendar/status queue, one for content gaps, category
   balance, cannibalization, and internal-link opportunities, and one for
   audience/editorial fit. Sol merges the evidence into a short candidate list.
   None of these workers may finalize the title; Phases 0a through 1.5 provide
   the ranking evidence that selects the publishable topic.

### Phase -0: Editorial Relevance Gate (MANDATORY — before any research or credit)

Before Phase -1 quota checks or any Topic Discovery, Keyword Explorer, Golden
Filter, Keyword Planner, permanent keyword-list, or drafting action, apply the
single contract in `.claude/rules/editorial-relevance-gate.md`. The candidate
record must name the proposed subject and semantically faithful seed, one
approved DigiTrust Lab pillar/category, the actual reader problem, an
authenticity basis (demonstrated tool/workflow use or an explicitly planned
first-hand test), and a distinct/non-cannibalizing comparison against
`content/content-calendar.md` and published inventory. It must also name the
existing approved cluster/pillar being extended, a published parent/peer URL,
a plausible inbound source from an existing post, incremental reader value, and
the planned anchor/context. An orphan or brand-new cluster is blocked unless
the user explicitly approves it.

Freeze the structured classifications `topic_family_id`, `approved_pillar_id`,
`approved_cluster_id`, `topic_intent_id`, `subject_entity_ids`, and
`declared_seed_intent` with the handoff. Research,
SEO, and Operations must each supply `decision`, `status`, `evidence_ref`,
`checked_at`, and `owner`; Operations must additionally supply independently
current structured calendar/published-URL/link-feasibility arrays with exact
canonical identity. Content rejects
missing, stale, contradictory, or non-PASS records rather than inferring them.

Research must attest `RESEARCH_RELEVANCE: PASS`; SEO must independently attest
`SEO_RELEVANCE: PASS` before metric work; Operations must independently attest
`OPERATIONS_RELEVANCE: PASS` before any credit/project/list action and again
before the drafting handoff. Content rejects any missing or contradictory
attestation. Broad/noisy cards and adjacent SEO terms remain evidence only.
Metrics can reject a relevant candidate but never promote an irrelevant one.
Any pivot outside the approved topic family stops for explicit user approval.

Incident example: `ranking google` passed WriterZen metrics in a prior run, but
was editorially irrelevant to a planned Notion template article and had no
defensible adjacency/internal-link path to current clusters. Its volume,
Golden Score, All-in-Title, or Weak Spot must not bypass this gate.

### Phase -1: Quota Check (MANDATORY — before any research session)

Golden Filter costs **1 Keyword Credit per keyword in the result set** (39 keyword ideas = 39 credits). Never start research blind.

1. Navigate to `https://app.writerzen.net/user/profile-setting?tab=limit`
2. Record remaining: **Topic Lookup/Day**, **Keyword Lookup/Day**, **Keyword Credit/Month**, **AI Words/Month**
3. Apply the budget rules:
   - Keyword Credit < 10,000 → selective Golden Filter only (top 3-5 keywords, not full result sets)
   - Keyword Credit < 5,000 → skip Golden Filter, fall back to manual KD + All-in-Title checks via SERP overview
   - **AI Words/Month = 8,000 total.** This workflow never spends those words
     on a full WriterZen article. The Create Article gate permits only title,
     description, and outline; the body is always drafted natively. If the
     remaining credits do not cover the outline-only request, stop as `BLOCKED`.
4. Note consumption at end of session; update `content/SEO-CHEATSHEET.md` limits table if running low

> **30-day freshness rule:** WriterZen search results expire after 30 days. If the last Keyword Explorer run for this topic is older than 30 days, start a fresh search — do NOT reuse stale metrics.

### Phase 0a: Topic Discovery (find the winnable angle BEFORE committing to a title)

> **Why this exists:** DigiTrust Lab is a low-DA site. Picking a title first and hunting for a keyword afterwards is backwards — it commits you to an angle before checking whether it's rankable. Topic Discovery reverses that. Planned titles in `content-calendar.md` are **provisional** until this phase confirms them.

> **Relevance boundary:** Topic Discovery may refine an approved subject, but
> it may not redefine the category, reader problem, or subject family. Treat a
> noisy card or adjacent SEO term as evidence only; stop for explicit user
> approval before pivoting.

1. Navigate to WriterZen → Topic Discovery
2. Set **Language: Malay**, **Location: Malaysia**
3. Enter the broad seed for the planned post (e.g. "prompt AI illustration", not the full title)
4. Set **Relevancy: Closely** (start narrow; widen only if results are thin)
5. Sort **By Search Volume**
6. Review the topic cards:
   - **Golden star** = upward search volume trend → prioritize these
   - Open **Show Ideas** on the strongest cards → read *Headlines to Consider*, *Google Suggest Insights*, *Related Google Searches*
7. Pick 2-4 candidate angles/subtopics that look narrower and more winnable than the original planned title
8. **Confirm or revise the planned title** in `content-calendar.md` based on what Topic Discovery found
9. Carry the candidate seeds into Phase 0b

### Phase 0b: Keyword Research (Keyword Explorer → Golden Filter → Keyword List)

1. Navigate to WriterZen → Keyword Explorer
2. Set **Language: Malay**, **Location: Malaysia**
3. Check "Save language & location as default"
4. Enter the candidate seed from Phase 0a (e.g. "cara prompt chatgpt")
5. Click Search
6. Analyze results:
   - **Search volume** — check if sufficient (even 10-20/mo is OK if KD=0)
   - **KD metrics** — all 4 should be low (0 = easy to rank)
   - **Keyword ideas** — review all variants (phrase match + also searched for)
   - **Total search volume** — combined cluster volume
   - **SERP Overview** — check competitor content quality
7. **Apply Golden Filter (MANDATORY — this is the primary low-DA screen):**
   - Check the keyword idea count first and confirm the credit cost in the confirmation dialog before clicking Confirm
   - Thresholds: **Golden Score max 10** · **Search Volume min 100** · **All-in-Title max 10**
   - If nothing survives at Volume min 100 (common for Malay long-tail), relax volume to 50 — but **never relax Golden Score above 10 or All-in-Title above 10**
   - Golden Score bands (source `writerzen-guide/07`): **0–30** Level 1 (low competition, high volume — what we want) · **30–70** Level 2 · **70–100** Level 3 (crowded). Gate at **≤10** for low-DA; **≤1.618** is the ideal ceiling WriterZen names the score after. Both figures are sourced — do not "correct" one into the other.
   - ⚠️ When All-in-Title is 0, the score floors at ~1.0 with a volume tiebreaker rather than computing to 0 — in that case **read All-in-Title, not Golden Score**, as the competition signal
   - ⚠️ Golden Filter only works on keywords that have All-in-Title data
8. **Manual SERP sanity check** — metrics give numbers, the SERP gives reality. Open the SERP overview and confirm small Malaysian blogs are ranking in the top 10. If the page 1 is all global giants, the keyword is not winnable regardless of score
9. Select the surviving top 5-10 keyword variants (highest volume, most relevant intent)
10. Click **Add to** → **Add keyword to LIST** (NOT "Add keyword to group"!)
11. Select existing list: "DigiTrust Lab Blog Posts"
12. Click **Add**
13. Record keyword metrics in `content/content-calendar.md` — including **Golden Score** and **All-in-Title**, not just volume/KD

### Phase 1: Keyword List → Keyword Planner (Cluster)

1. Navigate to WriterZen → Keyword List → "DigiTrust Lab Blog Posts"
2. Select the newly added keywords (checkboxes)
3. Click **Cluster** → **Cluster Selected (N)**
4. In the clustering modal:
   - **Project name**: Create NEW project named after the post topic (e.g. "Post 3 — Cara Prompt ChatGPT")
   - **Location**: Malaysia
   - **Language**: Malay
   - **Cluster level**: MODERATELY RELEVANT (default)
   - **Activate golden filter**: ✅ Checked
5. Click **Add** to start clustering
6. Wait for clustering to complete (uses keyword credits)
7. Navigate to the new Keyword Planner project
8. Verify the keywords appear in clusters (check sidebar for topic/cluster names)
9. Click on the target cluster to view its keywords

### Phase 1.5: Verify the Keyword Is Beatable (Activate Metrics → Weak Spot)

> **Why this exists:** AGENTS.md and the WriterZen skill both set `Weak Spot ≥ 2` as a ranking criterion, but nothing in the pipeline ever measured it. This is the gate that proves a low-DA site can actually take the keyword. Do NOT proceed to the content brief until it passes.

1. In the Keyword Planner project, select the target cluster
2. Click **Activate Metrics** in the bottom taskbar (consumes keyword credits — confirm the cost first)
3. Read the new columns:

   | Metric | Meaning | DigiTrust Lab gate |
   |--------|---------|-------------------|
   | **Weak Spot** | URLs in top 10 with DA < 30 | **≥ 2** (≥ 3 ideal) |
   | **LDA** | Lowest DA in top 10 | Lower = more room |
   | **Average DA** | Mean DA of top 10 | Lower = more winnable |
   | **HDA** | Highest DA in top 10 | Context only |

4. **Decision:**
   - **Weak Spot ≥ 2** → proceed to Phase 2
   - **Weak Spot 0–1** → the top 10 is high-authority. **Do not write it yet** — run the fallback protocol below

#### Fallback protocol when the gate fails (do this before ANY override)

> ⚠️ "Go back to Phase 0a" means **pick a different candidate from the Topic Discovery output you already have** — it does NOT mean re-running Topic Discovery. That run already produced dozens of candidate angles; re-running the same seed burns a lookup and returns the same topics. Only re-run Topic Discovery when the existing candidates are exhausted, or when moving to a different subject area entirely.

1. Pick 2-4 alternative angles from the existing Topic Discovery output
2. Run each through Keyword Explorer (1 lookup each — cheap). **Check volume first** — many trending Malay phrases have literally 0 search volume because the interest lives on TikTok/Facebook, not Google
3. For any survivor with real volume, check its SERP for news-domination (high-DA outlets = unwinnable for a new site)
4. **Compare against the original candidate.** Then:
   - **A better option exists** → take it, no override needed
   - **All alternatives are worse** → an override may be justified, but only as a *comparative, evidence-backed* decision. Never override on the first failure without testing alternatives — that is rationalisation, not judgement

**If overriding, record ALL of this in `content/content-calendar.md`:** the measured Weak Spot values, every alternative tested and why it was rejected, the specific reasons the keyword is still viable (All-in-Title, LDA, intent-mismatched SERP slots), an honest ranking-timeline expectation, who approved it, and a revisit trigger. An undocumented override is not permitted — the audit trail is what separates a judgement call from ignoring the gate. See Post #4 (2026-07-29) for the reference example.

**Useful context when weighing an override:** DA is Moz's third-party estimate and **Google does not use it**, so Weak Spot is a proxy built on a proxy — a strong sanity check, not physics. Weigh it against All-in-Title (direct competition signal), LDA (proof a small site can hold a slot), and how many page-1 slots are intent-mismatched (product pages and news articles are far more displaceable than dedicated guides).
5. *(Optional, high-value)* Run **Domain Filter** → filter for social domains (YouTube, Reddit, Quora) ranking in top 10. Social results in the SERP = a genuine content gap a blog post can fill
6. Record **Weak Spot** and **Average DA** in the post's `content-calendar.md` entry

### Phase 2: Keyword Planner → Content Brief

> **WriterZen AI-credit gate:** Before Create Article, apply
> `.claude/rules/writerzen-ai-credit-gate.md`. The current authenticated UI
> must freshly prove **Write article title, description & outline = ON** and
> **Write the whole article = OFF**. Operations re-checks the exact state
> immediately before Create; unknown, missing, stale, or conflicting state
> blocks the submission.

1. Navigate to WriterZen → Keyword Planner → the project created in Phase 1
2. Find the topic/cluster containing the target keyword
3. Click **Suggest Content Brief** on the cluster
4. Manually adjust ALL 6 brief fields using values from `content-calendar.md`:
   - Content Format (dropdown — usually "Blog post")
   - Writing Tone (dropdown — usually "Informative/Explanatory")
   - Target Audience (text input — describe Malaysian audience)
   - Author's Perspective (text input — describe expert voice)
   - Content Angle (textarea — unique angle for this article)
   - Note for writer (textarea — writing guidelines, language style from AGENTS.md voice guide)
5. Click **Create Article**:
   - ⚠️ **CRITICAL: Select project FIRST** — the modal does NOT auto-select the last used project. The "Create" button stays disabled until you manually click the Project dropdown and select "DigiTrust Lab". This is the #1 reason the button appears stuck.
   - Project: Select existing "DigiTrust Lab" (NEVER create new)
   - AI Assistant: Check **only** "Write article title, description & outline"
   - **Never check "Write the whole article"**. This is prohibited for every
     DigiTrust Lab article mission, regardless of remaining credits.
   - Language: Malay, Location: Malaysia
6. Go to **Content Brief** tab in the modal — verify all 6 fields are populated from step 4
7. Click **Create** (button enables only after project is selected)

### Phase 3: Content Creator Step 1 — Outline

1. Review the AI-generated title, description, and outline
2. Adjust headings if needed using Competitive Analysis, Google Suggest Insights, and AI Assistant
3. **Plan internal links** — Check `content-calendar.md` Content Structure Strategy section:
   - Identify which existing posts this new post should link TO (pillar/parent content)
   - Identify which existing posts should link BACK to this new post (will be done in Phase 7)
   - Note the exact anchor text and target URLs for each link
4. Set word count target and heading/paragraph/image counts:
   - **Word count:** ~1000 (adjust based on topic depth)
   - **Headings:** 4+ (matches H2 count from outline)
   - **Paragraphs:** 4+ (matches content sections)
   - **Images:** 4 (standard for all posts — 1 featured + 3 in-content illustrations)
   - These are planning targets shown in the Content Creator score panel (e.g.,
     "WORDS 0/976", "IMAGES 0/4"); do **not** upload or insert images in
     WriterZen. Media work belongs to the WordPress/Respira publication stage.
5. Save the outline

### Phase 4: Content Creator Step 2 — Keywords to Include

1. **Enable the Highlight Keywords toggle FIRST** (before reviewing or editing any content):
   - Keywords sidebar panel → "Highlight keywords" checkbox (DOM id: `switch-enable-serp`)
   - In the existing Chrome tab, a normal click can be intercepted because a `<label>` captures the pointer event. Use the documented DOM/CUA workaround, then take a fresh snapshot and verify that the toggle and keyword count changed:
   - Take a fresh DOM snapshot and verify that the toggle and keyword count changed before editing.
   - This highlights every target keyword already present in the draft and shows the `0/N` missing count, so you can see exactly where to weave keywords in naturally
2. **Prioritize Opportunity keywords over Competitive keywords** — the two buckets are not equal:

   | Type | What it means | Priority |
   |------|--------------|----------|
   | **Opportunity keywords** | Ranking potential that competitors *underuse* | 🥇 Add these first — this is the easiest win |
   | **Competitive keywords** | Keywords competitors already rank for | Add naturally where they fit |

3. Review **Competitor's Keywords** — add relevant ones (target ~8-10)
4. Review **Suggested by WriterZen** only when the credit-gate handoff records
   documented keyword insufficiency, explicit user authorization, current
   displayed-cost evidence, and Operations' fresh pre-Create attestation;
   otherwise keep optional suggestions disabled
5. Optionally import from a saved WriterZen keyword list
6. Save keyword list

> **Never keyword-stuff.** Keywords must read naturally in Malay. If a keyword can't be placed without bending the sentence, leave it out — the Rank Math density target (0.5–2.5%) is a floor and ceiling, not a quota to force.

### Phase 5: Content Creator Step 3 — Native Drafting

**Writing Mode: "I'll write myself" (mandatory)**

> WriterZen supplies only the title, description, and competitor-backed
> outline. Never enable its full-article writer. Draft the body natively using
> the DigiTrust Lab voice and the frozen outline. If WriterZen reports
> insufficient AI credits for the outline-only request, stop as `BLOCKED`; do
> not upgrade, change plans, or switch to full-article generation without
> explicit user authorization.

1. Draft the article body natively from the approved content brief + outline
2. Review the draft section by section
3. **Edit for DigiTrust Lab voice** — match the semi-formal Malay standard from `.claude/skills/malay-voice-guide/SKILL.md`
4. **Reformat walls of text into rich visual structure** (MANDATORY):
   - WriterZen AI produces flat walls of text — every section must be reformatted
   - Use the full formatting toolkit: blockquotes, bullet/numbered lists, bold labels, before/after blocks, contrast pairs, warning/tip boxes
   - **See `.claude/skills/readability-pass/SKILL.md`** for the complete Rich Formatting Toolkit, blockquote/callout templates, and Formatting Checklist
   - Run the Formatting Checklist before publishing — no section should be a sea of text
   - Reference standards: Post #2 (`/cara-guna-chatgpt/`) and Post #3 (`/cara-buat-prompt-chatgpt/`)
5. Run **Show Analysis** — fix any flagged SEO issues
6. Apply the no-credit **Native Originality and Source-Attribution Gate**
   (`.claude/rules/native-originality-source-gate.md`). Record draft
   provenance, source/quotation attribution, clear distinctive-overlap review,
   and matching content/evidence hashes. Do not run WriterZen's Plagiarism
   Checker or claim that the dual naturalness reviews are a plagiarism scan.
7. **Note all Analysis improvements** for cross-checking in Phase 5.4/6.5:
   - Write down every "Problems" and "Improvements" item from the analysis panel
   - These get addressed during WordPress publishing and Rank Math optimization
   - Common items: content length, images, internal/external links, title length
8. Save the native draft and obtain the two independent fresh reviews required
   by the credit gate before publication: actual Anthropic/Claude Sonnet and
   independent OpenAI, both PASS and matched to the final content hash.

### Phase 5.4: Assemble and Stage the Final Publication Package

The naturalness hash is valid only when it covers the exact reader-facing
package that will be published. Complete every content-changing operation below
while the WordPress post remains a draft.

1. Extract the HTML from WriterZen and clean it:
   - Remove WriterZen annotations and `<hr>` separators.
   - Strip all `<h1>` tags because the Bricks template supplies the post H1.
   - Remove redundant uses of "Malaysia" unless context requires them.
   - Start the body with `<p>`, make the first body heading `<h2>`, and verify
     the H2 → H3 → H4 hierarchy.
   - Cross-check every Phase 5 analysis improvement.
   - Save the cleaned working copy to `content/drafts/<post-slug>.html` before
     running the local link gate.
   - Run the structural title gate and require a pass before staging:

     ```bash
     python scripts/verify-post-structure.py --file content/drafts/<post-slug>.html
     ```

     This must report zero body H1 elements. The Bricks single-post template
     supplies the page H1; a body H1 is a publication blocker because it
     duplicates the visible title for readers.
2. Insert the planned contextual internal and external links, then run:

   ```bash
   python scripts/verify-links.py --file content/drafts/<post-slug>.html
   ```

   This must pass before the draft is staged. Rank Math does not replace it.

> **NON-NEGOTIABLE MEDIA BOUNDARY:** WriterZen is text research and early
> article drafting only. Never upload, insert, attach, or troubleshoot
> images/media in WriterZen, including local-file chooser workarounds. All
> image/media upload, alt text, attachment verification, and insertion happen
> directly in WordPress via Respira during the publication-stage handoff. If an
> image is unavailable in WriterZen, record it as `Pending` and follow the
> WordPress media gate; do not retry a WriterZen upload.

> **WORDPRESS CAPTION DEFAULT:** Leave the WordPress Media Library `Image
> Caption` field empty by default for both featured images and inline article
> images. Never auto-generate or paste the image's alt text or description into
> `Image Caption`. Populate that field only when the user explicitly requests a
> reader-visible caption. Alt text remains a separate accessibility field and
> must still be finalized and set wherever the image requires it.

> **FEATURED/INLINE PLACEMENT RULE:** Real tool or UI screenshots (for example,
> Canva interface captures) are instructional inline media only and must never
> be used as the featured image. The featured image must be a separate DigiTrust
> Lab brand-color hero asset produced under the established design and
> `content/image-prompts.md` standard.

3. Before generating any featured, in-content, or CTA/card image, pause and ask
   the owner to choose exactly one image mode from `content/image-prompts.md`:
   `More Depth` or `Strict flat design`. Stop if the owner has not explicitly
   chosen; record the choice in each prompt and, for featured images, in the
   variety record. Then generate the images with ChatGPT or Gemini using the
   authoritative definitions and template in `content/image-prompts.md`.
   Before generating the featured image, inspect
   the previous six featured thumbnails together and complete the mandatory
   variety record: visual mode, subject class, composition, treatment, human
   presence, repeated-motif result, immediate-prior difference count, and
   thumbnail-comparison result. The gate requires no consecutive human-led
   images, no more than one human-led image in four consecutive posts, no
   person+desk+laptop+robot motif within the previous six, and at least three
   changed dimensions versus the immediate prior image. Run
   `python scripts/verify-featured-image-variety.py` with the completed record
   before archive. A failed thumbnail comparison blocks archive, upload, and
   publication. Finalize every Malay alt text before review.
3a. Apply the mandatory image audit gate before archiving or uploading:
   - Inspect each image at native resolution in the full frame and every marked
     region (faces, hands/arms, figures, edges, props, and any pseudo-writing).
   - PASS only when clean intentional pseudo-writing, abstract lines, bullets,
     and checkboxes remain acceptable, while distorted-looking letters,
     malformed glyphs, wobbly/uneven/merged strokes, inconsistent spacing,
     accidental readable text or numbers, logos, watermarks, orange blobs or
     halos behind or intersecting people/arms, and anatomy artifacts are absent.
   - On any failure, edit or regenerate non-destructively from the best
     composition, then repeat both inspections. Never “fix” by deleting all
     pseudo-writing. Record the pass before archive/upload.
4. Archive the generated images before cleanup:
   - Use each authoritative `Filename` from `content/image-prompts.md`.
   - Copy from the exact
     `C:\Users\Zamri\.codex\generated_images\<session-folder>` to
     `G:\Zamzam Biznez\DigiTrustLab\Blog images` in prompt order.
   - Set distinct destination `CreationTime` values so sorting descending shows
     Image 1 through the final image in order.
   - Verify every destination against its source by SHA-256 before upload or
     any explicitly requested source cleanup.
5. Through the Respira WordPress publication workflow, upload the images to
   WordPress Media, insert the final image elements and alt text into the
   WordPress draft, and set the featured image. Leave the Media Library `Image
   Caption` empty for featured and inline images unless the user explicitly
   requests a reader-visible caption; never copy alt text or description into
   that field. Do not attempt this in WriterZen. During this same handoff,
   verify and record separately that:
   - the featured placement uses the separate DigiTrust Lab brand-color hero
     asset; and
   - real tool/UI screenshots are placed only as instructional inline media,
     never as the featured image.
6. Stage the post as `draft` with the final content, title, category, and Rank
   Math title, description, focus keyword, primary category, and schema type.
7. Set the final 155–160 character excerpt through the editor data store:

   ```js
   const ex = "…final Malay excerpt containing the focus keyword…";
   wp.data.dispatch('core/editor').editPost({ excerpt: ex });
   await wp.data.dispatch('core/editor').savePost();
   ```

   Reload and require
   `wp.data.select('core/editor').getEditedPostAttribute('excerpt').length > 0`.
   Do not use Respira's unreliable `excerpt` parameter.
8. Register the draft post ID in `scripts/verify-malay-voice.py` before
   publication. An unknown ID exits 2 and blocks the live gate.
9. Export the exact final staged content to
   `content/drafts/<post-slug>.html` using the final-package format in
   `content/naturalness-reviews/README.md`: title, exact post content, an
   excerpt element marked `data-naturalness-kind="excerpt"`, then available SEO
   metadata. This package must include all headings, paragraphs, lists,
   blockquotes, captions, and alt text. No reader-facing edit is allowed between
   this export and the naturalness gate.

### Phase 5.5: Malay Naturalness Review Gate (MANDATORY — before WordPress publication)

This is a hard gate. Do not publish a draft that has only passed the mechanical
voice checker or received a high Rank Math score.

1. Freeze the exact final HTML exported in Phase 5.4. Confirm that its headings,
   paragraphs, lists, blockquotes, captions, alt text, excerpt, and available
   SEO metadata match the staged WordPress draft.
2. Run the deterministic naturalness rules and create
   `content/naturalness-reviews/<post-slug>.json`.
3. Ask two independent fresh sessions to review the same final content using
   the seven-check protocol in `content/naturalness-reviews/README.md`: one
   Claude Sonnet/Anthropic reviewer and one OpenAI reviewer. The Anthropic lane
   must use the repository's terminal-only Claude Code CLI helper with
   `--safe-mode --model sonnet --effort high --no-chrome
   --no-session-persistence --tools "" --output-format json --json-schema`.
   Do not use claude.ai, Claude in Chrome, or any GUI/web fallback. Fail closed
   when the CLI flags, logged-in authentication, runtime `modelUsage` provider,
   canonical model identity, or structured schema evidence is missing. Claude
   Code may report the genuine first-party runtime provider as `firstParty`;
   record that exact provider while keeping the artifact `model_family` as
   `anthropic`. Do not use Claude Opus unless the user explicitly changes the
   preference. Record both actual models and families in the artifact.
4. If either reviewer flags an issue, expresses uncertainty, or encounters an
   unapproved term, apply only a clear correction and rerun both reviews from
   scratch. If the wording requires a genuine editorial decision, stop for the
   user's decision.
5. Run the hard gate and require exit code 0:

   ```bash
   python scripts/verify-malay-naturalness.py \
     --file content/drafts/<post-slug>.html \
     --review content/naturalness-reviews/<post-slug>.json
   ```

6. Record the content hash, both model/family identities, artifact path, and
   passing result in the workflow evidence. Any later edit invalidates the hash
   and requires a complete fresh review by both families.

### Phase 6: Publish the Frozen WordPress Draft

Sol owns publication authorization and the final decision. A bounded worker
performs the publish transition and returns fresh live evidence; it may not
approve its own evidence or mark the article complete.

1. Re-fetch the staged draft and compare it with the Phase 5.5 reviewed package.
   Any reader-facing difference invalidates the approval and requires both fresh
   naturalness reviews.
2. Confirm the pre-publication evidence bundle:
   - passing local naturalness artifact and matching content hash;
   - passing local link gate;
   - final excerpt, images, alt text, featured image, category, SEO metadata,
     and schema already saved on the draft;
   - image archive destination and SHA-256 checks verified.
3. Publish with `respira_update_post(status=publish)`. Preserve the returned
   snapshot/evidence identifier when available.
4. Do not make a reader-facing edit after publication without invalidating and
   rerunning the corresponding naturalness or link evidence.
5. Open the live URL and verify that the intended article, title, images, and
   formatting render before beginning Phase 6.5. Confirm that the title
   appears once: the template title is the only H1 and the body begins with a
   paragraph.
6. Run the live structural title gate:

   ```bash
   python scripts/verify-post-structure.py --post-id <post-id>
   ```

   A body H1 or a body H1 matching the post title blocks the remaining Phase
   7 documentation and tracking gates until the content is corrected.

### Phase 6.5: Live Verification + Rank Math (MANDATORY — Never Skip)

This phase runs AFTER the post is published (Phase 6) but BEFORE documentation (Phase 7).

#### 6.5a: Live Malay Naturalness Revalidation

```bash
python scripts/verify-malay-naturalness.py \
  --post-id <post-id> \
  --review content/naturalness-reviews/<post-slug>.json
```

This must report exit code 0 against the live WordPress content. A live-content
hash mismatch means the published copy differs from the reviewed copy; stop,
fix the live post, save it, and rerun both gates before rank tracking.

#### 6.5b: Malay Voice Publish Gate

```bash
python scripts/verify-malay-voice.py <post-id>
```

**Must report 0 errors before proceeding.** If errors:
- Fix them in the content via `respira_update_post`
- Re-run the script
- If the command exits 2 for an unknown ID, stop and complete the Phase 5.4
  registration before rerunning. Do not treat configuration failure as a pass.

> **Full Malay voice standard:** See `.claude/skills/malay-voice-guide/SKILL.md` for the complete guide, including the publish gate protocol, DBP-aligned spelling, Bahasa Indonesia detection, and what the script cannot check (heading typos, tatabahasa, sentence fragments, comma splices, read-aloud flow).

#### 6.5c: Live Presentation and SEO Evidence

Verify the live page rather than relying on the editor or Rank Math score:

1. The expected featured image and in-content image count render, and every
   content image has the finalized Malay alt text.
2. The manual excerpt is non-empty after a reload.
3. The canonical URL, index/follow directive, SEO title, and meta description
   match the approved package.
4. The rendered schema includes the intended `Article` or `BlogPosting` data
   and featured image.
5. The heading hierarchy, table of contents, internal links, and outbound
   destinations render correctly.

Any reader-facing correction invalidates the naturalness hash. Any link edit
also invalidates the later link artifact.

#### 6.5d: Rank Math Sidebar Optimization

1. **Open the post in WordPress editor** and check the Rank Math sidebar score
2. **Prioritize essential SEO checks over cosmetic score points:**
   - Place the focus keyword naturally near the beginning of the SEO title.
   - Keep the title within the approved length and faithful to search intent.
   - A number or year may be used when genuinely useful and accurate.
   - Power words and sentiment words are cosmetic. Never force English hype
     such as "Ultimate", "Proven", or "Secret" into a Malay title merely to
     increase the score.
3. **Fix Additional issues:**
   - **Keyword density** — target 0.5%–2.5%. If below 0.5%, add the focus keyword naturally in intro, section transitions, and FAQ
   - **Outbound links** — at least one external link must be **dofollow** (not nofollow). If Rank Math says "all outbound links are nofollow":
     - Check Rank Math → Settings → Links → "Nofollow External Links" — if enabled, add the target domain to **"Nofollow Exclude Domains"** to make it dofollow
     - Alternatively, remove `target="_blank"` from the link (WordPress auto-adds nofollow to external links with target=_blank via Rank Math's setting)
   - **Table of Contents** — a ToC plugin must be active (Easy Table of Contents installed and configured). If "Content Readability" shows a ToC error, verify the plugin is active and the post has enough H2/H3 headings
4. **Fix Content Readability issues:**
   - Usually resolved by having a ToC plugin active + proper heading hierarchy (H2 → H3 → H4)
   - Ensure content length is sufficient (Rank Math flags short content)
5. **Re-check score** — aim for 80+, but never damage the approved Malay voice
   or natural title to chase cosmetic points. "Use Content AI" is a PRO upsell.
6. **Record the final score** in the post's content-calendar.md entry

If Rank Math optimization changes any reader-facing body, title, excerpt, alt
text, or SEO metadata, update the local final package and rerun both independent
naturalness reviews plus the local and live gates. A higher score cannot reuse a
stale approval hash.

> **Essential vs cosmetic checks:** Essential (MUST fix): keyword in title/URL/meta/intro/subheadings/alt, density 0.5-2.5%, content ≥600 words, has images, has internal links, schema. Cosmetic (skip): sentiment word, power word, "Use Content AI" (PRO upsell). The Respira Rank Math API (`respira_analyze_rankmath`) reports `computed_score` which only covers the 13 essential checks — the WP Admin sidebar score includes cosmetic checks too, so it will show a lower number.

### Phase 7: Post-Publish — Rank Tracking + Search Console + Internal Linking + Documentation

> **CLICKRANK DUAL-TRACKER HARD GATE:** Every published post requires two
> independent ClickRank tracker rows: the standard **Keyword Tracker** and the
> **AI Overview Tracker**. Add the same primary focus keyword (the one set in
> Rank Math) and the exact live URL to both surfaces. The standard tracker uses
> Malaysia + Device: All; the AI Overview tracker uses Malaysia + Malay where
> those controls are available. One ClickRank row never proves the other, and
> ClickRank Pages and Screpy are separate checks.
>
> **Shared pre-submit and async protocol for each ClickRank tracker:** take a
> fresh snapshot before submitting and record the visible tracker count. Search
> or filter for the exact focus keyword + live URL (including the current
> settings). If that exact row already exists, open it and verify it; do not
> submit another row. If no exact row exists, submit once, wait for async
> processing, then reload/reopen the same authenticated tab and verify the
> tracker count plus the exact keyword, URL, country, language/device, and
> visible result. A generic error toast, HTML parsed as JSON, or a stuck
> `Processing...` state is inconclusive. Do not retry until the count/row check
> proves that no row was created. `Not Found`, `N/A`, and `0%` are valid results.

1. **ClickRank — standard Keyword Tracker** (app.clickrank.ai/en/tracker):
   - Add the post's **primary focus keyword** only (the one set in Rank Math) + URL
   - Set country to Malaysia, device to All
   - **Do NOT add secondary keyword variants** — ClickRank auto-discovers those from Search Console. Only the focus keyword goes here. Keep the list clean.
   - This tracks traditional Google SERP rankings + impressions
   - Apply the shared pre-submit and async protocol above; the closeout must
     record both the pre-submit count and the post-submit/existing-row count.
2. **ClickRank — Website Optimization / Pages** (app.clickrank.ai/en/pages):
   - Add the exact published article URL to the Website Optimization queue using
     **Add URL**. If the URL is already present, do not add a duplicate; open its
     existing row instead.
   - Take a fresh snapshot and verify the exact URL appears in the queue with a
     visible optimization status. A successful Keyword Tracker or AI Overview
     entry does **not** prove that the URL is present here.
   - Open the page row and review the available title, meta description,
     headings, content, image-alt, and schema recommendations. Applying a
     recommendation is optional and remains subject to the ClickRank Usage
     Policy; reject hype wording and never overwrite the approved Malay copy
     without rerunning the affected naturalness and link gates.
   - Record the Pages queue result (URL, visible status, date, and any
     recommendation action or explicit no-change decision) in
     `content/content-calendar.md`. Missing Pages evidence blocks Phase 7
     completion.
3. **ClickRank — AI Overview Tracker** (app.clickrank.ai/en/ai-toolkit/overview-tracker):
   - Add the same focus keyword + URL (Malaysia, Malay language)
   - This monitors AI Overview visibility and AEO/organic presence; it is a
     separate required tracker from the standard Keyword Tracker
   - **Title/Meta optimization** — OPTIONAL. ClickRank's AI suggestions tend to be over-dramatic (hype words like "Ultimate", "Proven", "Secret"). Only apply if the suggestion is natural and matches our calm, helpful Malay voice. Manual titles are always preferred. When in doubt, ask the user.
   - Apply the shared pre-submit and async protocol above; verify the exact
     keyword, URL, Malaysia, and Malay row after submission or when an existing
     row is reused. Record the pre-submit and post-submit/existing-row counts.
4. **Screpy — Rank Tracker** (app.screpy.com → Rank Tracker → Add keywords):
   - Add the post's **primary focus keyword** only (Screpy associates the keyword with the tracked domain; it does not require a separate URL field)
   - Set Country: Malaysia, Language: Malay, and **Device: Both** in the same Add keywords action
   - **Do not add separate Mobile and Desktop entries** when the `Both` option is available; verify the keyword appears under both device tabs after submission
   - Screpy tracks traditional Google SERP rankings, competitor comparison, and page health
   - **Why this remains separate:** ClickRank AI Overview, ClickRank Keyword
     Tracker, and Screpy provide distinct evidence. Screpy is an independent
     traditional SERP rank check and cannot substitute for either ClickRank
     surface.
5. **Screpy — Re-run Crawler** (app.screpy.com → Pages → Analyze button):
   - Click "Analyze" to trigger a new crawl — this auto-discovers new post URLs for SEO health monitoring
   - Screpy does NOT have manual per-page URL addition — the crawler finds pages automatically
   - New posts published after the last crawl won't appear until the crawler runs again
6. **Google Search Console — URL Inspection and indexing request:**
   - Inspect the exact live article URL in the authenticated Search Console tab.
   - Request indexing when the URL is eligible and a request has not already
     been accepted for the same unchanged content.
   - Record the visible inspection status, request outcome, and timestamp.
     "Indexing requested" does not mean "indexed"; never collapse those states.
   - If authentication, quota, or a sitemap/cache issue blocks the request,
     record a follow-up instead of claiming completion.
7. **Run internal link builder** — Use the `internal-link-builder` skill to scan existing posts and add links pointing TO the new post:
   - Trigger: "build internal links" or load skill from `.claude/skills/internal-link-builder/SKILL.md`
   - This finds mentions of the new post's topic in older posts and adds contextual links back
   - Review the plan before applying (skill always asks for confirmation)
   - This is critical: the new post links UP to pillar content (done in Phase 5.4), but old posts must also link DOWN to the new post
   - Record the live inbound count and either the source post IDs or a specific `no_safe_context` reason in `content/link-reviews/<post-slug>.json`
   - After the scan creates or updates the artifact, run:
     `python scripts/verify-links.py --post-id <post-id> --inbound-review content/link-reviews/<post-slug>.json --check-destinations`
   - This is the live link hard gate. Any later inbound or outbound edit
     invalidates `link_hash` and requires a new scan and rerun.
8. Update `content/content-calendar.md`:
   - Change status to PUBLISHED ✅
   - Add URL, publish date, Post ID, WriterZen Article ID
   - Record final Rank Math score
   - Record **separate** ClickRank Keyword Tracker and ClickRank AI Overview
     evidence, plus ClickRank Pages, Screpy Both-device, Screpy crawl, and GSC:
     timestamp, exact keyword/URL, pre-submit and post-submit/existing-row
     counts, settings, and
     the verified visible result. These dashboards have no reliable API, so a
     generic "done" note is insufficient.
9. Update `STATE.json`:
   - Add to completed list
   - Increment blogPosts count
   - Update nextSteps (remove this post, add next post)
10. Update `NEXT.md`:
   - Mark Post as ✅ published
   - Add next post to task list
11. Update `ROADMAP.md` if applicable
12. **Content status gate (MANDATORY — run BEFORE committing):**
    ```bash
    python scripts/verify-content-status.py
    ```
    Compares steps 8–10 above against the live WordPress REST API. Must exit 0.
    - Catches: post marked PUBLISHED with no/wrong Post ID, slug or date drift,
      a live post missing from the calendar, a PLANNED entry that is already
      live, and a stale `blogPosts` count.
    - `--fix` repairs the safely derivable fields (currently `STATE.json`
      `keyMetrics.blogPosts`). Everything else it reports, you fix by hand.
    - **It does NOT verify steps 1–6** (ClickRank, Screpy, or GSC). Those have
      no reliable API. Confirm them in the authenticated dashboards and record
      the evidence in step 7.

    Why this is a gate and not a reminder: steps 8–10 were manual instructions
    for months and silently rotted. On 2026-08-05 an agent read the stale record
    and told the operator to redo finished work.
13. **Generate the article completion summary (MANDATORY AUTOMATIC CLOSEOUT):**
    - After the post-publish verification gate above, create or update exactly
      one concise Markdown artifact at
      `content/article-completion-summaries/<post-slug>.md` using the template
      in `content/article-completion-summaries/README.md`.
    - This is an execution step, not a suggestion or a chat-only report. It
      must run automatically for every article closeout and be completed before
      the workflow is considered complete.
    - For a published article, record the high-level journey from Topic
      Discovery through publication: why the angle was chosen, the selected
      keyword and key metrics, Golden Filter and Weak Spot results, the main
      writing/voice/SEO work, publication outcome, verification/tracking state,
      and open follow-ups.
    - Include a concise `Delegated work` section for every worker/agent
      involved: stage/role, actual model ID and reasoning effort when available,
      scope, high-level result/evidence, and any blocker or handoff. The
      orchestrator must reconcile returned worker outputs before writing this
      section and must not claim completion without evidence; mark missing or
      contradictory evidence as pending/blocking.
    - If publication is blocked or explicitly aborted, still create the same
      artifact with `Status: BLOCKED` or `Status: ABORTED`. Leave URL, Post ID,
      and publication date as `Not published`, state the blocking/abort reason,
      and never imply that publication or live verification occurred. If the
      block/abort happens before Phase 7, generate the artifact immediately at
      that terminal stop; do not wait for a post-publish gate that did not run.
    - Keep the artifact high-level: do not copy the article, browser
      transcripts, raw logs, or detailed UI steps. Link to existing evidence
      artifacts or the calendar when a detailed record is needed.
14. **Repository hygiene closeout (MANDATORY — every article posting):**
    - Run `git status --porcelain=v1 -uall` immediately after the article,
      evidence, media, and documentation work. Read every visible path and
      classify it before any completion claim. The closeout is blocked while
      any path is unreviewed.
    - Selectively stage only durable source, final hash-bound evidence, and
      approved durable media. Never use `git add .`, `git add -A`, or a broad
      wildcard. Keep the final naturalness package and its provider evidence;
      do not stage superseded retries or quarantine media as canonical
      evidence.
    - Keep exactly one final hash-bound naturalness evidence set per post.
      Explicitly locally exclude each superseded retry or quarantine path when
      it is not being retained for recovery, using exact paths only. Never use
      an exclusion that hides canonical evidence, `STATE.json`, or `NEXT.md`.
    - Remove only exact generated cache/temp files, and only after running the
      pre-action guard for each removal. Do not delete naturalness evidence,
      source, media, `STATE.json`, `NEXT.md`, or other durable artifacts as
      cleanup.
    - Commit and push logical groups, recording every commit SHA and the
      upstream/push result in the article completion summary. If a push is not
      authorized or fails, record that state and keep the closeout pending.
    - After cleanup and the final commit/push decision, rerun the fresh
      validators required by the article: `git diff --check`,
      `python scripts/verify-imports.py`,
      `python scripts/verify-content-status.py`, and the applicable SEO/link
      and structure validators (including `verify-links.py` and
      `verify-post-structure.py`). Record failures as blocking evidence.
    - Run `git status --porcelain=v1 -uall` again after the closeout actions,
      record its output and the residual-path decision for every remaining
      path, and do not declare the article complete while any path lacks an
      explicit classification and decision.

## Key Rules

- **Goal and Plan:** Use a Goal only when explicitly requested; keep a Plan for
  phases -2 through 7 and resume it instead of restarting completed work
- **Delegation:** All substantive execution goes to a configured bounded
  worker; Sol Light owns phase transitions, publishing authorization, synthesis,
  final decisions, and evaluation of worker-produced verification evidence
- **Single stateful owner:** Never parallelize authenticated Chrome, WriterZen,
  WordPress, tracking dashboards, or canonical documentation writes
- **Previous-post gate:** Verify the prior article's live and tracking status
  before selecting the next topic
- **Language:** Bahasa Melayu baku, formal–semi-formal, 'anda' not 'korang'
- **Italic Policy:** See `.claude/skills/malay-voice-guide/SKILL.md` §4c for full policy
- **AI Creativity Level:** Always set to 1
- **Content Creator Project:** Always use existing "DigiTrust Lab" — never create new
- **Keyword List:** Always use existing "DigiTrust Lab Blog Posts" (ID: 68708)
- **Keyword Planner Project:** Create a **NEW** project per post topic. WriterZen clustering is one-time and cannot append to an existing project
- **SERP View / AI Assistant toggles:** Leave OFF during Step 1 (Outline)
- **Create Article AI-credit gate:** Use only "Write article title, description & outline"; "Write the whole article" is prohibited. The article body is always drafted natively and must pass the dual independent review gate. See `.claude/rules/writerzen-ai-credit-gate.md` and run `python scripts/verify-writerzen-ai-credit-gate.py`.
- **WriterZen keyword suggestions:** Keep "Use WriterZen to suggest more keywords" OFF when the validated Keyword List/Planner cluster is adequate. Enable only with documented insufficiency, explicit user credit-spend authorization, current displayed cost evidence, and Operations' fresh pre-Create attestation. This is separate from Google NLP.
- **Quota check (MANDATORY):** Never start a research session without Phase -1
- **Golden Filter (MANDATORY):** Always apply in Phase 0b — Golden Score ≤10, All-in-Title ≤10, Volume ≥100 (relax volume to 50 if needed, never the other two)
- **Weak Spot gate (MANDATORY):** Never write a post whose target cluster has Weak Spot < 2
- **30-day freshness:** Re-run Keyword Explorer if the last search for this topic is older than 30 days
- **Titles are provisional:** Planned titles in `content-calendar.md` are placeholders until Topic Discovery confirms a winnable angle
- **Editorial relevance gate (MANDATORY):** Apply `.claude/rules/editorial-relevance-gate.md` before Phase -1 and require Research, SEO, and Operations relevance attestations before credit, project, list, or drafting actions
- **Image generation:** Use ChatGPT or Gemini for featured and in-content images. See `content/image-prompts.md` for the prompt template, design system, and variation guide
- **WordPress Image Caption default:** Leave `Image Caption` empty for featured and inline images by default; never paste alt text or description there. Only add a reader-visible caption when the user explicitly requests one. Keep alt text separate and required where appropriate.
- **Image filenames (MANDATORY):** `{post-slug}-{image-description}.png` (lowercase, hyphens only)
- **In-content images:** Add images under H2 sections to break up text. See `content/image-prompts.md` for prompts
- **Image prompts library:** All prompts stored in `content/image-prompts.md`. Update when a post is published
- **Featured-image variety gate (MANDATORY):** Inspect and record the previous six thumbnails, rotate approved bounded treatments, enforce the human/motif/difference rules, and block archive/upload on a failed thumbnail comparison. See `content/image-prompts.md`.
- **Image audit gate (MANDATORY):** Before archive/upload, inspect the full frame and marked regions at native resolution; preserve clean pseudo-writing, abstract lines, bullets, and checkboxes, but reject malformed glyphs or strokes, inconsistent spacing, accidental readable text/numbers, logos/watermarks, orange blobs/halos intersecting people/arms, and anatomy artifacts. Non-destructively edit or regenerate from the best composition and re-inspect on failure.
- **Post Excerpt (MANDATORY):** Every post MUST have a manual excerpt (155–160 characters). Set and reload-verify it via the `wp.data` store method in Phase 5.4 before naturalness review and publication — NOT via Respira's `excerpt` parameter
- **Content formatting (MANDATORY):** See `.claude/skills/readability-pass/SKILL.md` for Rich Formatting Toolkit, blockquote/callout templates, and Formatting Checklist
- **Malay naturalness gate (MANDATORY):** Run `python scripts/verify-malay-naturalness.py` against final HTML before Phase 6 and the live post after publication; both must exit 0
- **Claude reviewer lane (MANDATORY):** Use `scripts/run-claude-naturalness-review.ps1` through terminal-only Claude Code CLI with the exact no-history, no-browser, toolless flags and structured provider/model evidence. Never use claude.ai web/GUI or silently substitute another provider.
- **Malay mechanical voice gate (MANDATORY):** Run `python scripts/verify-malay-voice.py <post-id>` in Phase 6.5 — must be 0 errors before Phase 7
- **Content status gate (MANDATORY):** Run `python scripts/verify-content-status.py` at the end of Phase 7 — must exit 0 before committing. It does not cover ClickRank, Screpy, or GSC dashboard evidence
- **Article completion summary (MANDATORY):** After the Phase 7 verification gate, automatically create or update `content/article-completion-summaries/<post-slug>.md`; use `BLOCKED`/`ABORTED` without publication claims when the article does not publish
- **Internal links (outbound):** Always link new post UP to pillar/parent content during Phase 5.4 (1-3 links)
- **Internal links (inbound):** Always run `internal-link-builder` skill in Phase 7 to add links from older posts TO the new post
- **Internal link planning:** Always plan links in Phase 3 (outline) before writing
- **Link hardening:** Run `scripts/verify-links.py` before publication and against the live post after publication. Do not use Rank Math's link checks as a substitute. Store the inbound decision in `content/link-reviews/<post-slug>.json`.
- **SEO meta:** Always set Rank Math title (≤60 chars), description (≤160 chars), focus keyword, primary category
- **Rank tracking (MANDATORY):** Every published post's same focus keyword + exact live URL must be added and verified in BOTH ClickRank AI Overview Tracker AND ClickRank standard Keyword Tracker; Screpy Rank Tracker remains a separate required traditional-SERP check
- **ClickRank Pages gate (MANDATORY):** Every published post's exact URL must be present in ClickRank Website Optimization / Pages with a fresh visible status and a recorded recommendation/no-change decision before Phase 7 can complete. Tracker rows alone are insufficient.
- **Search Console (MANDATORY):** Inspect the final URL, request indexing when eligible, and record the visible state without equating a request with successful indexing
- **Manual dashboard evidence:** Record exact keyword/URL, settings, timestamp,
  and visible result separately for both ClickRank trackers, ClickRank Pages,
  Screpy, and GSC; `verify-content-status.py` cannot prove these steps
- **ClickRank title/meta optimization (OPTIONAL):** Reject hype words. Accept natural words. Manual titles always preferred
- **Content standardization:** Always strip `<h1>` tags from WriterZen content, remove redundant "Malaysia" mentions, cross-check formatting against Post #1
- **Template-title duplication gate:** Run `verify-post-structure.py` on the final draft and the live post. Zero body H1 elements are required because the Bricks single-post template owns the visible post H1.

## Where Things Live

| Topic | File | Rule |
|-------|------|------|
| Keyword research detail (WriterZen tools, Golden Filter, Weak Spot) | `.claude/skills/writerzen-keyword-research/SKILL.md` | Don't duplicate WriterZen UI steps here |
| Image prompt template, design system, variation guide, examples | `content/image-prompts.md` | Don't paste prompt templates here |
| Rich Formatting Toolkit, blockquote/callout templates, Formatting Checklist | `.claude/skills/readability-pass/SKILL.md` | Don't paste HTML templates here |
| Malay voice standard, publish gate, DBP rules, Bahasa Indonesia detection | `.claude/skills/malay-voice-guide/SKILL.md` | Don't paste voice rules here |
| Delegation concepts and examples | `docs/knowledge-library/delegation-patterns.md` | Keep this skill to routing and phase ownership |
| Sequential pipeline phases (−2 through 7) | **This file** | The pipeline lives here and only here |
| Key Rules summary | **This file** | One-line reminders with pointers to full docs |

> **If you are about to paste a table or template into this skill, it belongs in one of those files — add a pointer instead.**
