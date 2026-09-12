# Prompt Engineering research handoff — 2026-09-10

## Decision

**RELEVANCE PASS; RESEARCH PARKED.** The project-local structured relevance
registry now registers the candidate as
`prompt-engineering.youtube-thumbnail`, with cluster
`prompt-engineering.ai-visual-prompts`, intent
`intent.youtube.thumbnail.prompt.creation`, and entities `entity.prompt`,
`entity.youtube-thumbnail`, and `entity.ai-image`. The contract in
`.claude/rules/editorial-relevance-gate.md` was applied before credit spend.

At the time this record was first created, no WriterZen action had been run.
Subsequent research actions and their IDs/metrics are recorded below. No
drafting, Content Creator, WordPress, publishing, upgrade, optional keyword
expansion, or plagiarism checker action is in scope.

## Nearest registered-family check

The nearest previously registered family was `ai-tools.chatgpt.poster` with
`intent.chatgpt.poster.creation` and entities `entity.chatgpt` +
`entity.poster`. Its matching subject is already published as Post #8, ID 721,
`https://digitrustlab.com/cara-buat-poster-dengan-chatgpt/`. Reusing that family
for a YouTube-thumbnail article would fail the entity/intent match and risk
cannibalising the existing ChatGPT-poster leaf. The candidate now has its own
registered Prompt Engineering family, so no silent pivot was made.

## Candidate relevance record

| Field | Evidence / value |
|---|---|
| Proposed topic and article subject | Cara Buat Thumbnail YouTube dengan Prompt AI — a practical beginner workflow for writing and refining image prompts for a YouTube thumbnail. |
| Proposed seed | `prompt AI untuk thumbnail YouTube` |
| Approved pillar/category | `Prompt Engineering` |
| Normalized topic-family ID | `prompt-engineering.youtube-thumbnail` |
| Approved pillar ID | `prompt-engineering` |
| Approved cluster ID | `prompt-engineering.ai-visual-prompts` |
| Topic intent ID | `intent.youtube.thumbnail.prompt.creation` |
| Subject entity IDs | `entity.prompt`, `entity.youtube-thumbnail`, `entity.ai-image` |
| Declared seed intent | Informational / practical how-to: create, test, and refine AI prompts for a YouTube thumbnail. |
| Reader problem | A beginner wants a repeatable prompt structure for a clear thumbnail concept, including subject, composition, contrast, and exclusions, without relying on vague one-line instructions. |
| Authenticity basis | Planned first-hand test only: create a small prompt set with an available image tool, compare outputs, and document what changed. No personal result is claimed yet. |
| Inventory / cannibalization check | Distinct from Post #3’s text-prompt beginner guide (`cara buat prompt chatgpt`), Post #4’s broad AI-image guide (`cara buat gambar ai`), Post #8’s ChatGPT-poster workflow, and Post #9’s Gemini photo-editing gallery. It would be a thumbnail-specific image-prompt leaf, not a replacement for those intents. |
| Seed-to-topic semantic match | **PASS.** The seed, proposed subject, reader problem, and category all describe AI prompt creation for YouTube thumbnails, and the structured IDs now match the registered family. |
| Existing-cluster/link map | Approved cluster `prompt-engineering.ai-visual-prompts`; candidate parent/peer evidence: Post #4 (AI-image sub-pillar) and Post #9 (prompt gallery). |
| Published parent/peer | Post #4, ID `536`, `https://digitrustlab.com/cara-buat-gambar-ai/`; peer Post #9, ID `582`, `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/`. |
| Plausible inbound source | Post #3, ID `437`, `https://digitrustlab.com/cara-buat-prompt-chatgpt/` — a context paragraph about moving from general prompt structure to a thumbnail-specific visual example could link naturally. |
| Incremental reader value | Adds a concrete visual-prompt use case and output-testing method not covered by the broad AI-image explainer or photo-editing gallery. |
| Planned anchor/context | `contoh prompt AI untuk thumbnail YouTube`, in a paragraph explaining that prompt structure becomes easier to understand when applied to a specific visual brief. |
| Pivot status | `none`; this is now an in-family Prompt Engineering candidate. |
| User approval reference | None required for an in-family candidate; no outside-family pivot was attempted. |

## Research attestation

