# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 📁 File Architecture — Who Reads What

| Layer | Purpose | Read By |
|-------|---------|---------|
| `AGENTS.md` | Voice, copy policy, project rules — single source of truth | All agents (Claude, Codex, Devin, ChatGPT) |
| `.devin/rules/` | Operational behaviour — safety checks, tool constraints | Devin only (auto-loaded every session) |
| `.devin/skills/` | On-demand task recipes — SEO audit, keyword research, image optimisation | Devin only (trigger-based, not auto-loaded) |

**Rule:** Never duplicate content/voice standards into `.devin/rules/` — keep AGENTS.md as the single source. `.devin/rules/` should only contain operational behaviour constraints (e.g. "never edit template without snapshot").

### 🖥️ Editors — Zed is primary (as of 2026-08-05)

| Editor | Status | Agents reached from it |
|--------|--------|------------------------|
| **Zed** | ✅ **Primary** | Codex (via ACP / `codex-acp`), Claude Code (terminal or ACP) |
| Claude Code | ✅ Active | itself — CLI, desktop app, or a Zed terminal pane |
| Windsurf | ⚠️ Retained for Devin only | Devin. Not used for day-to-day editing. |
| VS Code | ⚠️ Legacy | — |

**Two naming traps — read before any find-and-replace:**

1. **`.windsurf/` is a path, not an editor endorsement.** `.windsurf/rules`,
   `.windsurf/skills`, and `.windsurf/workflows` are all **symlinks into the
   TSOT**, shared by every project on this machine. They stay exactly as they
   are regardless of which editor is in use. Renaming them breaks every project
   and is never the right fix.
2. **"Zed" is also the site's author/brand name** (`{author_name}` renders as
   "Zed"; `AGENTS.md` § Tentang Kami uses "Kami" = Zed + AI partner). Never run
   a blind `Windsurf → Zed` replace across this repo — it collides with the pen
   name and with the symlink paths above.

**Zed + Codex specifics** (adapter quirks, the `codex-skill-bridge`, and the
mandatory restart-after-change trap) are documented in
`docs/plan-tsot-git-migration.md` § "Codex workflows in Zed".

### ✅ Verify the doctrine actually loaded (run at session start)

```bash
python scripts/verify-imports.py
```

Asserts every `@import` target resolves, every symlinked tree points somewhere real, and the load-bearing skills exist. Exit 0 = clean, 1 = something is missing.

**Why this exists:** on 2026-07-30 a symlink migration silently removed three of the four rules `CLAUDE.local.md` imports. Nothing errored — agents simply ran without the Bricks-Only Policy and the content-planning rule for a full working day. **A missing `@import` is indistinguishable from a satisfied one unless something checks.**

Run it also after: editing any symlink, changing `.gitignore`, cloning to a new machine, or starting work in a **git worktree** (`CLAUDE.md` and `CLAUDE.local.md` are gitignored, so a worktree has neither — the script catches that immediately).

## 🚫 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Respira MCP (primary) or Bricks Builder GUI (fallback). NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Respira MCP or Bricks GUI, it doesn't get done.**

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

❌ **NEVER use `respira_inject_builder_content` with `mode: replace` on any `bricks_template` post type** — causes flatten bug (Bricks GUI Structure panel goes blank, elements written to DB but uneditable). Templates 10, 52, 185, 46 are all affected. For templates, ALL structural changes must go through `respira_update_element` or direct `_bricks_data` post meta editing via Devin in Windsurf.

## 🚫 PRIORITY #2: CSS Grid in Bricks — Incident on `#brxe-778413` (Learned 2026-07-18, Updated 2026-07-19)

**Incident:** On homepage element `#brxe-778413` (page ID 280), blog post cards stacked vertically instead of displaying in a 3-column grid. Full debugging timeline and evidence in `docs/bricks-grid-issue-report.md`.

**What was observed on this element:**
- Plain `1fr` grid tracks expanded to ~1100px each instead of sharing space equally (observed via `getComputedStyle`)
- Native `_display: grid` added a `brx-grid` class that triggered Bricks frontend JS, which overrode `grid-template-columns` with pixel values — even with `!important` CSS rules
- Child cards (`#brxe-4c6189`, class `brxe-container`) had computed `width: 1100px`
- `_cssCustom` survived CSS regeneration — the original "CSS stripping" diagnosis was wrong

**Deployed workaround (verified on this element only):**
```css
#brxe-CONTAINER_ID{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:20px !important;width:100% !important;}
#brxe-CONTAINER_ID > *{min-width:0 !important;max-width:100% !important;width:100% !important;}
@media(max-width:991px){#brxe-CONTAINER_ID{grid-template-columns:repeat(2,minmax(0,1fr)) !important;}}
@media(max-width:767px){#brxe-CONTAINER_ID{grid-template-columns:1fr !important;}}
```

**Key points:**
- `minmax(0, 1fr)` — forces tracks to shrink below content size (plain `1fr` expanded to content width on this element)
- `> * { width: 100% !important }` — overrides the observed 1100px width on child elements for this container
- `_cssCustom` survived CSS regeneration in this session
- On this element, native `_display: grid` + `_gridTemplateColumns` was overridden by Bricks JS — **reproduce and verify before assuming the same on other elements**

**After any Respira DB-level write to Bricks elements:**
1. Regenerate Bricks CSS (WP Admin → Bricks → Settings → Regenerate CSS files)
2. Purge LiteSpeed Cache (WP Admin → LiteSpeed → Toolbox → Purge All - LSCache)
3. Verify frontend with `?nocache=1`

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

**As of 2026-07-05, Respira MCP replaced the old Bricks MCP.** Respira takes a snapshot before every write and supports one-call rollback. The flattening bug was caused by the old Bricks MCP's `content:update_content` action — Respira does not use that API.

