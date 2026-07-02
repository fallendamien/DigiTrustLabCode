---
description: Audit static export for bloat and unnecessary files
---

# Bloat Check — Static Export Audit

Run a full audit of `D:\Coding Zone\digitrust-lab-static` to identify unnecessary files inflating deployment size.

## Steps

// turbo

1. Count total files in the static export directory
2. Break down by top-level directory (file count + size in MB)
3. Check that existing optimizations are working:
   - `wp-includes/blocks/` should NOT exist (removed by Phase 8)
   - `wp-content/themes/bricks/assets/svg/builder/` should NOT exist (excluded by mu-plugin)
   - `wp-includes/js/` should only contain emoji files (stripped by Phase 9)
   - `wp-includes/images/` should NOT exist (stripped by Phase 9)
   - `wp-includes/css/` should NOT exist (stripped by Phase 9)
   - `wp-content/plugins/seo-by-rank-math/` should NOT exist (stripped by Phase 10)
4. Scan all HTML files for actual `wp-includes/` and `wp-content/plugins/` references to find files that ARE loaded by the frontend
5. Flag any directory with 50+ files as a potential bloat candidate
6. Report findings in a summary table with:
   - Directory name
   - File count
   - Size in MB
   - Status (✅ needed / ⚠️ bloat / ❓ needs investigation)
7. If new bloat is found, suggest adding a new phase to `scripts/post-process-static.ps1`

## Key Paths

- Static export: `D:\Coding Zone\digitrust-lab-static`
- Post-process script: `G:\Zamzam Biznez\DigiTrustLabCode\scripts\post-process-static.ps1`
- Mu-plugins: `C:\Users\Zamri\Local Sites\digitrust-lab\app\public\wp-content\mu-plugins\`

## Output Format

Present results as a table:

```
| Directory | Files | Size | Status |
|-----------|-------|------|--------|
| ...       | ...   | ...  | ✅/⚠️/❓ |
```

End with total file count and any recommendations.
