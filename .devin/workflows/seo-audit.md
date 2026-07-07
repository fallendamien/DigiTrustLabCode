---
description: Run SEO analysis on a post and fix mechanical issues
---

# SEO Audit Workflow

**Use when:** You want to audit and fix SEO issues on a specific post or page.

## Steps

1. Identify the target post/page (user provides post ID, slug, or title).
2. Run `respira_analyze_seo` with the post ID.
3. Review the findings and categorize:
   - **Mechanical fixes** (auto-fixable): title tag, meta description, heading hierarchy, image alt text, internal links
   - **Judgment calls** (needs human): keyword strategy, content gaps, competitive positioning
4. Apply mechanical fixes using `respira_update_element` or `respira_update_post`.
5. If Rank Math is active, run `respira_analyze_rankmath` for additional scoring.
6. Report to user:
   - What was fixed (with evidence)
   - What needs a human decision (with recommendations)

## Notes

- Always snapshot before writing — keep `snapshot_uuid` for rollback
- Do NOT auto-fix keyword strategy or content decisions — surface those to the user
- If the post has no featured image, flag it (design spec rule #2: 1200×630px required)
