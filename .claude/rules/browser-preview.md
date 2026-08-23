---
trigger: always_on
description: Pop out browser preview so user can see visual changes in real-time during Bricks template edits or page verification
---

# Browser Preview Rule

**Always use the `browser_preview` tool to pop out the browser** so the user can see changes in real-time while working.

**Authentication rule:** For DigiTrust Lab verification, explicitly use the user's already-open authenticated Chrome extension session — not a blank or private browser. Select and claim the exact existing tab by its current title and URL before navigating or inspecting it. If that tab is unavailable, stop and ask the user to open or sign in to it.

## When to Pop Out

- After navigating to a page for visual verification
- After making Bricks template changes that affect the frontend
- After making changes that affect the frontend
- Any time browser navigation or visual inspection is needed

## Why

The user wants to visually follow along as changes are made, not just see screenshots after the fact.

## Why the Claude in Chrome extension is the path to your authenticated session

Since Chrome 136 (April 2025), `--remote-debugging-port` and `--remote-debugging-pipe` are
silently ignored when Chrome runs on the default user-data-dir. Chrome starts normally, but
never opens the port and never writes `DevToolsActivePort`. Pointing `--user-data-dir` at a
non-default path restores the flags — but that is a different, unauthenticated profile. The
stated motivation was cookie exfiltration via remote debugging
(https://developer.chrome.com/blog/remote-debugging-port).

Consequence: a CDP-based client (chrome-devtools MCP) launched conventionally lands on a blank
profile with none of your sessions. That is expected behavior, not a broken connector.

One supported exception exists: Chrome M144+ added `chrome://inspect/#remote-debugging`, which
lets the user grant a CDP client access to the real profile with an approval prompt per
connection. UNVERIFIED on this setup as of 2026-08-23 — test before relying on it.

Default: authenticated work goes through the Claude in Chrome extension, which is already tied
to your real, signed-in browser session.
