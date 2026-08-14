# Departments

This directory is the repo-local routing layer for bounded specialist work. It
organizes existing skills; it does not replace or duplicate the canonical
skills in `.claude/skills/` or the shared TSOT exposed through `.windsurf/skills/`.

All department work is subject to the [orchestration-only policy](../docs/ai/orchestration-policy.md):
orchestrators dispatch bounded workers and integrate evidence; they do not do
substantive work directly.

## Routing contract

1. **Classify automatically.** Claude identifies the task's primary outcome and
   routes it to the matching department below.
2. **Honor an explicit override.** If the user says `department: content`,
   `department: seo`, `department: operations`, or `department: research`, use
   that department unless the request is impossible or unsafe; explain any
   required cross-department handoff.
3. **Use one primary department.** Add secondary departments only when a
   concrete handoff is required. The primary department owns the user-facing
   result.
4. **Load pointers, not copies.** Read the selected department's `skills/README.md`,
   then read the referenced canonical skill before executing it.
5. **Run the department gate.** Follow `workflow.md`; do not claim completion
   without the listed verification evidence.

| Department | Route when the primary outcome is | Contract |
|---|---|---|
| `content` | Planning, drafting, editing, publishing, or content voice | [content/AGENTS.md](content/AGENTS.md) |
| `seo` | Search visibility, on-page SEO, AEO, links, or audits | [seo/AGENTS.md](seo/AGENTS.md) |
| `operations` | Site operations, safety, deployment, change propagation, or reporting | [operations/AGENTS.md](operations/AGENTS.md) |
| `research` | Discovery, competitors, audience, evidence gathering, or strategy inputs | [research/AGENTS.md](research/AGENTS.md) |

## Cross-department handoff

The originating department records the goal, evidence collected, open
decisions, and requested next action. The receiving department validates the
handoff against its own `AGENTS.md` and owns its own verification gate.

External writes remain subject to the project rules and user approval. The
department layer never broadens an MCP tool's authority.