Templates 185 (Header) and 52 (Blog Archive) are now editable via Respira MCP with confidence. Always use `respira_extract_builder_content` before editing and keep the returned `snapshot_uuid` for rollback if needed.

## 🚫 PRIORITY #3: Query Loop Placement Rules (CRITICAL — Learned 2026-07-18)

**RULE: Query Loop belongs on the CARD container ONLY — never on the Section or grid container. Only ONE Query Loop should be active in the element hierarchy.**

**What happened:** Query Loop was enabled on 3 nested elements (Section, grid container, AND card container). Bricks rendered one grid per post — each grid had 1 card + 2 empty columns = massive empty space on the right side of the homepage.

**Correct structure for blog card grids:**
- Section: Query Loop OFF
- Grid container: Query Loop OFF, Display: Grid (native), Columns: 3, Gap: 20px
- Card container: Query Loop ON, Query type: Post, postsPerPage: 3

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

## ✅ RESOLVED: Blog Archive Template 52 — Option C Layout (2026-07-20)

**Status:** Fully working on `/blog/`. Layout: archive title → hero post (1) → "Artikel Lain" label → 3-column grid (9) → pagination.
- **Full fix details:** See `docs/template-52-layout.md`

## ✅ RESOLVED: Category/Taxonomy Archives — Empty Categories Redirect (2026-07-23)

**Root cause:** Not a template issue. Empty categories (`ai-untuk-perniagaan-kecil`, `canva-design`, `digital-side-hustle`) have 0 posts assigned. WordPress + Rank Math's `noindex_empty_taxonomies` setting correctly redirects empty archives to the homepage. This is standard SEO practice.

**Current categories (updated 2026-07-25):**
- `ai-tools` — 3 posts ✅ (works correctly on `/category/ai-tools/`)
- `canva-design` — 0 posts (redirects to homepage — correct, will work once posts assigned)
- `prompt-engineering` — 0 posts (NEW — replaces Digital Side Hustle)
- `digital-skills` — 0 posts (NEW — replaces AI untuk Perniagaan Kecil)
- `digital-side-hustle` — DELETED (implied income claims)
- `ai-untuk-perniagaan-kecil` — DELETED (business advice without results)

**Fix:** No fix needed. Categories will automatically work once posts are assigned to them. The "missing canonical" warnings in Screpy are a side effect of the redirect — Screpy sees the homepage canonical instead.

**Action:** When publishing future posts about side hustles, Canva, or business AI, assign them to the appropriate categories. The category pages will automatically start working.

**Workaround still in place:** `.bricks-archive-title-wrapper { display: none !important; }` in WP Additional CSS hides the "Category: X" heading on category pages that do have posts.

### 🎨 WordPress Additional CSS Backup

All custom CSS added via WordPress Customizer → Additional CSS is backed up in `docs/tablepress-custom-css.md`. **Whenever CSS changes are made to the Customizer, update that backup file in the same session.** This includes TablePress styling, Bricks workarounds, and any other site-wide CSS rules.

### 🧩 Respira MCP (PRIMARY TOOL — replaced old Bricks MCP 2026-07-05)

**Respira MCP is active on digitrustlab.com (live Hostinger site).** Connected to Claude (Code + Desktop), Codex, and Devin.

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
- **MailerLite embed check:** Existing MailerLite embeds use Bricks Code elements. Keep **Execute Code ON** and verify it before saving; when disabled, the frontend displays the embed as raw HTML instead of rendering the form.
- The old flattening bug (`content:update_content` regenerating IDs) does NOT affect Respira

### ⚠️ Respira Honest Limits

- **Undo is per-page, not per-element** — snapshots capture/restore whole pages. Work in smaller sessions for fine-grained history.
- **Media files are not versioned** — snapshots cover page structure/content, not image binaries. Deleting media requires explicit approval.
- **Large single builds hit AI client ceilings** — a 300-element page in one call may get trimmed by the model. Use chunking: skeleton first, then append sections per request.
- **Post excerpts may not update via `respira_update_post`** — the `excerpt` parameter is accepted in the schema but does not reliably persist. If the excerpt panel in WP Admin still shows the old text after a Respira update, edit it directly in WP Admin (Post editor → Settings → Excerpt) and save.
- **Language is lossy** — no tool fixes an ambiguous ask. The primer + read-first habit exist because misunderstandings happen.

### 📝 Blog-Specific Recipes (Copy-Paste Prompts)

Use these in any Respira-connected environment (Claude Code, Claude Desktop, Codex in Zed, ChatGPT, Windsurf):

**SEO refresh on a post:**
> Run an SEO analysis on [post]. Then fix the mechanical findings: title tag, meta description, heading hierarchy, image alt text, and internal links to related posts. Show me anything that needs a judgment call.

**Accessibility pass:**
> Scan [post] for accessibility issues. Fix missing alt text, unlabeled buttons and broken heading order. Give me a short report of what you fixed and what needs a human decision.

**Readability pass (fix "sea of text"):**
> Audit [post] for wall-of-text sections. Move images above the fold, convert warning lists into callout boxes, restyle example prompts as blockquotes. Keep all wording and SEO structure intact.

**Monday morning audit:**
> Give me a site health snapshot: pages changed in the last week, anything that looks broken, SEO issues on the top 5 pages, and one prioritized list of what to fix this week.

**New page (two-pass build):**
> Build a draft [type] page: [list sections in order, one line each]. Use placeholder labels for every text module. Then read it back and confirm the structure before we fill in copy.

### 🎯 Key Skills for Blogging

**Respira MCP Skills (WordPress-side):**

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

