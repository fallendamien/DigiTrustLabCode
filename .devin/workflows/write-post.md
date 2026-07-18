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
2. Clean content: remove WriterZen annotations ("Kata kunci:" lines, `<hr>` separators)
3. **Insert internal links** — Replace plain text mentions with `<a href>` links to related posts:
   - Check the plan from Phase 2 Step 3
   - Link to pillar/parent content (e.g., "kecerdasan buatan (AI)" → `/apa-itu-ai/`)
   - Use natural anchor text, not keyword-stuffed
   - Aim for 1-3 internal links per post (don't over-link)
4. Update the draft post via `respira_update_post`:
   - Set content, title, status=draft
   - Set Rank Math SEO meta: `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`, `rank_math_primary_category`
   - Set categories
5. Search and sideload a featured image via `respira_search_stock_images` + `respira_sideload_image`
6. Set featured image via `respira_update_post` with `featured_media`
7. Publish via `respira_update_post` with `status=publish`
8. Verify on live site: navigate to URL, check rendering, SEO title, internal links, featured image

### Phase 6: Post-Publish — Internal Linking + Documentation

1. **Run internal link builder** — Use the `internal-link-builder` skill to scan existing posts and add links pointing TO the new post:
   - Trigger: "build internal links" or load skill from `.devin/skills/internal-link-builder/SKILL.md`
   - This finds mentions of the new post's topic in older posts and adds contextual links back
   - Review the plan before applying (skill always asks for confirmation)
   - This is critical: the new post links UP to pillar content (done in Phase 5), but old posts must also link DOWN to the new post
2. Update `content/content-calendar.md`:
   - Change status to PUBLISHED ✅
   - Add URL, publish date, Post ID, WriterZen Article ID
2. Update `STATE.json`:
   - Add to completed list
   - Increment blogPosts count
   - Update nextSteps (remove this post, add next post)
3. Update `NEXT.md`:
   - Mark Post as ✅ published
   - Add next post to task list
4. Update `ROADMAP.md` if applicable
5. Git commit + push all documentation updates

## Key Rules

- **Language:** Bahasa Melayu baku, formal–semi-formal, 'anda' not 'korang'
- **AI Creativity Level:** Always set to 1
- **WriterZen Project:** Always use existing "DigiTrust Lab" — never create new
- **Keyword Planner Project:** Always use "DigiTrust Lab Blog Posts" (ID: 178201)
- **SERP View / AI Assistant toggles:** Leave OFF during Step 1 (Outline)
- **Never skip the Content Creator pipeline** — outline must be generated through WriterZen's AI + competitor research
- **Featured image:** Always search stock images, sideload, set alt text, and assign
- **Internal links (outbound):** Always link new post UP to pillar/parent content during Phase 5 (1-3 links)
- **Internal links (inbound):** Always run `internal-link-builder` skill in Phase 6 to add links from older posts TO the new post
- **Internal link planning:** Always plan links in Phase 2 (outline) before writing — note anchor text and target URLs
- **SEO meta:** Always set Rank Math title (≤60 chars), description (≤160 chars), focus keyword, primary category
