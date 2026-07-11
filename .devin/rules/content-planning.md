---
trigger: always_on
description: Manage content planning files — update content-calendar.md with keyword metrics, post status, and publishing plan. Cross-reference from SEO-CHEATSHEET, AGENTS.md, writerzen skill, and breadcrumbs.
---

# Content Planning Management

**Priority:** MEDIUM — Activates when discussing blog post planning, keyword research, content calendar, or publishing schedule.

## Core Principle

`content/content-calendar.md` is the **single source of truth** for per-post planning. All keyword metrics, post status, and publishing decisions live there.

## Key Rules

1. **Per-post metrics go in `content-calendar.md`** — NOT in `SEO-CHEATSHEET.md` (which is general reference only)
2. **Update calendar during discussions** — When discussing post ideas, keywords, or publishing plans, update the relevant post entry immediately
3. **Cross-reference everywhere** — Any file that mentions a specific post's keyword or status should point to `content/content-calendar.md` as the source
4. **Use the metrics table format** — Keep the established table structure (Keyword, Volume, KD scores, CPC, competitor, status)
5. **Update status lifecycle** — `PLANNED` → `PARKED KEYWORD` → `DRAFTING` → `PUBLISHED ✅`
6. **After publishing a post** — Update the calendar entry status to `PUBLISHED ✅` with URL and date

## Files to Keep in Sync

| File | What to update |
|------|---------------|
| `content/content-calendar.md` | Per-post metrics, status, title, category |
| `content/SEO-CHEATSHEET.md` | General KD scales, volume benchmarks, research flow (no per-post data) |
| `AGENTS.md` | Reference path to `content/content-calendar.md` for post planning |
| `ROADMAP.md` | Milestone updates when posts are published |
| `NEXT.md` | Current task references to content calendar |
| `.devin/skills/writerzen-keyword-research/SKILL.md` | Point to `content/content-calendar.md` for recording metrics |

## When This Rule Activates

- User discusses post ideas or what to write next
- Keyword research is completed for a new post
- A post is published or status changes
- User asks about content planning or publishing schedule
- WriterZen keyword research session completes
