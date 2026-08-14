---
name: marketing-skills-index
description: Routing table for marketing skills — email sequences, ICP research, SEO audits, competitor analysis, UTM tracking. Triggers on marketing/SEO/content strategy requests.
---

# Marketing Skills Index (Pruned for DigiTrust Lab)

> **Purpose:** Lightweight routing table. When a user request matches a trigger below, read the corresponding skill file before executing.

## How to Use

1. Match the user's request against the trigger phrases below
2. Read the full SKILL.md from the listed file path
3. Follow the skill's process/workflow
4. Only load one skill at a time (the matching one)

## Skills Available

### Migrated to `.claude/skills/` (local, fast)

| Trigger Phrases | Skill | Path |
|----------------|-------|------|
| "full seo audit", "end to end seo", "seo strategy", "content gap analysis" | E2E SEO Assistant | `.claude/skills/e2e-seo-assistant/SKILL.md` |
| "email sequence", "nurture sequence", "welcome email flow", "email campaign" | Email Sequence Writer | `.claude/skills/email-sequence-writer/SKILL.md` |
| "programmatic seo", "scale content with templates", "bulk seo pages" | Programmatic SEO Builder | `.claude/skills/programmatic-seo-builder/SKILL.md` |

### TSOT-only (shared via `.windsurf/skills/` symlink)

| Trigger Phrases | Skill | Path |
|----------------|-------|------|
| "repurpose blog post", "atomize content", "content derivatives" | Content Repurposer | `.windsurf/skills/content-repurposer/SKILL.md` |
| "research ideal customer", "buyer persona", "icp research" | ICP Research Assistant | `.windsurf/skills/icp-research-assistant/SKILL.md` |
| "generate utm links", "utm builder", "conversion tracking" | UTM Tracking Generator | `.windsurf/skills/utm-tracking-generator/SKILL.md` |
| "analyze competitor", "competitor teardown", "positioning analysis" | Competitor Teardown | `.windsurf/skills/competitor-teardown/SKILL.md` |

## How These Complement Respira Skills

| Marketing Skill | Respira Skill | Relationship |
|----------------|---------------|--------------|
| E2E SEO Assistant | SEO & AEO Amplifier | Marketing = broader strategy (backlinks, gaps); Respira = on-page fixes + schema |
| Competitor Teardown | Conversion Audit | Marketing = competitor positioning; Respira = own-site CRO |
| ICP Research Assistant | Brand Voice Synthesizer | Marketing = who you're targeting; Respira = how you sound |
| Content Repurposer | Activity Report Composer | Marketing = create derivatives; Respira = report what was done |
| Programmatic SEO Builder | Internal Link Builder | Marketing = template structure; Respira = link existing content |
| Email Sequence Writer | — | No Respira equivalent |
| UTM Tracking Generator | — | No Respira equivalent |

## Rules

- **Read before executing:** Always read the full SKILL.md before following its workflow
- **One skill per request:** Don't load multiple skills simultaneously
- **Combine with Respira when relevant:** E.g., run E2E SEO Assistant for strategy, then Respira SEO Amplifier for on-page fixes
