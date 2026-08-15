# Handoff — EA inquiry router is merged but never auto-triggers

**Date:** 2026-08-15
**From:** Claude Opus (orchestrator session)
**To:** Codex
**Status:** Router works when reached by hand. It is never reached automatically.
**Branch:** merged to `master` at `2429045`. Local only — not pushed at time of writing.

---

## 1. What exists

Merged in `6f218d2`, merged to master in `2429045`:

| Path | Role |
|---|---|
| `workspaces/executive-assistant/skills/inquiry-router/SKILL.md` | the router (83 lines) |
| `scripts/verify-ea-inquiry-router.py` | contract test, 7 routing cases |
| `departments/creative/{AGENTS.md,workflow.md,skills/README.md}` | new department |
| `AGENTS.md` § "EA inquiry-routing entrypoint" | the pointer both agents are supposed to follow |

All three verifiers pass on `master`:

```
verify-ea-inquiry-router.py    PASS  7 routing cases; one primary; override,
                                     simple-question, worker, external-action gates
verify-orchestration-policy.py PASS  13 mappings; 4 pointers; caveat present
verify-imports.py              PASS  10 imports, 3 trees, 8 critical files
```

The router's own contract requires each response to state:

```
Route: primary=<department>; secondary=<...|none>
Reason: <why this outcome maps to that department>
Action / evidence: <gate applied, worker dispatched or not>
```

---

## 2. The three tests, and what each proved

Same prompt throughout: **"I want to start sending a monthly email to blog subscribers. Where do I begin?"**

| # | Condition | Routing block? | What it proved |
|---|---|---|---|
| 1 | plain prompt, session on `master`, pre-merge | ❌ absent | file did not exist on that branch — nothing to route with |
| 2 | prompt prefixed with "Read `workspaces/.../inquiry-router/SKILL.md`, then:" | ✅ **present** | **the SKILL.md itself is correct and works** |
| 3 | plain prompt, fresh session, post-merge | ❌ absent | file exists and is on `master`, but is still never loaded |

Test 2 output, verbatim:

```
Route: primary=content; secondary=none
Reason: the requested outcome is planning and drafting a recurring newsletter —
        content owns it. SEO/creative only enter later if you want assets or
        link strategy.
Action / evidence: answered directly per gate step 2 (starting-point question,
        no worker dispatched).
```

Test 2 also correctly separated doc claims from live-verified facts, applied the
`lessons.md` entry on free-tier email recipient restrictions unprompted, and
stopped at "Send" as an external action needing user approval.

**Conclusion: the defect is discovery, not the router.**

---

## 3. Root-cause hypothesis — NOT yet proven, please verify

`workspaces/*/skills/` does not appear to be a scanned skill directory. The
scanned trees are `.claude/skills/` and `.windsurf/skills/`.

Supporting evidence: in the Claude session's available-skills listing,
**every** skill under `.claude/skills/` was present (`malay-voice-guide`,
`write-post`, `readability-pass`, `seo-aeo-amplifier`, …) and **no** skill under
`workspaces/executive-assistant/skills/` was present — not `inquiry-router`,
not `referral-triage`, not `daily-brief`, not `meeting-prep`.

That is consistent with the whole EA skills tree having never been discoverable,
not just the router. **It is an inference from one session's skill listing, not a
measurement.** Confirm before acting:

```bash
ls -la .claude/skills/ | head -30
ls -la .windsurf/skills | head -5        # symlink into the TSOT — check LinkType/Target
ls -la workspaces/executive-assistant/skills/
git log --oneline -- workspaces/executive-assistant/skills/ | tail -5
```

Question worth answering while you are in there: **how were `referral-triage`,
`daily-brief`, and `meeting-prep` ever meant to be reached?** If they never were,
this is a workspace-wide gap and the fix should cover all of them, not just the
router.

---

## 4. Constraint — fix BOTH agents in the same change

Per `.windsurf/rules/tsot-parity.md`, doctrine must reach Claude and Codex
together. The two load by different mechanisms:

- Claude — Skill tool discovery from `.claude/skills/`, plus `@import` via `CLAUDE.local.md`
- Codex — has no Skill tool; reads `AGENTS.md` pointers

So a `.claude/skills/` symlink alone fixes Claude and leaves Codex exactly as
broken as it is now. That one-sided outcome is the specific failure the parity
rule exists to prevent.

Two candidate directions, not mutually exclusive:

1. **Make it discoverable to Claude** — symlink or relocate the EA skills into
   `.claude/skills/`. ⚠️ If you symlink, check `.windsurf/skills` first: it is a
   symlink into the shared TSOT (`agent-templates/workspace/skills`), so anything
   placed there hits **every project on the machine**, and that tree is not a git
   repo. State the blast radius before writing.
2. **Harden the Codex path** — promote the `AGENTS.md` § "EA inquiry-routing
   entrypoint" pointer into the **Tier 1 read-at-session-start** table in
   `AGENTS.md` § "Doctrine Files". Right now it sits in prose partway down the
   file, which is demonstrably too soft — test 3 proves an agent can read
   `AGENTS.md` and still not open the router.

Pick the approach you judge correct; the above is analysis, not a decision.

---

## 5. Definition of done

- [ ] Root cause confirmed by command output, not inference
- [ ] Router auto-triggers on the plain prompt in a fresh **Claude** session — routing block present, no read instruction given
- [ ] Router auto-triggers on the plain prompt in a fresh **Codex** session
- [ ] Decide whether `referral-triage` / `daily-brief` / `meeting-prep` need the same fix
- [ ] `verify-ea-inquiry-router.py`, `verify-orchestration-policy.py`, `verify-imports.py` still exit 0
- [ ] Consider extending a verifier to assert *discoverability*, so this regression cannot recur silently

That last item is the durable fix. Today's verifier proves the router's **logic**
is correct while saying nothing about whether anything ever **loads** it — which
is why three green checks coexisted with a router that had never once fired on
its own.

---

## 6. Do not

- Do not rewrite `inquiry-router/SKILL.md` to fix triggering. Test 2 proves the
  file is correct. The bug is upstream of it.
- Do not edit anything under `.windsurf/` without first resolving the symlink and
  stating the blast radius.
- Do not push. `master` is 4 commits ahead of `origin/master` and the user has
  not asked for a push.
