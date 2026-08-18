# Orchestration gate

Read [the repo-local orchestration adapter](../../docs/ai/orchestration-policy.md)
and the canonical TSOT policy before work. A brief marked `bounded-worker`
executes directly; orchestrator delegation triggers do not apply and nested
delegation remains prohibited.

Delegate external, destructive, irreversible, high-risk, approval-gated, or
broad/independently review-worthy work. Safe narrow local inspection,
reversible edits, focused tests, and ordinary implementation may be owned
directly. When delegation occurs, report the actual model ID, effort, scope,
and evidence; workers must not self-delegate, widen scope, or self-approve.

If dispatch fails, high-risk or approval-gated work stops. Safe local fallback
may continue only when disclosed, in preserved scope, and without claiming
worker validation.
