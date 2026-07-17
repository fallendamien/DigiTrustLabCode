---
name: writerzen-keyword-research
description: WriterZen full research pipeline for DigiTrust Lab. Triggers on keyword research, SEO keyword finding, WriterZen, golden filter, keyword clustering, topic discovery, content brief, seed keyword, KD analysis, search volume research, keyword planner, domain filter, domain authority, outline building.
---

# WriterZen Research Pipeline

> **Purpose:** Complete workflow for researching, planning, and preparing blog posts for DigiTrust Lab using WriterZen. Research is the critical SEO foundation — never write before the full pipeline is complete. The LLM handles writing natively once the research and outline are done.

## When to Use This Skill

- Starting a new blog post — need keyword research first
- Finding topics to write about (ideation phase)
- Evaluating keyword difficulty and competition
- Building keyword clusters for pillar content
- Generating a content brief before writing
- Building an outline from competitor research
- Any mention of WriterZen, Golden Filter, Keyword Planner, Topic Discovery

## Standard Settings (Always Use)

- **Location:** Malaysia
- **Language:** Malay
- **Keyword List:** "DigiTrust Lab Blog Posts" (master tracker, in publishing order)
- **30-day rule:** Search results expire after 30 days — start fresh if there's a gap

---

## ⚠️ Quota Check Protocol (MANDATORY)

**Before any research session, check remaining quotas to plan usage across the month.**

**Limits page URL:** `https://app.writerzen.net/user/profile-setting?tab=limit`
**Path:** Settings → Limits & Remaining
**Reference doc:** `content/SEO-CHEATSHEET.md` → "WriterZen Limits & Credits Reference"

### When to Check

| Trigger | Action |
|---------|--------|
| **Start of any Keyword Explorer session** | Navigate to limits page, note remaining Keyword Lookup/Day and Keyword Credit |
| **Before activating Golden Filter** | Golden Filter costs 1 Keyword Credit PER keyword in the result set — calculate cost first (e.g. 39 keywords = 39 credits) |
| **Before Topic Discovery** | Check Topic Lookup/Day remaining |
| **End of session** | Note credits consumed, update `content/SEO-CHEATSHEET.md` limits table if running low |
| **Monthly planning** | Check Keyword Credit/Month and AI Words/Month to budget across remaining posts |

### Current Plan: AppSumo Tier 2 (Lifetime)

| Limit | Allowance | What Consumes It |
|-------|-----------|-----------------|
| Topic Lookup / Day | 75 | 1 per Topic Discovery seed keyword |
| Keyword Lookup / Day | 75 | 1 per Keyword Explorer search |
| Keyword Credit / Month | 40,000 | 1 per keyword when Golden Filter is activated |
| Article / Month | 70 | Content Creator articles |
| Plagiarism Word Check / Day | 40,000 | Plagiarism scans |
| AI Words / Month | 8,000 | AI-generated content |
| Keyword List / Plan | 50 | Saved keyword lists |

### Budgeting Rule of Thumb

**Publishing schedule:**
- **Month 1 (launch sprint):** 1 post/day or 1 post/2 days — target 15-30 posts to build topical authority fast
- **Long-form content (>2,000 words):** 2-3 days per post
- **Month 2+:** Slow down to 2-3 posts/week once initial content base is established

**Credit budgeting for Month 1 sprint:**
- ~20-30 Keyword Explorer searches needed (1 per topic/keyword)
- Golden Filter cost: estimate before activating — check keyword idea count (e.g. "39 keywords" = 39 credits)
- **Batch research strategy:** Run Topic Discovery + Keyword Explorer for 5-10 keywords per session, then write posts in sequence without re-searching
- **Always confirm the credit cost** in the Golden Filter confirmation dialog before clicking "Confirm"
- If Keyword Credit/Month drops below 10,000 — switch to selective Golden Filter (only top 3-5 keywords per search, not entire result sets)
- If Keyword Credit/Month drops below 5,000 — skip Golden Filter entirely, rely on manual KD/Allintitle checks via SERP overview
- **Recycle research:** One Keyword Explorer search with 39 ideas can fuel 5-10 posts from the same cluster — don't waste searches on near-duplicate keywords

---

## The Pipeline (Overview)

```
Topic Discovery → Keyword Explorer → Keyword Planner → Content Brief → Outline → Write → Plagiarism Check
     (Phase 1)        (Phase 2)         (Phase 3)       (Phase 4)     (Phase 5)  (Phase 6)   (Post)
```

