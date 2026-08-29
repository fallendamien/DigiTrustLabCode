---
trigger: always_on
description: Fail-closed editorial relevance contract for DigiTrust Lab topic research and WriterZen credit actions.
---

# Editorial Relevance Gate

This is the single project-local contract for deciding whether a proposed
article may enter WriterZen research. It runs before Topic Discovery, Keyword
Explorer, Golden Filter, Keyword Planner, quota-consuming work, saved keyword
list additions, and any drafting handoff. Metrics can reject a relevant topic;
they can never make an irrelevant topic relevant.

## Required candidate record

Research must produce one record for the proposed article before spending a
WriterZen credit. The record must contain all of these fields, with evidence:

| Field | Pass requirement |
|---|---|
| Proposed topic and article subject | A concrete reader-facing subject, not just a keyword or tool name |
| Proposed seed | The seed expresses the same subject and search problem as the article |
| Approved pillar/category | Exactly one current DigiTrust Lab category: `AI Tools`, `Canva & Design`, `Prompt Engineering`, or `Digital Skills` |
| Normalized topic-family ID | An approved structured family ID, not a free-text similarity claim |
| Approved pillar/cluster IDs | The family registry's normalized pillar and existing-cluster IDs exactly match the candidate |
| Topic intent ID | An explicit registry intent ID allowed by that topic-family ID; do not infer intent with general NLP |
| Subject entity IDs | A non-empty subset of the selected family/cluster entity allowlist; unknown or off-family IDs fail unless the exact approved pivot authorizes the target family |
| Reader problem | A real task or question the intended reader is trying to solve, with registered positive concepts and no registered off-family concepts |
| Authenticity basis | Demonstrated tool/workflow use, or an explicitly planned first-hand test; never an invented personal result or experience claim |
| Inventory/cannibalization check | Compared against `content/content-calendar.md` and published inventory; distinct intent and role, or a documented non-cannibalizing reason |
| Seed-to-topic semantic match | The seed, proposed subject, reader problem, and category describe the same topic family |
| Existing-cluster/link map | Names the approved cluster or pillar this extends, at least one existing published parent/peer URL, one plausible inbound-link source from an existing post, the incremental reader value, and the planned anchor/context; every Operations evidence reference identifies the same URLs/IDs exactly |
| Pivot status | `none` when inside the approved family; otherwise the exact user approval must be recorded before any credit, project, list, or draft action |
| Evidence and owner | Source-of-truth paths, observed evidence versus inference, date, and accountable handoff owner |

An empty, contradictory, inferred-without-evidence, or stale field is a fail.
Attestations are fresh only when their ISO date is no more than 30 days old and
not in the future relative to the handoff date.
Do not fill a missing field with a WriterZen card, volume, CPC, Golden Score,
Weak Spot, or SERP result.

## Checkpoint order and attestations

1. **Research checkpoint (strong upstream gate):** classify the subject,
   category, reader problem, authenticity basis, inventory check, semantic
   match, and pivot status. Produce the existing-cluster/link map: the approved
   cluster or pillar being extended, a published parent/peer, a plausible
   inbound source from an existing post, incremental reader value, and the
   planned anchor/context. Attach the complete record to the research handoff.
   The handoff must carry a separate Research attestation with decision,
   status, evidence reference, checked-at date, owner, and the normalized
   family/pillar/cluster/seed-intent classification. It must explicitly attest
   `RESEARCH_RELEVANCE: PASS` or list every failed field. Do this before Topic
   Discovery or any other research credit.
2. **SEO checkpoint (strong upstream gate):** independently re-check the same
   fields, the proposed search intent, and cannibalization against the named
   cluster/parent/peer. Confirm that the link map is plausible for the actual
   published URLs. Do not trust a Research PASS without reading the evidence.
   Attach a separate SEO attestation with decision, status, evidence reference,
   checked-at date, owner, and matching normalized classifications. Attach
   `SEO_RELEVANCE: PASS` only when every field remains valid. Reject
   missing or contradictory attestations before metric work, including Golden
   Filter, Planner clustering, or Domain Authority.
3. **Operations checkpoint:** independently verify the same fields against the
   current calendar and published URLs, including that the named parent/peer
   exists, the proposed inbound source exists, and the anchor/context is
   feasible. The Operations record must name the current calendar evidence
   reference/status, structured calendar URL array, published parent/peer URL
   array and status, inbound-source URL array and status, link-feasibility URL
   array and evidence/status, checked-at date, and owner. Compare canonical
   parsed URLs exactly (scheme/host case and trailing slash normalized,
   fragments stripped). The arrays must identify the candidate's declared
   parent/peer and inbound-source URLs; valid statuses for different URLs
   still fail, and free-text references cannot establish identity.
   Attach a separate `OPERATIONS_RELEVANCE: PASS` attestation before any
   quota-consuming action, project creation, permanent keyword-list addition,
   or drafting handoff. A mismatch, missing evidence, orphan risk, or
   unapproved pivot stops the workflow.
