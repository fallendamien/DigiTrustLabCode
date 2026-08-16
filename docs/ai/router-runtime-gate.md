# EA Router Runtime Gate

The inquiry router remains a prompt-level coordinator; it cannot revoke a
tool's permission at runtime. This gate makes the boundary observable and
fail-closed in review.

## Required receipt

The first assistant output for every new substantive turn must contain:

```text
Route: primary=<content|seo|operations|research|creative>; secondary=<none or concrete handoff>
Route ID: <stable turn/thread identifier>
Router version: 2026-08-16
Scope: <bounded outcome and stop boundary>
Allowed systems: <systems or files this turn may touch>
External writes: <yes|no>
```

The receipt must precede tools, browser actions, connectors, delegation, and
external writes. A non-`none` secondary requires a concrete `Handoff / approval:`
line. Workers inherit the `route_id`, department, scope, allowed systems,
required evidence, and stop conditions, and must attest to them in their result.

## Freshness and compaction

If the router, root policy, or selected department policy is newer than the
session, the agent rereads it and emits a current-version receipt. Compaction,
context reset, or a changed objective starts a new routing boundary. The audit
does not treat a cached URL, a tool success, or an unobservable encrypted
assistant message as proof of compliance.

## Audit

Run the deterministic self-test:

```powershell
python scripts/verify-ea-router-runtime.py --self-test
```

Audit a transcript at the end of a task:

```powershell
python scripts/verify-ea-router-runtime.py --session-log <session.jsonl>
```

Exit code 1 means the evidence is incomplete or stale. It is then a stop-and-
reinitialize condition, not a reason to infer that routing happened.
