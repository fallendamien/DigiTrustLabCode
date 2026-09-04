# Orchestration gate

Read [the repo-local orchestration adapter](../../docs/ai/orchestration-policy.md)
and the canonical TSOT policy before work. A brief marked `bounded-worker`
executes directly; orchestrator delegation triggers do not apply and nested
delegation remains prohibited.

The default two-lane model permits direct execution of safe, narrow local work
with deterministic verification. Guarded work requires the relevant department,
a current route receipt, required approval, and a bounded worker. The exact
project marker `orchestration_mode: strict` restores the former
orchestration-only behavior.

When delegation occurs, preserve the actual model ID, effort, scope, evidence,
queue/steering rules, and fail-closed behavior from the canonical policy.
Workers must not self-delegate, widen scope, or self-approve.
