# Incident Log (Lessons Learned)

**Root cause pattern:** Reaching for scripts/MCP writes instead of Bricks standard operations.

## Incidents

**Incident 1:** Spent 45+ min writing PHP mu-plugins for a 2-min GUI task.

**Incident 2 (2026-07-04):** Post-process CSS injection fought with Bricks native CSS, making mobile menu worse.

**Incident 3 (2026-07-04):** AI-created JSON backups had structural issues on re-import. User banned all AI-created backups.

**Incident 4 (2026-07-04/05):** Flattening bug destroyed templates 185 & 52 THREE times via MCP writes. Templates now FROZEN.

**Incident 5 (2026-07-19):** `respira_inject_builder_content` with `mode: replace` on Bricks templates (post type `bricks_template`) causes the Bricks GUI editor to show a blank Structure panel — elements are written to the DB but Bricks can't parse them into clickable/editable nodes. The frontend may render correctly but the template becomes uneditable in GUI. This happened twice on template 52 (blog archive).
- **Rule:** NEVER use `respira_inject_builder_content` replace mode on `bricks_template` post types (templates 10, 52, 185, 46). Only use it on regular pages (post type `page`) if absolutely necessary. For templates, ALL structural changes must go through Devin in Windsurf via direct `_bricks_data` post meta editing.

**Incident 6 (2026-07-19):** Query loops (`hasLoop` and query settings) passed to Bricks container elements via Respira MCP are silently ignored — Respira warns "unknown control" and Bricks doesn't register them. Query loops in Bricks only work when set through the Bricks GUI editor or via direct `_bricks_data` post meta write with the correct Bricks internal schema.
- **Rule:** Any element requiring a Query Loop must be configured in Bricks GUI or via direct DB write by Devin. Never attempt to set `hasLoop` or `query` via `respira_update_element` or `respira_inject_builder_content`.

**Incident 7 (2026-07-20):** `respira_move_element` is unreliable for reordering elements within a container. Position numbers don't map correctly, and `position: -1` (append) does not change the DB children array order. `respira_reorder_elements` returns 500 errors ("Element id not found among children"). The ONLY reliable method for reordering elements via Respira MCP is `respira_apply_builder_patch` with `{"children": ["id1", "id2", ...]}` on the parent container — this directly sets the children array and changes the builder hash.
- **Rule:** For element reordering, ALWAYS use `respira_apply_builder_patch` with `children` array on the parent container. Never use `respira_move_element` or `respira_reorder_elements`.

**Incident 8 (2026-07-20):** Query loop settings (`postsPerPage`, `offset`) written to `_bricks_data` via Respira MCP (`respira_update_element`, `respira_apply_builder_patch`) are stored in the DB correctly but Bricks' frontend rendering engine IGNORES them. The posts per page defaults to 10 regardless of the DB value. The ONLY way to activate query loop settings is to open the template in Bricks GUI editor, set the values in the Query Loop UI, and Save — this triggers Bricks' internal PHP hooks to register the query.
- **Rule:** Query loop settings (postsPerPage, offset, order, orderby) MUST be set through Bricks GUI editor. Respira MCP can write them to DB but they won't be activated on the frontend. After setting in GUI, regenerate CSS + purge cache.
