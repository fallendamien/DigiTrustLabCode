# Repo-local orchestration adapter

The canonical policy is the TSOT rule at
`C:\my_Projektz\agent-templates\workspace\rules\orchestration-policy.md`.
This file is intentionally a thin project pointer; it does not duplicate the
role matrix or delegation policy.

The default is the canonical two-lane model. Safe, narrow local work may be
executed directly and verified by deterministic checks. External writes,
pushes, history rewrites, destructive or irreversible actions, credentials,
live systems, broad work, and independent review use the guarded lane: select
one department, emit a current route receipt, obtain required approval, and
delegate to a bounded worker. Queue, steering, worker identity, evidence, and
nested-delegation safeguards remain governed by the canonical policy.

The canonical policy also permits a narrow, user-authorized coordinator
fallback for one bounded action in the exact already-open authenticated Chrome
tab when a worker cannot claim that tab. It preserves the route, approval,
quota, evidence, no-new-tab, and no-credential restrictions; strict projects
remain fail-closed.

The exact project marker `orchestration_mode: strict` restores the former
orchestration-only behavior. This project has no such marker, so department
adapters are reusable specialist playbooks on the fast lane and guarded owners
when the risk classification requires it.

## Project adapter

- A brief marked `bounded-worker` executes directly within its bounded scope;
  orchestrator delegation triggers do not apply, and nested delegation remains
  prohibited.
- DigiTrust Lab approval gates, external-write restrictions, department
  boundaries, and evidence requirements remain in `AGENTS.md` and the selected
  department adapter.
- Run `scripts/verify-orchestration-policy.py` after policy changes. It checks
  this pointer and the canonical policy together.
