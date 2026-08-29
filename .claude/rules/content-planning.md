---
trigger: always_on
description: Manage content planning files — update content-calendar.md with keyword metrics, post status, and publishing plan. Cross-reference from SEO-CHEATSHEET, AGENTS.md, WriterZen research pipeline skill, and breadcrumbs.
---

> **Editorial relevance gate:** Before any Topic Discovery, Keyword Explorer,
> Golden Filter, Keyword Planner, quota/credit spend, permanent keyword-list
> addition, or drafting handoff, apply the single contract in
> `.claude/rules/editorial-relevance-gate.md`. Research and SEO must attest the
> proposed topic, approved pillar/category, reader problem, authenticity basis,
> inventory/cannibalization check, seed-to-topic semantic match, and the
> existing-cluster/link map: approved cluster or pillar, published parent/peer,
> plausible inbound source, incremental value, and planned anchor/context.
> Operations independently rechecks those fields and actual URLs before
> credit/project/list actions and before the drafting handoff. Content rejects
> missing or contradictory Research, SEO, or Operations attestations. Do not
> let metrics promote an irrelevant or orphan topic; record WriterZen metrics
> only after this gate passes.
>
> The record uses normalized `topic_family_id`, `approved_pillar_id`,
> `approved_cluster_id`, `topic_intent_id`, and `subject_entity_ids`, plus
> `declared_seed_intent`. Each department attestation
> must carry `decision`, `status`, `evidence_ref`, `checked_at`, and `owner`;
> Operations additionally carries independently current calendar, published
> structured URL arrays, and link-feasibility evidence. Canonical URL identity
> is exact after scheme/host case and trailing-slash normalization; a boolean
> recheck, free-text reference, or text-token overlap is insufficient.

# Content Planning Management

**Priority:** MEDIUM — Activates when discussing blog post planning, keyword research, content calendar, or publishing schedule.

## Core Principle

`content/content-calendar.md` is the **single source of truth** for per-post planning. All keyword metrics, post status, and publishing decisions live there.

## Key Rules

1. **Per-post metrics go in `content/content-calendar.md`** — NOT in `content/SEO-CHEATSHEET.md` (which is general reference only)
2. **Update calendar during discussions** — When discussing post ideas, keywords, or publishing plans, update the relevant post entry immediately
3. **Cross-reference everywhere** — Any file that mentions a specific post's keyword or status should point to `content/content-calendar.md` as the source
4. **Use the metrics table format** — Keep the established table structure (Keyword, Volume, KD scores, CPC, competitor, status)
5. **Update status lifecycle** — `PLANNED` → `PARKED KEYWORD` → `DRAFTING` → `PUBLISHED ✅`
6. **After publishing a post** — Update the calendar entry status to `PUBLISHED ✅` with URL and date

## Editorial relevance prerequisite

The calendar is the source of truth for inventory and approved topic family,
but it is not permission to spend research credits. Every proposed entry must
first have the relevance record and independent attestations required by
`.claude/rules/editorial-relevance-gate.md`. The current DigiTrust Lab topic
families are `AI Tools`, `Canva & Design`, `Prompt Engineering`, and
`Digital Skills`; a new subject or reader problem is a pivot until the user
approves it explicitly. The record must also show a non-orphan extension of an
existing cluster or pillar, a published parent/peer, a plausible inbound source
from an existing post, incremental reader value, and the planned anchor/context.

## Files to Keep in Sync

| File | What to update |
|------|---------------|
| `content/content-calendar.md` | Per-post metrics, status, title, category |
| `content/SEO-CHEATSHEET.md` | General KD scales, volume benchmarks, research flow (no per-post data) |
| `AGENTS.md` | Reference path to `content/content-calendar.md` for post planning |
| `ROADMAP.md` | Milestone updates when posts are published |
| `NEXT.md` | Current task references to content calendar |
| `.claude/skills/writerzen-keyword-research/SKILL.md` | Full WriterZen research pipeline (Topic Discovery → Keyword Explorer → Keyword Planner → Content Brief → Outline). 29 source files in `content/writerzen-guide/`. Point to `content/content-calendar.md` for recording metrics |

## When This Rule Activates

- User discusses post ideas or what to write next
- Keyword research is completed for a new post
- A post is published or status changes
- User asks about content planning or publishing schedule
- WriterZen research pipeline session completes (Topic Discovery → Keyword Explorer → Keyword Planner → Content Brief → Outline)
- User mentions any WriterZen tool: Topic Discovery, Keyword Explorer, Golden Filter, Keyword Planner, Domain Filter, Domain Authority, Content Brief
