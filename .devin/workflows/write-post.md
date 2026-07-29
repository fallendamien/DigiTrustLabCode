---
description: Write and publish a blog post using the WriterZen Option C pipeline. Starts with a quota check and Topic Discovery (never skip these — do NOT start at Keyword Explorer with a guessed keyword), then Keyword Explorer + Golden Filter → Keyword List → cluster into a NEW Keyword Planner project → Weak Spot ≥ 2 gate → Content Brief → Content Creator → publish via Respira MCP → Rank Math → ClickRank/Screpy rank tracking.
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

## WriterZen Tool Hierarchy (CRITICAL — know this before starting)

| Tool | Purpose | Persistence | When to use |
|------|---------|-------------|-------------|
| **Keyword Explorer** | Discover keywords + metrics | Session-only | Research phase |
| **Keyword List** | Permanent keyword storage | ✅ Permanent | Save keywords from Explorer |
| **Keyword Group** | Temporary scratchpad | ❌ Session-only | NEVER use — disappears after session |
| **Keyword Planner** | Cluster keywords into topics | Project-based | Planning phase |
| **Content Creator** | Generate outline + write article | Project-based | Writing phase |

### ⚠️ Keyword List vs Keyword Group (Learned 2026-07-21)

- **ALWAYS use "Add keyword to LIST"** (permanent) — NEVER "Add keyword to GROUP" (temporary, disappears after session)
- Keyword List is the bridge between Explorer and Planner

### ⚠️ Project Structure (Updated 2026-07-21 — verified against WriterZen official guide)

- **ONE Keyword List** for all blog posts: "DigiTrust Lab Blog Posts" (ID: 68708) — single source of truth
- **ONE Keyword Planner project PER blog post topic** — WriterZen clustering is one-time, cannot append to existing
- **ONE Content Creator project**: "DigiTrust Lab" (existing) — all articles under this project
- Previous rule "never create new Planner projects" was WRONG — WriterZen requires a new project per cluster run

## Steps

### Phase -1: Quota Check (MANDATORY — before any research session)

Golden Filter costs **1 Keyword Credit per keyword in the result set** (39 keyword ideas = 39 credits). Never start research blind.

1. Navigate to `https://app.writerzen.net/user/profile-setting?tab=limit`
2. Record remaining: **Topic Lookup/Day**, **Keyword Lookup/Day**, **Keyword Credit/Month**, **AI Words/Month**
3. Apply the budget rules:
   - Keyword Credit < 10,000 → selective Golden Filter only (top 3-5 keywords, not full result sets)
   - Keyword Credit < 5,000 → skip Golden Filter, fall back to manual KD + All-in-Title checks via SERP overview
   - **AI Words/Month = 8,000 total.** At ~1,000 words/post, "Write all for me" (Phase 5) supports roughly **8 posts/month**. If the remaining balance won't cover this post, switch to "I'll write myself" and draft natively instead.
4. Note consumption at end of session; update `content/SEO-CHEATSHEET.md` limits table if running low

> **30-day freshness rule:** WriterZen search results expire after 30 days. If the last Keyword Explorer run for this topic is older than 30 days, start a fresh search — do NOT reuse stale metrics.

### Phase 0a: Topic Discovery (find the winnable angle BEFORE committing to a title)

> **Why this exists:** DigiTrust Lab is a low-DA site. Picking a title first and hunting for a keyword afterwards is backwards — it commits you to an angle before checking whether it's rankable. Topic Discovery reverses that. Planned titles in `content-calendar.md` are **provisional** until this phase confirms them.

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

> ⚠️ "Go back to Phase 0a" means **pick a different candidate from the Topic Discovery output you already have** — it does NOT mean re-running Topic Discovery. That run already produced dozens of candidate angles; re-running the same seed burns a lookup and returns the same topics. Only re-run Topic Discovery when the existing candidates are exhausted, or when moving to a different subject area entirely. (Unmined depth in an existing run: the per-card **"Show ideas"** panels, and re-reading at a different Relevance setting.)

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
   - AI Assistant: Check "Write article title, description & outline"
   - Also check "Write the whole article" (per Write all for me strategy)
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
   - These targets appear in the Content Creator score panel (e.g., "WORDS 0/976", "IMAGES 0/4")