**Shared TSOT Skills (Content & SEO planning)** — live in `.windsurf/skills/`, which is a symlinked path shared by all agents, not a Windsurf-only tree:

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| `content-strategy` | Plans content pillars, topic clusters, keyword research by buyer stage | Before deciding what to write |
| `copywriting` | Writes conversion-focused marketing copy (headlines, CTAs, page structure) | Writing new posts or pages |
| `copy-editing` | Seven Sweeps Framework for polishing existing copy | Reviewing/editing drafts before publishing |
| `readability-pass` | Breaks up walls of text: image placement, callout boxes, blockquote examples | After publishing, when post looks too dense |
| `ai-seo` | Optimizes content for AI search citation (ChatGPT, Perplexity, Google AI Overviews) | After publishing, for AI visibility |
| `schema-markup` | Implements structured data (JSON-LD) for rich results | After publishing, for enhanced search results |
| `lead-magnets` | Plans lead magnet format, gating strategy, landing page structure | Building email list |
| `doc-co-authoring` | Structured workflow for long-form content (whitepapers, ebooks, guides) | Creating pillar content |
| `grill-me` | Relentless interview to stress-test a plan or idea before execution | Before committing to a content strategy |
| `grill-with-docs` | Same as grill-me but produces ADRs and glossary as you go | Documenting strategic decisions |

### 🔄 Playbooks (Save Repeatable Workflows)

When you and the agent work out a workflow you'll want again, save it as a playbook:

> Save what we just did as a playbook called [name], so next time I can just say "run the [name] report".

Playbooks are stored on the WordPress site itself and show up as tools the agent can run on demand. Use `respira_create_playbook`, `respira_list_playbooks`, `respira_delete_playbook`.

### Incident Log (Lessons Learned)

**8 incidents documented** — root cause pattern: reaching for scripts/MCP writes instead of Bricks standard operations.
- **Full incident log:** See `docs/incident-log.md`
- **Key rules:** No `inject_builder_content` replace on templates (Incident 5), no query loops via MCP (Incident 6), use `apply_builder_patch` for reordering (Incident 7), query loop settings require Bricks GUI save (Incident 8)

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
- Use emojis for headings, status, warnings, and milestones — not on ordinary bullets or comparison tables. Semantics per rule 6 of the `i-have-adhd` skill (✅ = verified, ⚠️ = warning, 🔍 = investigation, 🚀 = next step).
- Keep technical explanations clear, but make the presentation feel lively and easy to scan.

## 🎙️ DigiTrust Lab Writing Voice (ALL content — posts, pages, copy)

**Core principle:** Write Malay copy directly in Malay using **natural formal–semi-formal Bahasa Melayu**. Combine polished formal sentence structures with the warmth and accessibility of semi-formal writing. Never translate mechanically from English. Use proper baku (standard Malay), `anda` for the reader, full forms (`tidak` not `tak`), and no slang. Reference style: TrueNetLab.com (formal-natural tech), BarakahDigital.com.my (formal–semi-formal mix), Exabytes.my/blog BM section (formal business tech), PandaiTech.my (semi-formal comparison), Ecentral.my (formal grammar patterns) — professional, natural, and accessible.

**Authoritative reference:** Dewan Bahasa dan Pustaka (DBP) — `dbp.gov.my/pedoman-dan-panduan-bahasa-melayu/` for spelling, grammar, and formal BM standards.

### Voice Characteristics

| Trait | Do ✅ | Don't ❌ |
|-------|--------|----------|
| Pronoun | `anda`, `kami` | `korang`, `kau`, `awak` |
| Tone | Natural formal–semi-formal: polished and grammatically complete, yet warm and accessible | Casual slang OR bureaucratic, academic, textbook-dry prose |
| Sentence structure | Use formal constructions when they sound clearer and more natural aloud; vary length for rhythm and clarity | Mechanically simplify every sentence OR use long, winding clauses |
| **Tatabahasa** | **Every sentence MUST have complete grammar — especially a proper verb (kata kerja). Missing verbs make sentences sound stagnant and broken.** | **Loose colloquial structure with missing verbs (`banyak proses ulang-ulang` instead of `banyak melibatkan proses berulang`)** |
| **Comma usage** | **Use commas strategically to create natural breathing pauses. A sentence that runs flat from start to finish feels breathless.** (`Jadi persoalannya, bukan...` — comma creates a deliberate pause) | **No pause points at all — sentences run straight through without rhythm** |
| Opener | Engaging question or relatable scenario in proper BM | Press release, textbook definition, or slang hook |
| Mixed language | BM baku with English tech terms (AI, tools, API, ChatGPT) + natural English retention for awkward BM translations (`copy & paste`, `drag & drop`, `brainstorm`, `feedback`, `deadline`). English terms italicized in BM sentences for visual clarity. | Slang code-switching (`confirm`, `gila`, `je`) OR forced awkward BM translations (`salin & tampal`, `seret & lepas`) OR English terms not italicized |
| **"Malaysia" usage** | **Avoid inserting "Malaysia" / "rakyat Malaysia" / "warga Malaysia" into copy unless the context specifically requires it (e.g., a keyword target). The audience is already Malaysian — no need to belabour it.** | **Stuffing "Malaysia" into every title, description, or sentence for SEO padding (`Blog AI Malaysia`, `untuk rakyat Malaysia`, `AI tools Malaysia` in body copy) — sounds bombastic and unnatural** |

### Register Selection — The Read-Aloud Rule

Do not reject a sentence merely because it is fully formal. Formal wording is preferred when it sounds natural, precise, and smooth when read aloud. Use semi-formal phrasing where it improves warmth or accessibility.

**Decision order:**
1. Grammatically correct and faithful to the intended meaning
2. Natural when read aloud by a Malaysian speaker
3. Clear to a general reader on the first reading
4. Consistent with the surrounding paragraph

