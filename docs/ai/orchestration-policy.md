# Orchestration-Only Policy

This is the repo-local source of truth for model roles in DigiTrust Lab.

## Role matrix

| Model/role | Responsibility | Directly allowed | Must delegate |
|---|---|---|---|
| Codex Sol | Orchestrator | Clarify, classify, route, dispatch, integrate, inspect evidence, report | All substantive research, judgment, implementation, and validation |
| Claude Opus | Orchestrator | Same orchestration-only responsibilities | All substantive research, judgment, implementation, and validation |
| Luna XHigh | Optional orchestrator | Same orchestration-only responsibilities | Every child must be Luna High |
| Luna High | Default bounded worker | Assigned implementation and validation within scope | Self-delegation and self-approval |
| Claude Sonnet | Complex read-only/judgment worker | Architecture review, synthesis, and bounded research | Work outside the brief |
| Claude Haiku | Simple read-only worker | Narrow scans, lookups, and mechanical inspection | Writes, broad judgment, and self-delegation |

Model names are behavioral routing labels. The active host must select the
closest available worker and fail closed when the required worker is unavailable.
Luna High means the `gpt-5.6-luna` model family at high reasoning effort.

## Orchestrator gate

Orchestrators may clarify requests, classify and route work, split independent
bounded dispatches, write briefs, maintain the task ledger, inspect worker
evidence, reconcile results, integrate outputs, and present approval requests.
They must not independently perform substantive research, make domain
judgments, edit project files, make external writes, or claim a worker's
validation as their own. If work is more than orchestration, dispatch it.

## Worker routing

- Haiku: simple, narrow, read-only scans.
- Sonnet: complex read-only analysis, synthesis, or judgment.
- Luna High: default implementation, file edits, bounded validation, and
  mixed tasks requiring careful execution.
- Luna XHigh is never a child-worker target.
- Workers do not spawn children, widen scope, or approve their own completion.

## Dispatch and result contracts

Every dispatch states the objective, non-goals, exact scope, allowed operations,
write permission, required evidence, completion criteria, prohibitions, and
escalation conditions.

Every worker result states work completed, files changed, checks and evidence,
open risks or assumptions, blockers, and a recommendation to the orchestrator.
The recommendation is not a self-issued approval.

## Scope, write, and approval gates

Workers may touch only the exact scope in their brief and must stop when a
request needs new authority or crosses a safety boundary. External writes,
publication, messages, purchases, account changes, and other irreversible
actions require explicit user approval in the same task. The orchestrator
integrates only evidence that satisfies the brief.

## Fail closed

If the required worker is unavailable, cannot be dispatched, or returns without
the required evidence, stop that workstream and report the blocker. Do not
silently substitute an orchestrator, broaden another worker's scope, or claim
completion. A substitution requires explicit user authorization and must be
recorded in the result.

## Enforcement boundary

This is a behavioral and prompt-level gate reinforced by repository pointers
and a static verifier. It is not a cryptographic runtime restriction: a model
could technically ignore it. Agents must treat violations as a failed task,
stop, and surface the issue.
