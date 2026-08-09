# Malay Naturalness Review Artifacts

Every new or edited article needs one JSON artifact named after its post slug:

```text
content/naturalness-reviews/<post-slug>.json
```

The artifact must describe the exact final content reviewed. The validator
compares `content_hash` and every segment hash, so changing one character
invalidates the approval.

To obtain the current content hash and segment manifest while the artifact is
still being prepared, run the validator with a temporary or missing review
path and `--json`. The output includes IDs, kinds, and hashes but does not
duplicate the article text.

## Reviewer protocol

Ask two independent fresh sessions to review the final content: one
Claude/Anthropic session and one OpenAI session. Do not provide either reviewer
with the other review, an older review, or a suggested correction as context.
Both reviewers use the same six binary checks for the complete document and
every extracted segment:

1. Would a Malaysian technology writer naturally use this wording?
2. Is there a literal translation or unusual word combination?
3. Does any phrase sound bureaucratic, academic, or overly governmental?
4. Would an English technical term be clearer in this context?
5. Does the text sound natural on the first read and when read aloud?
6. Is terminology and register consistent throughout the article?

Both reviewers must return `true` for every check, `confidence: "high"`, and
an empty `findings` list before the artifact can pass. A finding or uncertainty
requires revision and a complete fresh review by both families. If either
reviewer cannot decide between materially different wording, record the issue
for the user's decision; unresolved decisions block publication. The artifact
must contain exactly two reviewer records: one Claude/Anthropic and one OpenAI.
Every reviewer record must include the actual nonblank model identity; family
labels alone are insufficient.

## Artifact shape

```json
{
  "schema_version": 2,
  "post_id": 559,
  "slug": "example-post",
  "reviewed_at": "2026-08-08T00:00:00Z",
  "content_hash": "sha256-from-validator",
  "status": "pass",
  "reviewers": [
    {"id": "claude", "model_family": "anthropic", "model": "sonnet"},
    {"id": "openai", "model_family": "openai", "model": "gpt-5"}
  ],
  "document_review": {
    "claude": {"checks": {}, "confidence": "high", "findings": []},
    "openai": {"checks": {}, "confidence": "high", "findings": []}
  },
  "segments": [
    {
      "id": "seg-001",
      "hash": "sha256-from-validator",
      "reviewers": {
        "claude": {"checks": {}, "confidence": "high", "findings": []},
        "openai": {"checks": {}, "confidence": "high", "findings": []}
      }
    }
  ],
  "disagreements": [],
  "human_resolutions": []
}
```

Validate a local final draft with:

```text
python scripts/verify-malay-naturalness.py --file <final.html> --review <review.json>
```

For a pre-publication file that must match the later WordPress hash, serialize
the reader-facing package in the same order used by the live fetch: title,
content, excerpt, then available SEO metadata. Mark the excerpt explicitly:

```html
<title>Final article title</title>
<!-- exact final post content, including image alt text -->
<p data-naturalness-kind="excerpt">Final manual excerpt.</p>
<meta name="rank_math_title" content="Final SEO title">
<meta name="rank_math_description" content="Final SEO description">
```

`data-naturalness-kind="excerpt"` affects only the verifier's segment type. Do
not paste this wrapper into the WordPress post body. Build it as the local review
package from the staged draft values.

Validate the live WordPress result after publishing with:

```text
python scripts/verify-malay-naturalness.py --post-id <post-id> --review <review.json>
```

Live mode also binds the artifact to the exact WordPress post ID and slug and
requires the post status to be `publish`. A matching content hash from another
post cannot satisfy the gate.

Do not store a duplicate article in the artifact. Store hashes, exact flagged
excerpts when applicable, corrections, reviewer identities, and resolutions.
