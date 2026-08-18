# Operations workflow

## Bounded specialist loop

1. Establish the change boundary, rollback path, affected systems, and approval state.
2. Select one canonical operations skill and read it in full.
3. Execute only the requested bounded change or produce a runbook/checklist.
4. Verify immediately, document evidence, and stop when the next action belongs to another department.

## Delegation decision

An explicitly marked `bounded-worker` brief executes directly within its scope;
nested delegation is prohibited. For orchestrator turns, delegate external,
destructive, irreversible, high-risk, approval-gated, or broad/
independently review-worthy work. Safe narrow local inspection, reversible
edits, focused tests, and ordinary implementation may be owned directly. If
dispatch fails, high-risk and approval-gated work stops; safe local fallback
must disclose the fallback and cannot claim worker validation.

## MCP boundary

Use only the MCP server appropriate to the requested system. For WordPress and
Bricks, Respira is primary and builder-native; never use the decommissioned
Bricks MCP or raw post-processing. External actions remain approval-gated.

## Verification gate

Run `python scripts/verify-imports.py` after doctrine/import/symlink-related
work. Run `python scripts/verify-content-status.py` for live content-status
work, or `--offline` when the task explicitly requires offline verification.
Capture exit codes and summarize failures before handoff.

## Image replacement handoff

For a Creative request to `fix this image`, `audit this image`, or `reupload
the corrected image`, use the existing authenticated Chrome session and the
current attachment ID. In WordPress, open **Media → Edit Media → Replace
Media → Upload a new file**, then use the in-place replacement workflow with
**Just replace the file** and **Keep the date** selected. Preserve the
attachment ID, filename, source URL, title, description, caption, and alt
text. Never create a `-1`, `-2`, or otherwise numbered duplicate when URL
continuity is requested.

After the upload, purge the site image/page cache, then verify all of the
following from fresh reads: the attachment ID and metadata are unchanged, the
original `.png` URL returns the corrected image, the LiteSpeed `.webp`
derivative loads, and the live post renders the corrected asset. If the
authenticated browser cannot attach the file, stop at the handoff page and
ask the user to select the archived file manually. Do not claim completion and
do not fall back to a new media upload.

## Codex handoff

Provide: change scope, files/systems touched, commands and exit codes,
rollback/restore handle, residual risk, and the exact validation or approval
needed next. Codex may reject a handoff with missing evidence.
