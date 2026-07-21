---
description: Write and publish a blog post using the WriterZen Option C pipeline (Keyword Explorer → Keyword List → Keyword Planner → Content Brief → Content Creator → publish via Respira MCP)
---

# Write & Publish a Blog Post (Option C Pipeline)

This is the standard workflow for every DigiTrust Lab blog post. Follow these steps in order.

## Prerequisites

- WriterZen account active (app.writerzen.net)
- Respira MCP connected to digitrustlab.com
- Existing WriterZen Keyword Planner project: "DigiTrust Lab Blog Posts" (ID: 178201)
- Existing Content Creator project: "DigiTrust Lab"
- Existing Keyword List: "DigiTrust Lab Blog Posts" (ID: 68708)

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

### Phase 0: Keyword Research (Keyword Explorer → Keyword List)

1. Navigate to WriterZen → Keyword Explorer
2. Set **Language: Malay**, **Location: Malaysia**
3. Check "Save language & location as default"
4. Enter target keyword (e.g. "cara prompt chatgpt")
5. Click Search
6. Analyze results:
   - **Search volume** — check if sufficient (even 10-20/mo is OK if KD=0)
   - **KD metrics** — all 4 should be low (0 = easy to rank)
   - **Keyword ideas** — review all variants (phrase match + also searched for)
   - **Total search volume** — combined cluster volume
   - **SERP Overview** — check competitor content quality
7. Select the top 5-10 most relevant keyword variants (highest volume, most relevant intent)
8. Click **Add to** → **Add keyword to LIST** (NOT "Add keyword to group"!)
9. Select existing list: "DigiTrust Lab Blog Posts"
10. Click **Add**
11. Record keyword metrics in `content/content-calendar.md`

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
   - Project: Select existing "DigiTrust Lab" (NEVER create new)
   - AI Assistant: Check "Write article title, description & outline"
   - Language: Malay, Location: Malaysia
6. Click **Create**

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

1. Review **Competitor's Keywords** — add relevant ones (target ~8-10)
2. Review **Suggested by WriterZen** — add any that fit naturally
3. Optionally import from a saved WriterZen keyword list
4. Save keyword list

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
6. Run **Show Analysis** — fix any flagged SEO issues
7. Run **Plagiarism Check** — ensure 0% plagiarism
8. **Note all Analysis improvements** for cross-checking in Phase 6/6.5:
   - Write down every "Problems" and "Improvements" item from the analysis panel
   - These get addressed during WordPress publishing and Rank Math optimization
   - Common items: content length, images, internal/external links, title length
9. Save (not Done — keep article in Content Creator)

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
5. **Generate featured image via ChatGPT (DALL-E)** (NOT Openverse stock photos — those break visual consistency):
   - Use the standard DigiTrust Lab illustration prompt template (see Key Rules below)
   - Style: flat illustration, brand colors, 16:9 aspect ratio
   - Download the generated image, then sideload via `respira_sideload_image`
   - Set alt text describing the illustration in Malay
6. Set featured image via `respira_update_post` with `featured_media`
7. Publish via `respira_update_post` with `status=publish`
8. Verify on live site: navigate to URL, check rendering, SEO title, internal links, featured image

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

### Phase 7: Post-Publish — ClickRank + Internal Linking + Documentation

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
- **Image filenames (MANDATORY):** Every time you provide a DALL-E prompt, ALSO provide the SEO-optimized filename. Format: `{post-slug}-{image-description}.png` (lowercase, hyphens only, no underscores). Example: `apa-itu-ai-neural-network.png`. This applies to both featured images and in-content images.
- **In-content images (SEO best practice):** Add images under H2 sections to break up text, increase time on page, and earn Google Image search traffic. Workflow: (1) Agent audits post and identifies H2s needing images, (2) Agent provides prompts + filenames, (3) User generates in ChatGPT/DALL-E and uploads to WordPress Media, (4) Agent inserts each image into correct section with Malay alt text and caption.

### Image Prompt Template (ChatGPT / DALL-E)

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

**Rule:** Vary the visual element style across images within the same post so they feel like a curated art collection, not a template repeat. The color palette and flat illustration style stay consistent — the composition and decorative elements change. Think "art lover's blog," not "corporate stock art."

**DALL-E anatomy fix (MANDATORY):** DALL-E frequently generates images with missing, deformed, or unnaturally positioned hands and arms. ALWAYS append this to prompts featuring humans or robots: `"Both person and robot have complete visible arms and hands with natural positioning."` If the generated image still has hand issues, regenerate with emphasis: `"All hands fully rendered with five fingers each, arms complete from shoulder to fingertips, natural pose."`

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
- **ClickRank optimization (MANDATORY):** Never skip ClickRank in Phase 7 — optimize title via Bulk Titles tool and add focus keyword to keyword tracker. ClickRank handles ongoing title optimization and rank tracking that Rank Math doesn't do.
- **Content standardization:** Always strip `<h1>` tags from WriterZen content (template handles title), remove redundant "Malaysia" mentions, and cross-check formatting against Post #1 as the reference standard
