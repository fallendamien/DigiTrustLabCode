# Zed ACP handover — next Prompt Engineering article

**Prepared:** 2026-09-12
**Project:** `G:\Zamzam Biznez\DigiTrustLabCode`
**Target agents:** Codex ACP or Claude Code terminal/ACP in Zed
**Current outcome:** `prompt video ai` passed bounded relevance, exact Keyword
Explorer, one-keyword Golden Filter, and manual SERP review. It is eligible for
Planner Weak Spot validation, but the guarded list/project write is blocked
until the authenticated WriterZen tab is released or handed off. Do not draft.

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

Do not reset, clean, discard, stage, commit, or overwrite unrelated work. Inspect
the current status and preserve any user-owned changes. At handoff preparation the
project tree was clean and one commit ahead of `origin`; recheck rather than
assuming that state.

## Context7 readiness gate (run after restarting Zed)

Context7 is now persistent across the two clients:

| Client | Canonical source | Expected state |
|---|---|---|
| Codex | Global `@upstash/context7-mcp@4.1.0`, registered in `~/.codex/config.toml` | `context7` entry uses `cmd.exe /d /c context7-mcp.cmd --transport stdio` |
| Claude | Account-level `claude.ai Context7` connector | Connected; no local `context7` entry in `~/.claude.json` |

The current Zed/ACP process was started before the Codex registration and must be
restarted once. Then paste the prompt below into both Codex ACP and Claude Code
terminal/ACP. Do not add a second Claude server if the account connector is
connected.

### Copy-paste Context7 verification prompt

> Verify Context7 for both Codex and Claude without changing WordPress, browser
> authentication, credentials, or MCP configuration. Do not create a duplicate
> Claude file-based `context7` server.
>
> **Codex:** run `codex mcp get context7 --json`; confirm the command is
> `cmd.exe /d /c context7-mcp.cmd --transport stdio`, the package is
> `@upstash/context7-mcp` version `4.1.0`, and the server is enabled. Invoke
> Context7 `resolve-library-id` for `vue` and report the returned library IDs.
>
> **Claude:** run `claude mcp list` and `claude mcp get "claude.ai Context7"`;
> confirm the account-level connector is `Connected`. Confirm that
> `~/.claude.json` has no local `context7` server. Invoke Context7
> `resolve-library-id` for `vue` and report the returned library IDs.
>
> Finally run `& C:\my_Projektz\agent-templates\scripts\startup-integrity-check.ps1
> -ProjectPath "G:\Zamzam Biznez\DigiTrustLabCode"` and
> `python C:\my_Projektz\agent-templates\scripts\verify-agent-mcp-parity.py
> --project "G:\Zamzam Biznez\DigiTrustLabCode" --require-claude
> --require-codex`. Expect the Context7 package/config checks and parity summary
> to pass with zero failures and zero warnings. If any check fails, stop, report
> the exact output, and do not retry by adding another server.

Record the client-specific evidence in the session handoff. A config listing
alone is not enough; each client needs one successful Context7 tool call.

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

### Candidate 3 — qualified through Golden/SERP; live continuation blocked

| Field | Evidence |
|---|---|
| Topic | Cara Menulis Prompt Video AI yang Lebih Jelas |
| Bounded Topic Discovery | Report `246755`; seed `contoh prompt AI video`; 76 topics, 36 `Closely`; lead `prompt video ai` card volume `90` |
| Exact Keyword Explorer | Report `1576000`; volume `90`; last month `140`; 12-month average `90`; lowest `50`; Malaysia/Malay; Content/Traffic/Signal KD `0` |
| Golden Filter | Report `1576001`; Allintitle `0`; Golden Score `1.002`; one selected keyword; one credit spent. The 752-keyword broad filter was cancelled. |
| SERP | Mixed intent, but relevant local practitioner/course pages appeared at ranks 4 and 9 (Hazril Hafiz and Sifoo). Pass with an intent caveat; keep the article tightly instructional. |
| Permanent list | Read-only exact search in list `68708` returned no row. |
| Guarded continuation | Four bounded `gpt-5.6-luna` worker attempts, including after a tab-handoff mark and CUA reset, received the same provider result: the exact authenticated WriterZen tab was already claimed by session `01a09530-700e-7e90-ac79-abd632d41b36`. No list addition or Planner project was made. |
| Evidence | `content/research/prompt-engineering-2026-09-12-relevance.md` |

Resume only after the current browser-control session ends or the tab is
released/reopened by the user. Repeat the
bounded list-add (one exact row) and create one new Planner project, then
activate metrics and require Weak Spot `>=2`. Do not draft, publish, or use
WriterZen whole-article generation.

### Remaining cards from report 246697

