# SEO workflow

## Bounded specialist loop

1. Define the URL/site surface, target query or business outcome, and evidence required.
2. Select one canonical SEO skill and read it in full.
3. Produce an audit, prioritized opportunity list, content brief, or change proposal.
4. Stop before implementation when a live-site write, design change, or new research stream is needed; hand it off explicitly.

## MCP boundary

Use Respira MCP for WordPress/site evidence and authorized builder-native SEO
changes. Confirm the active site and use only documented tools from the
canonical skill. Screpy/rank-tracking evidence remains dashboard evidence and
must not be represented as verified by local scripts.

## Verification gate

Check search intent, source URLs, internal-link targets, metadata constraints,
and evidence timestamps. For repository changes, run
`python scripts/verify-imports.py`; for content-status-sensitive work, also run
`python scripts/verify-content-status.py` or `--offline` when explicitly
offline.

## Codex handoff

Provide: target surface, findings with evidence, prioritized fixes, items that
need user judgment, and the proposed validation command. Codex validates
mechanical correctness and scope; it does not turn recommendations into live
changes without authorization.
