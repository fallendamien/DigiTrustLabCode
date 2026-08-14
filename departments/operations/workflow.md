# Operations workflow

## Bounded specialist loop

1. Establish the change boundary, rollback path, affected systems, and approval state.
2. Select one canonical operations skill and read it in full.
3. Execute only the requested bounded change or produce a runbook/checklist.
4. Verify immediately, document evidence, and stop when the next action belongs to another department.

## MCP boundary

Use only the MCP server appropriate to the requested system. For WordPress and
Bricks, Respira is primary and builder-native; never use the decommissioned
Bricks MCP or raw post-processing. External actions remain approval-gated.

## Verification gate

Run `python scripts/verify-imports.py` after doctrine/import/symlink-related
work. Run `python scripts/verify-content-status.py` for live content-status
work, or `--offline` when the task explicitly requires offline verification.
Capture exit codes and summarize failures before handoff.

## Codex handoff

Provide: change scope, files/systems touched, commands and exit codes,
rollback/restore handle, residual risk, and the exact validation or approval
needed next. Codex may reject a handoff with missing evidence.
