# Repo-local orchestration adapter

The canonical policy is the TSOT rule at
`C:\my_Projektz\agent-templates\workspace\rules\orchestration-policy.md`.
This file is intentionally a thin project pointer; it does not duplicate the
role matrix or delegation policy.

Codex Sol and Claude Opus are orchestration-only for substantive work. Tool,
browser, edit, external-write, test, and verification execution is delegated
to bounded workers; the orchestrator evaluates returned evidence and owns the
final decision. Queued or steered items follow the canonical queue and steering
gate; no orchestrator fallback is permitted when dispatch is unavailable.
If Sol is unavailable, only the canonical `gpt-5.6-luna` `xhigh`/`max`
substitute-orchestrator path may be used, with the same strict gate.

## Project adapter

- A brief marked `bounded-worker` executes directly within its bounded scope;
  orchestrator delegation triggers do not apply, and nested delegation remains
  prohibited.
- DigiTrust Lab approval gates, external-write restrictions, department
  boundaries, and evidence requirements remain in `AGENTS.md` and the selected
  department adapter.
- Run `scripts/verify-orchestration-policy.py` after policy changes. It checks
  this pointer and the canonical policy together.
