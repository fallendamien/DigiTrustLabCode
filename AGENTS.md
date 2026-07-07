# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Bricks standard procedures — Bricks Builder GUI or Respira MCP. NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Bricks GUI or Respira MCP, it doesn't get done.**

**Exception:** Wrangler CLI is allowed for Cloudflare Pages deployment only — it's a deploy tool, not a Bricks internal operation.

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

**As of 2026-07-05, Respira MCP replaced the old Bricks MCP.** Respira takes a snapshot before every write and supports one-call rollback. The flattening bug was caused by the old Bricks MCP's `content:update_content` action — Respira does not use that API.

Templates 185 (Header) and 52 (Blog Archive) are now editable via Respira MCP with confidence. Always use `respira_extract_builder_content` before editing and keep the returned `snapshot_uuid` for rollback if needed.

## ✅ Devin's Permitted Scope

**You ARE permitted to:**
- Create and edit WordPress POSTS, PAGES, and Bricks templates via Respira MCP
- Manage menus via Respira MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins
- Manage media via Respira MCP

**You are NOT permitted to:**
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — it is decommissioned
- Use Raw HTML Code elements in Bricks templates

## ✅ Current Priority: Write and Publish Post #1

This is the only task that matters right now. Do NOT work on any template, design,
or infrastructure task unless Zamri explicitly instructs it.

## 🔴 UNRESOLVED: Category/Taxonomy Archives Don't Use Custom Template

Template ID 52 (Blog Archive) has condition `{"main": "archiveType", "archiveType": "any"}`
set via `template_condition:set`. This correctly applies to `/blog/` (post type
archive) but does NOT apply to `/category/ai-tools/` or `/category/digital-side-hustle/`
(taxonomy term archives).

**Confirmed via DOM inspection:** on category pages, `#brx-content` contains ONLY
`<div class="brxe-container"><div class="bricks-no-posts-wrapper">...</div></div>`
— none of our template's elements (section/header block/heading/grid) are present
at all. This means Bricks is not loading template 52 on taxonomy archives — it's
using some other fallback entirely.