**Preferred example:** `Tanpa memerlukan kefahaman konsep matematik yang rumit` — polished and formal, but still natural aloud. Do not automatically flatten it to `Tanpa perlu faham matematik yang rumit` merely to make the prose less formal.

**Rule:** Simplify bureaucratic or academic wording, not good formal Malay. The target is natural prose, not the lowest possible level of formality.

**Concrete before → after examples:** See `.devin/skills/malay-voice-guide/SKILL.md` § "Concrete Before → After Examples" for 12 real editing patterns from Post #1, plus guidance on which casual sentences to leave as-is (humour, punchiness, parallel structure).

### Humour — Light Wit Without Slang

DigiTrust Lab content should have a light sense of humour woven in naturally — not forced jokes, but the kind of dry wit that makes someone smile while reading. Think: a knowledgeable mentor who occasionally adds a human touch.

**How to add humour naturally (in formal–semi-formal BM):**
- Self-deprecating honesty: *"Kami juga pernah melakukan kesilapan ini — jangan tertawa."*
- Relatable exaggeration: *"Membuka laptop, membuka 47 tab, akhirnya menutup semula semuanya."*
- Gentle sarcasm about obvious things: *"Kami tahu polisi privasi bukan bacaan paling menarik..."*
- Unexpected honest admissions: *"Jujur, kami juga tidak menjangka ia akan berjaya."*
- Lighthearted aside in brackets: *"(percaya atau tidak, memang boleh)"*

**Rules for humour:**
- Never punch down or mock the reader
- Keep it relevant — don't force a joke where none fits
- One or two light moments per page/post is enough — don't overdo it
- Humour works best in openers, transitions, and asides — not in conclusions or CTAs
- All humour must use proper BM — no slang-based humour

### Punctuation — Write Properly, Not Like AI

**Em dash (`—`) rule:** Use sparingly. Maximum 1 per post/page, only when genuinely needed. Malay prose flows naturally with commas, `iaitu`, `memandangkan`, `kerana`, `jadi`, or a new sentence entirely. Frequent em dashes are a strong AI-writing tell in Malay because native writers almost never use them.

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

### ⚠️ The Voice Policy Applies to Site METADATA Too (added 2026-07-29)

The voice rules are not limited to post and page bodies. They apply to **every string a reader can see**, including surfaces that are easy to forget because they are configured once and never revisited:

| Surface | Where | Checked? |
|---------|-------|----------|
| **Category / tag descriptions** | WP Admin → Posts → Categories (renders on archive pages) | ✅ Audited + rewritten 2026-07-29 |
| Menu item labels | Appearance → Menus | ⬜ Not yet audited |
| Widget titles and text | Appearance → Widgets / Bricks | ⬜ Not yet audited |
| Site tagline | Settings → General | ⬜ Not yet audited |
| Form labels, buttons, placeholders | Bricks form elements | ⬜ Not yet audited |
| Image alt text and captions | Media Library | ⬜ Not yet audited |
| Rank Math meta titles + descriptions | Per post | ✅ Set per post |

**Why this rule exists:** on 2026-07-29 the **AI Tools** category description was found live on the site reading *"…tools AI yang **korang** boleh guna hari ini — dari ChatGPT sampai ke automation."* It carried the banned pronoun **and** an em dash, and had been rendering on category archive pages unnoticed because voice checks were only ever run against post content. All four category descriptions were rewritten.

**Rule:** when auditing voice, do NOT stop at post bodies. Sweep the metadata surfaces above. Anything written once during setup is the most likely place for stale voice to survive.

### Red Flag Phrases — Always Rewrite These

**Salesy / Corporate red flags:**
- ❌ `"Privasi anda penting bagi kami"` → sounds like a copy-paste template
- ❌ `"Anda berhak untuk"` → translated legalese
- ❌ `"Kami sentiasa terbuka"` → press release language
- ❌ `"Kunjungi link external pada risiko anda sendiri"` → sounds threatening
- ❌ `"Untuk pertanyaan umum, kerjasama, atau sokongan"` → call center language
- ❌ Any sentence that starts with `"Maklumat di blog ini adalah untuk tujuan..."` → textbook opening

**Casual slang red flags (do NOT use):**
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

### 🚫 Anti-Salesy Copy Policy (added 2026-07-10)

**Rule:** DigiTrust Lab copy must never sound like a sales pitch. We lead with usefulness, not with money promises.

**The specific trigger:** Any phrase that implies "use this → make money" in a direct, pushy way is banned from UI copy — buttons, sidebar widgets, CTA boxes, opt-in forms, hero text, anywhere.

**Banned patterns in UI copy:**

| ❌ Salesy | ✅ Replace with |
|---|---|
| `jana duit` / `jana pendapatan` / `menjana pendapatan` | NEVER use anywhere — not in UI copy, not in blog post titles, not in hero headlines |
| `buat duit` / `dapatkan duit` / `buat duit mudah` | NEVER use anywhere — replaced with tool-focused language |
| `untuk perniagaan anda` / `untuk bisnes anda` | NEVER use — positions as business guru without results |
| `tingkatkan jualan` | Only in blog post body when discussing real results, not in opt-in or CTA buttons |
| `jual digital products` / `mula jual di Etsy` | Avoid in titles — focus on the skill, not the selling |
| Stacking benefit claims: `jimat masa, jana duit, kurangkan kerja` | Pick one — the strongest and most specific one |

**Why:** The user has not yet achieved business success (FB ads failure, no proven income). Teaching others to "make money" without results is inauthentic and damages credibility. The blog's purpose is to share genuine learning and tool expertise — not to promise income.

**Correct approach:** Focus on "here's how to use this tool well" — not "here's how to make money." Affiliate links are natural tool mentions, not sales pitches. Business/income posts ONLY when real results exist to share honestly.

