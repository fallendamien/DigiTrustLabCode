# Article completion summaries

Create or update one concise Markdown artifact per article at:

```text
content/article-completion-summaries/<post-slug>.md
```

The write-post workflow generates this artifact automatically as its final
closeout step, after the post-publish verification gate. It is a high-level
handoff, not a replacement for the detailed evidence in the content calendar,
naturalness review, link review, or dashboard records.

Use this template:

```markdown
# Article Completion Summary — [Post title]

| Field | Value |
|---|---|
| Post | [title] |
| URL | [published URL, or `Not published`] |
| WordPress Post ID | [ID, or `Not published`] |
| Status | `PUBLISHED` / `BLOCKED` / `ABORTED` |
| Published | [date and outcome, or `Not published`] |

## Topic Discovery rationale

[The angle Topic Discovery surfaced and why it was selected at a high level.]

## Keyword and metrics rationale

- Focus keyword: [keyword]
- Key metrics: [volume, KD, Golden Score, All-in-Title, and brief SERP/intent note]

## Research gates

- Golden Filter: [pass/fail, with the headline result]
- Weak Spot: [value and pass/fail; note any approved evidence-backed override]

## Writing and editorial work

[Briefly note the outline/content work, Malay voice and naturalness edits,
formatting, internal links, images, excerpt, and SEO/Rank Math work that
materially shaped the final article.]

## Delegated work

| Stage / role | Agent and model | Scope | High-level result / evidence | Blocker or handoff |
|---|---|---|---|---|
| [stage/role] | [actual model ID, effort] | [bounded scope] | [result and evidence pointer] | [blocker/handoff, or `None`] |

[Include one row per worker/agent involved. If no worker was involved, write
`None — coordinator-only`. The orchestrator reconciles returned worker outputs
before recording them and must not claim completion without evidence; mark
missing or contradictory evidence as `Pending` or `Blocked`.]

## Publication, verification, and tracking

[Publish date/outcome and a high-level state for live rendering, structure,
voice/naturalness, links, both ClickRank trackers, Screpy, and Google Search
Console. Every `PUBLISHED` summary must report the two ClickRank tracker
surfaces independently; one row does not imply the other. Use
`Pending` or `Deferred` where evidence is not yet available.]

- Media stage: [WordPress/Respira upload and insertion status for featured and
  in-content images, with a high-level evidence pointer]
- Image Caption policy: [`Image Caption` left empty by default for featured and
  inline images; never populated from alt text or description; reader-visible
  caption added only on explicit user request. Alt text remains separate and
  verified where appropriate.]
- Featured placement: [separate DigiTrust Lab brand-color hero asset verified]
- Inline placement: [tool/UI screenshots verified as instructional inline media
  only, or `None`]
- ClickRank AI Overview Tracker: [independent status/evidence — exact focus keyword,
  exact live URL, Malaysia/Malay settings where available, pre-submit count,
  post-submit or existing-row count, verification timestamp, and visible result;
  use `Pending` or `Blocked` when not proven]
- ClickRank standard Keyword Tracker: [independent status/evidence — the same
  focus keyword and exact live URL, Malaysia/Device: All, pre-submit count,
  post-submit or existing-row count, verification timestamp, and visible result;
  use `Pending` or `Blocked` when not proven]
- ClickRank Website Optimization / Pages: [exact URL, visible status, date, and
  recommendation/no-change decision]
- Screpy Rank Tracker: [separate traditional-SERP status/evidence — focus
  keyword, Malaysia/Malay, Device: Both, verification timestamp, and visible
  Desktop/Mobile rows]

Placement boundary: real tool/UI screenshots, such as Canva interface captures,
are inline instructional media only. The featured image is always a separate
DigiTrust Lab brand-color hero asset following `content/image-prompts.md`; keep
the two verification results separate in this summary.

Media boundary: WriterZen is text research/drafting only. Never record or retry
WriterZen image uploads; if an asset is unavailable there, record it as
`Pending` and use the WordPress/Respira media-stage result.

## Open follow-ups

- [Pending item, or `None`]

## Evidence pointers

- Content calendar: [entry or link]
- Detailed artifacts: [relevant paths, if any]
```

For `BLOCKED` or `ABORTED` outcomes, use `Not published` for URL, Post ID, and
publication date, record the concrete reason in the relevant section, and do
not describe live verification or tracking as completed. If the block/abort
happens before Phase 7, generate the artifact immediately at that terminal
stop. Keep the summary short; never duplicate article text, raw dashboard
transcripts, or command logs.