| Exact visible wording | Card volume | Decision |
|---|---:|---|
| `tips prompt ai: kepentingan konteks untuk penghasilan` | `10` | Best remaining concept, but below the relaxed volume threshold of 50 |
| `kuasai prompt seni memimpin ai untuk pelajar ipt` | `10` | Awkward wording and uncertain academic/product intent |
| `teknik prompting yang digunakan oleh prompt engineer openai` | `N/A` | Advanced and potentially overlapping with Post #3 |

The previous seed is exhausted. Do not force one of these into production.

## Recommended continuation

Resume the qualified Candidate 3 record in
`content/research/prompt-engineering-2026-09-12-relevance.md`. Do not spend
another Topic Discovery or Keyword Explorer lookup unless the candidate is
explicitly invalidated by a fresh read. The next action is the guarded
permanent-list add and one new Planner project for `prompt video ai` after the
authenticated WriterZen tab is released or handed off.

Before spending a credit, refresh WriterZen limits and produce matching
Research, SEO, and Operations relevance attestations. Confirm the candidate
extends the Prompt Engineering cluster, has a published parent or peer, and
has a plausible inbound source. Reject image-editing, broad AI-image, ChatGPT
basics, poster, business, income, automation, SEO, and other off-family or
cannibalising results.

After the tab handoff is available:

1. Confirm the exact row is still absent from list `68708`; add only that row.
2. Create one new Planner project; never reuse `179213` or legacy `178201`.
3. Activate metrics and require Weak Spot `>=2`.
4. Record either the qualified or parked outcome in the calendar and this dated
   evidence file.

Stop if no candidate passes. Do not lower Golden or All-in-Title limits,
silently override Weak Spot, change category, or begin drafting.

## Browser and credit safeguards

- Use Zamri's already-open authenticated Chrome session. Claim the exact
  WriterZen tab, take a fresh snapshot, and reuse it.
- If that tab is unavailable, ask Zamri to open or sign in. Do not switch to a
  blank, private, or separate CDP profile.
- Last observed on 2026-09-12 after the exact lookup and one-keyword Golden
  Filter: Topic `74/75`, Keyword `73/75`, Article `69/70`, Keyword Credit
  `39,780/40,000`, AI Words `7,471/8,000`. Refresh before the guarded resume.
- Keep `Write the whole article` and optional keyword expansion OFF. Do not use
  WriterZen's plagiarism checker.
- Do not retry uncertain submissions. Reload and check for the resulting row
  or project first.

## Relevant worktree paths

| Path | State at the 2026-09-12 handoff | Purpose |
|---|---|---|
| `scripts/verify-editorial-relevance-gate.py` | Tracked and committed | Registered/tested the two Prompt Engineering research families |
| `content/content-calendar.md` | Tracked and committed | Records both parked candidates |
| `content/research/prompt-engineering-2026-09-10-relevance.md` | Tracked and committed | Thumbnail evidence and attestations |
| `content/research/prompt-engineering-ai-video-2026-09-10-research.md` | Tracked and committed | AI-video evidence and volume failure |
| `content/research/prompt-engineering-2026-09-12-relevance.md` | New, uncommitted | Candidate 3 exact metrics, Golden/SERP evidence, quota, and guarded-write blocker |

Other changes may be introduced in Zed after this handoff. Preserve and report
them separately; do not assume a clean tree when staging later work.

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
> completely, restart Zed if it predates the Context7 registration, and run the
> Context7 readiness prompt for both Codex and Claude. Verify imports, offline
> content status, and the current worktree. Resume Candidate 3 from
> `content/research/prompt-engineering-2026-09-12-relevance.md`. Use my existing
> authenticated Chrome WriterZen tab, release or hand it off before any guarded
> external write, and refresh quota. Confirm the exact list `68708` row is absent,
> add only `prompt video ai`, create one new Planner project, and stop at Weak
> Spot `<2` or any ambiguity. Do not draft, publish, alter WordPress, duplicate
> WriterZen records, override Weak Spot, enable keyword expansion, add a duplicate
> Context7 server, or touch unrelated Post #8 files. Report exact IDs, metrics,
> quota changes, Context7 tool-call evidence, tests, and blockers.

## Definition of done for the next ACP session

The research handoff ends with either:

1. **Qualified:** one distinct keyword passes relevance, volume, Golden, SERP,
   and Weak Spot gates and is recorded without duplicates; or
2. **Parked:** the fresh seed yields no qualifying candidate, with exact IDs,
   metrics, quota delta, rejection reasons, and updated evidence; or
3. **Blocked:** Candidate 3 remains qualified through Golden/SERP but the
   authenticated WriterZen tab cannot be safely handed off for the bounded
   external write. Record the exact ownership/blocker and do not bypass it.

Neither outcome authorizes drafting or publication.
