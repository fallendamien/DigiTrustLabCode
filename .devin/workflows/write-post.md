---
description: Write and publish a blog post using the WriterZen Option C pipeline (Keyword Explorer → Keyword Planner → Content Brief → Content Creator → publish via Respira MCP)
---

# Write & Publish a Blog Post (Option C Pipeline)

This is the standard workflow for every DigiTrust Lab blog post. Follow these steps in order.

## Prerequisites

- WriterZen account active (app.writerzen.net)
- Respira MCP connected to digitrustlab.com
- Keyword already researched and recorded in `content/content-calendar.md`
- Existing WriterZen Keyword Planner project: "DigiTrust Lab Blog Posts" (ID: 178201)
- Existing Content Creator project: "DigiTrust Lab"

## Steps

### Phase 1: Keyword Planner → Content Brief

1. Navigate to WriterZen → Keyword Planner → Project "DigiTrust Lab Blog Posts" (ID: 178201)
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
   - Project: Select existing "DigiTrust Lab" (NEVER create new)
   - AI Assistant: Check "Write article title, description & outline"
   - Language: Malay, Location: Malaysia
6. Click **Create**

### Phase 2: Content Creator Step 1 — Outline

1. Review the AI-generated title, description, and outline
2. Adjust headings if needed using Competitive Analysis, Google Suggest Insights, and AI Assistant
3. **Plan internal links** — Check `content-calendar.md` Content Structure Strategy section:
   - Identify which existing posts this new post should link TO (pillar/parent content)
   - Identify which existing posts should link BACK to this new post (will be done in Phase 6)
   - Note the exact anchor text and target URLs for each link
4. Set word count target and heading/paragraph/image counts
5. Save the outline

### Phase 3: Content Creator Step 2 — Keywords to Include

1. Review **Competitor's Keywords** — add relevant ones (target ~8-10)
2. Review **Suggested by WriterZen** — add any that fit naturally
3. Optionally import from a saved WriterZen keyword list
4. Save keyword list

### Phase 4: Content Creator Step 3 — Write

1. Use **Write all for me** feature (AI Creativity Level = 1 for best quality)
2. Review generated content section by section
3. Run **Show Analysis** — fix any flagged SEO issues
4. Run **Plagiarism Check** — ensure 0% plagiarism
5. Save (not Done — keep article in Content Creator)

### Phase 5: Publish to WordPress via Respira MCP

1. Extract HTML content from WriterZen editor (via browser evaluate)
2. **Clean and standardize content** (critical for consistent formatting across all blog posts):
   - Remove WriterZen annotations ("Kata kunci:" lines, `<hr>` separators)
   - **Strip all `<h1>` tags** — the Bricks template renders the post title as H1; any H1 in content creates a duplicate massive title
   - **Remove redundant "Malaysia" mentions** — the audience is already Malaysian; WriterZen AI tends to over-localize when Target Audience mentions Malaysians. Keep only if contextually necessary (e.g., comparing Malaysian vs international context)
   - **Cross-check formatting against Post #1** (`/apa-itu-ai/`) as the reference standard — content should start with `<p>` tags, first heading should be `<h2>`, no H1 in content body
   - Verify heading hierarchy: H2 → H3 → H4 (no skipped levels)
