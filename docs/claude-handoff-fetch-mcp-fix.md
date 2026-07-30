# Handoff for Claude — Fix broken `devin/fetch` MCP server

**Raised:** 2026-07-30 by Windsurf (Devin)
**Status:** Needs Claude to fix

---

## Problem

The `devin/fetch` MCP server in Devin's config fails with:
```
failed to initialize server: transport error: transport closed
```

## Root Cause (Diagnosed by Windsurf)

The `mcp-server-fetch` Python package has a **broken import** with the latest `mcp` library:

```
ImportError: cannot import name 'McpError' from 'mcp.shared.exceptions'
Did you mean: 'MCPError'?
```

The `mcp` Python SDK renamed `McpError` → `MCPError` in a recent version. The `mcp-server-fetch` package hasn't been updated to match.

## What Was Tried

1. ✅ Confirmed `disabled: false` in config (was set to `true` by Claude during migration — fixed by Windsurf)
2. ✅ Confirmed `uvx` is installed and working (`uv 0.11.24`)
3. ✅ Cleared uv cache (`uv cache clean` — removed 68,775 files, 1.6GB)
4. ✅ Fresh reinstall with `uvx --refresh mcp-server-fetch` — same ImportError
5. ⏳ Attempted `uvx --refresh --with "mcp<1.0" mcp-server-fetch` — was running when user asked to hand off to Claude

## Config Location

```
C:\Users\Zamri\AppData\Roaming\devin\mcp_config.json
```

Current `devin/fetch` entry:
```json
"devin/fetch": {
  "args": ["mcp-server-fetch"],
  "command": "uvx",
  "disabled": false,
  "registry": "devin/fetch"
}
```

## Possible Fixes for Claude

1. **Pin `mcp` version** — Add `--with "mcp<1.0"` to args in the config:
   ```json
   "args": ["--with", "mcp<1.0", "mcp-server-fetch"]
   ```

2. **Use npx equivalent** — If there's an npm-based fetch MCP server

3. **Check for updated `mcp-server-fetch`** — The package may have a newer release that fixes the import

4. **Use a different fetch MCP** — Replace with another web fetch MCP server if the package is abandoned

## Also Fixed (Already Done)

`respira-wordpress` was also `disabled: true` — Windsurf set it to `disabled: false`. User needs to restart Devin for both changes to take effect.

## How This Happened — Claude Disabled 3 MCP Servers in Devin's Config

During the MCP config migration on 2026-07-30, Claude was editing `C:\Users\Zamri\AppData\Roaming\devin\mcp_config.json` — **Devin's MCP config file** — but appears to have treated it as though it were Claude's own config. Claude set `"disabled": true` on **3 servers**:

| Server | Disabled by Claude | Re-enabled by Windsurf | Notes |
|--------|-------------------|----------------------|-------|
| `devin/fetch` | ✅ `disabled: true` | ✅ Fixed | But still broken due to `McpError` import bug (separate issue) |
| `respira-wordpress` | ✅ `disabled: true` | ✅ Fixed | Should work after Devin restart |
| `github-remote` | ✅ `disabled: true` | ✅ Fixed (Claude re-enabled it later) | Was also disabled during migration |

**Key point:** Devin and Claude Desktop have **completely separate MCP config files**:
- Devin: `C:\Users\Zamri\AppData\Roaming\devin\mcp_config.json`
- Claude Desktop: `C:\Users\Zamri\AppData\Roaming\Claude\claude_desktop_config.json`

Disabling servers in Devin's config has zero effect on Claude Desktop, and vice versa. Claude should not have been modifying Devin's config at all for the purpose of managing Claude's own MCP servers.

## Context from LTM

Claude disabled 3 MCP servers (`devin/fetch`, `respira-wordpress`, `github-remote`) in Devin's config during the MCP config migration from Windsurf to Devin paths on 2026-07-30. They were never re-enabled after migration completed. Windsurf discovered and fixed the `disabled` flags, but `devin/fetch` has a separate broken-import issue that still needs Claude's attention.