### Content Authenticity Rules (added 2026-07-25)

**Core principle:** The blog is a practitioner sharing knowledge — not a business guru teaching success. Content must be authentic and educational first.

- NEVER use income claims in titles, body, or UI: "jana pendapatan", "buat duit", "untuk perniagaan anda", "menjana pendapatan", "buat duit mudah"
- NEVER position as business guru or success story — you're a practitioner sharing what you learn
- Focus on: "here's how to use this tool well" — not "here's how to make money"
- Affiliate links are natural tool mentions, not sales pitches
- Business/income posts ONLY when you have real results to share honestly
- Prompt gallery posts: show the prompt + the result + the tool used. No income promises.
- Content categories: AI Tools, Canva & Design, Prompt Engineering, Digital Skills (NOT Digital Side Hustle or AI untuk Perniagaan — those are deleted)

**Approved sidebar/CTA copy pattern (reference):**
```
Title:   Dapatkan Panduan Percuma
Body:    50 Prompt AI yang anda boleh guna terus untuk membuat kerja dan menjimatkan masa.
Sub:     Percuma sepenuhnya. Unsubscribe bila-bila masa.
Button:  Hantar →
```

### Green Light Patterns — Use These

Natural formal–semi-formal BM examples that hit the right tone — polished, professional, and accessible:

- ✅ `"Kami tahu halaman ini biasanya membosankan, tetapi kami akan menerangkan dengan cara yang mudah difahami."`
- ✅ `"Kami tidak menjual data sesiapa kepada sesiapa."` — direct, reassuring
- ✅ `"Itu janji kami."` — personal, accountable
- ✅ `"Biasanya dalam masa 48 jam pada hari bekerja."` — plain, no jargon
- ✅ `"Jika anda ingin mengetahui tentang...anda berada di tempat yang betul."` — warm, inclusive
- ✅ `"Pernahkah anda tertanya-tanya bagaimana AI berfungsi di sebalik skrin?"` — engaging question hook

### Natural Malay Flow Patterns

AI-generated Malay has predictable awkwardness — half-casual/half-formal mixing, over-translated English terms, unfinished sentences, textbook intros. The full fix guide with before/after tables lives in:

**📖 `.devin/skills/malay-voice-guide/SKILL.md`** — Load this skill before writing or reviewing any Malay content.

Quick summary of the 14 sections (natural formal–semi-formal BM standard):
1. **Natural Formal–Semi-Formal BM Standard** — contextual register, read-aloud test, and reference sites (PandaiTech.my, Ecentral.my, DBP)
2. **Pronoun & Address** — `anda` not `korang`, `kami` for company voice, `beliau` for professionals
3. **Full Forms vs Contractions** — `tidak` not `tak`, `sudah` not `dah`, `apabila` not `bila`
4. **Code-Switching Rules** — Tech terms stay English (AI, tools, API). Common nouns use BM. No slang. English retention for awkward BM translations (`copy & paste`, `drag & drop`, `brainstorm`, `feedback`, `deadline`). English terms italicized in BM sentences (except brand names, acronyms, and absorbed loan words).
5. **"Malaysia" Usage — CRITICAL** — Do NOT explicitly mention "Malaysia", "rakyat Malaysia", or "warga Malaysia" in titles, content, or meta unless contextually necessary (e.g., geographic facts, comparing Malaysian vs international context, or keyword target literally includes "Malaysia"). The .my domain, Malay language, and local context already signal the audience. Repeatedly saying "Malaysia" sounds bombastic and like SEO padding. If removing "Malaysia" doesn't change the meaning, remove it.
6. **Sentence Structure** — Complete every thought with concrete examples
7. **Opening Lines** — Hook with question/scenario in proper BM, no textbook intros
8. **Transitions** — `Selain itu`, `Walau bagaimanapun`, `Oleh itu` (formal); `Jadi`, `Tetapi` (conversational OK)
9. **Emphasis** — `sangat`, `amat`, `penting`, `pasti`, `terbukti` (not `confirm`, `gila`, `wajib` as slang)
10. **Humour** — Light wit in proper BM, no slang-based humour
11. **Punctuation** — Em dash max 1 per post, avoid AI punctuation patterns. **Blockquote** (`<blockquote>`) for all notes, heads-up, callouts, and closing sign-offs. **Always match the brand blockquote style exactly:** orange left border `#e8621a`, light peach background `#fff8f5`, italic, Plus Jakarta Sans font, 14px font-size, `#3a3a3a` text color, `0 6px 6px 0` border-radius. For Bricks pages, add this CSS to the container element's `_cssCustom`.
12. **Red Flag Phrases** — Salesy/corporate + casual slang red flags with replacements
13. **Green Light Patterns** — Natural formal–semi-formal examples in the PandaiTech.my and Ecentral.my style
14. **DBP Reference** — `ialah` vs `adalah`, `ia` not `ianya`, `dalam kalangan`, `daripada` vs `dari`

### Page-Specific Voice Notes

**Tentang Kami:** Personal founder story tone. "Kami" = Zed + AI partner. Natural formal–semi-formal BM with flowing paragraphs and personality. Use `beliau` for professional references.

**Polisi Privasi / Disclaimer:** Clear and accurate, written in plain formal–semi-formal BM. Add a human touch — acknowledge these pages are normally boring. Keep legal meaning, strip bureaucratic and corporate language.

**Hubungi Kami:** Friendly invitation in natural formal–semi-formal BM, not a corporate FAQ. Feels like you're genuinely happy to hear from readers.

**Blog posts:** Natural formal–semi-formal BM, first-person, experience-led. Use polished formal constructions when they read naturally aloud; use semi-formal warmth for accessibility. Opener should hook emotionally or with a relatable scenario. Never start with a definition or statistics dump.

