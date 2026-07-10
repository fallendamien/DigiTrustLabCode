# Simply Static Deploy Verification Skill

## When to Use

Before ANY Simply Static Push or Wrangler deploy. This skill ensures the static export contains fresh content and no Bricks cache issues.

## The Problem

Bricks caches rendered HTML separately from the database. `respira_update_element` changes the DB, but Bricks keeps serving cached HTML to Simply Static's crawler. Regen CSS + code signatures alone does NOT fix this — you must also re-save the page/template.

## Full Protocol

### Step 1: Clear Bricks Cache (Manual GUI)

1. WP Admin → Bricks → Settings
2. Click **"Regenerate CSS files"** button
3. Click **"Regenerate code signatures"** button (accept confirmation dialog)

### Step 2: Re-save All Changed Pages/Templates

For every page or template that was modified in this session:

```
respira_update_page({ id: <page_id>, status: "publish", confirm_live_edit: true, edit_target: "live" })
```

This forces Bricks to re-render the HTML from the updated database content.

**Known page/template IDs:**

| Name | ID | Type |
|------|-----|------|
| Homepage | 280 | Page |
| Header | 185 | Template |
| Footer | 46 | Template |
| Blog Archive | 52 | Template |
| Single Post | 10 | Template |

### Step 3: Run Simply Static Export

- WP Admin → Simply Static → Generate → Click **"Push"** button
- Wait for completion (title shows "Generate" without percentage)

### Step 4: Verify Static Output

Run these PowerShell checks from `D:\Coding Zone\digitrust-lab-static`:

```powershell
# Check 1: index.html timestamp is today
Get-ChildItem "D:\Coding Zone\digitrust-lab-static\index.html" | Format-Table LastWriteTime, Length, Name

# Check 2: New content keywords exist in output
Select-String -Path "D:\Coding Zone\digitrust-lab-static\index.html" -Pattern "warga Malaysia" | Select-Object -First 1

# Check 3: New Bricks element IDs exist
Select-String -Path "D:\Coding Zone\digitrust-lab-static\index.html" -Pattern "brxe-b8bfe4" | Select-Object -First 1
```

### Step 5: Deploy (ONLY if Step 4 passes)

```powershell
# Run from D:\Coding Zone\digitrust-lab-static
npx wrangler pages deploy . --project-name=digitrust-lab-static
```

## If Verification Fails

### Symptom: index.html timestamp is old / content not found

**Cause:** Bricks still serving cached HTML despite regen.

**Fix:**
1. Re-save the page again via Respira
2. Clear Simply Static's internal cache (Simply Static → Utilities → Clear Log)
3. Re-run the export
4. Re-verify

### Symptom: 502 errors during export

**Cause:** Local server overloaded (common with Local by Flywheel on large sites).

**Fix:**
1. Restart Local (Stop site → Start site)
2. Re-run the export

## Key Details

- Static output directory: `D:\Coding Zone\digitrust-lab-static`
- Cloudflare Pages project: `digitrust-lab-static`
- Live URL: `https://www.digitrustlab.com/`
- Wrangler caches previously uploaded files (only changed files get uploaded)
- No `wrangler.toml` needed — uses CLI flags
- Run Wrangler from the static output directory, NOT the repo directory

## Common Mistakes

- ❌ Skipping re-save step (regen alone is NOT enough)
- ❌ Deploying without verifying index.html content
- ❌ Running Wrangler from the wrong directory (`G:\Zamzam Biznez\DigiTrustLabCode` instead of `D:\Coding Zone\digitrust-lab-static`)
- ❌ Searching for `wrangler.toml` (there isn't one)
- ❌ Assuming export success means content is fresh (it doesn't)
