# Bricks Template Backup Skill

## When to Activate

- Before any MCP template editing session (header, footer, single post, blog archive)
- After successful template restructure or major element changes
- Monthly routine backup (1st of month)
- Pre-deploy checkpoint before Simply Static export
- User explicitly requests backup or says `/backup-bricks-templates`

## What It Does

Exports Bricks templates as JSON files to `bricks-exports/` with version numbering, then git commits.

## Templates

| Template | ID | File |
|----------|----|------|
| Header | 21 | `bricks-exports/header-v{N}.json` |
| Footer | 46 | `bricks-exports/footer-v{N}.json` |
| Single Post | 10 | `bricks-exports/single-post-v{N}.json` |
| Blog Archive | 52 | `bricks-exports/blog-archive-v{N}.json` |

## Execution Steps

### Step 1 — Check existing versions
```
ls bricks-exports/
```
Determine next version number for each template.

### Step 2 — Export each template via Bricks MCP
```
mcp1_template(action=export, template_id={ID}, include_classes=true)
```

### Step 3 — Save JSON
- Pretty-printed (2-space indent)
- Add `exportedAt` and `exportedBy` fields
- Save to `bricks-exports/{name}-v{N}.json`

### Step 4 — Git commit
```bash
git add bricks-exports/
git commit -m "backup: Bricks templates v{N} snapshot

- Export {template names} as JSON backups
- {N} templates, {total elements} elements total"
```

### Step 5 — Version rotation
- If more than 3 versions exist for a template, move oldest to `bricks-exports/archive/`
- Never delete — only move

## Restore Instructions

### Via Bricks MCP
Read the JSON file, then:
```
mcp1_template(action=import, template_data={JSON content})
```

### Via Bricks GUI
1. Bricks → Templates → Import
2. Upload the JSON file
3. Apply to target template

## Guardrails

- Never overwrite existing version files — always increment
- Never skip git commit
- Never backup during active Simply Static export
- Only backup templates listed above unless user requests others