3. **Insert internal links** — Replace plain text mentions with `<a href>` links to related posts:
   - Check the plan from Phase 2 Step 3
   - Link to pillar/parent content (e.g., "kecerdasan buatan (AI)" → `/apa-itu-ai/`)
   - Use natural anchor text, not keyword-stuffed
   - Aim for 1-3 internal links per post (don't over-link)
4. Update the draft post via `respira_update_post`:
   - Set content, title, status=draft
   - Set Rank Math SEO meta: `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`, `rank_math_primary_category`
   - Set categories
5. **Generate featured image via ChatGPT (DALL-E)** (NOT Openverse stock photos — those break visual consistency):
   - Use the standard DigiTrust Lab illustration prompt template (see Key Rules below)
   - Style: flat illustration, brand colors, 16:9 aspect ratio
   - Download the generated image, then sideload via `respira_sideload_image`
   - Set alt text describing the illustration in Malay
6. Set featured image via `respira_update_post` with `featured_media`
7. Publish via `respira_update_post` with `status=publish`
8. Verify on live site: navigate to URL, check rendering, SEO title, internal links, featured image

### Phase 5.5: Rank Math Sidebar Optimization (MANDATORY — Never Skip)

This phase runs AFTER the post is published (Phase 5) but BEFORE documentation (Phase 6). The goal is to push the Rank Math SEO score as high as possible before moving on.

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

### Phase 6: Post-Publish — ClickRank + Internal Linking + Documentation

1. **Run ClickRank optimization** (app.clickrank.ai):
   - **Bulk Titles** — Navigate to ClickRank → Bulk → Titles, find the new post, click "Optimize Title" to generate an AI-optimized SEO title. This modifies the `<title>` tag directly on the live page via the ClickRank verification script.
   - **Keyword Tracker** — Add the post's focus keyword to the ClickRank keyword tracker (Malaysia, all devices) if not already tracked. This monitors ranking progress over time.
   - ClickRank complements Rank Math: Rank Math scores the on-page SEO, ClickRank handles ongoing title optimization and rank tracking
2. **Run internal link builder** — Use the `internal-link-builder` skill to scan existing posts and add links pointing TO the new post:
   - Trigger: "build internal links" or load skill from `.devin/skills/internal-link-builder/SKILL.md`
   - This finds mentions of the new post's topic in older posts and adds contextual links back
   - Review the plan before applying (skill always asks for confirmation)
   - This is critical: the new post links UP to pillar content (done in Phase 5), but old posts must also link DOWN to the new post
3. Update `content/content-calendar.md`:
   - Change status to PUBLISHED ✅
   - Add URL, publish date, Post ID, WriterZen Article ID
   - Record final Rank Math score
4. Update `STATE.json`:
   - Add to completed list
   - Increment blogPosts count
   - Update nextSteps (remove this post, add next post)
5. Update `NEXT.md`:
   - Mark Post as ✅ published
   - Add next post to task list
6. Update `ROADMAP.md` if applicable
7. Git commit + push all documentation updates

## Key Rules

- **Language:** Bahasa Melayu baku, formal–semi-formal, 'anda' not 'korang'
- **Italic Policy (MANDATORY):** Italicize English terms code-switched into BM sentences using `<em>` tags (e.g. <em>prompt</em>, <em>brainstorming</em>, <em>chat</em>, <em>Sign Up</em>, <em>Enter</em>, <em>vs</em>, <em>chatbot</em>, <em>natural</em>). Do NOT italicize: brand names (ChatGPT, OpenAI), acronyms (AI, NLP, API), or fully absorbed loan words (online, email/emel, blog, download, upload, login, link, video, tutorial). Standardize spelling — use BM spelling "emel" not "email" throughout. See `malay-voice-guide/SKILL.md` §4c for full policy.
- **AI Creativity Level:** Always set to 1
- **WriterZen Project:** Always use existing "DigiTrust Lab" — never create new
- **Keyword Planner Project:** Always use "DigiTrust Lab Blog Posts" (ID: 178201)
- **SERP View / AI Assistant toggles:** Leave OFF during Step 1 (Outline)
- **Never skip the Content Creator pipeline** — outline must be generated through WriterZen's AI + competitor research
- **Featured image:** Always use ChatGPT/DALL-E (NOT Openverse stock photos). Use the standard prompt template below. Cross-check visual style against Post #1 (`/apa-itu-ai/`)

### Featured Image Prompt Template (ChatGPT / DALL-E)

```
Flat illustration style. [SUBJECT DESCRIPTION]. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. [ICONS FLOATING AROUND]. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
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

**Example (Post #1 — "Apa Itu AI"):**
> Flat illustration style. A Malaysian man sitting at a desk with a glowing brain icon on a computer screen. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around: chat bubble, lightbulb, gears. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Example (Post #2 — "Cara Guna ChatGPT"):**
> Flat illustration style. A split scene: left side shows a messy desk with scattered papers and a frustrated person, right side shows the same desk organized with a glowing ChatGPT interface on a tablet, tasks neatly sorted into folders. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around: magic wand, folder, calendar, coffee cup. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Important:** Each post's illustration must have a distinctly different composition and subject — do not reuse the same scene layout (person at desk with screen). Vary the perspective, objects, and visual metaphor for every post.
- **Internal links (outbound):** Always link new post UP to pillar/parent content during Phase 5 (1-3 links)
- **Internal links (inbound):** Always run `internal-link-builder` skill in Phase 6 to add links from older posts TO the new post
- **Internal link planning:** Always plan links in Phase 2 (outline) before writing — note anchor text and target URLs
- **SEO meta:** Always set Rank Math title (≤60 chars), description (≤160 chars), focus keyword, primary category
- **Rank Math optimization (MANDATORY):** Never skip Phase 5.5 — check Rank Math sidebar, fix Title Readability (power word + sentiment word + number), Additional (keyword density 0.5-2.5%, at least 1 dofollow outbound link), and Content Readability (ToC plugin active). Aim for 80+ score. Use English power/sentiment words (Rank Math doesn't recognize Malay words). The only unfixable error is "Use Content AI" (PRO feature).
- **ClickRank optimization (MANDATORY):** Never skip ClickRank in Phase 6 — optimize title via Bulk Titles tool and add focus keyword to keyword tracker. ClickRank handles ongoing title optimization and rank tracking that Rank Math doesn't do.
- **Content standardization:** Always strip `<h1>` tags from WriterZen content (template handles title), remove redundant "Malaysia" mentions, and cross-check formatting against Post #1 as the reference standard
