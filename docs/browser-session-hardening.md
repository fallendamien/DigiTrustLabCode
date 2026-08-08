# DigiTrust Lab Browser Session Hardening

**Status:** Mandatory first gate for every browser-based DigiTrust Lab workflow.

## Rule

Use the user’s already-open, authenticated Chrome extension session for WriterZen, WordPress, ClickRank, Screpy, Google Search Console, and visual verification. Do not use a separate Chrome DevTools/CDP browser, standalone Playwright browser, blank tab, or unauthenticated fallback.

The in-skill `tab.playwright` API is allowed only after the exact existing Chrome tab has been claimed. It does not authorize starting a separate Playwright browser.

## Required selection sequence

1. Connect through `chrome:control-chrome` and reuse its persistent Chrome binding.
2. Name the browser session before opening or claiming a tab.
3. Call the user-tab list and choose the exact tab by its current title and URL.
4. Claim that exact tab.
5. Take a fresh DOM snapshot and verify the expected authenticated dashboard or site state.
6. Reuse the claimed tab for the rest of the workflow.

If the exact authenticated tab is missing, stop and ask the user to open or sign in to it. Never navigate an arbitrary blank or login tab and treat it as proof of the user’s browser state. Never inspect cookies, local storage, passwords, or session stores.

## Incident record: 2026-08-09

A separate Chrome DevTools connection exposed only a WordPress login tab, while the user’s actual Chrome extension session still had authenticated DigiTrust Lab, ClickRank, and other tabs open. The root cause was selecting the wrong browser surface, not loss of the user’s authentication.

## Prevention check

Before any authenticated workflow action, the agent must be able to identify all three signals from the same claimed tab:

| Signal | Required evidence |
|---|---|
| Browser | Chrome extension session, not a separate DevTools/CDP browser |
| Tab | Exact current title and URL returned by the open-tab list |
| Auth | Fresh visible dashboard/site state, not a login screen |
