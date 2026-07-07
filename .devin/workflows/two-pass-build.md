---
description: Build a new page — skeleton first, then fill content section by section
---

# Two-Pass Build Workflow

**Use when:** Building a new content-heavy page (about, landing, services, etc.)

## Pass 1: Skeleton

1. User describes the page type and lists sections in order.
2. Run `respira_build_page` with:
   - Title: user-provided
   - Status: `draft`
   - Structure: sections with placeholder labels for every text module
   - Example: `[{type: "section", children: [{type: "heading", settings: {title: "[HERO TITLE]"}}}]`
3. Read back the structure with `respira_extract_builder_content` to confirm it landed correctly.
4. Report to user: "Skeleton built with X sections. Ready to fill in copy?"

## Pass 2: Fill Content

5. For each section, user provides the actual copy/content.
6. Use `respira_find_element` to locate each placeholder by its label text.
7. Use `respira_update_element` to replace placeholder text with real content.
8. After all sections filled, run `respira_make_responsive` to generate mobile breakpoints.
9. Report to user with preview URL.

## Notes

- Always keep `snapshot_uuid` from each write for rollback
- Build section by section — don't try to fill everything in one giant request
- Use Bricks global classes and theme styles — say "reuse my global classes" when building
- If a section is too large for one call, use `target_path` to append modules into columns
- Status stays `draft` until user explicitly approves publishing
