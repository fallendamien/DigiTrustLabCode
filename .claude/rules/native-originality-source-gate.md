---
trigger: always_on
description: Fail-closed no-credit originality and source-attribution gate for native DigiTrust Lab drafting.
---

# Native Originality and Source-Attribution Gate

This is the single project-local control for originality evidence after the
WriterZen outline handoff. WriterZen is restricted to the article title,
description, and outline. Its paid Plagiarism Checker is **not part of the
DigiTrust Lab workflow**, is not a publication prerequisite, and must not be
run merely because it is visible in Content Creator.

This gate validates workflow evidence and source practice. It does **not**
claim to detect all plagiarism or replace a plagiarism database.

## Required native-draft evidence

Before Content hands a draft to publication, the frozen handoff must record:

| Field | Required value | Meaning |
|---|---|---|
| `native_drafting_mode` | `native` | The body was drafted outside WriterZen's full-article writer |
| `draft_provenance` | non-empty | Where the draft came from and what first-hand test/research informed it |
| `source_attribution_status` | `complete` or `not_applicable` | Whether source-grounded claims have been accounted for |
| `source_attribution_refs` | non-empty when `complete` | URLs/citations for factual claims, quotations, or close paraphrases |
| `competitor_text_copied` | `false` | No competitor/source passage was copied into the draft |
| `uncredited_close_paraphrase` | `false` | No close paraphrase is left without clear attribution |
| `distinctive_overlap_status` | `clear` | Reviewers found no suspicious distinctive overlap requiring resolution |
| `draft_content_hash` and `originality_evidence_content_hash` | identical, non-empty | The evidence is bound to the exact draft reviewed |
| `writerzen_plagiarism_checker_used` | `false` | No WriterZen plagiarism action occurred |
| `writerzen_plagiarism_checker_required` | `false` | No handoff silently reinstates that prerequisite |
| `writerzen_plagiarism_credit_spent` | `false` | No WriterZen plagiarism words/credits were spent |

`not_applicable` is valid only when the draft has no source-grounded claims,
quotations, or close paraphrases; record that decision explicitly rather than
leaving attribution unknown. Source-grounded claims must retain descriptive
links/citations in the draft and are checked separately by the link gate.

The Anthropic/Claude Sonnet and OpenAI naturalness reviews remain mandatory
under `content/naturalness-reviews/README.md`. They may flag suspicious
distinctive overlap, but they are not plagiarism-database reports and a
naturalness PASS cannot override copied text, uncredited paraphrase, missing
attribution, or a hash mismatch.

## Operations and external-checker boundary

Operations must independently attest that no WriterZen plagiarism action,
requirement, or credit spend occurred. Content rejects a handoff missing this
attestation or the originality evidence above. Research and SEO carry the
source/provenance references forward but do not trigger a checker.

An unusual third-party or imported-copy risk may justify an external paid
checker only after explicit user authorization recorded before the cost or
submission. The exception must name the provider and authorization evidence.
It remains outside the normal workflow, and it must never be WriterZen's
checker or be enabled implicitly by a generic "check plagiarism" instruction.

## Required handoff evidence

```text
native_drafting_mode: native
draft_provenance:
source_attribution_status: complete|not_applicable
source_attribution_refs:
competitor_text_copied: false
uncredited_close_paraphrase: false
distinctive_overlap_status: clear|flagged|pending
distinctive_overlap_findings:
draft_content_hash:
originality_evidence_content_hash:
writerzen_plagiarism_checker_used: false
writerzen_plagiarism_checker_required: false
writerzen_plagiarism_credit_spent: false
external_checker_attempted: false
external_checker_authorized: false
external_checker_provider: none
external_checker_authorization_ref:
operations_originality_decision: PASS|FAIL|PENDING|BLOCKED
operations_originality_evidence_ref:
operations_originality_checked_at:
operations_originality_owner:
```

Run `python scripts/verify-native-originality-gate.py` for deterministic
positive and adversarial fixtures. The validator proves these invariants only;
it does not scan the web or make a true plagiarism-detection claim.
