---
trigger: always_on
---

# Bricks Template Backup Rule

**Priority:** High  
**Scope:** Workspace-level (DigiTrust Lab only)

## Rule

Always export Bricks templates as JSON backups before and after major template editing sessions.

## Auto-Trigger Conditions

Backup templates when ANY of these occur:

| Trigger | When | Action |
|---------|------|--------|
| Before AI/MCP template editing | User asks to modify header/footer/layout | Run `/backup-bricks-templates` first |
| After successful template restructure | Major layout or element changes complete | Run `/backup-bricks-templates` with incremented version |
| Monthly routine | 1st of each month | Run `/backup-bricks-templates` for all 4 templates |
| Pre-deploy | Before Simply Static export | Run `/backup-bricks-templates` as checkpoint |

## Templates Covered

| Template | ID | File Pattern |
|----------|----|-------------|
| Header | 21 | `bricks-exports/header-v{N}.json` |
| Footer | 46 | `bricks-exports/footer-v{N}.json` |
| Single Post | 10 | `bricks-exports/single-post-v{N}.json` |
| Blog Archive | 52 | `bricks-exports/blog-archive-v{N}.json` |

## Version Rules

- Always increment version number — never overwrite
- Keep last 3 versions, archive older to `bricks-exports/archive/`
- Every backup must be git committed

## Workflow Reference

See `.devin/workflows/backup-bricks-templates.md` for detailed steps.

## Skill Activation

When this rule triggers, auto-load:

| Skill | Path | Purpose |
|-------|------|---------|
| `bricks-backup` | `.devin/skills/bricks-backup/SKILL.md` | Export, version, and commit Bricks template backups |

## Forbidden

- Do NOT backup during Simply Static export (template may be mid-edit)
- Do NOT skip git commit after export
- Do NOT overwrite existing versions
- Do NOT backup templates not listed above unless explicitly requested
