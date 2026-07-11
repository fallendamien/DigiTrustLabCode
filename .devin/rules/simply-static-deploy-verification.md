---
trigger: always_on
---
# Simply Static Deploy Verification

**Priority:** CRITICAL — Activates before any Simply Static Push or Wrangler deploy.

## Core Principle

NEVER deploy to Cloudflare Pages until the static export is verified fresh. Bricks caches rendered HTML — regen CSS + code signatures alone is NOT enough. You must re-save changed pages before Push, then verify the output files after.

## Mandatory Pre-Push Checklist

1. **Regen Bricks CSS** — Bricks → Settings → Regenerate CSS files
2. **Regen Bricks code signatures** — Bricks → Settings → Regenerate code signatures (accept dialog)
3. **Re-save ALL changed pages/templates** — `respira_update_page` with `status: "publish"` for each changed page/template
4. **Mobile overflow check** — Before pushing, verify no horizontal overflow on mobile:
   - Navigate to each changed page in browser at 375px viewport
   - Run: `document.body.scrollWidth === document.body.clientWidth` — must be `true`
   - If `false` → STOP. Fix overflow before exporting. See TROUBLESHOOTING.md → "CSS Grid 1fr Tracks"
5. **Hit Push** in Simply Static
6. **Verify output** — After export completes, check `D:\Coding Zone\digitrust-lab-static\index.html`:
   - `LastWriteTime` must be TODAY
   - Search for new content keywords (e.g. "warga Malaysia", specific element IDs)
   - If stale → STOP. Re-save page + re-export. Do NOT deploy.
7. **Only then** run `npx wrangler pages deploy . --project-name=digitrust-lab-static`

## Missing Page? Check `additional_urls` + mu-plugin FIRST

If any page is missing or stale in the static output, **do NOT** try Bricks CSS regen, code signature regen, template re-saves, or temp file clearing. None of those fix URL discovery or fetching.

**Two separate problems cause missing pages:**
1. **URL not discovered** — Posts Page (`/blog/`) is suppressed by `get_posts()`. Fix: `additional_urls`.
2. **cURL loopback deadlock** — Local by Flywheel single-threaded PHP-FPM deadlocks when Simply Static tries to fetch `.local` URLs. Fix: mu-plugin `ss-blog-page-fix.php` increases timeout to 90s + allows loopback.

**Correct diagnostic order:**
1. Check static file exists: `D:\Coding Zone\digitrust-lab-static\[path]\index.html`
2. If missing → `respira_get_option(option="simply-static")` → check `additional_urls`
3. If URL is queued but file still missing → check debug log for `cURL error 28` (timeout)
4. Verify mu-plugins exist: `ss-blog-page-fix.php` + `ss-skip-dirs.php`
5. If cURL error 28 persists → nuclear option: `curl -k https://digitrust-lab.local/blog/ -o "D:\Coding Zone\digitrust-lab-static\blog\index.html"` then find-replace URLs

**Permanent `additional_urls` (NEVER remove):**
```
https://digitrust-lab.local/
https://digitrust-lab.local/blog/
```

**Two-layer mental model (NEVER cross these when debugging):**
- Bricks layer (CSS, templates) → controls what page LOOKS like
- Simply Static layer (URLs, crawlers, cURL) → controls whether page is EXPORTED at all

See `TROUBLESHOOTING.md` → "Simply Static — Blog Page Never Exported" for full details.

## Red Flags — STOP

- `index.html` timestamp is NOT today → stale export
- New content keywords NOT found in output → Bricks served cached HTML
- You skipped re-saving pages after regen → export will be stale
- `body.scrollWidth > body.clientWidth` on 375px viewport → mobile overflow not fixed
- **Page missing from export entirely** → check `additional_urls` first, NOT Bricks settings

## Bricks CSS Selector Rules (NEVER violate)

- **Query loop containers lose `id` attributes** — always use `.brxe-{id}` class selectors, NEVER `#brxe-{id}` ID selectors for query loop elements
- **CSS Grid `1fr` expands to fit content** — always use `minmax(0, 1fr)` instead of `1fr` in `grid-template-columns`
- **Grid children need `min-width: 0`** — add `min-width: 0` to grid children to prevent them from expanding tracks

## Skill Activation

When this rule triggers, auto-load:

| Skill | Path | Purpose |
|-------|------|---------|
| `simply-static-deploy-verification` | `.devin/skills/simply-static-deploy-verification/SKILL.md` | Full verification protocol with commands and troubleshooting |