### Malay Proofreading Workflow (updated 2026-07-17)

No dedicated Malay proofreading tool is used. DewanEja 11 was evaluated but not purchased. LanguageTool browser extension is paywalled. ProWritingAid is English-only. The workflow is:

1. **Writer drafts** in WordPress editor (or anywhere)
2. **Before publishing** — paste the full draft here and say "proofread this"
3. **AI checks against** `malay-voice-guide/SKILL.md`: spelling, grammar, contextual formal–semi-formal register, read-aloud flow, word choice, English term retention, italic policy, blockquote style, DBP rules, **brand name capitalization**, **"Jika" not "Kalau"**
4. **Apply fixes** — writer applies suggested corrections
5. **Rank Math SEO checklist** (before clicking Publish):
   - [ ] Focus keyword set
   - [ ] SEO title and meta description written
   - [ ] **Pillar Content checkbox** — enable if this post is a foundational/broad topic that other posts will link back to (e.g. "Apa Itu AI?" = pillar; "Cara Guna ChatGPT untuk Saham" = spoke, not pillar)
   - [ ] Schema type set to `Article` (or `BlogPosting`)
   - [ ] Featured image set (required for schema)
   - [ ] **Click WordPress Save/Update button** after ANY block editor change (Rank Math, Schema Builder, meta boxes) — modal-level saves are NOT enough
6. **Publish**
7. **Rank Math sidebar optimization (MANDATORY — Phase 5.5 of write-post workflow):**
   - [ ] Open Rank Math sidebar in WP editor, check score (aim 80+)
   - [ ] **Title Readability:** SEO title has power word (English: Ultimate, Proven, Essential) + sentiment word (English: Best, Amazing, Powerful) + number (year counts). Malay words NOT recognized by Rank Math.
   - [ ] **Additional — Keyword density:** 0.5%–2.5%. Add focus keyword naturally in intro, transitions, FAQ if too low.
   - [ ] **Additional — Dofollow link:** At least 1 external link must be dofollow. If Rank Math auto-nofollows, add domain to Settings → Links → Nofollow Exclude Domains.
   - [ ] **Content Readability:** ToC plugin active (Easy Table of Contents), proper heading hierarchy H2→H3→H4.
   - [ ] Record final score in `content-calendar.md`
8. **Rank tracking (MANDATORY — Phase 7 of write-post workflow):**
   - [ ] ClickRank → AI Overview Tracker → Add focus keyword + URL (Malaysia, Malay)
   - [ ] Screpy → Rank Tracker → Add focus keyword + URL (Malaysia, desktop+mobile)
   - [ ] Both tools are required — ClickRank = AI Overview/AEO tracking, Screpy = traditional SERP rank tracking
   - [ ] **ClickRank title/meta optimization is OPTIONAL** — see ClickRank Usage Policy below

### ClickRank Usage Policy (updated 2026-07-24)

**Primary purpose for DigiTrust Lab:** AI Overview Rank Tracker — tracks whether our content appears in Google's AI-generated answers. This is the main reason we use ClickRank.

**Secondary features (use with caution):**

| Feature | Use? | Policy |
|---|---|---|
| **AI Overview Tracker** | ✅ Always | Add every published post's focus keyword + URL (Malaysia, Malay) |
| **Title optimization** | ⚠️ Optional | AI suggestions tend to be over-dramatic. Review carefully — reject hype words like "Ultimate", "Game-Changing", "Secret". Only accept if natural and matches our calm, helpful Malay voice. Manual titles are always preferred. |
| **Meta description optimization** | ⚠️ Optional | Same policy as titles — review for hype, edit to match voice, reject overly dramatic wording |
| **Smart Internal Links** | ⚠️ Review | Suggestions are usually safe (based on existing content text). Review anchor text naturalness before approving. |
| **Image Alt Text** | ❌ Skip | We manage alt text manually in Malay via Respira MCP |
| **Schema Markup** | ❌ Skip | Rank Math already handles schema |
| **AI Model Compatibility** | 🟢 Optional | Can run occasionally to check if AI models parse our pages correctly |

**Voice standard for ClickRank suggestions:**
- Reject words: Ultimate, Proven, Secret, Game-Changing, Revolutionary, Shocking, Mind-Blowing
- Accept words: Panduan, Tips, Cara, Mudah, Praktikal, Lengkap, Bermula
- If a suggestion feels "boombastic" or unnatural in Malay context → reject it
- Manual editing after accepting is always allowed
- When in doubt → ask the user before applying any ClickRank suggestion

**Full workflow:** See `.devin/skills/write-post/SKILL.md` for the complete step-by-step process including Phase 6.5 (Rank Math + Malay voice gate) and Phase 7 (ClickRank/Screpy).

Optional: Claude Desktop can provide a second opinion with a fresh perspective.

### Core Pages — Voice Standard (updated 2026-07-17)

All core pages are being re-rewritten in natural formal–semi-formal BM (previous 2026-07-06 casual rewrites are SUPERSEDED). This contextual register standard applies to all content: posts, pages, templates, email copy, everything.
- Tentang Kami — re-rewrite in natural formal–semi-formal BM
- Polisi Privasi — re-rewrite in natural formal–semi-formal BM
- Disclaimer — re-rewrite in natural formal–semi-formal BM
- Hubungi Kami — re-rewrite in natural formal–semi-formal BM

## Quick Reference

| File | Purpose |
|------|---------|
| `BRICKS-BUILDER-GUIDE.md` | Bricks element reference — read BEFORE editing Bricks elements (tool names are old Bricks MCP, use Respira equivalents) |
| `DESIGN.md` | Design system source of truth (colors, typography, components) |

### Page Editing Guidelines

