---
trigger: always_on
description: Fail-closed WriterZen AI-credit and article-generation gate for DigiTrust Lab.
---

# WriterZen AI-Credit Gate

This is the single project-local control for the WriterZen **Create Article**
modal and the handoff into native drafting. It protects the monthly AI-credit
budget and does not replace the editorial-relevance gate in
`.claude/rules/editorial-relevance-gate.md`.

## Non-negotiable generation mode

Before any Create Article submission, the current authenticated WriterZen UI
must visibly prove all of the following in a fresh snapshot:

| Control | Required state | Reason |
|---|---:|---|
| `Write article title, description & outline` | **ON** | WriterZen supplies the competitor-backed planning artifact |
| `Write the whole article` | **OFF** | WriterZen must not consume the article's AI-writing budget |
| `Use WriterZen to suggest more keywords` | **OFF** when the validated list/cluster is adequate | Existing validated keywords are sufficient; do not spend optional credits |

The whole-article control is prohibited for every DigiTrust Lab article
mission. Unused credits, convenience, deadlines, or a tempting UI default are
not exceptions. Unknown, missing, stale, or conflicting checkbox state fails
closed; never infer the state from the Create button, a previous screenshot, or
the selected seed keyword.

The same snapshot must record the current AI-credit status. If the outline-only
request reports insufficient credits, the workflow is `BLOCKED`: do not click
Upgrade, change plans, enable full-article generation, or attempt a bypass.
Unknown credit status, or unknown Upgrade/bypass status, also fails closed.

Operations must independently re-check the three controls immediately before
Create and attest to the exact fresh evidence. Content rejects any handoff
without that attestation. The attestation must identify the same evidence
reference as the current UI snapshot, not merely say that a re-check happened.

## Optional keyword suggestions

The keyword-suggestion control is separate from Google NLP. Do not enable it
when a validated Keyword List/Planner cluster already supplies adequate
keywords. If the validated set is insufficient, the control may be enabled
only after all of these are recorded:

1. the insufficiency and the missing intent/coverage are documented;
2. the user explicitly authorizes the additional credit spend;
3. the current UI shows the control ON and any displayed cost/confirmation is
   recorded; and
4. Operations attests to the fresh state immediately before Create.

This rule does **not** assert a credit amount for keyword suggestions. Record
the product's current displayed cost when it is shown; otherwise treat the
cost as unknown and block the optional spend. Google NLP remains off for Malay
content and is not a substitute for keyword research.

## Credit exhaustion and native drafting

If the outline-only request cannot run because AI credits are insufficient,
stop and record `BLOCKED`. Do not click Upgrade, change plans, enable whole
article, bypass the UI, or spend account funds without explicit user
authorization. A failed outline request is not permission to improvise a
WriterZen full draft.

WriterZen's permitted output for this workflow is the title, description, and
competitor-backed outline. The article body is drafted natively afterward,
using DigiTrust Lab's Malay voice, formatting, link, and structure rules.
After native drafting, apply the separate canonical no-credit originality and
source-attribution contract in
`.claude/rules/native-originality-source-gate.md`; never substitute WriterZen's
Plagiarism Checker for that gate.

Native drafting is not complete until the exact final content package has two
fresh, independent, content-hash-matched reviews:

- an actual Anthropic/Claude reviewer (the required Claude Sonnet lane); and
- an independent OpenAI reviewer.

Both review records must be present, PASS, identify their actual provider and
model, and cover the same final content hash. Missing, stale, mismatched, or
same-family-only review evidence fails closed before publication.

## Required handoff evidence

The WriterZen-to-Content handoff must carry:

```text
writerzen_generation_mode: outline_only
outline_toggle: ON
whole_article_toggle: OFF
keyword_suggestion_toggle: OFF|AUTHORIZED_ON
keyword_set_status: adequate|insufficient
writerzen_ui_evidence_ref:
writerzen_ui_captured_at:
writerzen_create_attempted_at:
writerzen_ai_credit_status: adequate|insufficient|unknown
upgrade_attempted: NO
bypass_attempted: NO
operations_ai_credit_decision: PASS|FAIL|PENDING|BLOCKED
operations_ai_credit_status: PASS|FAIL|PENDING|BLOCKED
operations_ai_credit_evidence_ref:
operations_ai_credit_checked_at:
operations_ai_credit_owner:
native_drafting_mode: native
dual_review_status: PASS|PENDING|FAIL
anthropic_review_provider:
anthropic_review_model:
anthropic_review_content_hash:
openai_review_provider:
openai_review_model:
openai_review_content_hash:
```

`AUTHORIZED_ON` is valid only with the documented insufficiency and explicit
user approval. `PENDING`, `FAIL`, `BLOCKED`, or a missing field is never
permission to submit or publish. Run
`python scripts/verify-writerzen-ai-credit-gate.py` for deterministic positive
and adversarial fixtures before handing the artifact onward.
