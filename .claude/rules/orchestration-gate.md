# Orchestration gate

Read [the repo-local orchestration policy](../../docs/ai/orchestration-policy.md)
before substantive work. Codex Sol and Claude Opus orchestrate only; Luna XHigh
may orchestrate but all children must be Luna Medium. Dispatch substantive work
to bounded workers: Haiku for simple read-only scans, Sonnet for complex
read-only/judgment work, and Luna Medium by default for implementation or
validation. Workers do not self-delegate or approve their own completion. If
the required worker or evidence is unavailable, fail closed.