| Page / Content | Content stored in | Edit via |
|---|---|---|
| Home (ID 280) | Bricks `_bricks_data` | Bricks only |
| Tentang Kami (ID 72) | Bricks `_bricks_data` | Bricks only |
| Disclaimer (ID 74) | Gutenberg `post_content` | WP native (easier) |
| Hubungi Kami (ID 75) | Gutenberg `post_content` | WP native (easier) |
| Privasi (ID 73) | Gutenberg `post_content` | WP native (easier) |
| Blog posts (body text) | Gutenberg `post_content` | WP native (easier) |
| Blog post template (sidebar, meta, layout) | Bricks template ID 10 | Bricks only |

**Rules:**
- New simple text pages → WP native Gutenberg (consistent with Disclaimer/Hubungi/Privasi)
- New pages needing custom layout → Bricks
- When pasting text into Bricks editor → always `Ctrl+Shift+V` (plain text, no rogue CSS classes)
- `respira_update_page` with `content` = writes to WP `post_content` only — useless for Bricks pages
- `respira_find_element` + `respira_update_element` = correct way to edit Bricks page content via MCP

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
| "keyword research", "find keywords", "writerzen", "seed keyword", "kd analysis", "golden filter", "keyword clustering", "topic discovery", "content brief", "keyword planner", "domain filter", "domain authority", "outline building", "SERP analysis" | `.devin/skills/writerzen-keyword-research/SKILL.md` | Full WriterZen research pipeline: Topic Discovery → Keyword Explorer → Keyword Planner → Content Brief → Outline → Writing. Deep on research, light on AI writing. 29 source files in `content/writerzen-guide/` |

### Marketing Skills (on-demand only)

For broader marketing strategy (competitor teardown, E2E SEO, ICP research, content repurposing, email sequences, programmatic SEO, UTM tracking), read `.devin/skills/marketing-skills-index/SKILL.md` when explicitly asked. These are not auto-triggered — Claude handles generic marketing tasks natively.

### How to Use (For Claude Desktop)

1. Match the user's request against trigger phrases in the tables above
2. Read the full `SKILL.md` file from the listed path
3. Follow the skill's workflow
4. Only load one skill at a time (the matching one)
5. Combine with Respira MCP tools when relevant (e.g., SEO strategy → then Respira on-page fixes)

## 🔍 WriterZen Research Pipeline (Option C — Standard)

**Before writing any blog post, load the `write-post` skill (`.devin/skills/write-post/SKILL.md`) for the full end-to-end pipeline.** Load the `writerzen-keyword-research` skill for keyword research, then follow the Option C workflow for content creation.

**Option C Pipeline:** Quota check → **Topic Discovery** → Keyword Explorer (**+ Golden Filter**) → Keyword List → Cluster into a NEW Planner project → **Verify Weak Spot ≥ 2** → Keyword Planner (Suggest Content Brief + manually adjust 6 fields) → Content Creator (outline → keywords → write) → publish via Respira MCP → Rank Math → rank tracking → internal linking → documentation

> **Never skip the Content Creator pipeline.** The outline must be generated through WriterZen's AI + competitor research, not manually planned.

> ### ⛔ Four research gates — never skip these (added 2026-07-29)
>
> These were previously absent from this summary, so agents (Devin included) jumped straight to Keyword Explorer and silently skipped the research front-half. All four are MANDATORY:
>
> 1. **Quota check** — WriterZen → Settings → Limits, BEFORE spending anything. Golden Filter costs 1 credit per keyword in the result set. **AI Words cap is 8,000/month (~8 AI-drafted posts)** — check the balance covers this post before choosing "Write all for me".
> 2. **Topic Discovery FIRST** — never start at Keyword Explorer with a guessed keyword. Seed the broad topic, find the winnable angle, then confirm or revise the planned title. **Titles in `content-calendar.md` are provisional until Topic Discovery validates them** — the keyword decides the title, not the reverse.
> 3. **Golden Filter** — apply in Keyword Explorer before clustering. Golden Score ≤10, All-in-Title ≤10, Volume ≥100 (volume may relax to 50 for Malay long-tail; **never relax the other two**). Then manually check the SERP for small Malaysian blogs ranking — metrics give numbers, the SERP gives reality.
> 4. **Weak Spot gate** — in Keyword Planner, click *Activate Metrics* and read Weak Spot. **≥ 2 required to proceed.** If 0–1, the top 10 is all high-authority: go back to Topic Discovery and pick another angle. Do not write it anyway.
>
> **Keyword Planner projects:** create a **NEW** project per post topic — WriterZen clustering is one-time and cannot append. Legacy project 178201 is NOT a reuse target. (The Keyword List "DigiTrust Lab Blog Posts" ID 68708 *is* reused — one permanent list for all posts.)

**Quick reference:**
- Tools: Topic Discovery, Keyword Explorer, Keyword Planner, Content Creator
- Location: Malaysia | Language: Malay
- Target: Golden Score < 10, KD < 20, All-in-Title < 10, Weak Spot ≥ 2
- Save to: WriterZen Keyword List → "DigiTrust Lab Blog Posts"
- Record metrics in: `content/content-calendar.md` (per-post entry)
- Image prompts: `content/image-prompts.md` (copy-paste Gemini prompts + filenames per post; update when publishing)
- Deep reference: 29 course files in `content/writerzen-guide/`
- **Content Creator project**: Always select existing "DigiTrust Lab" project (readonly dropdown — click to open, select from table). Never create new Content Creator projects.
- **Content Brief fields**: Fill ALL 6 fields (Content format, Writing Tone, Target Audience, Author perspective, Content Angle, Note for writer). Use Playwright `fill()` for text inputs — native JS setter doesn't trigger Vue reactivity on Audience/Perspective fields.
- **Content Creator toggles (SERP View / AI Assistant):** Leave both OFF. They currently add no useful UI. Generate/update the AI outline via the explicit "Set up & Start building outline" / "Generate outline" buttons instead.
- **Internal linking (required):** Plan links in outline phase → insert outbound links during publish → run `internal-link-builder` skill after publish to add inbound links from older posts
- **Content formatting (MANDATORY — NON-NEGOTIABLE):** Every article must be richly formatted — NO sea of text. Use blockquotes (orange `#E8621A` border, `#F5F3EE` bg), bullet/numbered lists with bold labels, before/after example blocks, "Elakkan" vs "Gunakan" contrast pairs, warning/tip boxes, `<em>` for English terms, short paragraphs (max 3-4 sentences). At least 2-3 blockquotes per instructional article. Reference standards: Post #2 and Post #3. See `.devin/skills/readability-pass/SKILL.md` for full toolkit, templates, and checklist.
- **Full workflow:** See `.devin/skills/write-post/SKILL.md` for the complete step-by-step process

