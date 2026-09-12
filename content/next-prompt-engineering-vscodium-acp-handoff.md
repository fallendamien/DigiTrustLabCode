# Zed ACP handover — next Prompt Engineering article

**Prepared:** 2026-09-13
**Project:** `G:\Zamzam Biznez\DigiTrustLabCode`
**Target agents:** Codex ACP or Claude Code terminal/ACP in Zed
**Current outcome:** Candidate 3 `prompt video ai` remains parked at Planner
Weak Spot `0`. Candidate 4 `apa itu prompt engineering` was validated in exact
Keyword Explorer report `1576139` and failed volume (`10`). Candidate 5
`contoh prompt ai` passed exact/Golden and was added once to the permanent list,
but Planner `179242` returned Weak Spot `0`. The broad exact `prompt
engineering` term was parked for commercial/job/course intent. A follow-up
AI-video Topic Discovery reports `246781`–`246782` and exact reports
`1576144`–`1576147` found only volume `10`/`0`/`0`/`0` terms. Zamri has now
approved the new generic `prompt-engineering.prompt-writing` family for
`cara tulis prompt ai`; the exact gate is the next action. No candidate is ready
for drafting or publication yet.

## Objective

Find one useful, non-cannibalising Prompt Engineering article and validate it
through the Option C research gates. Stop before Content Creator, drafting,
WordPress, or publication unless Zamri separately approves further work.

## Current research state

| Field | Evidence |
|---|---|
| Candidate 4 | Topic Discovery `246776`; exact Keyword Explorer `1576139`; `apa itu prompt engineering`; volume `10`; **parked at volume** |
| Candidate 5 | Keyword Explorer `1576140`; Golden `1576141`; list row `56`; Planner `179242`; Weak Spot `0`; **parked** |
| Candidate 6 | Topic Discovery `246779`; exact Keyword Explorer `1576142`; volume `1,600`, but job/course/training SERP; **parked for intent** |
| AI-video follow-up | Topic Discovery `246781`–`246782`; exact reports `1576144`–`1576147`; volumes `10`/`0`/`0`/`0`; **parked** |
| Approved pivot | Topic Discovery `246780`; `cara tulis prompt ai` card volume `70`; family `prompt-engineering.prompt-writing`; approval `approval://user/2026-09-13/topic-family/prompt-engineering.prompt-writing` |
| Quota read-back | Topic `68/75`; Keyword `65/75`; Article `69/70`; Keyword Credit `39,677/40,000`; AI Words `7,471/8,000`; list plan `47/50`; seats `2/3` |
| Gate status | **No qualifying registered candidate.** Stop before Content Brief, Content Creator, drafting, WordPress, tracking, or publication. |

Do not treat card volume as exact-keyword evidence. Candidate 4's exact volume
failed, and Candidate 5's Weak Spot failed. The approved pivot must still pass
exact volume, Golden, SERP, and Weak Spot `>=2` before any list, Planner, or
content action.

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
| Guarded continuation | Four bounded `gpt-5.6-luna` worker attempts before the blocked-goal handoff, plus one fresh-resume attempt, received the same provider result: the exact authenticated WriterZen tab was already claimed by session `01a09530-700e-7e90-ac79-abd632d41b36`. No list addition or Planner project was made. |
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

Keep Candidate 3 (`prompt video ai`) and Candidate 5 (`contoh prompt ai`)
parked: both Planner projects returned Weak Spot `0`. Candidate 4 failed exact
volume, and Candidate 6 failed the reader-facing intent gate. The approved
generic prompt-writing family is now ready for its first exact gate.

1. Refresh limits in the existing authenticated tab and validate exact
   `cara tulis prompt ai` in Keyword Explorer.
2. Record exact volume, SERP/intent, and quota delta before deciding on Golden.
3. Add the exact row or create a Planner project only if exact, Golden, SERP,
   and Weak Spot `>=2` all pass.
4. Do not lower Golden or All-in-Title limits, silently override Weak Spot,
   change the category, or begin drafting.