**Phases 1-4 are the critical SEO foundation.** This is where WriterZen earns its value. Phases 5-6 use the Content Creator tool — covered lightly here since the LLM handles writing natively once the research is done.

Deep reference files for each phase are in `content/writerzen-guide/` (29 files from the official WriterZen course).

---

## Phase 1: Topic Discovery (DEEP)

**When to use:** Ideation, finding content gaps, building a topical map, finding angles competitors miss.

### How It Works

Enter a seed keyword → WriterZen scans the top 100 Google results → extracts all headlines and sub-headlines → groups them into topic cards showing what competitors are covering.

### Key Features

| Feature | What It Does |
|---------|-------------|
| **Relevancy filter** | Closely / Medium / Widely — controls how far topics stretch from seed |
| **Sort order** | By Search Volume or By Relevancy |
| **Golden star** | Topic with upward search volume trend in recent months |
| **Cards view** | Default — each topic as a card with subtopics |
| **Mind Map view** | Visual showing how topics connect to pillar content |
| **Export** | Excel file of all topic ideas |

### Inside a Topic Card (Show Ideas)

Three sections:
1. **Headlines to Consider** — top-ranking titles for inspiration
2. **Google Suggest Insights** — related searches as subtopic ideas
3. **Related Google Searches** — bottom-of-SERP searches

### Use Cases for DigiTrust Lab

| Use Case | Approach |
|----------|---------|
| **Low-DA site targeting competitive keywords** | Find specific subtopics you can realistically rank for → take to Keyword Explorer for metrics |
| **Finding a different angle** | Run seed keyword through Topic Discovery → look for narrower angles with golden stars |
| **Building topical authority** | Map all topics → create content plan covering each → internal link to pillar page |

### Textbook Mode

Enable for tooltips — hover any underlined element for definitions. Also available in Learning Hub (top right).

> **Deep reference:** `content/writerzen-guide/01-topic-discovery-introduction.md` and `02-topic-discovery-report-analysis-in-depth.md`

---

## Phase 2: Keyword Explorer (DEEP)

**When to use:** Finding keywords, evaluating metrics, applying Golden Filter, clustering keywords.

### Three Search Types

| Type | When to Use | Example |
|------|------------|---------|
| **Keyword Search** | Default — gather all variations of seed keyword | `pelan pemakanan` |
| **Domain Search** | See what keywords a specific domain ranks for | Analyze competitor's keyword portfolio |
| **Wildcard Search** | Discover intent-specific keywords from broad seed | `cara * quora` or `* untuk pemakanan` |

### Wildcard Search Details

Uses asterisk (`*`) like Google's wildcard operator. Asterisk = a word Google substitutes based on real searches. Place anywhere in phrase.

**Full-funnel use:** Combine with Golden Filter + Clustering:
- `how to * [topic]` → TOFU (informational)
- `[topic] vs *` → MOFU (comparison)
- `best * [topic]` → BOFU (ready to buy)

### Top Panels

| Panel | What It Shows |
|-------|--------------|
| **SERPs Overview** (top right) | Top-ranking results for seed keyword |
| **Overview Chart** (top right) | Search trends — Volume tab + Trend tab (Google Trends data) |
| **4 Metric Cards** (top left) | Search Volume, CPC, Keyword Ideas count, Total Search Volume |

### Keyword Data Tab — 4 Sub-tabs

| Sub-tab | What It Shows |
|---------|--------------|
| **Total** | All variations with metrics |
| **Phrase Match** | Exact order as written |
| **Having Same Terms** | Any order |
| **Also Search For** | Related keywords users search alongside |

### Insights Tab

Content ideas grouped into clusters: Questions (what/where/when/why/who/how), Prepositions (with/for/without), Comparisons, Alphabet (single letter — grey keywords), Numerical (numbers — specific keywords).

> **High CPC on a question keyword = money in that market.**

### Key Metrics

| Metric | What It Measures | DigiTrust Lab Target |
|--------|-----------------|---------------------|
| **Search Volume** | Monthly average searches | 50–2,400+ |
| **CPC** | Cost per click — commercial intent signal | Any (higher = more commercial) |
| **PPC Competition** | How many advertisers bid | Info only |
| **Keyword Difficulty (KD)** | Chances of ranking top 10 | < 20 (0 = ideal) |
| **Trend** | 12-month search volume chart | Upward or stable |
| **Keyword Trending** | Star icon = recent upward trend | Prioritize starred |

