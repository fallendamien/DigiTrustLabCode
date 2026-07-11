# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 📁 File Architecture — Who Reads What

| Layer | Purpose | Read By |
|-------|---------|---------|
| `AGENTS.md` | Voice, copy policy, project rules — single source of truth | All agents (Claude, Devin, Windsurf, ChatGPT) |
| `.devin/rules/` | Operational behaviour — safety checks, tool constraints | Devin only (auto-loaded every session) |
| `.devin/skills/` | On-demand task recipes — SEO audit, keyword research, image optimisation | Devin only (trigger-based, not auto-loaded) |

**Rule:** Never duplicate content/voice standards into `.devin/rules/` — keep AGENTS.md as the single source. `.devin/rules/` should only contain operational behaviour constraints (e.g. "never edit template without snapshot").

## 🚫 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Respira MCP (primary) or Bricks Builder GUI (fallback). NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Respira MCP or Bricks GUI, it doesn't get done.**

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

**As of 2026-07-05, Respira MCP replaced the old Bricks MCP.** Respira takes a snapshot before every write and supports one-call rollback. The flattening bug was caused by the old Bricks MCP's `content:update_content` action — Respira does not use that API.

Templates 185 (Header) and 52 (Blog Archive) are now editable via Respira MCP with confidence. Always use `respira_extract_builder_content` before editing and keep the returned `snapshot_uuid` for rollback if needed.

## ✅ Agent's Permitted Scope

**You ARE permitted to:**
- Create and edit WordPress POSTS, PAGES, and Bricks templates via Respira MCP
- Manage menus via Respira MCP menu tools
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins
- Manage media via Respira MCP
- Run SEO, accessibility, and performance audits via Respira MCP

**You are NOT permitted to:**
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — it is decommissioned
- Use Raw HTML Code elements in Bricks templates
- Use non-Bricks frameworks (React, Vue, etc.) injected into templates

## ✅ Current Priority: Write and Publish Post #1

This is the only task that matters right now. Do NOT work on any template, design,
or infrastructure task unless Zamri explicitly instructs it.

## ✅ RESOLVED: Blog Archive Template 52 Now Rendering on /blog/ (2026-07-09)

**Fixed:** Template 52 was not rendering on `/blog/` due to 3 root causes:
1. **Template status was `private`** — Bricks only queries `publish` templates (database.php line 766)
2. **`archiveType: any` doesn't match `is_home()`** — Bricks treats posts page as `content_type: content`, not archive (database.php line 492, 961)
3. **Stale `ids: ['260']`** — Blog page was deleted and recreated as ID 277

**Fix applied:** Status → `publish`, condition → `ids: ['277']` only (score 10 match).

## 🔴 UNRESOLVED: Category/Taxonomy Archives Don't Use Custom Template

Template 52 now works on `/blog/` (posts page) via `ids: ['277']` condition, but does NOT apply to `/category/ai-tools/` or `/category/digital-side-hustle/` (taxonomy term archives).