4. **Content checkpoint:** Content may accept a brief, outline, or draft only
   when the frozen handoff includes valid Research, SEO, and Operations
   relevance attestations. Missing, stale, or contradictory attestations are a
   hard rejection, not a request to infer the missing work during drafting.

The three downstream attestations do not replace Research and SEO’s upstream
gates. They are independent checkpoints. No checkpoint may promote an
irrelevant candidate because its metrics look attractive.

### Structured attestation contract

Research, SEO, and Operations are three distinct records. Each must contain
`decision`, `status`, `evidence_ref`, `checked_at`, `owner`, `topic_family_id`,
`pillar_id`, `cluster_id`, `topic_intent_id`, and `subject_entity_ids`. Content rejects the handoff when
any record is missing, stale, non-PASS, decision/status contradictory, or
classified differently from the frozen candidate. Operations additionally
requires independently current calendar and published-URL/link-feasibility
evidence; a boolean such as `operations_recheck: true` is not sufficient.

The semantic check is an explicit registry check: normalized family, pillar,
cluster, topic-intent, and subject-entity IDs must be registered and mutually
consistent. Human-readable proposed topic, reader problem, seed, incremental
value, cluster map, and anchor/context are evidence that may reject registered
off-family concepts, but text or token overlap cannot grant relevance without
the structured allowlist. This is a deterministic classification control, not
a claim of general natural-language understanding. A volume, Golden Score, KD,
SERP result, or other metric cannot rescue a failed semantic, adjacency, or
attestation gate.

## Pivot and noisy-evidence rule

WriterZen cards, keyword variants, related searches, and adjacent SEO terms are
research evidence only. They do not silently redefine the approved topic. A
candidate that moves to another category, reader problem, or subject family is
a pivot and requires explicit user approval before any further credit, project,
keyword-list, or draft action. Record the approval text or a stable approval
reference in the candidate record.

## Concrete examples

| Scenario | Gate result | Reason |
|---|---|---|
| `Cara Buat Poster Guna ChatGPT`, as the documented future AI Tools leaf | **Pass** only when the record extends the existing AI Tools/Post #2 cluster, names published Post #2 as a parent, identifies Post #2 as a plausible inbound source, distinguishes the ChatGPT workflow from Canva-specific Post #5, and plans a descriptive anchor/context | It has an evidenced cluster path and incremental reader value; the example does not claim an unpublished link already exists |
| `ranking google` discovered while planning the Notion template article | **Fail**, even with volume 50, Golden Score 1.003, All-in-Title 0, or other positive metrics | It is a Google-ranking/SEO subject, not the approved Notion task-template problem, and has no defensible adjacency or internal-link path to the current AI/Canva/Prompt Engineering/Digital Skills clusters |
| `audit seo wordpress` proposed as a pivot from the Notion article | **Stop for explicit user approval** before any lookup or project/list action | It is an adjacent SEO/WordPress subject outside the approved Notion family; proximity is not permission |

The examples illustrate the general control. They do not whitelist or ban a
keyword family without a fresh candidate record.

## Handoff minimum

Every research-to-SEO handoff and SEO-to-content handoff must carry:

```text
proposed_topic:
approved_pillar_category:
target_reader_problem:
authenticity_basis:
inventory_cannibalization_check:
seed_topic_semantic_match:
topic_family_id:
approved_pillar_id:
approved_cluster_id:
topic_intent_id:
subject_entity_ids:
declared_seed_intent:
existing_cluster_or_pillar:
published_parent_or_peer_url:
plausible_inbound_source:
incremental_reader_value:
planned_anchor_and_context:
pivot_status_and_user_approval:
evidence_paths_and_date:
research_decision:
research_status:
research_evidence_ref:
research_checked_at:
research_owner:
seo_decision:
seo_status:
seo_evidence_ref:
seo_checked_at:
seo_owner:
operations_decision:
operations_status:
operations_evidence_ref:
operations_checked_at:
operations_owner:
operations_calendar_ref_and_status:
operations_published_parent_or_peer_url_and_status:
operations_inbound_source_url_and_status:
operations_link_feasibility_ref_and_status:
operations_calendar_urls:
operations_published_parent_peer_urls:
operations_inbound_source_urls:
operations_link_feasibility_urls:
RESEARCH_RELEVANCE: PASS|FAIL|PENDING
SEO_RELEVANCE: PASS|FAIL|PENDING
OPERATIONS_RELEVANCE: PASS|FAIL|PENDING
```

`PENDING` is not permission to proceed. Any `FAIL`, missing field, mismatch,
or unapproved pivot is fail-closed. A candidate that would be an orphan, create
a brand-new cluster without explicit approval, or rely only on generic category
similarity fails even when its search metrics are attractive.