### Basic Filters

| Filter | Purpose |
|--------|---------|
| **Include** | All Words (must contain every word) or Any Words (contain any) |
| **Exclude** | Remove unwanted words from results |
| **Volume** | Min/max search volume |
| **CPC** | Min/max cost per click |
| **Word Count** | Min/max word count (filter long-tail) |
| **Keyword Trending** | Show only starred (upward trend) keywords |

### Golden Filter & Golden Score (CRITICAL)

**Golden Score** = probability a keyword will rank. Lower score = higher ranking potential.

**Formula:** Based on Keyword Golden Ratio (KGR):
```
KGR = All-in-Title count ÷ Monthly Search Volume
```

**Golden Score classification:**
- **< 10:** Excellent — high probability of ranking (prioritize these)
- **10–36:** Good — worth targeting with good content
- **36–100:** Fair — possible but harder
- **> 100:** Poor — avoid for low-DA sites

**Golden Filter settings for DigiTrust Lab (low-DA site):**
- Golden Score: max 10
- Search Volume: min 100
- All-in-Title: max 10

**How to activate:** Click Golden Filter button → set thresholds → Apply. Filter only works on keywords with All-in-Title data available.

### Revenue Forecast

**ESKP Formula:** `Estimated Sales = Search Volume × CTR × Conversion Rate`