**Why:** The `ids` condition only matches the specific Blog page ID. Category pages are true WordPress archives (`is_archive() = true`), so they need an `archiveType` condition — but Template 52 currently has no `archiveType` condition (it was removed because it didn't work for the posts page).

**Needs investigation:**
- Add a second condition `archiveType: ['term']` to Template 52 (this WILL match category pages since `is_archive()` is true there)
- Or create a separate template for category archives with `archiveType: ['term']` condition
- Verify in Bricks GUI: Template 52 → Settings → Conditions, to see what the visual condition picker offers for taxonomy targeting

**Workaround in place:** `.bricks-archive-title-wrapper { display: none !important; }`
in WP Additional CSS hides the ugly "Category: X" heading.

### 🧩 Respira MCP (PRIMARY TOOL — replaced old Bricks MCP 2026-07-05)

**Respira MCP is active on digitrustlab.com (live Hostinger site).** Connected to Windsurf and Claude Desktop.

**Builder guide:** `BRICKS-BUILDER-GUIDE.md` — Bricks element concepts still apply (settings schema, `_cssCustom`, gotchas). Tool names in the guide refer to old Bricks MCP — use equivalent Respira tools instead.

### 📝 Respira Session Primer

**For Claude Desktop / ChatGPT sessions:** Paste this first, once per session, before any work:

> You're connected to my WordPress site through Respira. Before doing anything, detect my page builder and read my site's structure, then follow Respira's safe workflow: edit through the builder's native modules (never raw HTML), and duplicate or snapshot a page before changing it live. Confirm what builder I'm on and what you can do.

**For Windsurf sessions:** Not needed — AGENTS.md and `.devin/rules/` already provide this context automatically.

**Optional intent line** (add to the primer to focus the session):
> Today we're [specific task] — read [page/template] structure first.

### The 4 Write Workflows

| # | Workflow | When | Example |
|---|----------|------|---------|
| 1 | **Small edit** | Text, colors, one element | "Change the button to say 'Get a quote'" |
| 2 | **Redesign existing** | Restructure existing page | "Read homepage structure, then rewrite the hero section" |
| 3 | **Build from scratch** | New page | "Build a draft about page with these sections..." |
| 4 | **Two-pass build** | Content-heavy pages (max control) | "Build skeleton with placeholder labels, then fill each section" |

### Anti-Patterns (NEVER do)

- ❌ Ask for raw HTML — builder can't edit it later
- ❌ Skip the read step — agent guesses wrong
- ❌ Edit live without snapshot/duplicate
- ❌ One giant ask — break it into sections instead

### Decision Matrix

| Task | Use Respira MCP (Primary) | Use Bricks GUI (Fallback) | Why |
|------|---------------------------|--------------------------|-----|
| Edit page/template content | ✅ `respira_update_element` | Only if Respira can't | Respira has snapshot + rollback |
| Add/remove pages | ✅ `respira_create_custom_post` | Only if Respira can't | Respira is faster, no browser needed |
| Change colors/typography | ✅ `respira_update_bricks_*` | Only for visual preview | Respira writes directly to DB |
| Manage WP menus | ✅ `respira_*_menu*` tools | Only if Respira can't | Respira is faster |
| Edit templates 185/52 | ✅ With snapshot | ❌ Avoid | Respira has rollback, GUI doesn't |
| Manage media | ✅ `respira_upload_media` | Only if Respira can't | Respira handles sideload + alt text |
| SEO/accessibility audits | ✅ `respira_analyze_*` | ❌ Not available in GUI | Respira-only feature |
| Content text edits | ✅ `respira_update_element` | ✅ Quick GUI edits OK | Either works, Respira preferred |

### ⚠️ Respira MCP Safety Protocol

- Every write auto-captures a snapshot — response includes `snapshot_uuid`
- Rollback: `respira_restore_snapshot` with the `snapshot_uuid`
- Before ANY template edit: run `respira_extract_builder_content` to see current state
- The old flattening bug (`content:update_content` regenerating IDs) does NOT affect Respira

### ⚠️ Respira Honest Limits

- **Undo is per-page, not per-element** — snapshots capture/restore whole pages. Work in smaller sessions for fine-grained history.
- **Media files are not versioned** — snapshots cover page structure/content, not image binaries. Deleting media requires explicit approval.
- **Large single builds hit AI client ceilings** — a 300-element page in one call may get trimmed by the model. Use chunking: skeleton first, then append sections per request.
- **Language is lossy** — no tool fixes an ambiguous ask. The primer + read-first habit exist because misunderstandings happen.

### 📝 Blog-Specific Recipes (Copy-Paste Prompts)

Use these in any Respira-connected environment (Claude Desktop, ChatGPT, Windsurf):

**SEO refresh on a post:**
> Run an SEO analysis on [post]. Then fix the mechanical findings: title tag, meta description, heading hierarchy, image alt text, and internal links to related posts. Show me anything that needs a judgment call.

**Accessibility pass:**
> Scan [post] for accessibility issues. Fix missing alt text, unlabeled buttons and broken heading order. Give me a short report of what you fixed and what needs a human decision.

**Monday morning audit:**
> Give me a site health snapshot: pages changed in the last week, anything that looks broken, SEO issues on the top 5 pages, and one prioritized list of what to fix this week.

**New page (two-pass build):**
> Build a draft [type] page: [list sections in order, one line each]. Use placeholder labels for every text module. Then read it back and confirm the structure before we fill in copy.

### 🎯 Key Respira Skills for Blogging

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| `seo-aeo-amplifier` | On-page SEO + Answer Engine Optimization audit with schema markup | After publishing a post |
| `wordpress-ai-image-optimizer` | Compress, WebP convert, resize, rename images locally | Before deploying |
| `internal-link-builder` | Analyzes all content, maps topic relationships, suggests internal links | After publishing several posts |
| `brand-voice-synthesizer` | Reads 5-10 posts, extracts your brand voice for consistent AI content | Before writing posts with AI |
| `stale-content-detector` | Finds posts that haven't been updated, suggests refresh/redirect/archive | Monthly maintenance |
| `conversion-audit` | Audits for CTA hierarchy, form length, social proof, trust signals | Optimizing key pages |
| `design-system-synthesizer` | Extracts your site's design system (colors, typography, components) | One-time setup |
| `activity-report-composer` | Turns audit log into a polished report | Client or self reporting |

### 🔄 Playbooks (Save Repeatable Workflows)

When you and the agent work out a workflow you'll want again, save it as a playbook:

> Save what we just did as a playbook called [name], so next time I can just say "run the [name] report".

Playbooks are stored on the WordPress site itself and show up as tools the agent can run on demand. Use `respira_create_playbook`, `respira_list_playbooks`, `respira_delete_playbook`.

### Incident Log (Lessons Learned)

**Incident 1:** Spent 45+ min writing PHP mu-plugins for a 2-min GUI task.
**Incident 2 (2026-07-04):** Post-process CSS injection fought with Bricks native CSS, making mobile menu worse.
**Incident 3 (2026-07-04):** AI-created JSON backups had structural issues on re-import. User banned all AI-created backups.
**Incident 4 (2026-07-04/05):** Flattening bug destroyed templates 185 & 52 THREE times via MCP writes. Templates now FROZEN.

**Root cause:** Reaching for scripts/MCP writes instead of Bricks standard operations.

### Correct Workflow

```
1. Use Respira MCP as the PRIMARY tool for all Bricks/WP changes
2. Fall back to Bricks Builder GUI only when Respira MCP can't do the task
3. Changes go live immediately on the Hostinger server — no build or deploy step needed
```

## Default Expectations

- Verify important code changes before claiming completion.
- Keep reusable workflows in shared TSOT when they are useful across projects.
- Keep project-specific decisions and constraints in this repo.
- Prefer updating shared skills and workflows at the source when they should apply everywhere.

## Communication Preferences

- Prefer visually engaging responses with clear structure when helpful.
- Use relevant emojis for headings, status, and scannability instead of plain wall-of-text responses.
- Keep technical explanations clear, but make the presentation feel lively and easy to scan.

## 🎙️ DigiTrust Lab Writing Voice (ALL content — posts, pages, copy)

**Core principle:** Write Malay copy directly in Malay. Never translate from English — translated Malay sounds stiff and robotic. If it wouldn't sound natural said out loud to a Malaysian friend, rewrite it.

### Voice Characteristics

| Trait | Do ✅ | Don't ❌ |
|-------|--------|----------|
| Pronoun | `korang`, `kami` | `anda`, `pengguna` |
| Tone | Casual, warm, like talking to a friend | Formal, corporate, legal-sounding |
| Sentence length | Short, punchy, scannable | Long winding clauses |
| Opener | Direct, honest, relatable | Press release / marketing fluff |
| Mixed language | Natural Malay + occasional English terms (AI, tools, content) | Full formal BM or full English |

### Humour — Make Them Smile, Not Just Read

DigiTrust Lab content should have a light sense of humour woven in naturally — not forced jokes, but the kind of dry wit that makes someone smile while reading. Think: a Malaysian friend explaining tech stuff over teh tarik.

**How to add humour naturally:**
- Self-deprecating honesty: *"Saya pun pernah buat silap ni — jangan gelak."*
- Relatable exaggeration: *"Buka laptop, bukak 47 tabs, akhirnya tutup semua balik."*
- Gentle sarcasm about obvious things: *"Kami tahu polisi privasi bukan benda paling best nak baca..."*
- Unexpected honest admissions: *"Jujur cakap, kami pun tak expect ia akan work."*
- Lighthearted aside in brackets: *"(percaya ke tak, memang boleh)"* or *"(yes, serius ni)"*

**Rules for humour:**
- Never punch down or mock the reader
- Keep it relevant — don't force a joke where none fits
- One or two light moments per page/post is enough — don't overdo it
- Humour works best in openers, transitions, and asides — not in conclusions or CTAs

### Punctuation — Write Like a Malaysian, Not Like AI

**Em dash (`—`) rule:** Use sparingly. Maximum 1 per post/page, only when genuinely needed. Malay prose flows naturally with commas, `iaitu`, `memandangkan`, `sebab`, `jadi`, or a new sentence entirely. Frequent em dashes are a strong AI-writing tell in Malay because native writers almost never use them.

| Instead of `—` | Use this |
|---|---|
| `AI tools dah canggih — korang kena tahu cara guna.` | `AI tools dah canggih, jadi korang kena tahu cara guna.` |
| `Kami tulis dari pengalaman — bukan teori semata.` | `Kami tulis dari pengalaman sebenar, bukan teori semata.` |
| `Ini bukan kursus — ini perkongsian jujur.` | `Ini bukan kursus. Ini perkongsian jujur.` |

**Other AI punctuation patterns to avoid:**
- ❌ Stacking em dashes within the same sentence
- ❌ Starting bullets with em dashes
- ❌ Using `—` as a substitute for a full stop
- ❌ Overusing `...` (ellipsis) for dramatic pauses — one or two per post max

### Red Flag Phrases — Always Rewrite These

- ❌ `"Privasi anda penting bagi kami"` → sounds like a copy-paste template
- ❌ `"Anda berhak untuk"` → translated legalese
- ❌ `"Kami sentiasa terbuka"` → press release language
- ❌ `"Kunjungi link external pada risiko anda sendiri"` → sounds threatening
- ❌ `"Untuk pertanyaan umum, kerjasama, atau sokongan"` → call center language
- ❌ Any sentence that starts with `"Maklumat di blog ini adalah untuk tujuan..."` → textbook opening

### 🚫 Anti-Salesy Copy Policy (added 2026-07-10)

**Rule:** DigiTrust Lab copy must never sound like a sales pitch. We lead with usefulness, not with money promises.

**The specific trigger:** Any phrase that implies "use this → make money" in a direct, pushy way is banned from UI copy — buttons, sidebar widgets, CTA boxes, opt-in forms, hero text, anywhere.

**Banned patterns in UI copy:**

| ❌ Salesy | ✅ Replace with |
|---|---|
| `jana duit` in widget/CTA copy | Focus on the action benefit instead — `buat kerja`, `jimat masa`, `mudahkan hidup` |
| `jana pendapatan` in above-the-fold hero | OK in blog post body, NOT in hero headline |
| `dapatkan duit` / `buat duit` | Never in UI copy |
| `tingkatkan jualan` | Only in blog post body, not in opt-in or CTA buttons |
| Stacking benefit claims: `jimat masa, jana duit, kurangkan kerja` | Pick one — the strongest and most specific one |

**Why:** "Jana duit" reads as bombastic and desperate when placed in sidebar widgets or hero copy. The reader already knows this site is about making money — they came here for that. Hitting them with it again in every widget cheapens the brand.

**Correct approach:** Let the *content* make the money promise implicitly. UI copy should be about the *immediate action benefit* — what they get right now by clicking or subscribing.

**Approved sidebar/CTA copy pattern (reference):**
```
Title:   Dapatkan Panduan Percuma
Body:    50 Prompt AI yang korang boleh guna terus untuk buat kerja dan jimat masa.
Sub:     Percuma sepenuhnya. Unsubscribe bila-bila masa.
Button:  Hantar →
```

### Green Light Patterns — Use These

- ✅ `"Kami tahu page ni biasanya boring — tapi kami nak jelaskan dengan cara yang mudah faham."`
- ✅ `"Kami tak jual data sesiapa kepada sesiapa."` — direct, reassuring
- ✅ `"Tu janji kami."` — personal, accountable
- ✅ `"Biasanya dalam masa 48 jam pada hari bekerja."` — plain, no jargon
- ✅ `"Kalau korang nak tahu tentang...korang dah ada kat tempat yang betul."` — warm, inclusive

### Natural Malay Flow Patterns

AI-generated Malay has predictable awkwardness — half-casual/half-formal mixing, over-translated English terms, unfinished sentences, textbook intros. The full fix guide with before/after tables lives in:

**📖 `.devin/skills/malay-voice-guide/SKILL.md`** — Load this skill before writing or reviewing any Malay content.

Quick summary of the 7 patterns:
1. **No formal + casual mixing** — `korang` + `manfaatkan` = uncanny valley
2. **Code-switch naturally** — `content` not `kandungan`, `marketing` not `pemasaran`
3. **Complete every thought** — vague claims need concrete examples right after
4. **Skip textbook intros** — no `AI bermaksud...` or `Dalam artikel ini...`
5. **Use casual transitions** — `jadi` not `oleh itu`, `tapi` not `walau bagaimanapun`
6. **Emphasise like a Malaysian** — `confirm`, `memang`, `wajib` not `sangat`, `amat`
7. **Always contract** — `tak` not `tidak`, `dah` not `sudah`, `sebab` not `kerana`

### Page-Specific Voice Notes

**Tentang Kami:** Personal founder story tone. "Kami" = Zed + AI partner. Avoid bullet-point brochure style — write in flowing paragraphs with personality.

**Polisi Privasi / Disclaimer:** Still needs to be clear and accurate, but written in plain language. Add a human touch — acknowledge these pages are normally boring. Keep legal meaning, strip corporate language.

**Hubungi Kami:** Friendly invitation, not a corporate FAQ. Feels like you're genuinely happy to hear from readers.

**Blog posts:** Casual Malay, first-person, experience-led. Opener should hook emotionally or with a relatable scenario. Never start with a definition or statistics dump.

### Core Pages — Approved Rewrites (2026-07-06)

All 4 core pages were audited and rewritten with natural voice on 2026-07-06. Use these as the voice benchmark for all future content:
- Tentang Kami ✅ rewritten
- Polisi Privasi ✅ rewritten
- Disclaimer ✅ rewritten
- Hubungi Kami ✅ rewritten

## Quick Reference

| File | Purpose |
|------|---------|
| `BRICKS-BUILDER-GUIDE.md` | Bricks element reference — read BEFORE editing Bricks elements (tool names are old Bricks MCP, use Respira equivalents) |
| `DESIGN.md` | Design system source of truth (colors, typography, components) |

### Key Template IDs

| Template | ID | Type | Status |
|----------|----|------|--------|
| Header | 185 | header | ✅ Editable via Respira MCP (snapshot before edit) |
| Footer | 46 | footer | ✅ Native elements |
| Single Post | 10 | content | ✅ Native elements |
| Blog Archive | 52 | archive | ✅ Editable via Respira MCP (snapshot before edit) |

## 🧠 Skills Auto-Trigger Table (For Claude Desktop)

Claude Desktop cannot read `.devin/` or `.windsurf/` rules. When a user request matches a trigger below, read the corresponding `SKILL.md` file before executing. Only skills that require Respira MCP, WriterZen, or DigiTrust Lab-specific context are listed — generic marketing tasks (email sequences, UTM tracking, competitor analysis, content repurposing) can be handled natively without a skill file.

### Respira MCP Skills (require WordPress + Respira connection)

| Trigger Phrases | Skill File | What It Does |
|----------------|-----------|--------------|
| "amplify my seo", "seo audit", "aeo audit", "optimize for search" | `.devin/skills/seo-aeo-amplifier/SKILL.md` | On-page SEO + AEO audit with schema markup via Respira MCP |
| "extract my brand voice", "analyze my tone", "writing style" | `.devin/skills/brand-voice-synthesizer/SKILL.md` | Reads your posts, extracts DigiTrust Lab brand voice |
| "build internal links", "link my content", "topic relationships" | `.devin/skills/internal-link-builder/SKILL.md` | Analyzes your content via Respira MCP, suggests internal links |
| "stale content", "old posts", "content refresh" | `.devin/skills/stale-content-detector/SKILL.md` | Finds posts that haven't been updated via Respira MCP |
| "compress images", "webp convert", "optimize images" | `.devin/skills/wordpress-ai-image-optimizer/SKILL.md` | Compress, WebP convert, resize images via Respira MCP |
| "site dna", "wordpress audit", "site health check" | `.devin/skills/wordpress-site-dna/SKILL.md` | Full WordPress site audit via Respira MCP |
| "activity report", "what did I do", "audit log report" | `.devin/skills/activity-report-composer/SKILL.md` | Turns Respira audit log into a polished report |
| "prime the agent", "session start", "load site context" | `.devin/skills/prime-the-agent/SKILL.md` | Fast session starter — loads site, builder, schemas |
| "bricks mcp", "mcp tool selection", "bricks via mcp" | `.devin/skills/bricks-mcp-absolute/SKILL.md` | MCP tool selection and execution protocol for Bricks |

### WriterZen Skill (requires specific tool workflow)

| Trigger Phrases | Skill File | What It Does |
|----------------|-----------|--------------|
| "keyword research", "find keywords", "writerzen", "seed keyword", "kd analysis" | `.devin/skills/writerzen-keyword-research/SKILL.md` | WriterZen keyword research — Malaysia, Malay, KD < 20 |

### Marketing Skills (on-demand only)

For broader marketing strategy (competitor teardown, E2E SEO, ICP research, content repurposing, email sequences, programmatic SEO, UTM tracking), read `.devin/skills/marketing-skills-index/SKILL.md` when explicitly asked. These are not auto-triggered — Claude handles generic marketing tasks natively.

### How to Use (For Claude Desktop)

1. Match the user's request against trigger phrases in the tables above
2. Read the full `SKILL.md` file from the listed path
3. Follow the skill's workflow
4. Only load one skill at a time (the matching one)
5. Combine with Respira MCP tools when relevant (e.g., SEO strategy → then Respira on-page fixes)

## 🔍 WriterZen Keyword Research

**Before writing any blog post, research the keyword first.** Load the `writerzen-keyword-research` skill for the full workflow.

**Quick reference:**
- Tool: WriterZen → Keyword Explorer
- Location: Malaysia | Language: Malay
- Target: KD by Content < 20, some search volume
- Save to: WriterZen Keyword List → "DigiTrust Lab Blog Posts"
- Record metrics in: `content/content-calendar.md` (per-post entry)

## Notes

- This is a WordPress blog hosted on Hostinger, using Bricks Builder theme
- Live URL: `https://digitrustlab.com` (WordPress is served directly — no static export or build step)
- WP Admin URL: `https://digitrustlab.com/wp-admin/`
- Respira MCP: connected to Windsurf and Claude Desktop (replaced old Bricks MCP on 2026-07-05)
- Respira API key stored in Claude Desktop via `.mcpb` install and in Windsurf `mcp_config.json`
- Old Bricks MCP bridge (`bricks-mcp-bridge.mjs`) is decommissioned — do not use
- Template type filter: Use `type: "content"` (not `"single"`) for single post templates
- Previous architecture (Local WP + Simply Static + Cloudflare Pages) was fully decommissioned on 2026-07-12 — see `deprecated/` folder for archived documentation
