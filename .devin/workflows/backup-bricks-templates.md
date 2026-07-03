---
description: Export Bricks templates as JSON backups before/after major edits
---

# Backup Bricks Templates

## When to Run

- **Before** any AI/MCP template editing session (safety net)
- **After** successful template restructure or major edits
- **Monthly** routine snapshot (1st of month)
- **Before** Simply Static export + deploy

## Templates to Backup

| Template | ID | File |
|----------|----|------|
| Header | 21 | `bricks-exports/header-v{N}.json` |
| Footer | 46 | `bricks-exports/footer-v{N}.json` |
| Single Post | 10 | `bricks-exports/single-post-v{N}.json` |
| Blog Archive | 52 | `bricks-exports/blog-archive-v{N}.json` |

## Steps

### 1. Check current version
```bash
ls bricks-exports/
```
Find the highest version number for each template.

### 2. Export via Bricks MCP
For each template, call:
```
mcp1_template(action=export, template_id={ID}, include_classes=true)
```

### 3. Save JSON
Save the response to `bricks-exports/{template-name}-v{N}.json` with:
- Pretty-printed JSON (2-space indent)
- Added fields: `exportedAt`, `exportedBy`

### 4. Git commit
```bash
git add bricks-exports/
git commit -m "backup: Bricks templates v{N} snapshot

- Export {template names} as JSON backups
- {N} templates, {total elements} elements total"
```

### 5. Version rotation
- Keep last 3 versions of each template
- Archive older versions to `bricks-exports/archive/`
- Never delete — just move

## Restore

### Via Bricks MCP
```
mcp1_template(action=import, template_data={JSON content from file})
```

### Via Bricks GUI
1. Bricks → Templates → Import
2. Upload the JSON file
3. Apply to target template

## Forbidden

- Do NOT backup during Simply Static export (template may be mid-edit)
- Do NOT skip git commit after export
- Do NOT overwrite existing versions — always increment
