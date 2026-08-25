# Orchestration gate

Read [the repo-local orchestration adapter](../../docs/ai/orchestration-policy.md)
and the canonical TSOT policy before work. A brief marked `bounded-worker`
executes directly; orchestrator delegation triggers do not apply and nested
delegation remains prohibited.

Claude Opus is an orchestrator-only role for substantive work. Delegate every
tool, browser action, edit, external write, test, and verification command to a
bounded worker, including safe narrow local inspection, reversible edits,
focused tests, and ordinary implementation. The orchestrator owns
requirements, routing, worker briefs, supervision, integration, final
decisions, and evidence evaluation only. When delegation occurs, report the
actual model ID, effort, scope, and evidence; workers must not self-delegate,
widen scope, or self-approve.

For queued or steered work, dispatch unrelated items to another bounded worker,
use multiple workers for independent items when slots permit, and send related
additions to the existing relevant worker. If no slot is available, queue the
item and dispatch it when a slot frees; never execute it inline. If dispatch
fails, stop all substantive execution and fail closed.
