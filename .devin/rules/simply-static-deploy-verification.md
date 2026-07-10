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
4. **Hit Push** in Simply Static
5. **Verify output** — After export completes, check `D:\Coding Zone\digitrust-lab-static\index.html`:
   - `LastWriteTime` must be TODAY
   - Search for new content keywords (e.g. "warga Malaysia", specific element IDs)
   - If stale → STOP. Re-save page + re-export. Do NOT deploy.
6. **Only then** run `npx wrangler pages deploy . --project-name=digitrust-lab-static`

## Red Flags — STOP

- `index.html` timestamp is NOT today → stale export
- New content keywords NOT found in output → Bricks served cached HTML
- You skipped re-saving pages after regen → export will be stale

## Skill Activation

When this rule triggers, auto-load:

| Skill | Path | Purpose |
|-------|------|---------|
| `simply-static-deploy-verification` | `.devin/skills/simply-static-deploy-verification/SKILL.md` | Full verification protocol with commands and troubleshooting |
