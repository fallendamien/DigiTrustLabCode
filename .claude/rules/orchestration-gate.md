# Orchestration gate

Read [the repo-local orchestration policy](../../docs/ai/orchestration-policy.md)
before substantive work. Codex Sol and Claude Opus orchestrate only; Luna XHigh
may orchestrate but all children must be Luna High. Dispatch substantive work
to bounded workers using host-specific adapters: Codex Sol uses the actual
OpenAI `gpt-5.6-luna` worker at `high` effort by default; Claude Opus may use
the actual Claude `claude-sonnet-4-6` adapter when available. Never label an
OpenAI model as Claude Sonnet. Workers do not self-delegate or approve their
own completion. Announce and report the actual model ID, effort, and evidence.
If the required worker or evidence is unavailable, fail closed or obtain
explicit authorization for a named substitute.
