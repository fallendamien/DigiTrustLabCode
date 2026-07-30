---
description: Scan a page for accessibility issues and auto-fix what's safe
---

# Accessibility Scan Workflow

**Use when:** You want to audit and fix WCAG accessibility issues on a post or page.

## Steps

1. Identify the target post/page (user provides post ID, slug, or title).
2. Run `respira_scan_page_accessibility` with the post ID.
   - Default standard: `wcag2aa`
   - Optionally specify: `wcag2a`, `wcag21aa`, `wcag22aa`, `section508`
3. Review violations grouped by severity:
   - **Auto-fixable:** missing alt text, unlabeled buttons, broken heading order
   - **Human decisions:** color contrast, link text wording, ARIA semantics
4. If auto-fixable issues found, run `respira_apply_accessibility_fixes` with the `scan_id`.
   - Optionally specify `rule_ids` to fix only specific rules
5. Report to user:
   - What was fixed (rule IDs + elements affected)
   - What needs a human decision (with specific recommendations)

## Notes

- Always snapshot before writing — keep `snapshot_uuid` for rollback
- Do NOT auto-fix color contrast — that's a design decision for the user
- Malaysian audience consideration: ensure Bahasa Melayu text is readable in alt text and labels
