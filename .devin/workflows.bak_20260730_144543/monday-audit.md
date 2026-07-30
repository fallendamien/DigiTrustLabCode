---
description: Site health snapshot — changed pages, broken stuff, SEO issues, priority list
---

# Monday Morning Audit Workflow

**Use when:** Weekly site health check — typically Monday or start of work session.

## Steps

1. Run `respira_list_pages` to get all pages (check for recent changes).
2. Run `respira_list_posts` to get all posts (check recent publications).
3. For top 5 pages by traffic importance, run `respira_analyze_seo` on each.
4. Run `respira_analyze_pagespeed` on the homepage (optional but recommended).
5. Check for broken or missing elements:
   - Run `respira_bricks_health_check` on key template pages (185, 52, 10)
   - Flag orphaned elements, duplicate IDs, broken references
6. Compile a prioritized report:
   - 🔴 **Critical:** Broken pages, missing content, SEO errors
   - 🟡 **Warning:** Suboptimal scores, outdated content, missing alt text
   - 🟢 **OK:** Things that are fine
7. Present ONE prioritized list of what to fix this week.

## Notes

- This is a READ-ONLY audit — do NOT make any changes without user approval
- Keep the report concise — the user wants a quick overview, not a 20-page document
- If no posts exist yet, skip post-related checks and focus on page/template health