5. Save the outline

### Phase 4: Content Creator Step 2 — Keywords to Include

1. **Enable the Highlight Keywords toggle FIRST** (before reviewing or editing any content):
   - Keywords sidebar panel → "Highlight keywords" checkbox (DOM id: `switch-enable-serp`)
   - Playwright `click()` times out here — a `<label>` intercepts pointer events. Toggle via JS evaluate:
     ```js
     document.getElementById('switch-enable-serp').click()
     ```
   - This highlights every target keyword already present in the draft and shows the `0/N` missing count, so you can see exactly where to weave keywords in naturally
2. **Prioritize Opportunity keywords over Competitive keywords** — the two buckets are not equal:

   | Type | What it means | Priority |
   |------|--------------|----------|
   | **Opportunity keywords** | Ranking potential that competitors *underuse* | 🥇 Add these first — this is the easiest win |
   | **Competitive keywords** | Keywords competitors already rank for | Add naturally where they fit |

3. Review **Competitor's Keywords** — add relevant ones (target ~8-10)
4. Review **Suggested by WriterZen** — add any that fit naturally
5. Optionally import from a saved WriterZen keyword list
6. Save keyword list

> **Never keyword-stuff.** Keywords must read naturally in Malay. If a keyword can't be placed without bending the sentence, leave it out — the Rank Math density target (0.5–2.5%) is a floor and ceiling, not a quota to force.

### Phase 5: Content Creator Step 3 — Write

**Writing Mode: "Write all for me" (AI Draft → Human Edit)**

> **Strategy (Learned 2026-07-21):** Always use "Write all for me" instead of "I'll write myself".
> The detailed content brief (Malay angle, audience, tone, perspective) gives the AI enough
> context to produce a usable Malay draft. We then refine for DigiTrust Lab voice consistency.
> This is the most efficient path for a solo blogger — let AI draft, human edits.

1. Click **Write all for me** (NOT "I'll write myself")
2. Set AI Creativity Level = 1 for best quality
3. Let AI generate the full draft based on the content brief + outline
4. Review generated content section by section
5. **Edit for DigiTrust Lab voice** — match the semi-formal Malay standard from AGENTS.md voice guide
6. **Reformat walls of text into rich visual structure** (MANDATORY — see Key Rules → "Content formatting"):
   - WriterZen AI produces flat walls of text — every section must be reformatted
   - Use the full formatting toolkit: blockquotes, bullet/numbered lists, bold labels, before/after blocks, contrast pairs, warning/tip boxes
   - Copy-paste blockquote template from Key Rules (orange border, warm bg, rounded corners)
   - Run the Formatting Checklist (Key Rules) before publishing — no section should be a sea of text
   - Reference standards: Post #2 (`/cara-guna-chatgpt/`) and Post #3 (`/cara-buat-prompt-chatgpt/`)
7. Run **Show Analysis** — fix any flagged SEO issues
8. Run **Plagiarism Check** — ensure 0% plagiarism
9. **Note all Analysis improvements** for cross-checking in Phase 6/6.5:
   - Write down every "Problems" and "Improvements" item from the analysis panel
   - These get addressed during WordPress publishing and Rank Math optimization
   - Common items: content length, images, internal/external links, title length
10. Save (not Done — keep article in Content Creator)

### Phase 6: Publish to WordPress via Respira MCP

1. Extract HTML content from WriterZen editor (via browser evaluate)
2. **Clean and standardize content** (critical for consistent formatting across all blog posts):
   - Remove WriterZen annotations ("Kata kunci:" lines, `<hr>` separators)
   - **Strip all `<h1>` tags** — the Bricks template renders the post title as H1; any H1 in content creates a duplicate massive title
   - **Remove redundant "Malaysia" mentions** — the audience is already Malaysian; WriterZen AI tends to over-localize when Target Audience mentions Malaysians. Keep only if contextually necessary (e.g., comparing Malaysian vs international context)
   - **Cross-check formatting against Post #1** (`/apa-itu-ai/`) as the reference standard — content should start with `<p>` tags, first heading should be `<h2>`, no H1 in content body
   - Verify heading hierarchy: H2 → H3 → H4 (no skipped levels)
   - **Cross-check against Phase 5 Step 8 improvement notes** — ensure each item is addressed:
     - Content length gap → add intro/conclusion paragraphs if needed
     - Images → handled in Step 5 (featured image) + Step 5b (in-content images)
     - Internal/external links → handled in Step 3
     - Title length → handled in Rank Math meta (Phase 6.5)
