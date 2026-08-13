---
trigger: always_on
description: Pop out browser preview so user can see visual changes in real-time during Bricks template edits or page verification
---

# Browser Preview Rule

**Always use the `browser_preview` tool to pop out the browser** so the user can see changes in real-time while working.

**Authentication rule:** For DigiTrust Lab verification, the preview must remain tied to the user's already-open authenticated Chrome extension session. Do not substitute a separate Chrome DevTools/CDP browser, standalone Playwright browser, or blank/login tab. Select and claim the exact existing tab by its current title and URL before navigating or inspecting it. If that tab is unavailable, stop and ask the user to open or sign in to it.

## When to Pop Out

- After navigating to a page for visual verification
- After making Bricks template changes that affect the frontend
- After making changes that affect the frontend
- Any time browser navigation or visual inspection is needed

## Why

The user wants to visually follow along as changes are made, not just see screenshots after the fact.
