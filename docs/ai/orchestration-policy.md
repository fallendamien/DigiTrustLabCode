# Repo-local orchestration adapter

The canonical policy is the TSOT rule at
`C:\my_Projektz\agent-templates\workspace\rules\orchestration-policy.md`.
This file is intentionally a thin project pointer; it does not duplicate the
role matrix or delegation policy.

## Project adapter

- A brief marked `bounded-worker` executes directly within its bounded scope;
  orchestrator delegation triggers do not apply, and nested delegation remains
  prohibited.
- DigiTrust Lab approval gates, external-write restrictions, department
  boundaries, and evidence requirements remain in `AGENTS.md` and the selected
  department adapter.
- Run `scripts/verify-orchestration-policy.py` after policy changes. It checks
  this pointer and the canonical policy together.
