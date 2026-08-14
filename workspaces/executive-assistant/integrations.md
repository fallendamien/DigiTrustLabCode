# Executive Assistant Integrations

## Pilot scope

The first pilot is designed for Gmail and Google Calendar. Both integrations
are read-first and account-explicit. If more than one account is connected,
the EA must identify the account before reading or proposing an action.

### Gmail

Allowed in the pilot:

- read selected messages needed for triage, briefings, or meeting preparation;
- summarize threads and extract action items;
- prepare reply drafts for user review.

Not allowed without approval:

- sending, replying, forwarding, deleting, archiving, or labelling messages;
- changing filters, signatures, permissions, or account settings.

### Google Calendar

Allowed in the pilot:

- read events and availability;
- identify preparation needs and conflicts;
- prepare a proposed event or change for approval.

Not allowed without approval:

- creating, changing, cancelling, or inviting attendees to events;
- sending calendar notifications.

## Deferred adapters

Notion, Granola, and Stripe remain future adapters. Their eventual scopes must
follow the same read-first, explicit-account, approval-gated contract before
they are connected.

## Connector failure behavior

If an integration is unavailable, expired, ambiguous, or returns incomplete
data, report that limitation and continue only with the sources that are
available. Never infer missing messages, events, recipients, or financial
facts.