## Browser and credit safeguards

- Use Zamri's already-open authenticated Chrome session. Claim the exact
  WriterZen tab, take a fresh snapshot, and reuse it.
- In this non-strict project, the coordinator may use that exact tab directly
  after a bounded worker fails closed on same-tab ownership, but only for the
  named low-impact lookup or submission, with a route receipt, visible quota or
  cost preflight, and fresh post-action read-back. Do not create, close, or
  replace tabs/profiles, touch credentials or account settings, publish, or
  perform destructive actions.
- If the exact authenticated tab is unavailable, ask Zamri to open or sign in.
  Do not switch to a blank, private, or separate CDP profile.
- Last independently observed on 2026-09-13 after the final quota read-back:
  Topic `68/75`, Keyword `65/75`, Keyword Credit `39,677/40,000`, Article
  `69/70`, AI Words `7,471/8,000`, Keyword List `47/50`, seats `2/3`.
- Keep `Write the whole article` and optional keyword expansion OFF. Do not use
  WriterZen's plagiarism checker.
- Do not retry uncertain submissions. Reload and check for the resulting row
  or project first.

## Relevant worktree paths

| Path | State at the 2026-09-12 handoff | Purpose |
|---|---|---|
| `scripts/verify-editorial-relevance-gate.py` | Tracked; family update pending commit | Registers/tests the approved prompt-writing family plus the two existing Prompt Engineering families |
| `content/content-calendar.md` | Tracked; family approval update pending commit | Records the approved pivot and all parked candidates |
| `content/research/prompt-engineering-2026-09-10-relevance.md` | Tracked and committed | Thumbnail evidence and attestations |
| `content/research/prompt-engineering-ai-video-2026-09-10-research.md` | Tracked and committed | AI-video evidence and volume failure |
| `content/research/prompt-engineering-2026-09-12-relevance.md` | Tracked; updated 2026-09-12 | Candidate 3 exact metrics, Golden/SERP evidence, verified list row, quota, and Planner gate |

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

Baseline: relevance `16 scenarios; 7 pass / 9 fail`; calendar `12 post
entries`; imports PASS; no whitespace errors. Existing LF/CRLF warnings may
print.

## Copy-paste ACP opening prompt

> Read `AGENTS.md` and `content/next-prompt-engineering-vscodium-acp-handoff.md`
> completely, restart Zed if it predates the Context7 registration, and run the
> Context7 readiness prompt for both Codex and Claude. Verify imports, offline
> content status, and the current worktree. Keep Candidates 3 and 5 parked
> because Planner `179241` and `179242` returned Weak Spot `0`; Candidate 4
> failed exact volume and Candidate 6 failed editorial intent. Zamri has approved
> `prompt-engineering.prompt-writing` for the `cara tulis prompt ai` pivot;
> refresh quota and run its one exact Keyword Explorer lookup. Stop before
> Golden/list/Planner/drafting unless the exact, SERP, and Weak Spot gates pass.
> Do not reset, close, or replace the authenticated tab; do not duplicate
> WriterZen records, override Weak Spot, enable keyword expansion, add a
> duplicate Context7 server, or touch unrelated Post #8 files. Report exact
> IDs, metrics, quota changes, Context7 tool-call evidence, tests, and blockers.

## Definition of done for the next ACP session

The research handoff ends with either:

1. **Qualified:** one distinct keyword passes relevance, volume, Golden, SERP,
   and Weak Spot gates and is recorded without duplicates; or
2. **Parked:** the fresh seed yields no qualifying candidate, with exact IDs,
   metrics, quota delta, rejection reasons, and updated evidence; or
3. **Exact gate pending:** the approved family has a current candidate, but exact
   volume and SERP evidence are still required before Golden or downstream work.

This handoff is currently **Exact gate pending**: the family approval is recorded
and the next bounded action is the exact `cara tulis prompt ai` lookup. It does
not authorize drafting or publication by itself.

Neither outcome authorizes drafting or publication.
