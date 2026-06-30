# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: GUI-First Policy (CRITICAL)

**RULE: Always prefer WordPress/Bricks GUI over code for content and layout changes.**

This is a blogging business project, NOT a development project. The user does not want to deal with raw code hassles when the same result can be achieved through the WordPress or Bricks Builder GUI.

### Decision Matrix

| Task | Use GUI | Use Code | Why |
|------|---------|----------|-----|
| Change nav labels | ✅ Bricks → Header template → edit text | ❌ | 2 min in GUI vs 45 min in code |
| Edit page content | ✅ WordPress → Pages → edit | ❌ | Standard WP editing |
| Change footer links/labels | ✅ Bricks → Footer template → edit | ❌ | 2 min in GUI |
| Add/remove pages | ✅ WordPress → Pages | ❌ | Standard WP |
| Change colors/typography | ✅ Bricks → Settings → Custom CSS | ❌ | Visual editor |
| Add/remove nav items | ✅ Bricks → Header template | ❌ | Drag and drop |
| Search bar injection | ❌ | ✅ PowerShell | Simply Static strips forms — no GUI fix |
| Double-slash link fix | ❌ | ✅ PowerShell | Simply Static bug — no GUI fix |
| Post-processing pipeline | ❌ | ✅ PowerShell | Automates export fixes across 100+ files |
| Deploy to Cloudflare | ❌ | ✅ Wrangler CLI | Faster than dashboard upload |

### Protocol

```
BEFORE writing any code for this project, ask:

1. Can this be done in the Bricks Builder GUI? → If YES, guide the user to do it there
2. Can this be done in the WordPress admin GUI? → If YES, guide the user to do it there
3. Is this a Simply Static export bug with no GUI fix? → ONLY THEN use code
4. Is this a bulk automation task across many files? → ONLY THEN use code
```

### What Happened (Lesson Learned)

The previous sessions spent 45+ minutes writing PHP mu-plugins, dealing with serialized arrays, `wp_hash()` signatures, and DB queries — for tasks that would have taken **2 minutes in the Bricks GUI** (changing nav labels, editing page text, updating footer links).

**The code approach was needed initially** because the header was broken (missing signature, corrupted data). But once the header was working, all subsequent content edits (Tentang→Tentang Kami, Hubungi→Hubungi Kami, Zamri→Zed, 2024→2022, Privasi→Polisi Privasi) should have been done in the GUI.

### The Correct Workflow

```
1. Make content/layout changes in WordPress or Bricks GUI
2. Run Simply Static export (WP Admin → Simply Static → Generate)
3. Run post-process-static.ps1 (PowerShell — fixes export-only bugs)
4. Deploy via wrangler CLI
```

### When Code IS Appropriate

- `post-process-static.ps1` — fixes Simply Static export bugs (form stripping, double-slash links)
- Wrangler CLI deploy — faster than dashboard
- One-shot DB fixes when Bricks GUI can't access broken data
- Bulk find/replace across 100+ static HTML files

## Default Expectations

- Verify important code changes before claiming completion.
- Keep reusable workflows in shared TSOT when they are useful across projects.
- Keep project-specific decisions and constraints in this repo.
- Prefer updating shared skills and workflows at the source when they should apply everywhere.

## Communication Preferences

- Prefer visually engaging responses with clear structure when helpful.
- Use relevant emojis for headings, status, and scannability instead of plain wall-of-text responses.
- Keep technical explanations clear, but make the presentation feel lively and easy to scan.

## Troubleshooting Reference (CRITICAL)

**This is a blogging business project, NOT a development project.**

- **ALWAYS** read `TROUBLESHOOTING.md` at session start before working on this project
- **ALWAYS** check `TROUBLESHOOTING.md` before suggesting fixes or approaches — documented issues may already have solutions
- **ALWAYS** append new issues to `TROUBLESHOOTING.md` when encountering problems that took >5 minutes to resolve
- **DO NOT** use global `lessons.md` for this project — all project-specific issues stay in `TROUBLESHOOTING.md`
- **DO NOT** create separate troubleshooting files — one file, appended chronologically

### Quick Reference

| File | Purpose |
|------|---------|
| `TROUBLESHOOTING.md` | All known issues, fixes, and prevention rules |
| `DESIGN.md` | Design system source of truth (colors, typography, components) |

## Notes

- This is a WordPress + Simply Static + Cloudflare Pages blog, not a traditional codebase
- Static files live in `D:\Coding Zone\digitrust-lab-static`
- WordPress local URL: `https://digitrust-lab.local`
- Live URL: `https://blog.digitrustlab.com`
- Deploy command: `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`