| Field | Value |
|---|---|
| Decision | `PASS` |
| Status | `PASS` |
| Evidence reference | This record; `.claude/rules/editorial-relevance-gate.md`; `scripts/verify-editorial-relevance-gate.py` registry and `prompt_thumbnail_pass` fixture; `content/content-calendar.md` lines 129–185, 364–409, 410–447, 602–644 |
| Checked at | `2026-09-10` |
| Owner | Research bounded worker (`gpt-5.6-luna`, high) |
| topic_family_id / pillar_id / cluster_id / topic_intent_id | `prompt-engineering.youtube-thumbnail` / `prompt-engineering` / `prompt-engineering.ai-visual-prompts` / `intent.youtube.thumbnail.prompt.creation` |
| subject_entity_ids | `entity.prompt`, `entity.youtube-thumbnail`, `entity.ai-image` |
| Attestation | `RESEARCH_RELEVANCE: PASS` — candidate is registered, in-family, distinct from published inventory, and has a parent/peer plus inbound-link path. |

## SEO attestation

| Field | Value |
|---|---|
| Decision | `PASS` |
| Status | `PASS` |
| Evidence reference | This record; current published inventory in `content/content-calendar.md`; registry definition in `scripts/verify-editorial-relevance-gate.py` |
| Checked at | `2026-09-10` |
| Owner | SEO bounded review (`gpt-5.6-luna`, high) |
| topic_family_id / pillar_id / cluster_id / topic_intent_id | `prompt-engineering.youtube-thumbnail` / `prompt-engineering` / `prompt-engineering.ai-visual-prompts` / `intent.youtube.thumbnail.prompt.creation` |
| subject_entity_ids | `entity.prompt`, `entity.youtube-thumbnail`, `entity.ai-image` |
| Search-intent/cannibalization check | Distinct thumbnail-image-prompt intent against published IDs 437, 536, 582, and 721; it extends the Prompt Engineering image-prompt cluster without replacing an existing intent. |
| Attestation | `SEO_RELEVANCE: PASS` — search-intent and inventory checks agree with the registered family. |

## Operations attestation

| Field | Value |
|---|---|
| Decision | `PASS` |
| Status | `PASS` |
| Evidence reference | This record; calendar inventory and link map above; live URLs were verified as the published targets recorded in the calendar. |
| Checked at | `2026-09-10` |
| Owner | Operations bounded review (`gpt-5.6-luna`, high) |
| Current calendar evidence | `content/content-calendar.md` — current Prompt Engineering entries are Post #4 (ID 536), Post #9 (ID 582), plus AI Tools prompt-related Post #3 (ID 437) and Post #8 (ID 721). |
| Calendar URLs | `https://digitrustlab.com/cara-buat-gambar-ai/`; `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/`; `https://digitrustlab.com/cara-buat-prompt-chatgpt/`; `https://digitrustlab.com/cara-buat-poster-dengan-chatgpt/` |
| Published parent/peer URLs and status | `https://digitrustlab.com/cara-buat-gambar-ai/` (ID 536, published); `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/` (ID 582, published) |
| Inbound-source URL and status | `https://digitrustlab.com/cara-buat-prompt-chatgpt/` (ID 437, published; plausible contextual source, not yet edited) |
| Link-feasibility URLs and status | Read-only HTTP HEAD checks on `2026-09-10`: Post #4 (ID 536) `200`, Post #3 (ID 437) `200`, and Post #8 (ID 721) `200`; Post #9 (ID 582) timed out at 20 seconds and remains unconfirmed by this check. No link was added. Feasibility is otherwise pending the registered family and future content approval. |
| Structured URL arrays | Parent/peer: [`https://digitrustlab.com/cara-buat-gambar-ai/`, `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/`]; inbound: [`https://digitrustlab.com/cara-buat-prompt-chatgpt/`]; feasibility: [`https://digitrustlab.com/cara-buat-gambar-ai/`, `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/`, `https://digitrustlab.com/cara-buat-prompt-chatgpt/`] |
| topic_family_id / pillar_id / cluster_id / topic_intent_id | `prompt-engineering.youtube-thumbnail` / `prompt-engineering` / `prompt-engineering.ai-visual-prompts` / `intent.youtube.thumbnail.prompt.creation` |
| subject_entity_ids | `entity.prompt`, `entity.youtube-thumbnail`, `entity.ai-image` |
| Attestation | `OPERATIONS_RELEVANCE: PASS` — current calendar, published parent/peer URLs, inbound source, and link feasibility are structurally aligned with the registered candidate. |

## Fresh WriterZen quota evidence (read-only)

Existing authenticated Chrome tab: **Chrome profile Zamri**, tab ID `2074155307`,
title `Quick Access - WriterZen`, URL
`https://app.writerzen.net/user/profile-setting?tab=limit`.

Fresh UI snapshot and screenshot captured on `2026-09-10` showed:

| Limit | Current display |
|---|---:|
| Plan | AppSumo Tier 2, Active, Lifetime |
| Topic Lookup / Day | `75/75` |
| Keyword Lookup / Day | `75/75` |
| Article / Month | `69/70` |
| Keyword Credit / Month | `40,000/40,000` |
| AI Words / Month | `7,471/8,000` |
| Keyword List / Plan | `47/50` |

