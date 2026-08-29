# Content workflow

## Bounded specialist loop

1. Confirm the content outcome, audience, format, and current source of truth.
2. Before accepting a brief, outline, draft, or drafting handoff, require a
   frozen candidate record plus valid `RESEARCH_RELEVANCE: PASS`,
   `SEO_RELEVANCE: PASS`, and `OPERATIONS_RELEVANCE: PASS` attestations under
   `.claude/rules/editorial-relevance-gate.md`. The handoff must carry the
   existing-cluster/link map, and Content must carry its parent/peer, inbound
   source, incremental value, and anchor/context into the outline. Reject
   missing, stale, contradictory, or orphan fields; Content must not infer
   relevance from metrics or repair an unapproved pivot while drafting.
3. Select one canonical skill from `skills/README.md` and read it in full.
4. Produce the bounded artifact: brief, outline, draft, edit report, or publishing checklist.
5. Stop at the department boundary when the task requires SEO validation, live-site operations, or new research; create a handoff instead of improvising.

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
open judgment calls, the exact next action requested from Codex, and all three
relevance attestations. Codex returns validation findings and does not silently
publish or broaden scope.

Content accepts only a frozen handoff containing the normalized
`topic_family_id`, `approved_pillar_id`, `approved_cluster_id`,
`topic_intent_id`, `subject_entity_ids`, and `declared_seed_intent`, with separate Research, SEO, and Operations records
that each have `decision`, `status`, `evidence_ref`, `checked_at`, and `owner`.
Operations must additionally include current calendar, published-URL, and
link-feasibility evidence. Any missing, stale, contradictory, or non-PASS
record is a hard rejection.
Content also verifies that the proposed topic, reader problem, seed intent, and
incremental value match the registered family concepts, and that the link-map
URLs carried into the outline are exactly the Operations-verified canonical URL
arrays. Text-token overlap cannot substitute for the structured entity/intent
allowlist.
