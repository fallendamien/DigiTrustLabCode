# Content workflow

## Bounded specialist loop

1. Confirm the content outcome, audience, format, and current source of truth.
2. Select one canonical skill from `skills/README.md` and read it in full.
3. Produce the bounded artifact: brief, outline, draft, edit report, or publishing checklist.
4. Stop at the department boundary when the task requires SEO validation, live-site operations, or new research; create a handoff instead of improvising.

## MCP boundary

Use Respira MCP for WordPress reads/writes only when the task requires live-site
data or an authorized content change. Follow the project Bricks/Respira rules,
including read-first, builder-native operations, duplicate/snapshot safeguards,
and no raw HTML. Research and SEO tools belong to their departments.

## Verification gate

Before handoff or completion, verify the requested artifact against the
canonical skill, `.claude/rules/content-planning.md` where applicable, the
Malay voice requirements, and the relevant source-of-truth files. For a
publishing workflow, run `python scripts/verify-imports.py` and
`python scripts/verify-content-status.py` at the documented gate.

## Codex handoff

Provide: objective, source files, artifact produced, evidence/commands run,
open judgment calls, and the exact next action requested from Codex. Codex
returns validation findings and does not silently publish or broaden scope.
