# SEO workflow

## Bounded specialist loop

1. Define the URL/site surface, target query or business outcome, and evidence required.
2. Before metric work, independently re-check the Research relevance record
   using `.claude/rules/editorial-relevance-gate.md`: approved pillar/category,
   actual reader problem, authenticity basis, calendar/published inventory and
   cannibalization, and seed-to-topic semantic fidelity. Validate the named
   existing cluster/pillar, published parent/peer, plausible inbound source,
   incremental reader value, and planned anchor/context against search intent.
   Verify search intent rather than treating volume, KD, Golden Score, or Weak
   Spot as editorial proof. Reject a missing, stale, contradictory, or orphan
   record and stop an outside-family pivot without explicit user approval.
3. Select one canonical SEO skill and read it in full.
4. Produce an audit, prioritized opportunity list, content brief, or change proposal.
5. Stop before implementation when a live-site write, design change, or new research stream is needed; hand it off explicitly.

For WriterZen-related SEO handoffs, reference the canonical
`.claude/rules/writerzen-ai-credit-gate.md`. SEO may validate search intent and
the outline brief, but it must not authorize full-article generation. The
handoff must preserve outline-only ON, whole-article OFF, and the Operations
pre-Create attestation; native drafting and dual review remain Content's gate.

## MCP boundary

Use Respira MCP for WordPress/site evidence and authorized builder-native SEO
changes. Confirm the active site and use only documented tools from the
canonical skill. Screpy/rank-tracking evidence remains dashboard evidence and
must not be represented as verified by local scripts.

## Verification gate

Check search intent, source URLs, internal-link targets, metadata constraints,
and evidence timestamps. For repository changes, run
`python scripts/verify-imports.py`; for content-status-sensitive work, also run
`python scripts/verify-content-status.py` or `--offline` when explicitly
offline.

## Codex handoff

Provide: target surface, findings with evidence, prioritized fixes, items that
need user judgment, the proposed validation command, and the independent
relevance check. Explicitly attest `SEO_RELEVANCE: PASS|FAIL|PENDING` and carry
the proposed topic, approved pillar/category, reader problem, authenticity
basis, inventory/cannibalization check, seed-to-topic semantic match, pivot
status, Research evidence, existing cluster/pillar, published parent/peer,
plausible inbound source, incremental reader value, and planned anchor/context.
Codex validates mechanical correctness and scope; it does not turn
recommendations into live changes without authorization.

The SEO handoff schema must carry the normalized `topic_family_id`,
`approved_pillar_id`, `approved_cluster_id`, `topic_intent_id`,
`subject_entity_ids`, and `declared_seed_intent`, plus
SEO `decision`, `status`, `evidence_ref`, `checked_at`, and `owner`. These must
match the frozen candidate and Research record; missing, stale, contradictory,
or non-PASS values fail closed.
SEO must verify the registered positive/forbidden concepts for the proposed
topic and reader problem, and validate that the parent/peer and inbound-source
URLs in the link map are the same candidate-declared URLs, not merely valid
URLs for another topic. Operations must later receive structured URL arrays
for exact canonical identity.