## Notes

- This is a WordPress blog hosted on Hostinger, using Bricks Builder theme
- Live URL: `https://digitrustlab.com` (WordPress is served directly — no static export or build step)
- WP Admin URL: `https://digitrustlab.com/wp-admin/`
- Respira MCP: connected to Devin and Claude Desktop (replaced old Bricks MCP on 2026-07-05)
- Respira API key stored in Claude Desktop via `.mcpb` install and in Devin `mcp_config.json` (`$env:APPDATA\devin\mcp_config.json`, symlinked to Google Drive TSOT)
- Old Bricks MCP bridge (`bricks-mcp-bridge.mjs`) is decommissioned — do not use
- Template type filter: Use `type: "content"` (not `"single"`) for single post templates
- Previous architecture (Local WP + Simply Static + Cloudflare Pages) was fully decommissioned on 2026-07-12 — see `deprecated/` folder for archived documentation

---

## 📌 Doctrine Files — Agents Without an Import Mechanism MUST Read These

**Who this section is for:** any agent that reads `AGENTS.md` but has no
`@import` equivalent — **Codex**, ChatGPT, and any future tool. Claude Code
loads all of these automatically via `CLAUDE.local.md`; Devin auto-loads
`.devin/rules/` on trigger. Everyone else gets them **only by reading this
table**.

**Why this exists:** on 2026-07-31 a Codex session was audited and found to have
loaded `AGENTS.md` and nothing else — running without the verification protocol,
the Pieces LTM rule, and both lessons files, while Claude had all twelve. Nothing
errored. A missing rule is indistinguishable from a followed one unless something
checks.

### Tier 1 — read at session start, every session (~9 KB total)

These change baseline behaviour and are cheap to load. Read all five before your
first substantive action.

| File | What it governs |
|------|-----------------|
| `.windsurf/rules/verification-protocol.md` | **The Iron Law** — no completion claims without fresh evidence |
| `.devin/rules/bricks-mcp-absolute.md` | Enforcement detail for PRIORITY #1 above |
| `.windsurf/rules/pieces-ltm-integration.md` | Query Pieces LTM before answering anything about project history |
| `.windsurf/rules/context7-default.md` | Use Context7 for library/API docs by default |
| `.windsurf/rules/change-summary-rule.md` | Required output format after multi-file changes |

### Tier 2 — read when the trigger matches

| Trigger | File |
|---------|------|
| Editing any Bricks element | `.devin/rules/bricks-standard-guide.md` |
| Content planning, keywords, calendar | `.devin/rules/content-planning.md` |
| Visual verification of frontend changes | `.devin/rules/browser-preview.md` |
| Writing code (naming, structure, DRY) | `.windsurf/rules/coding-standards.md` |
| Session start, or stuck >10 min on a bug | `.windsurf/rules/self-improvement-loader.md` |

### Tier 3 — lessons (66 KB, read on trigger only, never wholesale)

Hard-won corrections from past sessions. **Do not read these at session start** —
they are large. Read the relevant one when: starting a debugging session, stuck
more than 10 minutes, or about to recommend a tool/provider/approach.

| File | Scope |
|------|-------|
| `~/.codeium/windsurf/agent-templates/tasks/lessons.md` | Global — 50 lessons across UI, deployment, debugging, git |
| `~/.codeium/windsurf/agent-templates/tasks/lessons-digitrustlab.md` | This project — WordPress, Bricks, Respira, WriterZen, Malay voice |

Both resolve through the `~/.codeium/windsurf/agent-templates` symlink to the
Google Drive TSOT. **The drive letter varies per device** (`E:` on one laptop,
`G:` on another) — never hardcode it; always go through the `~/.codeium/...`
path, which is drive-letter-free.

### Workflows — available to every agent, not just Claude

Claude Code exposes 31 reusable workflows as `/slash-commands` via
`~/.claude/commands/` (symlinked to the TSOT). **Agents without a slash-command
mechanism are not excluded** — those commands are plain markdown files. Read and
follow them directly:

```
~/.codeium/windsurf/agent-templates/global-workflows/<name>.md
```

Examples: `commit.md`, `validate-skills.md`, `sync-docs.md`, `status.md`,
`plan.md`, `pr.md`, `deploy.md`, `check-sync.md`. The instructions are identical
to what Claude receives — only the invocation shorthand differs. When the user
says "run /commit", read `global-workflows/commit.md` and follow it.

### Verify the chain

```bash
python scripts/verify-imports.py
```

Exit 0 = every import target and symlinked tree resolves. Run it at session
start, and after any symlink or `.gitignore` change.

> **Note on symlinks:** `.windsurf/rules` and `.windsurf/skills` are symlinks
> into the TSOT. On Windows a symlink reports size 0 — judge liveness by
> resolving the target and testing that path, never by file size.