**What was tried (didn't work):**
- `archiveType: any` condition alone
- Adding a second condition `archivePostType: post`
- Adding `hasLoop: true` + `is_main_query: true` to the query object per the Bricks
  MCP builder guide's Archive Templates section

**Needs investigation:**
- Check `bricks:get_condition_schema` or `template_condition:types` for the correct
  condition to target taxonomy archives specifically (may need something like
  `archiveType: taxonomy` or a `terms` condition type, not `archivePostType`)
- Verify whether Bricks WP core theme even supports a single template covering
  BOTH post-type archives AND taxonomy archives, or if they need separate
  templates/conditions
- Check in Bricks GUI directly: Template 52 → Settings → Conditions, to see what
  the visual condition picker actually offers for taxonomy targeting

**Workaround in place:** `.bricks-archive-title-wrapper { display: none !important; }`
in WP Additional CSS hides the ugly "Category: X" heading. The "Nothing found"
state is cosmetic-only until Post #1 exists, but the missing centered header/grid
styling on category pages will persist even after posts are published, since the
custom template isn't being used there at all.

### 🧩 Respira MCP (PRIMARY TOOL — replaced old Bricks MCP 2026-07-05)

**Respira MCP is active on digitrust-lab.local.** Connected to Windsurf and Claude Desktop.

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

| Task | Use GUI | Use Respira MCP | Use Non-Bricks Code | Why |
|------|---------|----------------|---------------------|-----|
| Edit page/template content | ✅ WordPress/Bricks GUI | ✅ `respira_update_element` | ❌ | Primary tools |
| Add/remove pages | ✅ WordPress → Pages | ✅ `respira_create_custom_post` | ❌ | Either works |
| Change colors/typography | ✅ Bricks GUI | ✅ `respira_update_bricks_*` | ❌ | Visual editor or MCP |
| Manage WP menus | ✅ Appearance → Menus | ✅ `respira_*_menu*` tools | ❌ | GUI or MCP |
| Deploy to Cloudflare | ✅ Cloudflare dashboard | ❌ | ✅ Wrangler CLI | Deploy tool only |
| Edit templates 185/52 | ✅ With care | ✅ With snapshot | ❌ | Respira has rollback |

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
1. Make all changes via Bricks Builder GUI (primary) or Respira MCP (when GUI impractical)
2. Run Simply Static export (WP Admin → Simply Static → Generate)
3. Deploy via Wrangler CLI or Cloudflare dashboard
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

### Green Light Patterns — Use These

- ✅ `"Kami tahu page ni biasanya boring — tapi kami nak jelaskan dengan cara yang mudah faham."`
- ✅ `"Kami tak jual data sesiapa kepada sesiapa."` — direct, reassuring
- ✅ `"Tu janji kami."` — personal, accountable
- ✅ `"Biasanya dalam masa 48 jam pada hari bekerja."` — plain, no jargon
- ✅ `"Kalau korang nak tahu tentang...korang dah ada kat tempat yang betul."` — warm, inclusive

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

## Troubleshooting Reference (CRITICAL)

**This is a blogging business project, NOT a development project.**

- **ALWAYS** read `TROUBLESHOOTING.md` at session start before working on this project
- **ALWAYS** check `TROUBLESHOOTING.md` before suggesting fixes or approaches — documented issues may already have solutions
- **ALWAYS** append new issues to `TROUBLESHOOTING.md` when encountering problems that took >5 minutes to resolve
- **DO NOT** use global `lessons.md` for this project — all project-specific issues stay in `TROUBLESHOOTING.md`
- **DO NOT** create separate troubleshooting files — one file, appended chronologically

### Quick Reference

| File | Purpose |
|------|---------|
| `BRICKS-BUILDER-GUIDE.md` | Bricks element reference — read BEFORE editing Bricks elements (tool names are old Bricks MCP, use Respira equivalents) |
| `TROUBLESHOOTING.md` | All known issues, fixes, and prevention rules |
| `DESIGN.md` | Design system source of truth (colors, typography, components) |

### Key Template IDs

| Template | ID | Type | Status |
|----------|----|------|--------|
| Header | 185 | header | ✅ Editable via Respira MCP (snapshot before edit) |
| Footer | 46 | footer | ✅ Native elements |
| Single Post | 10 | content | ✅ Native elements |
| Blog Archive | 52 | archive | ✅ Editable via Respira MCP (snapshot before edit) |

### Bricks Template Cache — Simply Static Export Issue (CRITICAL)

**Symptom:** You update a Bricks template via Respira MCP (e.g. footer link), WordPress renders the change correctly, but Simply Static export still outputs the OLD content.

**Root cause:** Bricks caches rendered template HTML separately from the database. `update_element` changes the data, but Bricks keeps serving cached HTML to Simply Static's crawler.

**Fix (3 steps — all required):**
1. **Bricks → Settings → Regenerate CSS files** (clears CSS cache)
2. **Bricks → Settings → Regenerate code signatures** (clears code cache — confirm the dialog alert)
3. **Re-save the template** via `respira_update_page` with `status: "publish"` (forces Bricks to re-render)

Then run Simply Static export — the fresh render will be picked up.

**Manual GUI steps to clear Bricks cache:**
1. WP Admin → Bricks → Settings
2. Click **"Regenerate CSS files"** button
3. Click **"Regenerate code signatures"** button (accept the confirmation dialog)
4. Go to Bricks → Templates → edit the template → click **"Update"** to re-save

**When to do this:** Any time a Bricks template change (footer, header, archive) doesn't appear in the Simply Static export despite WordPress showing it correctly.

## Notes

- This is a WordPress + Simply Static + Cloudflare Pages blog, not a traditional codebase
- Static files live in `D:\Coding Zone\digitrust-lab-static`
- WordPress local URL: `https://digitrust-lab.local`
- Simply Static generate URL: `https://digitrust-lab.local/wp-admin/admin.php?page=simply-static-generate` (NOT `simply-static` — that's settings, not generate)
- Live URL: `https://www.digitrustlab.com` (fully migrated from `blog.digitrustlab.com`, which no longer has a DNS record — do not reference the old subdomain)
- Deploy: Run from `D:\Coding Zone\digitrust-lab-static`:
  ```powershell
  npx wrangler pages deploy . --project-name=digitrust-lab-static
  ```
  No wrangler.toml needed. Wrangler caches uploaded files — only changed files get re-uploaded. Must run from the static output directory, not the repo.
- Respira MCP: connected to Windsurf and Claude Desktop (replaced old Bricks MCP on 2026-07-05)
- Respira API key stored in Claude Desktop via `.mcpb` install and in Windsurf `mcp_config.json`
- Old Bricks MCP bridge (`bricks-mcp-bridge.mjs`) is decommissioned — do not use
- Template type filter: Use `type: "content"` (not `"single"`) for single post templates
