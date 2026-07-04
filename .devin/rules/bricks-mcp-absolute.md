---
trigger: always_on
---

# Bricks MCP Absolute Priority

**Priority:** CRITICAL — see `AGENTS.md` § PRIORITY #1 for full rule, incident log, and workflow.

## Quick Decision Table

| Use Bricks MCP | Use GUI | Use Non-Bricks |
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

## 🔴 FROZEN TEMPLATES (185 & 52)

**Templates 185 (Header) and 52 (Blog Archive) are FROZEN.**

Do NOT:
- Read, write, or open these templates in Bricks GUI
- Use `content:update_content` on post_id 185 or 52
- Attempt to fix, modify, or restore them via any method

If a task requires changes to these templates, **STOP and tell Zamri**: "This requires touching a frozen template. Escalate to Claude."

## Scope Matrix

### ✅ Permitted Scope
- Create and edit WordPress POSTS and PAGES (content only, not Bricks templates)
- Manage menus via Bricks MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins (not Bricks templates)
- Manage media via Bricks MCP

### ❌ NOT Permitted
- Write to template IDs 185 or 52 via any method
- Open template 185 or 52 in the Bricks visual editor
- Use `content:update_content` on post_id 185 or 52
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Raw HTML Code elements in Bricks templates (element name "code")
- Inline HTML/CSS/JS pretending to be Bricks elements
- Non-Bricks frameworks (React, Vue, etc.) injected into templates
- Random PHP that doesn't use Bricks APIs or WordPress hooks
- PHP mu-plugins for Bricks tasks
- Any script that modifies static HTML files after Simply Static export

### Allowed (Non-Bricks, deploy only)
- Wrangler CLI for Cloudflare Pages deployment — deploy tool only, not Bricks internal
