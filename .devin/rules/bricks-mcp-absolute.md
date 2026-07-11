---
trigger: always_on
---

# Respira MCP Absolute Priority

**Priority:** CRITICAL — see `AGENTS.md` § PRIORITY #1 for full rule, incident log, and workflow.

## Quick Decision Table

| Use Respira MCP | Use GUI | Use Non-Bricks |
|----------------|---------|---------------|
| Padding, margins, layout | Simple text edits | ❌ NEVER |
| Colors, fonts, typography | Nav label changes | ❌ NEVER |
| Animation, transitions | Page content text | ❌ NEVER |
| Responsive CSS | | ❌ NEVER |
| Mobile menu styling | | ❌ NEVER |
| Footer layout | | ❌ NEVER |

## Skill Activation

When this rule triggers, auto-load:

| Skill | Path | Purpose |
|-------|------|---------|
| `bricks-mcp-absolute` | `.devin/skills/bricks-mcp-absolute/SKILL.md` | MCP tool selection and execution protocol |

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

Templates 185 (Header) and 52 (Blog Archive) are editable via Respira MCP. Respira snapshots before every write.

- Always run `respira_extract_builder_content` before editing
- Keep `snapshot_uuid` from response for rollback via `respira_restore_snapshot`

## Scope Matrix

### ✅ Permitted Scope
- Create and edit WordPress POSTS, PAGES, and Bricks templates via Respira MCP
- Manage menus via Respira MCP menu tools
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins
- Manage media via Respira MCP

### ❌ NOT Permitted
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — decommissioned
- Raw HTML Code elements in Bricks templates (element name "code")
- Inline HTML/CSS/JS pretending to be Bricks elements
- Non-Bricks frameworks (React, Vue, etc.) injected into templates
- Random PHP that doesn't use Bricks APIs or WordPress hooks
- PHP mu-plugins for Bricks tasks
- Any script that modifies static HTML files
