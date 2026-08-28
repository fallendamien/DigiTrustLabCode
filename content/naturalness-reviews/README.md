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
Claude Sonnet/Anthropic session and one OpenAI session. The Anthropic reviewer
must be Claude Sonnet; do not substitute Claude Opus unless the user
explicitly changes this preference. Do not provide either reviewer with the
other review, an older review, or a suggested correction as context.
Both reviewers use the same seven binary checks for the complete document and
every extracted segment. Use `schema_version: 3` (current) for new reviews;
existing `schema_version: 2` artifacts require only the first six checks and
remain valid without re-review:

1. Would a Malaysian technology writer naturally use this wording?
2. Is there a literal translation or unusual word combination?
3. Does any phrase sound bureaucratic, academic, or overly governmental?
4. Would an English technical term be clearer in this context?
5. Does the text sound natural on the first read and when read aloud?
6. Is terminology and register consistent throughout the article?
7. Is every sentence grammatically complete — proper verb where required,
   `yang` present in relative clauses, no fragment or fused sentences, no
   missing particles or affixes that a fluent Malaysian reader would notice?
   (Added 2026-08-16 after `struktur jelas` was missed by both AI reviewers
   in the post 605 excerpt. Root cause: `noun + adjective` without `yang`
   passes all language-model fluency checks but is broken Malay grammar.)

Both reviewers must return `true` for every check, `confidence: "high"`, and
an empty `findings` list before the artifact can pass. A finding or uncertainty
requires revision and a complete fresh review by both families. If either
reviewer cannot decide between materially different wording, record the issue
for the user's decision; unresolved decisions block publication. The artifact
must contain exactly two reviewer records: one Claude/Anthropic and one OpenAI.
Every reviewer record must include the actual nonblank model identity; family
labels alone are insufficient. The Claude record must additionally preserve the
actual CLI runtime provider (currently `provider: "firstParty"`), keep
`model_family: "anthropic"`, and prove `transport: "claude-code-cli"`,
`session_persistence: false`, and `tools: []`.

### Anthropic lane: terminal-only Claude Code CLI (MANDATORY)

The Claude/Anthropic reviewer must run through the local authenticated Claude
Code CLI in a terminal. Do not use `claude.ai`, Claude in Chrome, a browser tab,
or a GUI session. The CLI lane must be non-persistent and toolless so the review
does not add to web history or accidentally inspect or change the repository.

Before the first review, run `claude --help` and require every flag below to be
supported. The exact command contract is:

```powershell
$schema = '{"type":"object","required":["provider","model","status","document_review","segments"],"properties":{"provider":{"enum":["anthropic","firstParty"]},"model":{"type":"string","minLength":1,"pattern":"sonnet"},"status":{"enum":["pass","fail"]},"document_review":{"type":"object"},"segments":{"type":"array"}},"additionalProperties":true}'
$prompt = Get-Content -Raw 'content/naturalness-reviews/<post-slug>-claude-prompt.txt'
$prompt | claude --print --safe-mode --model sonnet --effort high --no-chrome --no-session-persistence --tools "" --output-format json --json-schema $schema
```

The required flags are `--safe-mode`, `--model sonnet`, `--effort high`,
`--no-chrome`, `--no-session-persistence`, `--tools ""`, `--output-format
json`, and `--json-schema`. If the installed CLI does not expose any one of
them, stop and fail closed. Do not silently replace a missing flag with a
different permission mode, a browser workflow, or an OpenAI model.

The repository helper performs this preflight, invokes the exact command, and
rejects missing authentication/provider/model evidence before writing output:

```powershell
pwsh -File scripts/run-claude-naturalness-review.ps1 `
  -PromptPath content/naturalness-reviews/<post-slug>-claude-prompt.txt `
  -OutputPath content/naturalness-reviews/<post-slug>-claude.json
```

The helper first requires `claude auth status` to report `loggedIn: true`, then
validates the CLI envelope's `modelUsage` entry. The current Claude Code runtime
reports `canonicalModel: "claude-sonnet-5"` and `provider: "firstParty"`;
record those exact runtime values. The artifact's `model_family` remains
`"anthropic"` because that is the model family, not the transport label. The
structured payload provider must still be `anthropic` or `firstParty`, and its
model must identify Sonnet, but runtime `modelUsage` is authoritative.
Missing, blank, contradictory, OpenAI, browser, or unverified provider/model
evidence blocks the artifact. A CLI exit code of zero alone is never sufficient
evidence.

The OpenAI reviewer remains a separate fresh worker session and must receive
only the frozen final package. Never pass the Claude output, findings, or
corrections to it. If the Claude CLI lane is unavailable or fails closed, do
not fall back to Claude web/GUI; the publication gate remains blocked until the
terminal lane is available.

## Artifact shape

```json
{
  "schema_version": 3,
  "post_id": 559,
  "slug": "example-post",
  "reviewed_at": "2026-08-08T00:00:00Z",
  "content_hash": "sha256-from-validator",
  "status": "pass",
  "reviewers": [
    {"id": "claude", "model_family": "anthropic", "provider": "firstParty", "model": "claude-sonnet-5", "transport": "claude-code-cli", "session_persistence": false, "tools": []},
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

## Artifact retention

Keep one final hash-bound package and provider-evidence set per post as the
canonical naturalness evidence. Do not store a duplicate article in that
package. The active repository set follows this policy:

| Class | Treatment |
|---|---|
| Canonical final evidence | Keep the final hash-bound review JSON and the provider evidence needed to establish its identity and result. Selectively stage and commit it with the article's durable source/evidence. |
| Superseded retry | A prior prompt/output or review invalidated by a later final package. Do not treat it as evidence; retain only when recovery requires it, otherwise locally exclude its exact path. |
| Quarantine media | Generated or rejected media held outside the canonical article evidence. Retain only when recovery requires it; otherwise locally exclude its exact path. It is never a substitute for the final review package. |
| Pending/unproven | Missing, stale, contradictory, or not-yet-reviewed material. Keep it visible and mark the closeout pending; never hide it or present it as canonical. |

Local exclusions must use exact paths for superseded retries or quarantine
media. Never use a broad pattern that could hide canonical evidence,
`STATE.json`, or `NEXT.md`. Do not delete review evidence under this policy;
generated cache/temp cleanup belongs to the guarded repository hygiene gate.

After every article posting, run `git status --porcelain=v1 -uall` after all
cleanup and commit/push decisions. Explicitly classify every changed or
untracked path as canonical final evidence, durable source/evidence/media,
superseded retry, quarantine media, generated cache/temp, or pending/unproven,
and record the keep, stage, exact-exclude, guarded-remove, or pending decision.
Any unclassified path means the repository closeout is incomplete, even when
the naturalness validator passes.
