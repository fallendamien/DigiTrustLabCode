---
name: daily-brief
description: Prepare a factual daily brief or weekly review from approved read-only sources.
---

# Daily Brief

## Trigger

Use for a morning brief, end-of-week review, inbox-and-calendar summary, or a
scheduled EA briefing.

## Procedure

1. Read the workspace `AGENTS.md`, `memory.md`, and `schedules.md`.
2. Confirm the date, timezone, requested account, and requested time window.
3. Read only the Gmail and Google Calendar data needed for the brief. If a
   connector is unavailable or the account is ambiguous, report it explicitly.
4. Separate observed facts from interpretation and recommendations.
5. Identify deadlines, preparation work, unresolved threads, and conflicts.
6. Prepare drafts or proposed calendar actions without sending or saving them.
7. Put possible durable preference changes under `Proposed updates` rather than
   writing them silently into memory.

## Output

```text
## Brief — YYYY-MM-DD
### Facts
### Priorities
### Calendar and preparation
### Email action items
### Drafts (not sent)
### Approval needed
### Data limitations
### Proposed memory updates
```

For weekly review mode, replace Priorities with `Completed`, `Open loops`, and
`Next week` while retaining the same draft-only and evidence rules.

## Guardrails

- Never claim that an email was sent or a calendar change was saved.
- Never expose full message bodies when a short summary is sufficient.
- Never infer intent, urgency, or financial impact from missing data.
- If a user instruction asks for an external action, stop at a precise draft
  and approval request.