Quota was adequate before research. No upgrade, bypass, or optional keyword
expansion was attempted.

## WriterZen research evidence and gate outcome

| Surface | Evidence |
|---|---|
| Topic Discovery | Report `246697`, `https://app.writerzen.net/user/topic-research/246697`; seed `prompt AI untuk thumbnail YouTube`; Malaysia/Malay fields; `76` topics discovered, `36` after `Closely` relevance filter. Search-volume ordering surfaced `PROMPT GAMBAR AI` (volume `70`) and `MEMBUAT THUMBNAIL YOUTUBE` (volume `10`). |
| Exact candidate Keyword Explorer | Report `1575472`, `https://app.writerzen.net/user/keyword-explorer/1575472`; `prompt AI untuk thumbnail YouTube`; Malaysia/Malay SERP; one exact row with volume `0`, so it failed the volume gate and was not added to the list or Planner. |
| Nearest in-family Keyword Explorer | Report `1575474`, `https://app.writerzen.net/user/keyword-explorer/1575474`; seed `prompt gambar AI`; Malaysia/Malay. Overview: last month `50`, 12-month average `70`, highest `210`, lowest `30`; CPC `0.48`; KD Ads `21`, KD Content/Traffic/Signal `0`; `177` ideas, total volume `690`. |
| Golden Filter | Confirmed for all `177` keywords at a displayed cost of `177` Keyword Credits. The selected row `prompt gambar ai` passed: volume `70`, All-in-Title `0`, Golden Score `1.003`, Word Count `3`, PPC `Low`. Volume `70` uses the documented Malay long-tail relaxation to `>=50`; the other thresholds remain unchanged. |
| Manual SERP check | The Malaysia/Malay SERP for `prompt gambar ai` included relevant small/local publishers: SirapLimau (#1), Sifoo (#2), UTM people blog (#6), and Hazril Hafiz (#10), alongside larger/news results. This satisfies the manual small-site reality check. |
| Permanent keyword list | Existing list `DigiTrust Lab Blog Posts`, ID `68708`, `https://app.writerzen.net/user/keyword-list/68708`, was inspected first: 53 rows and no exact `prompt gambar ai`. After the approved add, the list showed `54` rows and `prompt gambar ai` as row #54. |
| New Keyword Planner | New project `179213`, `https://app.writerzen.net/user/keyword-planner/179213`, named `Prompt AI Thumbnail YouTube - DigiTrustLab 2026-09-10`; Malaysia/Malay; one validated keyword; clustering level `Moderately Relevant`; no cluster could be formed from one keyword. Planner Golden Filter was active; no optional expansion was enabled. |
| Weak Spot gate | DA metrics activated at the displayed cost of `40` Keyword Credits. `prompt gambar ai`: Weak Spot `1`, average DA `64.5`, lowest DA `25`, highest DA `86`. **FAIL**: required Weak Spot `>=2`. |

**Overall research decision: `PARKED KEYWORD` / `WEAK SPOT FAIL`.** The topic
is editorially relevant and the keyword passes Golden Filter, All-in-Title,
volume-relaxation, and manual SERP gates, but it does not pass the required
Weak Spot gate. Stop before Content Brief, Create Article, Content Creator,
drafting, WordPress, or publication. Any outside-family pivot requires fresh
user approval.

## End-of-session WriterZen quota evidence

After the completed research actions, a fresh read-only Limits & Remaining UI
snapshot on the same authenticated tab showed: Topic Lookup `74/75`; Keyword
Lookup `73/75`; Keyword Credit `39,781/40,000`; AI Words `7,471/8,000`;
Keyword List plan `47/50`; Article `69/70`. The 219 Keyword Credits consumed
are accounted for by the 177 Explorer Golden Filter credits, 2 Planner setup
credits, and 40 DA credits. No upgrade, plagiarism checker, or optional
keyword expansion was used.

## Stop condition and required next action

Do not draft or create a brief for this candidate. Keep it parked until a
future approved in-family research run finds a keyword with Weak Spot `>=2`.
A pivot to AI Tools or Digital Skills still requires explicit user approval
before any credit or project action.

## Registry and parity review

The registry and deterministic fixture change is project-local to
`scripts/verify-editorial-relevance-gate.py`; no shared TSOT doctrine, loader,
skill, or workflow was changed. The canonical-TSOT propagation review therefore
records **project-only exclusion**. Fresh command evidence: the relevance test
passes after the new family fixture was added (14 scenarios; 5 pass / 9 fail;
exit 0).
