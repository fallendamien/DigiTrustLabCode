# Bricks Template Backup Skill

> **Triggered by:** Rule `.devin/rules/bricks-backup.md`  
> **Quick trigger:** `/backup-bricks-templates`

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

## Restore

### Via Bricks MCP
Read the JSON file, then:
```
mcp1_template(action=import, template_data={JSON content})
```

### Via Bricks GUI
1. Bricks → Templates → Import
2. Upload the JSON file
3. Apply to target template
