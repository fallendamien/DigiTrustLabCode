# Zed ACP handover — next Prompt Engineering article

**Prepared:** 2026-09-13
**Project:** `G:\Zamzam Biznez\DigiTrustLabCode`
**Target agents:** Codex ACP or Claude Code terminal/ACP in Zed
**Current outcome:** Post #13, `Contoh Prompt AI: Cara Menulis Arahan yang Jelas
dan Berkesan`, is published at
`https://digitrustlab.com/contoh-prompt-ai/` (WordPress ID `734`) from the
approved generic `prompt-engineering.prompt-writing` family. Exact keyword,
Golden, SERP and Weak Spot gates passed for `contoh prompt`; the outline-only
WriterZen handoff, native draft, media, Rank Math, live structure and dual
naturalness gates are verified. The ClickRank standard row (count `12 → 13`, ID
`14ed7c5c3cd2a51ccabfbf5683e250f9`) and AI Overview row (count `11 → 12`,
`Pending`) are verified. Screpy MCP rows `728617` (Mobile) and `728618`
(Desktop) are both `completed` for MY/ms. The two approved contextual inbound
links are now applied and independently verified. Post 437 links to Post 734
with anchor `panduan umum menulis prompt AI`; Post 536 links to Post 734 with
anchor `asas menulis prompt AI`. Respira snapshots and exact-diff read-backs are
recorded in the completion summary. Search Console Test Live URL passed and the
Google Index surface reports the URL as indexed.

## Objective

Post #13 is closed out. Start the next editorial cycle at the relevance gate;
do not reopen the parked
WriterZen candidates or create a duplicate Planner project.

## Current research state

| Field | Evidence |
|---|---|
| Candidate 4 | Topic Discovery `246776`; exact Keyword Explorer `1576139`; `apa itu prompt engineering`; volume `10`; **parked at volume** |
| Candidate 5 | Keyword Explorer `1576140`; Golden `1576141`; list row `56`; Planner `179242`; Weak Spot `0`; **parked** |
| Candidate 6 | Topic Discovery `246779`; exact Keyword Explorer `1576142`; volume `1,600`, but job/course/training SERP; **parked for intent** |
| AI-video follow-up | Topic Discovery `246781`–`246782`; exact reports `1576144`–`1576147`; volumes `10`/`0`/`0`/`0`; **parked** |
| Approved family | `prompt-engineering.prompt-writing`; approval `approval://user/2026-09-13/topic-family/prompt-engineering.prompt-writing` |
| Published candidate | `contoh prompt` — Topic Discovery `246783`; exact `1576173`; Golden `1576174`; Planner `179243`; Weak Spot `2` |
| WordPress | Post `734`, live URL `https://digitrustlab.com/contoh-prompt-ai/`; featured Media `730`, inline Media `731/732/733` |
| Live gates | Naturalness PASS, structure PASS, voice 0 errors/one italic warning, Rank Math `92/A`, GSC Test Live `URL is available to Google` / `Page can be indexed`, Google Index `URL is on Google` / `Page is indexed` |
| Remaining gates | ClickRank standard + AI Overview and Screpy Device Both are verified; ClickRank Pages read-only check found no exact URL record; inbound link gate passes with two source posts |
| Quota read-back after article | Topic `67/75`; Keyword `59/75`; Article `68/70`; Keyword Credit `39,625/40,000`; AI Words `7,236/8,000`; list `47/50`; seats `2/3` |
| Gate status | **Post #13 is fully closed out; live tracking, approved inbound links, validators, commit, push, and remote parity are verified.** |

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

The three tracker surfaces and the approved inbound-link closeout have now been
submitted/applied once and independently verified. Repository commit/push
closeout is complete. Do not reopen the parked
WriterZen candidates, spend further credits, or use whole-article generation.

### Remaining cards from report 246697

| Exact visible wording | Card volume | Decision |
|---|---:|---|
| `tips prompt ai: kepentingan konteks untuk penghasilan` | `10` | Best remaining concept, but below the relaxed volume threshold of 50 |
| `kuasai prompt seni memimpin ai untuk pelajar ipt` | `10` | Awkward wording and uncertain academic/product intent |
| `teknik prompting yang digunakan oleh prompt engineer openai` | `N/A` | Advanced and potentially overlapping with Post #3 |

The previous seed is exhausted. Do not force one of these into production.

## Recommended continuation

1. Keep the ClickRank standard, AI Overview and Screpy verification recorded:
   standard count `12 → 13` with row ID
   `14ed7c5c3cd2a51ccabfbf5683e250f9`, AI Overview count `11 → 12` with
   `Pending`, and Screpy rows `728617`/`728618` completed for MY/ms. The
   ClickRank Pages read-only search returned no exact URL record, so no
   recommendation was applied.
2. Keep the approved inbound-link evidence: Post 437 → Post 734 with anchor
   `panduan umum menulis prompt AI`; Post 536 → Post 734 with anchor `asas
   menulis prompt AI`; link review `content/link-reviews/contoh-prompt-ai.json`;
   link gate passes with inbound count `2`.
3. Update `content/content-calendar.md`, `STATE.json`, `NEXT.md`, `ROADMAP.md`,
   and `content/article-completion-summaries/contoh-prompt-ai.md` with the final
   inbound decision evidence, then run the complete validator set and
   commit/push only classified durable paths.
4. After Post #13 closeout, restart future work at editorial relevance and
   Topic Discovery; keep Candidates 3–6 and the AI-video sweep parked as
   recorded in the research evidence.

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
- Last independently observed on 2026-09-13 after the Post #13 article:
  Topic `67/75`, Keyword `59/75`, Keyword Credit `39,625/40,000`, Article
  `68/70`, AI Words `7,236/8,000`, Keyword List `47/50`, seats `2/3`.
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

Baseline: relevance `16 scenarios; 7 pass / 9 fail`; calendar `13 post
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

This handoff is currently **Post #13 COMPLETE; next article starts at editorial
relevance**: the
approved family already produced the published `contoh prompt` article, and its
exact, Golden, SERP, Weak Spot, outline, naturalness, structure, voice, Rank
Math, Search Console, ClickRank/Screpy and two approved contextual inbound links
are recorded above. Commit `e12401d2a380849f63dff7b28d5aa2610c39adca` is pushed
to `origin/master`; final worktree and remote parity are clean. Keep the
ClickRank Pages no-record result documented, and start the next article with
editorial relevance and Topic Discovery.
Do not reopen the parked candidates or create a duplicate Planner project.

Neither outcome authorizes drafting or publication.
