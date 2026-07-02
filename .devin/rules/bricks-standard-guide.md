---
trigger: always_on
---

# Bricks Standard Guide

## 📖 Bricks Builder Guide (REFERENCE FILE)

**`BRICKS-BUILDER-GUIDE.md`** is the local reference for Bricks MCP element settings, style properties, animations, query loops, forms, components, popups, and gotchas.

**ALWAYS read `BRICKS-BUILDER-GUIDE.md` before editing Bricks elements via MCP.** It documents:
- Element settings schema (content vs style properties, underscore prefix rules)
- Layout element caveats (`_gap`/`_display` don't work on section/container/block — use `_cssCustom`)
- Custom CSS selector format (`#brxe-{id}`, NOT `%root%`)
- Key gotchas that prevent trial-and-error (e.g. `_maxWidth` doesn't exist → use `_widthMax`)
- Animation/interaction patterns, query loops, forms, WooCommerce, popups, and more

This file saves significant time by preventing common MCP mistakes.

## MCP Server Reference

| MCP Tool | Purpose |
|----------|---------|
| `get_site_info` | Read WordPress site details and run diagnostics |
| `get_builder_guide` | Read the Bricks builder guide before editing content |
| `bricks` | Manage Bricks settings, schema, queries, references |
| `content` | Manage WordPress and Bricks content (posts, pages, elements) |
| `template` | Manage Bricks templates, conditions, template taxonomies |
| `design` | Manage Bricks design tokens (classes, styles, palettes, variables, fonts) |
| `media` | Upload media, search Unsplash, manage library |
| `menu` | WordPress menu management |
| `component` | Bricks component (reusable element) management |
| `woocommerce` | WooCommerce page templates and product layouts |
| `code` | Page-level CSS and JavaScript |

**MCP Endpoint:** `https://digitrust-lab.local/wp-json/bricks-mcp/v1/mcp`