Only suitable for **transactional intent** keywords. Not for informational blog posts (DigiTrust Lab's primary use case). Useful when evaluating affiliate or product review posts.

CTR data from Advanced Web Ranking (advancedwebranking.com) — varies by device, location, category.

### Keyword Clustering

Groups keywords that share similar SERP results → one article can rank for multiple keywords.

**Process:**
1. Apply Golden Filter first → select filtered keywords
2. Click **Cluster** → **Cluster Selected**
3. Set clustering level (default 3 = keywords must share 3+ SERP results)
4. Name project → click **Activate**
5. Results save to Keyword Planner (notified via email when complete)

**Benefits:** Fewer articles needed, each ranks for multiple keywords, builds topical authority.

**Groups vs Lists:** Groups = temporary (expire at session end). Lists = permanent. Save keepers to a list before finishing.

### Supporting Functions

- **Add To** → List (permanent) or Group (temporary)
- **Export** → Excel or CSV
- **Pin Up** → Freezes filter bar while scrolling
- **Columns Icon** → Toggle which metrics display
- **Filter Config** → Save filter settings as reusable template

> **Deep reference:** `content/writerzen-guide/03-keyword-explorer-introduction.md` through `09-keyword-explorer-keyword-clustering.md`

---

## Phase 3: Keyword Planner (DEEP)

**When to use:** After clustering — analyze keyword insights, use Domain Filter for competitive analysis, generate content briefs.

### Two Views

| View | What It Shows |
|------|--------------|
| **Cluster View** (default) | Topics → Clusters (subtopics) → Keywords. Left to right hierarchy |
| **All Keywords View** | Flat list of all keywords. Use "Show Not In Any Cluster" toggle to find ungrouped keywords |

### Keyword Insights

| Insight | What It Tells You |
|---------|------------------|
| **Intent** | Informational / Navigational / Transactional / Commercial |
| **Micro Intent** | More granular intent classification |
| **Buying Journey** | Awareness / Consideration / Decision / Retention |
| **Keyword Type** | Short-tail / Long-tail / Question / etc. |
| **SERP Type** | What Google shows for this keyword (articles, videos, shopping, etc.) |

### Cluster Insights

Each cluster shows intent labels and SERP type — helps decide what format your content should take.

### Bottom Taskbar Actions

- **Suggest Content Brief** — auto-generates a brief from the selected cluster
- **Create Article** — sends keywords to Content Creator
- **Activate Metrics** — unlocks DA Score, Weak Spot, and Domain Focus (uses credits)
- **Domain Filter** — competitive analysis tool
- **Domain Focus** — zoom into a single domain's performance

### Domain Filter (5 Use Cases)

| Use Case | How |
|----------|-----|
| **Market overview** | Overview tab → see all competing domains with market share |
| **Own performance** | Filter by your domain → see where you rank |
| **Competitor reverse-engineering** | Include competitor → Ranked Top 5 → study their best content |
| **Find weak spots** | Filter rules → find keywords where low-DA sites rank in top 10 |
| **Social media opportunities** | Filter by social domains (YouTube, Reddit, Quora) → find keywords where social ranks = content gap |

### Domain Authority (DA) Score

Moz's 0-100 scale predicting ranking potential. WriterZen uses Moz data via third-party provider.

**Activate:** Click "Activate Metrics" in bottom taskbar (consumes keyword credits).

**New columns after activation:**

| Metric | What It Shows |
|--------|--------------|
| **Weak Spot** | # of URLs in top 10 with DA < 30 — higher = easier to rank |
| **Average DA** | Average DA of all domains in top 10 |
| **LDA** | Lowest DA in top 10 |
| **HDA** | Highest DA in top 10 |

**DA Filter Strategies for DigiTrust Lab:**

| Goal | Method |
|------|--------|
| Find easy-to-rank keywords | Weak Spot filter → minimum 2 |
| Find keywords below our DA | DA Score filter → max = our DA − 5 |
| Study proven content | Filter top competitor → ranked top 5 |
| Find beatable competitors | Filter lower-DA domains → ranked top 5 |

### Domain Focus

Zoom into a single domain's performance across all clusters.

**Key metrics:**
- **Progress bar** — proportion of search volume captured
- **Weighted Rank** — average ranking position (blue number, dash = no top 10 rankings)
- **Captured/Total Keywords** — e.g. 28/55 keywords captured

**Sort options (Domain Focus exclusive):** By Captured Volume, By Captured Keywords, By Weighted Rank.

**Most powerful combo:** Domain Focus + Domain Filter + DA Score = full competitive intelligence.

### Arrange Topics & Clusters

- Rename topics and clusters for clarity
- Move keywords between clusters
- Merge or delete clusters
- Organize into a logical content plan

> **Deep reference:** `content/writerzen-guide/10-keyword-planner-introduction.md` through `16-keyword-planner-domain-focus.md`

---

## Phase 4: Content Brief (MEDIUM)

**When to use:** After identifying target cluster → generate a brief to guide content creation.

### Suggest Content Brief

Click **Suggest Content Brief** in the bottom taskbar → WriterZen auto-generates a brief from keyword insights.

### Content Brief Components

| Component | What It Sets | DigiTrust Lab Default |
|-----------|-------------|----------------------|
| **Content Angle** | The approach/perspective | Educational / practical |
| **Target Audience** | Who the content is for | Malaysian internet users |
| **Perspective** | First person / third person / instructional | Conversational first person |
| **Seed Keyword** | Primary target keyword | From research |
| **Content Format** | Article / listicle / guide / review | Match SERP type |
| **Writing Tone** | Tone of voice | Informative/Explanatory |

### Note for Writer Template

When generating a content brief, use this as the **Note for writer** field:

```
Gunakan Bahasa Melayu semi-formal. Guna 'anda', bukan 'korang'. Ejaan penuh, bukan singkatan. Elakkan slang dan code-switching berlebihan. Rujuk DBP untuk ejaan dan tatabahasa yang betul.
```

### Bulk Content Generation

Generate briefs for multiple clusters at once — useful when planning a content cluster (pillar + supporting articles).

> **Deep reference:** `content/writerzen-guide/12-keyword-planner-content-brief-article-creation.md`

---

## Phase 5: Outline Building (LIGHT)

**When to use:** After content brief → build the article structure before writing.

### Content Creator Layout

- **Left panel:** Research area (competitor data, Google Suggests, PAA, Reddit topics)
- **Right panel:** Outline builder (drag-and-drop structure)

### Step 1: Set General Article Info

1. **Title** — type manually or AI-generate from seed keyword
2. **Description** — AI-generate based on title
3. **Content Structure** — set word count (aim above 70-80% of competitors), headings, paragraphs, images

### Building the Outline

- Double-click competitor headings to add to your outline
- Multi-select with Shift/Ctrl for bulk operations
- Change heading levels (H2, H3, H4, bullet)
- Drag to reorder
- Blue line indicator shows where new items insert

### Research Panel Sources

- **Competitive Analysis** — top 20 competitors with AI-generated summary views
- **People Also Ask** — from Google PAA panel
- **Topics** — related discussions
- **Comparisons** — what people compare in this niche
- **Reddit Topics** — questions from Reddit

### AI Assistant (Outline Builder)

Template categories: Outlines, Rewrite. Use for generating outline structures, rewriting items. History tab preserves past generations. SERP view (3-panel mode) shows competitor content alongside your outline.

> **Key principle:** SEO structure comes from competitors. Creative input comes from AI/LLM. Combine both.

> **Deep reference:** `content/writerzen-guide/18-content-creator-writing-outline.md` and `22-content-creator-ai-assistant-outline-builder.md`

---

## Phase 6: Keywords to Include + Writing (LIGHT)

### Step 2: Keywords to Include

Two types:

| Type | What It Means | Usage Target |
|------|--------------|-------------|
| **Competitive Keywords** | Keywords competitors rank for | Include naturally in content |
| **Opportunity Keywords** | Keywords with ranking potential but competitors underuse | Prioritize these |

**Critical principle:** Keywords must flow naturally. Never stuff. The LLM handles this natively — provide the keyword list and let it write naturally.

### Step 3: Content Writing

- Writing interface with left (research) and right (editor) panels
- AI shortcuts on hover: Expand, Rewrite, Topic paragraph, Copy
- Bullet-to-paragraph feature for quick expansion
- Content Score and Show Analysis for optimization feedback
- Plagiarism checker integrated

### Google NLP (Optional — English Only)

Adds entity analysis and sentiment from Google's NLP API. **3 credits per article.** Currently supports English, Spanish, Japanese only — **not available for Malay content.**

> **Deep reference:** `content/writerzen-guide/19-content-creator-keywords-to-include.md` through `23-content-creator-ai-assistant-full-article.md`

---

## Post-Writing: Plagiarism Check (BRIEF)

Run plagiarism check after writing. Review orange (some similarity) and red (high similarity) highlights. Export report if needed. Exclude your own domain when rewriting existing content.

> **Deep reference:** `content/writerzen-guide/24-plagiarism-checker-introduction.md` and `25-plagiarism-checker-report-analysis.md`

---

## Team Function (BRIEF)

Members (full seats) vs Guests (limited). Article status workflow: Draft → In Review → Approved → Published. Use for delegation and tracking when working with multiple writers.

> **Deep reference:** `content/writerzen-guide/26-team-function-workspace-management.md` and `27-team-function-collaboration.md`

---

## DigiTrust Lab Decision Frameworks

### Low-DA Site Strategy

DigiTrust Lab is a new site with low Domain Authority. Strategy:

1. **Target Golden Score < 10** — highest probability of ranking
2. **Check All-in-Title < 10** — low competition content
3. **Check Weak Spot ≥ 2** — at least 2 low-DA sites ranking in top 10
4. **Look for small MY blogs in SERP** — if small blogs rank, we can too
5. **Build topical authority first** — cover subtopics before targeting competitive head terms
6. **Internal linking** — subtopic articles link up to pillar page

### Malaysia/Malay-Specific Settings

- **Location:** Always Malaysia
- **Language:** Always Malay
- **Search volume:** Malaysia-specific (lower than US but more relevant)
- **SERP analysis:** Check if Malaysian sites rank (not just US/global giants)
- **Content language:** Malay — Google NLP not available (English/Spanish/Japanese only)

### KD Thresholds

| Metric | Target | Ideal |
|--------|--------|-------|
| KD by Content | < 20 | 0 |
| KD by Traffic | < 20 | 0 |
| KD by Signal | < 20 | 0 |
| Golden Score | < 10 | < 5 |
| All-in-Title | < 10 | < 5 |
| Weak Spot | ≥ 2 | ≥ 3 |

### Content Calendar Integration

After completing research for a post:
1. Record confirmed metrics in `content/content-calendar.md` (per-post entry)
2. Update status: `PLANNED` → `PARKED KEYWORD` → `DRAFTING` → `PUBLISHED ✅`
3. Add keyword to WriterZen Keyword List → "DigiTrust Lab Blog Posts"
4. Full KD scale reference: `content/SEO-CHEATSHEET.md`

### Workflow: New Blog Post Research

```
1. Topic Discovery → find subtopics and angles
2. Keyword Explorer → search seed keyword, apply Golden Filter
3. Evaluate metrics → KD < 20, Golden Score < 10, volume 50+
4. Check SERP → small MY blogs ranking? = winnable
5. Cluster keywords → group related terms
6. Keyword Planner → analyze insights, domain filter, DA
7. Generate Content Brief → set angle, audience, tone
8. Build outline → from competitor research + AI
9. Record in content-calendar.md → update metrics
10. Hand to LLM for writing → with keyword list + outline + brief
```

---

## Quick Reference

### Glossary

| Term | Definition |
|------|-----------|
| **KGR** | Keyword Golden Ratio = All-in-Title ÷ Monthly Search Volume |
| **Golden Score** | WriterZen's ranking probability score (lower = better) |
| **All-in-Title** | Number of pages with exact keyword in title tag |
| **Weak Spot** | URLs in top 10 with DA < 30 (higher = easier to rank) |
| **Weighted Rank** | Average ranking position of a domain across captured keywords |
| **ESKP** | Estimated Sales Per Keyword Position = Volume × CTR × CR |
| **DA** | Domain Authority (Moz, 0-100 scale) |
| **LDA/HDA** | Lowest/Highest DA in top 10 SERPs |
| **Captured Keyword** | Keyword where a domain has top 10 ranking |
| **Clustering Level** | Min SERP results two keywords must share to be grouped (default 3) |

### UI Tips

- **Textbook Mode** → tooltips on hover (enable in any tool)
- **Columns Icon** → toggle which metrics display in tables
- **Pin Up** → freezes filter bar while scrolling
- **Filter Config** → save reusable filter templates
- **30-day expiry** → search results expire, start fresh if gap exists
- **Keyword List widget** → top right, next to notifications
- **Learning Hub** → top right, detailed use case explanations

### Filter Combination Cheat Sheet

| Goal | Filters to Apply |
|------|-----------------|
| Find golden keywords | Golden Score max 10 + Volume min 100 + All-in-Title max 10 |
| Find trending keywords | Keyword Trending filter (star only) + Volume min 100 |
| Find low-competition | Weak Spot min 2 + Golden Score max 10 |
| Find questions | Insights tab → Questions category |
| Find long-tail | Word Count min 4 + Volume min 50 |
| Exclude brands | Exclude filter → brand names |

---

## Source Reference

All 29 detailed WriterZen course files are in `content/writerzen-guide/`:

| File | Phase | Title |
|------|-------|-------|
| 000 | Index | Glossary & File Index |
| 00 | Intro | Introduction to WriterZen User Guide |
| 01 | Topic Discovery | Introduction to Topic Discovery |
| 02 | Topic Discovery | Report Analysis In-Depth |
| 03 | Keyword Explorer | Introduction |
| 04 | Keyword Explorer | Keyword Search |
| 05 | Keyword Explorer | Wildcard Search |
| 06 | Keyword Explorer | Metrics & Basic Filters |
| 07 | Keyword Explorer | Golden Filter |
| 08 | Keyword Explorer | Revenue Forecast |
| 09 | Keyword Explorer | Keyword Clustering |
| 10 | Keyword Planner | Introduction |
| 11 | Keyword Planner | Report Analysis |
| 12 | Keyword Planner | Content Brief & Article Creation |
| 13 | Keyword Planner | Arrange Topics & Clusters |
| 14 | Keyword Planner | Domain Filter |
| 15 | Keyword Planner | Domain Authority |
| 16 | Keyword Planner | Domain Focus |
| 17 | Content Creator | Overview |
| 18 | Content Creator | Writing Outline |
| 19 | Content Creator | Keywords to Include |
| 20 | Content Creator | Content Writing Function |
| 21 | Content Creator | Google NLP |
| 22 | Content Creator | AI Assistant Outline Builder |
| 23 | Content Creator | AI Assistant Full Article |
| 24 | Plagiarism | Introduction |
| 25 | Plagiarism | Report Analysis |
| 26 | Team | Workspace Management |
| 27 | Team | Collaboration |

## Rules

- **Research before writing:** Never write a blog post without completing the research pipeline
- **One keyword per post:** Each blog post targets exactly one primary keyword
- **Malay language:** All keyword research targets Malay search terms
- **Malaysia location:** All volume and competition data must be Malaysia-specific
- **Update content/content-calendar.md:** Record confirmed metrics after every research session
- **Golden Filter first:** Always apply Golden Filter before clustering to ensure quality input
- **Check SERP manually:** Metrics tell you numbers; SERP tells you reality — always verify small MY blogs are ranking
- **30-day freshness:** If research is older than 30 days, start a new search
