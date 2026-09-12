# Operations workflow

## Specialist playbook loop

Run this loop directly for safe, narrow fast-lane operations. For guarded work,
add the route receipt, required approval, bounded-worker scope, and independent
evidence at the orchestration boundary.

1. Establish the change boundary, rollback path, affected systems, and approval state.
2. Independently apply `.claude/rules/editorial-relevance-gate.md` before any
   WriterZen credit, project, or permanent keyword-list action and again before
   a drafting handoff. Verify the approved pillar/category, reader problem,
   authenticity evidence, calendar/published inventory and cannibalization,
   and seed-to-topic semantic fidelity. Independently verify the named
   existing cluster/pillar, current published parent/peer URL, plausible
   inbound source from an existing post, incremental reader value, and planned
   anchor/context; do not trust an upstream attestation without checking its
   evidence. An orphan, mismatch, or unapproved pivot is blocked.
   For WriterZen Create Article, also apply
   `.claude/rules/writerzen-ai-credit-gate.md`: immediately before submission,
   Operations must attest from a fresh snapshot that title/description/outline
   is ON, whole article is OFF, and optional keyword suggestions are OFF unless
   documented insufficiency, explicit user credit authorization, current cost
   evidence, and the same fresh snapshot justify `AUTHORIZED_ON`. Unknown or
   conflicting toggle state is a hard stop. Do not claim a credit amount for
   keyword suggestions unless the current product UI displays it.
   Before the native-draft handoff, independently verify from a fresh
   WriterZen Content Writing snapshot that **Copy to editor** has populated the
   main editor with the generated title, description, and full ordered outline,
   and that word and heading counters are non-zero. Verify the recorded report
   ID and an outline-to-draft map covering every WriterZen heading and bullet.
   The map must distinguish genuine WriterZen H3 nodes from supporting bullets.
   Preserve every genuine H3 as a visible H3 under its source H2 by default;
   accept an H3-to-prose, H3-to-list, or H3-to-other-heading conversion only
   when the map names the editorial reason and the final heading tree proves
   the conversion. Supporting bullets may be expanded or promoted to H3, but
   their source and final levels must be recorded separately.
   Attest `WRITERZEN_OUTLINE_HANDOFF: PASS` only when every item is preserved,
   merged, reordered, expanded, or explicitly justified as omitted. A
   side-panel-only outline, unexplained omission, or silently replaced heading
   tree blocks the handoff.
   For native-draft handoffs, also apply
   `.claude/rules/native-originality-source-gate.md` and attest that no
   WriterZen plagiarism action, requirement, or credit spend occurred. Any
   external checker requires explicit user authorization recorded before cost
   or submission.
   Before any Google Search Console indexing request, independently inspect the
   exact live URL, click **Test Live URL**, and wait for the completed live-test
   result. Record whether Google fetched the page and whether it is eligible for
   indexing. Click **Request Indexing** only after a successful/eligible test
   when the URL is not already indexed and no unchanged-content request has
   already been accepted. A 5xx/server error, failed fetch, timeout,
   authentication/quota issue, or other non-eligible result blocks the request;
   record the failure, timestamp, and follow-up instead.
3. Select one canonical operations skill and read it in full.
4. Execute only the requested bounded change or produce a runbook/checklist.
5. Verify immediately, document evidence, and stop when the next action belongs to another department.

## Delegation decision

An explicitly marked `bounded-worker` brief executes directly within its scope;
nested delegation is prohibited. In the guarded lane, delegate external,
destructive, irreversible, high-risk, approval-gated, or broad/
independently review-worthy work. Safe narrow local inspection, reversible
edits, focused tests, and ordinary implementation belong in the fast lane. If
guarded dispatch fails, the work stops; fast-lane execution cannot claim worker
validation.

## MCP boundary

Use only the MCP server appropriate to the requested system. For WordPress and
Bricks, Respira is primary and builder-native; never use the decommissioned
Bricks MCP or raw post-processing. External actions remain approval-gated.

## Verification gate

Run `python scripts/verify-imports.py` after doctrine/import/symlink-related
work. Run `python scripts/verify-content-status.py` for live content-status
work, or `--offline` when the task explicitly requires offline verification.
Capture exit codes and summarize failures before handoff.

## Image replacement handoff

For a Creative request to `fix this image`, `audit this image`, or `reupload
the corrected image`, use the existing authenticated Chrome session and the
current attachment ID. In WordPress, open **Media → Edit Media → Replace
Media → Upload a new file**, then use the in-place replacement workflow with
**Just replace the file** and **Keep the date** selected. Preserve the
attachment ID, filename, source URL, title, description, caption, and alt
text. Never create a `-1`, `-2`, or otherwise numbered duplicate when URL
continuity is requested.

After the upload, purge the site image/page cache, then verify all of the
following from fresh reads: the attachment ID and metadata are unchanged, the
original `.png` URL returns the corrected image, the LiteSpeed `.webp`
derivative loads, and the live post renders the corrected asset. If the
authenticated browser cannot attach the file, stop at the handoff page and
ask the user to select the archived file manually. Do not claim completion and
do not fall back to a new media upload.

## Codex handoff

Provide: change scope, files/systems touched, commands and exit codes,
rollback/restore handle, residual risk, the exact validation or approval needed
next, and `OPERATIONS_RELEVANCE: PASS|FAIL|PENDING` with the independently
verified relevance fields, current URLs, existing cluster/pillar, published
parent/peer, inbound source, incremental value, and anchor/context. Codex may
reject a handoff with missing evidence.

The Operations schema must carry the normalized `topic_family_id`,
`approved_pillar_id`, `approved_cluster_id`, `topic_intent_id`,
`subject_entity_ids`, and `declared_seed_intent`, plus
Operations `decision`, `status`, `evidence_ref`, `checked_at`, and `owner`.
It must also carry independently verified `calendar_ref`/status and structured
`calendar_urls`, `published_parent_or_peer_urls`/status,
`inbound_source_urls`/status, and `link_feasibility_urls` plus
`link_feasibility_ref`/status. A boolean recheck flag or free-text URL
reference is not evidence. Canonicalize scheme/host case and trailing slash,
strip fragments, then compare exact URL identity. A PASS status attached to a
different URL fails closed.
