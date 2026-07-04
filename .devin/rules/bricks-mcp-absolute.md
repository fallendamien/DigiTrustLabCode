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

## Scope Matrix

### Bricks MCP (THE ONLY TOOL for visual/styling changes)
- Reading/writing templates, elements, global classes, theme styles
- Managing WordPress menus, media, components
- Page-level CSS/JS management
- Design tokens (palettes, variables, typography scales, fonts)
- Padding, margins, layout, responsive CSS, mobile menu styling
- Animation transitions, colors, fonts — ALL visual properties

### NEVER Allowed
- Post-process scripts (PowerShell, Python, or any background code)
- Raw HTML Code elements in Bricks templates (element name "code")
- Inline HTML/CSS/JS pretending to be Bricks elements
- Non-Bricks frameworks (React, Vue, etc.) injected into templates
- Random PHP that doesn't use Bricks APIs or WordPress hooks
- PHP mu-plugins for Bricks tasks
- Any script that modifies static HTML files after Simply Static export

### Allowed (Non-Bricks, deploy only)
- Wrangler CLI for Cloudflare Pages deployment — deploy tool only, not Bricks internal