3. **Insert internal links** — Replace plain text mentions with `<a href>` links to related posts:
   - Check the plan from Phase 3 Step 3
   - Link to pillar/parent content (e.g., "kecerdasan buatan (AI)" → `/apa-itu-ai/`)
   - Use natural anchor text, not keyword-stuffed
   - Aim for 1-3 internal links per post (don't over-link)
4. Update the draft post via `respira_update_post`:
   - Set content, title, status=draft
   - Set Rank Math SEO meta: `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`, `rank_math_primary_category`
   - Set categories
5. **Generate featured image via Gemini Nano Banana 2** (NOT Openverse stock photos — those break visual consistency):
   - Use the standard DigiTrust Lab illustration prompt template (see Key Rules below)
   - Style: flat illustration, brand colors, 16:9 aspect ratio
   - Download the generated image, then sideload via `respira_sideload_image`
   - Set alt text describing the illustration in Malay
6. Set featured image via `respira_update_post` with `featured_media`
7. Publish via `respira_update_post` with `status=publish`
8. **Set post excerpt via WordPress editor (NOT Respira — `excerpt` param is unreliable):**
   - Navigate to `wp-admin/post.php?post={ID}&action=edit`
   - Open Settings sidebar (gear icon) → Post tab
   - Click "Add an excerpt…" button
   - Type 155–160 char Malay summary including focus keyword
   - Close excerpt modal
   - Click Save/Update button (`button.editor-post-publish-button`)
9. Verify on live site: navigate to URL, check rendering, SEO title, internal links, featured image

### Phase 6.5: Rank Math Sidebar Optimization (MANDATORY — Never Skip)

This phase runs AFTER the post is published (Phase 6) but BEFORE documentation (Phase 7). The goal is to push the Rank Math SEO score as high as possible before moving on.

1. **Open the post in WordPress editor** and check the Rank Math sidebar score
2. **Fix Title Readability issues:**
   - SEO title must contain a **power word** (Rank Math uses an English-based list — e.g., "Ultimate", "Proven", "Essential", "Complete", "Secret")
   - SEO title must contain a **sentiment word** (positive/negative — e.g., "Best", "Amazing", "Proven", "Powerful", "Easy")
   - SEO title must contain a **number** (year counts, e.g., "2026")
   - Focus keyword must appear at the **beginning** of the SEO title
   - **Malay words like "Terbaik", "Mudah", "Penting" are NOT recognized** by Rank Math — use English power/sentiment words that blend naturally
3. **Fix Additional issues:**
   - **Keyword density** — target 0.5%–2.5%. If below 0.5%, add the focus keyword naturally in intro, section transitions, and FAQ. Count includes exact match + word combinations.
   - **Outbound links** — at least one external link must be **dofollow** (not nofollow). If Rank Math says "all outbound links are nofollow":
     - Check Rank Math → Settings → Links → "Nofollow External Links" — if enabled, add the target domain to **"Nofollow Exclude Domains"** to make it dofollow
     - Alternatively, remove `target="_blank"` from the link (WordPress auto-adds nofollow to external links with target=_blank via Rank Math's setting)
   - **Table of Contents** — a ToC plugin must be active (Easy Table of Contents installed and configured). If "Content Readability" shows a ToC error, verify the plugin is active and the post has enough H2/H3 headings
4. **Fix Content Readability issues:**
   - Usually resolved by having a ToC plugin active + proper heading hierarchy (H2 → H3 → H4)
   - Ensure content length is sufficient (Rank Math flags short content)
5. **Re-check score** — aim for 80+. The only unfixable error is "Use Content AI" (Rank Math PRO feature)
6. **Record the final score** in the post's content-calendar.md entry

### Phase 7: Post-Publish — Rank Tracking + Internal Linking + Documentation

1. **ClickRank — Keyword Tracker** (app.clickrank.ai/en/tracker):
   - Add the post's **primary focus keyword** only (the one set in Rank Math) + URL
   - Set country to Malaysia, device to All
   - **Do NOT add secondary keyword variants** — ClickRank auto-discovers those from Search Console. Only the focus keyword goes here. Keep the list clean.
   - This tracks traditional Google SERP rankings + impressions
2. **ClickRank — AI Overview Tracker** (app.clickrank.ai/en/ai-toolkit/overview-tracker):
   - Add the same focus keyword + URL (Malaysia, Malay language)
   - This is the PRIMARY reason we use ClickRank — monitors AI Overview visibility and organic ranking
   - **Title/Meta optimization** — OPTIONAL. ClickRank's AI suggestions tend to be over-dramatic (hype words like "Ultimate", "Proven", "Secret"). Only apply if the suggestion is natural and matches our calm, helpful Malay voice. Manual titles are always preferred. When in doubt, ask the user.
3. **Screpy — Rank Tracker** (app.screpy.com → Rank Tracker → Add keywords):
   - Add the post's **primary focus keyword** only + URL (Malaysia, Malay, desktop + mobile)
   - Screpy tracks traditional Google SERP rankings, competitor comparison, and page health
   - **Why both tools:** ClickRank = AI Overview/AEO tracking, Screpy = traditional SERP rank tracking + technical audits. They serve different purposes.
4. **Screpy — Re-run Crawler** (app.screpy.com → Pages → Analyze button):
   - Click "Analyze" to trigger a new crawl — this auto-discovers new post URLs for SEO health monitoring
   - Screpy does NOT have manual per-page URL addition — the crawler finds pages automatically
   - New posts published after the last crawl won't appear until the crawler runs again
   - **Screpy Uptime** monitors the domain (digitrustlab.com) as a whole, not individual pages
5. **Run internal link builder** — Use the `internal-link-builder` skill to scan existing posts and add links pointing TO the new post:
   - Trigger: "build internal links" or load skill from `.devin/skills/internal-link-builder/SKILL.md`
   - This finds mentions of the new post's topic in older posts and adds contextual links back
   - Review the plan before applying (skill always asks for confirmation)
   - This is critical: the new post links UP to pillar content (done in Phase 5), but old posts must also link DOWN to the new post
6. Update `content/content-calendar.md`:
   - Change status to PUBLISHED ✅
   - Add URL, publish date, Post ID, WriterZen Article ID
   - Record final Rank Math score
7. Update `STATE.json`:
   - Add to completed list
   - Increment blogPosts count
   - Update nextSteps (remove this post, add next post)
8. Update `NEXT.md`:
   - Mark Post as ✅ published
   - Add next post to task list
9. Update `ROADMAP.md` if applicable
10. Git commit + push all documentation updates

## Key Rules

- **Language:** Bahasa Melayu baku, formal–semi-formal, 'anda' not 'korang'
- **Italic Policy (MANDATORY):** Italicize English terms code-switched into BM sentences using `<em>` tags (e.g. <em>prompt</em>, <em>brainstorming</em>, <em>chat</em>, <em>Sign Up</em>, <em>Enter</em>, <em>vs</em>, <em>chatbot</em>, <em>natural</em>). Do NOT italicize: brand names (ChatGPT, OpenAI), acronyms (AI, NLP, API), or fully absorbed loan words (online, email/emel, blog, download, upload, login, link, video, tutorial). Standardize spelling — use BM spelling "emel" not "email" throughout. See `malay-voice-guide/SKILL.md` §4c for full policy.
- **AI Creativity Level:** Always set to 1
- **Content Creator Project:** Always use existing "DigiTrust Lab" — never create new
- **Keyword List:** Always use existing "DigiTrust Lab Blog Posts" (ID: 68708) — one permanent list for all posts
- **Keyword Planner Project:** Create a **NEW** project per post topic (e.g. "Post 4 — Prompt AI Illustration"). WriterZen clustering is one-time and cannot append to an existing project. ⚠️ The older rule "always reuse project ID 178201 / never create new" was **WRONG** — 178201 is a legacy project, not a target. Do not reuse it.
- **SERP View / AI Assistant toggles:** Leave OFF during Step 1 (Outline)
- **Quota check (MANDATORY):** Never start a research session without Phase -1. Golden Filter costs 1 credit per keyword; AI Words cap is 8,000/month (~8 posts at 1,000 words)
- **Golden Filter (MANDATORY):** Always apply in Phase 0b before clustering — Golden Score ≤10, All-in-Title ≤10, Volume ≥100 (relax volume to 50 if needed, never the other two)
- **Weak Spot gate (MANDATORY):** Never write a post whose target cluster has Weak Spot < 2. Pick a different angle instead
- **30-day freshness:** Re-run Keyword Explorer if the last search for this topic is older than 30 days
- **Titles are provisional:** Planned titles in `content-calendar.md` are placeholders until Topic Discovery (Phase 0a) confirms a winnable angle. Keyword decides the title, not the reverse
- **Never skip the Content Creator pipeline** — outline must be generated through WriterZen's AI + competitor research
- **Featured image:** Always use Gemini Nano Banana 2 (NOT Openverse stock photos). Use the standard prompt template below. Cross-check visual style against Post #1 (`/apa-itu-ai/`)
- **Image filenames (MANDATORY):** Every time you provide a Gemini prompt, ALSO provide the SEO-optimized filename. Format: `{post-slug}-{image-description}.png` (lowercase, hyphens only, no underscores). Example: `apa-itu-ai-neural-network.png`. This applies to both featured images and in-content images.
- **In-content images (SEO best practice):** Add images under H2 sections to break up text, increase time on page, and earn Google Image search traffic. Workflow: (1) Agent audits post and identifies H2s needing images, (2) Agent provides prompts + filenames, (3) User generates in Gemini Nano Banana 2 and uploads to WordPress Media, (4) Agent inserts each image into correct section with Malay alt text and caption.
- **Image prompts library:** All prompts and filenames are stored in `content/image-prompts.md`. Published posts have content-derived prompts; planned posts are TBD until content is drafted. **Update this file** when a post is published (replace TBD with actual prompts) or when a new post is planned (add a TBD section).
- **Post Excerpt (MANDATORY):** Every post MUST have a manual excerpt (155–160 characters). The excerpt is a concise Malay summary that includes the focus keyword. It appears on blog archive pages, category pages, search results, and RSS feeds. Without it, WordPress auto-generates a truncated first paragraph which often cuts off awkwardly. **Must be set via WordPress editor** (Settings sidebar → Post tab → "Add an excerpt…") — NOT via Respira's `excerpt` parameter, which is unreliable and silently ignored on some posts. Always click Save/Update after setting the excerpt.

### Image Prompt Template (Gemini Nano Banana 2)

**Always provide BOTH the prompt AND the filename together:**

```
Prompt:
Flat illustration style. [SUBJECT DESCRIPTION]. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. [VISUAL ELEMENT — see variation guide below]. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

Filename: {post-slug}-{image-description}.png
```

**Design system (never change these):**

| Element | Value |
|---------|-------|
| Style | Flat illustration, simple geometric shapes, bold outlines |
| Background | Warm off-white `#FAFAF8` (matches blog background) |
| Primary accent | Orange `#E8621A` (DigiTrust Lab brand) |
| Dark elements | Dark charcoal `#1A1A1A` |
| Highlights | White |
| Aspect ratio | 16:9 (wide format, min 1024×576) |
| Text in image | NEVER — no text or words |

**Visual element variation guide (rotate these — avoid repeating "icons floating around" every time):**

| Variation | Example |
|-----------|---------|
| Icons floating around | Icons floating around: chat bubble, lightbulb, gears |
| Geometric patterns | Subtle geometric patterns and dotted lines connecting elements |
| Abstract shapes | Abstract organic shapes flowing through the composition |
| Minimalist negative space | Minimalist composition with generous negative space and a single focal element |
| Split composition | Split scene showing before/after or contrast between two concepts |
| Isometric scene | Isometric view of the scene with layered depth |
| Top-down flat lay | Top-down flat lay perspective of objects arranged on a surface |
| Cinematic editorial poster | Large irregular framed scene, dramatic silhouettes, a simple adjacent symbolic object, plus dashed orbital lines and small geometric accents |

### Optional: Cinematic Editorial-Poster Variation

Use this selectively for high-concept articles, cautionary topics, myth-vs-reality explainers, or a dramatic visual metaphor. It is an accent style, **not the default**.

- Keep the DigiTrust Lab palette: warm off-white `#FAFAF8`, orange `#E8621A`, charcoal `#1A1A1A`, white highlights.
- Use a large irregular framed/vignette scene, strong outlines, foreground silhouettes, cinematic depth, and slight retro print energy.
- Add a simple adjacent symbolic object and subtle dashed orbital lines or geometric accents to connect the composition.
- **Never request a direct imitation of a named living artist or copy a reference composition.** Describe visual traits instead.
- Avoid logos, watermarks, legible text, gore, overly dark scenes, or excessive detail that harms the clean blog aesthetic.

**Prompt addition:** `Cinematic editorial-poster composition: a large irregular framed vignette scene with dramatic orange-and-charcoal contrast, bold black outlines, foreground silhouettes, a simple symbolic object outside the frame, and subtle dashed orbital lines with small geometric accents. Flat, clean, text-free, with slight retro print energy.`

**Rule:** Vary the visual element style across images within the same post so they feel like a curated art collection, not a template repeat. The color palette and flat illustration style stay consistent — the composition and decorative elements change. Think "art lover's blog," not "corporate stock art."

**Anatomy fix (MANDATORY):** AI image generators frequently produce images with missing, deformed, or unnaturally positioned hands and arms. ALWAYS append this to prompts featuring humans or robots: `"Both person and robot have complete visible arms and hands with natural positioning."` If the generated image still has hand issues, regenerate with emphasis: `"All hands fully rendered with five fingers each, arms complete from shoulder to fingertips, natural pose."`

**Gemini image reference workflow (for fixing background color or style drift):** When an AI generator produces a great composition but wrong background color or style, use Gemini's image reference feature to recreate it on-brand:
1. Upload the image you like to Gemini
2. Ask: "Re-create this exact scene but with warm off-white (#FAFAF8) background, flat illustration style, charcoal (#1A1A1A) outlines, orange (#E8621A) accents, white highlights. All human hands must have five fingers. No text, labels, logos, or watermarks."
3. Gemini preserves the composition while fixing the brand colors
4. Save the result with the same SEO filename and re-upload to WordPress Media

**Example (Post #1 — "Apa Itu AI" — featured image, icons floating):**
> Flat illustration style. A Malaysian man sitting at a desk with a glowing brain icon on a computer screen. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around: chat bubble, lightbulb, gears. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Example (Post #2 — "Cara Guna ChatGPT" — split composition):**
> Flat illustration style. A split scene: left side shows a messy desk with scattered papers and a frustrated person, right side shows the same desk organized with a glowing ChatGPT interface on a tablet, tasks neatly sorted into folders. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Subtle geometric patterns connecting the two sides. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Example (Post #1 in-content — "Bagaimana AI Berfungsi" — minimalist, illustrates article analogy):**
> Flat illustration style. A child pointing at different animals on flashcards — a cat, a dog, a bird — learning to recognize patterns, with a parallel digital grid showing the same concept with data points being sorted into categories. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist composition with generous negative space and a single focal element. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Example (cinematic editorial poster — myth-vs-reality explainer):**
> Flat cinematic editorial-poster illustration. A large irregular framed vignette shows a giant charcoal robot looming over a small city while human silhouettes run in the foreground, representing a fictional AI fear. Outside the frame, a simple calculator represents practical everyday AI. Connect the two scenes with subtle dashed orbital lines and small orange geometric accents. Bold black outlines, dramatic orange-and-charcoal contrast, warm off-white (#FAFAF8) background, orange (#E8621A) accents, charcoal (#1A1A1A) elements, white highlights, slight retro print energy. Clean, modern, minimal. No text, words, logos, or watermarks. Wide format 16:9.

**Key lesson:** When creating in-content images, illustrate the *analogy or metaphor* used in that section's text — not the literal concept. This creates unique visuals per section and avoids repetitive imagery (e.g. don't use a brain icon for every AI-related image).

**Important:** Each post's illustration must have a distinctly different composition and subject — do not reuse the same scene layout (person at desk with screen). Vary the perspective, objects, and visual metaphor for every post.
- **Internal links (outbound):** Always link new post UP to pillar/parent content during Phase 6 (1-3 links)
- **Internal links (inbound):** Always run `internal-link-builder` skill in Phase 7 to add links from older posts TO the new post
- **Internal link planning:** Always plan links in Phase 3 (outline) before writing — note anchor text and target URLs
- **SEO meta:** Always set Rank Math title (≤60 chars), description (≤160 chars), focus keyword, primary category
- **Rank Math optimization (MANDATORY):** Never skip Phase 6.5 — check Rank Math sidebar. Aim for 80+ score. Use English power/sentiment words (Rank Math doesn't recognize Malay words).
  - **Essential checks (MUST fix):** keyword in title, URL, meta description, intro (first 10% of content), subheadings, image alt text · keyword density 0.5-2.5% · content ≥600 words · has images · has internal links · schema markup
  - **External links (dofollow):** Add 1-2 natural dofollow external links to authoritative sources (Wikipedia, official product pages like openai.com). Link when mentioning a factual reference or named entity — don't force it. This passes small trust signals to Google and clears the Rank Math "all outbound links are nofollow" warning.
  - **Cosmetic checks (skip — not worth the effort):** sentiment word in title · power word in title · "Use Content AI" (PRO upsell)
  - **Note:** The Respira Rank Math API (`respira_analyze_rankmath`) reports `computed_score` which only covers the 13 essential checks. The WP Admin sidebar score includes cosmetic checks too, so it will show a lower number. Don't chase 100/100 in the sidebar — focus on the essential checks being green.
- **Rank tracking (MANDATORY):** Never skip Phase 7 steps 1-2 — every published post's focus keyword + URL must be added to BOTH ClickRank AI Overview Tracker (Malaysia, Malay) AND Screpy Rank Tracker (Malaysia, desktop+mobile). ClickRank = AI Overview/AEO visibility, Screpy = traditional SERP rank tracking + technical audits. Both serve different purposes and both are required.
- **ClickRank title/meta optimization (OPTIONAL):** ClickRank's AI suggestions tend to be over-dramatic. Only apply if natural and matches our calm Malay voice. Reject hype words (Ultimate, Proven, Secret, Game-Changing). Accept natural words (Panduan, Tips, Cara, Mudah, Praktikal, Lengkap). Manual titles always preferred. When in doubt, ask the user. See full policy in AGENTS.md → "ClickRank Usage Policy".
- **Content standardization:** Always strip `<h1>` tags from WriterZen content (template handles title), remove redundant "Malaysia" mentions, and cross-check formatting against Post #1 as the reference standard
- **Content formatting (MANDATORY — Learned 2026-07-26, Updated 2026-07-26):** WriterZen's "Write all for me" AI produces walls of text — flat paragraphs with no visual breaks. **Every article must be richly formatted with varied visual elements.** No section should be a mere sea of text. Apply these formatting types throughout every article:

  ### Rich Formatting Toolkit (USE ALL APPROPRIATE TYPES)

  | Formatting Type | When to Use | HTML Pattern |
  |----------------|-------------|--------------|
  | **Bullet lists** | Enumerations, features, tips, reasons | `<ul><li>...</li></ul>` |
  | **Numbered lists** | Steps, sequences, rankings | `<ol><li>...</li></ol>` |
  | **Bold labels** | Start of each bullet for scannability | `<li><strong>Label</strong>: description</li>` ⚠️ use a **colon**, never an em dash |
  | **Blockquotes** | Examples, key quotes, before/after comparisons | See template below |
  | **Contrast pairs** | Dos and don'ts, good vs bad | `<li><strong>Elakkan:</strong> ...</li><li><strong>Gunakan:</strong> ...</li>` |
  | **Before/after blocks** | Instructional examples (bad vs good prompt, wrong vs right approach) | Two blockquotes back-to-back with labeled headers |
  | **Inline emphasis** | English terms in BM sentences | `<em>prompt</em>, <em>brainstorming</em>` |
  | **Warning/tip boxes** | Important cautions, pro tips | See box template below |
  | **Short paragraphs** | One idea per paragraph — never more than 3-4 sentences without a visual break | — |
  | **Figures with captions** | In-content images | `<figure class="wp-block-image"><img ... /><figcaption>...</figcaption></figure>` |
  | **Internal links** | Contextual anchor text linking to related posts | `<a href="...">natural anchor text</a>` |

  ### Blockquote Template (DigiTrust Lab Standard — copy-paste this)

  ```html
  <blockquote style="border-left:3px solid #E8621A;padding:8px 16px;margin:12px 0;background:#F5F3EE;border-radius:0 6px 6px 0;">
  <p><strong>Contoh label:</strong></p>
  <p><em>"Example content here."</em></p>
  <p>Explanation of what happens when you use this example.</p>
  </blockquote>
  ```

  **Blockquote design system:**
  - Left border: `3px solid #E8621A` (DigiTrust Lab orange)
  - Background: `#F5F3EE` (warm off-white, slightly darker than page bg)
  - Border radius: `0 6px 6px 0` (rounded right side only)
  - Padding: `8px 16px`
  - Margin: `12px 0`
  - Use for: examples, before/after comparisons, key quotes, important callouts

  ### Warning/Tip Box Template

  ```html
  <div style="background:#FFF8F5;border-left:3px solid #E8621A;border-radius:0 6px 6px 0;padding:12px 16px;margin:16px 0;">
  <p><strong>⚠️ Amaran penting:</strong> Warning text here.</p>
  <p><strong>Tip:</strong> Helpful tip text here.</p>
  </div>
  ```

  > ⚠️ **Em dash conflict — resolved 2026-07-29.** This toolkit previously specified `<strong>Label</strong> — description` for bullets, which silently contradicted the AGENTS.md punctuation rule capping em dashes at **1 per post** (they read as an AI tell in Malay). A single 5-item list blew the whole budget. **Always use a colon in list items.** Reserve the one permitted em dash for prose, if used at all. Caught on Post #4, where the drafted article scored 10 dashes against a max of 1.

  ### Formatting Checklist (Run After Every AI Draft)

  Before publishing ANY post, verify:
  - [ ] **Em/en dash count ≤ 1** across the whole post (list items use colons, not dashes)
  - [ ] No section is a wall of text (3+ paragraphs without a list, blockquote, or visual break)
  - [ ] All enumerations use bullet or numbered lists
  - [ ] All examples use blockquotes (not plain paragraphs)
  - [ ] All list items have bold labels where applicable
  - [ ] Dos/don'ts sections use "Elakkan" vs "Gunakan" contrast pairs
  - [ ] At least 2-3 blockquotes per instructional article
  - [ ] English terms italicized with `<em>` tags
  - [ ] Paragraphs are short (max 3-4 sentences)
  - [ ] Warning/tip boxes used for important callouts

  ### Reference Standards

  | Post | What to Copy |
  |------|-------------|
  | Post #2 (`/cara-guna-chatgpt/`) | Blockquotes for examples, bullet lists with bold labels, warning boxes, FAQ section |
  | Post #3 (`/cara-buat-prompt-chatgpt/`) | Before/after blockquote pairs, contrast pairs, bullet lists with bold labels (reformatted 2026-07-26) |
  | Post #1 (`/apa-itu-ai/`) | Clean paragraph flow with lists, figure captions, natural internal links |

  **Why this matters:** Rich formatting improves time-on-page, reduces bounce rate, increases readability on mobile, and matches the visual quality that Google's helpful content system rewards. Walls of text get skipped — structured content gets read. This is a non-negotiable quality standard for DigiTrust Lab.
