# VSCodium ACP handover — next Prompt Engineering article

**Prepared:** 2026-09-12
**Project:** `G:\Zamzam Biznez\DigiTrustLabCode`
**Target agents:** Codex ACP or Claude ACP in VSCodium
**Current outcome:** No next topic has qualified yet. Resume research; do not draft.

## Objective

Find one useful, non-cannibalising Prompt Engineering article and validate it
through the Option C research gates. Stop before Content Creator, drafting,
WordPress, or publication unless Zamri separately approves further work.

## Read and verify first

Read `AGENTS.md`, `.claude/rules/editorial-relevance-gate.md`,
`.claude/rules/content-planning.md`,
`.claude/skills/writerzen-keyword-research/SKILL.md`, and
`.claude/skills/write-post/SKILL.md`. Then run:

```powershell
python scripts/verify-imports.py
python scripts/verify-content-status.py --offline
git status --short
```

Do not reset, clean, discard, stage, commit, or overwrite the existing dirty
worktree. It contains user-owned Post #8 evidence and this research.

## Completed research

### Candidate 1 — parked at Weak Spot

| Field | Evidence |
|---|---|
| Topic | Cara Buat Thumbnail YouTube dengan Prompt AI |
| Preferred seed | `prompt AI untuk thumbnail YouTube` |
| Topic Discovery | Report `246697`; 76 topics; 36 `Closely` |
| Exact seed | Volume `0`; rejected |
| Nearest keyword | `prompt gambar ai`; Keyword Explorer `1575474` |
| Golden result | Volume `70`; All-in-Title `0`; Golden Score `1.003`; PPC Low |
| Keyword list | `DigiTrust Lab Blog Posts`, ID `68708`; row count `54` after addition |
| Planner | `Prompt AI Thumbnail YouTube - DigiTrustLab 2026-09-10`, ID `179213` |
| Weak Spot | `1`; required `>=2`; parked |
| Evidence | `content/research/prompt-engineering-2026-09-10-relevance.md` |

Do not duplicate the Planner project or keyword-list row. Do not override Weak
Spot 1 without Zamri's explicit approval.

### Candidate 2 — parked at volume

| Field | Evidence |
|---|---|
| Topic | Starter Prompt Video AI: Cara Bina Arahan untuk Video yang Lebih Jelas |
| Topic Discovery | `PROMPT VIDEO` → `starter prompt video ai`; card volume `140` |
| Keyword Explorer | Report `1575483`; exact and 12-month-average volume `0` |
| Downstream actions | No Golden Filter, list addition, or Planner project |
| Evidence | `content/research/prompt-engineering-ai-video-2026-09-10-research.md` |

The card volume was not the exact-keyword volume. Do not treat `140` as
validation of `starter prompt video ai`.

### Remaining cards from report 246697

| Exact visible wording | Card volume | Decision |
|---|---:|---|
| `tips prompt ai: kepentingan konteks untuk penghasilan` | `10` | Best remaining concept, but below the relaxed volume threshold of 50 |
| `kuasai prompt seni memimpin ai untuk pelajar ipt` | `10` | Awkward wording and uncertain academic/product intent |
| `teknik prompting yang digunakan oleh prompt engineer openai` | `N/A` | Advanced and potentially overlapping with Post #3 |

The previous seed is exhausted. Do not force one of these into production.

## Recommended continuation

Start a fresh Topic Discovery report using the provisional broad seed
`contoh prompt AI`, Malaysia and Malay. This is a research seed, not an
approved keyword or title.

Before spending a credit, refresh WriterZen limits and produce matching
Research, SEO, and Operations relevance attestations. Confirm the candidate
extends the Prompt Engineering cluster, has a published parent or peer, and
has a plausible inbound source. Reject image-editing, broad AI-image, ChatGPT
basics, poster, business, income, automation, SEO, and other off-family or
cannibalising results.

After relevance passes:

1. Run Topic Discovery first.
2. Run Keyword Explorer with Malaysia/Malay.
3. Apply Golden Score `<=10`, All-in-Title `<=10`, and volume `>=100`; volume
   may relax to `50` only for a genuine Malay long-tail.
4. Inspect the SERP for matching intent and small Malaysian publishers.
5. Check permanent list `68708` for an exact row before adding anything.
6. Create one new Planner project; never reuse `179213` or legacy `178201`.
7. Activate metrics and require Weak Spot `>=2`.
8. Record either the qualified or parked outcome in the calendar and a dated
   evidence file.

Stop if no candidate passes. Do not lower Golden or All-in-Title limits,
silently override Weak Spot, change category, or begin drafting.

## Browser and credit safeguards

- Use Zamri's already-open authenticated Chrome session. Claim the exact
  WriterZen tab, take a fresh snapshot, and reuse it.
- If that tab is unavailable, ask Zamri to open or sign in. Do not switch to a
  blank, private, or separate CDP profile.
- Last observed on 2026-09-10: Topic `74/75`, Keyword `72/75`, Article `69/70`,
  Keyword Credit `39,781/40,000`, AI Words `7,471/8,000`. Refresh these values.
- Keep `Write the whole article` and optional keyword expansion OFF. Do not use
  WriterZen's plagiarism checker.
- Do not retry uncertain submissions. Reload and check for the resulting row
  or project first.

## Relevant worktree paths

| Path | State before this handover | Purpose |
|---|---|---|
| `scripts/verify-editorial-relevance-gate.py` | Modified | Registered/tested the two Prompt Engineering research families |
| `content/content-calendar.md` | Modified | Records both parked candidates |
| `content/research/prompt-engineering-2026-09-10-relevance.md` | Untracked | Thumbnail evidence and attestations |
| `content/research/prompt-engineering-ai-video-2026-09-10-research.md` | Untracked | AI-video evidence and volume failure |

Other modified or untracked paths predate or sit outside this handover.
Preserve and report them separately.

## Verification before reporting

```powershell
python scripts/verify-editorial-relevance-gate.py
python scripts/verify-content-status.py --offline
python scripts/verify-imports.py
git diff --check
git status --short
```

Baseline: relevance `15 scenarios; 6 pass / 9 fail`; calendar `12 post
entries`; imports PASS; no whitespace errors. Existing LF/CRLF warnings may
print.

## Copy-paste ACP opening prompt

> Read `AGENTS.md` and `content/next-prompt-engineering-vscodium-acp-handoff.md`
> completely, then verify imports, offline content status, and the dirty
> worktree. Resume only the next Prompt Engineering topic research from the
> Recommended continuation section. Use my existing authenticated Chrome
> WriterZen tab, refresh quota, and apply the editorial relevance gate before
> spending credits. Do not draft, publish, alter WordPress, duplicate WriterZen
> records, override Weak Spot, enable keyword expansion, or touch unrelated
> Post #8 files. Report exact IDs, metrics, quota changes, tests, and blockers.

## Definition of done for the next ACP session

The research handoff ends with either:

1. **Qualified:** one distinct keyword passes relevance, volume, Golden, SERP,
   and Weak Spot gates and is recorded without duplicates; or
2. **Parked:** the fresh seed yields no qualifying candidate, with exact IDs,
   metrics, quota delta, rejection reasons, and updated evidence.

Neither outcome authorizes drafting or publication.
