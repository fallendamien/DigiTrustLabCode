---
trigger: always_on
---

# Bricks Standard Guide

## 📖 Bricks Builder Guide (REFERENCE FILE)

**`BRICKS-BUILDER-GUIDE.md`** is the local reference for Bricks element settings, style properties, animations, query loops, forms, components, popups, and gotchas.

**ALWAYS read `BRICKS-BUILDER-GUIDE.md` before editing Bricks elements via MCP.** It documents:
- Element settings schema (content vs style properties, underscore prefix rules)
- Layout element caveats (`_gap`/`_display` don't work on section/container/block — use `_cssCustom`)
- Custom CSS selector format (`#brxe-{id}`, NOT `%root%`)
- Key gotchas that prevent trial-and-error (e.g. `_maxWidth` doesn't exist → use `_widthMax`)
- Animation/interaction patterns, query loops, forms, WooCommerce, popups, and more

> ⚠️ Tool names in `BRICKS-BUILDER-GUIDE.md` refer to the old Bricks MCP (decommissioned 2026-07-05). Use equivalent Respira tools instead.

## MCP Server Reference (Respira)

| MCP Tool | Purpose |
|----------|---------|
| `respira_get_site_context` | Read WordPress site details and run diagnostics |
| `respira_get_builder_info` | Detect active builder and version |
| `respira_extract_builder_content` | Read full page/template element tree |
| `respira_update_element` | Update a specific element's settings |
| `respira_find_element` | Find element by ID, type, class, or content |
| `respira_update_bricks_global_class` | Manage Bricks global classes |
| `respira_update_bricks_color_palette` | Manage Bricks color palette |
| `respira_update_bricks_theme_styles` | Manage Bricks theme styles |
| `respira_upload_media` | Upload media to library |
| `respira_list_menus` / `respira_create_menu_item` | WordPress menu management |
| `respira_restore_snapshot` | Rollback any write using `snapshot_uuid` |

**MCP Endpoint:** `https://digitrust-lab.local` (Respira auto-negotiates `/wp-json/respira/v2`)

