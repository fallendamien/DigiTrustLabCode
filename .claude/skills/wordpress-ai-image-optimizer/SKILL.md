---
name: wordpress-ai-image-optimizer
description: "Compress, WebP-convert, resize, and rename images on a WordPress site. Uses Respira's media tools to process images locally — no external uploads, no API keys. Batch-processes the media library or a single page's images."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: optimization
---

# WordPress AI Image Optimizer

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** optimization
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Compress, WebP-convert, resize, and rename images on a WordPress site — all locally via Respira's media tools. No external uploads, no API keys, no third-party services. The skill processes images in batches (whole media library or a single page's images) and produces a before/after report with exact savings per image.

This is the "I have 200 images and my site is slow" skill. It's not a design tool — it doesn't change how images look, just how much they weigh.

---

## What it does

1. **Compress** — reduces JPEG/PNG file size with minimal quality loss. Targets a 60–80% reduction for uncompressed originals.
2. **WebP convert** — creates a WebP version of every JPEG/PNG. WebP is ~25–35% smaller at equivalent quality. Modern browsers all support it.
3. **Resize** — scales oversized images down to a sensible max width (default 1920px for hero images, 1200px for content images). A 4000px-wide image displayed at 800px is 25x the necessary bytes.
4. **Rename** — renames files from `IMG_20231015_143221.jpg` to `descriptive-slug.jpg` based on the alt text or surrounding content context. This is an SEO win (image search) and an accessibility win (screen readers announce the filename when alt is missing).

All four operations are optional and configurable per run.

---

## When to Use

- After importing a batch of images from a photoshoot
- When PageSpeed flags image weight as the top opportunity
- Before deploying a new site (final cleanup pass)
- Quarterly maintenance — images accumulate
- When a specific page is slow and you suspect images are the cause

---

## Trigger Phrases

- "optimize my images"
- "compress my media library"
- "convert images to webp"
- "my images are too big"
- "image optimization audit"
- "reduce image file sizes"
- "fix my slow images"

---

## Execution Workflow

### Step 1 — Confirm site + scope

Call `respira_get_active_site` + `respira_get_site_context`.

Ask the user: *"Whole media library, or just images on a specific page?"*

### Step 2 — Inventory images

**Whole library mode:**
Call `respira_list_media(per_page=100)` and paginate until all media is collected.

**Single page mode:**
Call `respira_extract_builder_content(page_id)` and walk the builder tree for image elements. For each image element, extract the attachment ID (if native) or the URL (if external). Only process native attachments — external URLs can't be optimized locally.

### Step 3 — Analyze each image

For each image, call `respira_get_media(id)` to get:
- File size (original)
- MIME type (jpeg, png, gif, webp, svg)
- Dimensions (width × height)
- Filename
- Alt text (if set)

Build a table:

| ID | Filename | Size | Dimensions | Type | Alt text | Issues |
|---|---|---|---|---|---|---|
| 42 | IMG_1234.jpg | 4.2MB | 4032×3024 | jpeg | (empty) | oversized, no alt, no webp |
| 43 | hero-banner.png | 1.8MB | 1920×1080 | png | "Hero banner" | png should be webp, no webp version |

Flag issues:
- **Oversized**: width > 1920px for hero images, > 1200px for content images
- **Uncompressed**: JPEG > 500KB, PNG > 1MB (rough heuristics)
- **No WebP**: JPEG or PNG without a corresponding WebP version
- **Poor filename**: `IMG_`, `DSC_`, `Screenshot`, `image (1)`, numeric-only, or generic names
- **Missing alt text**: empty or generic alt ("image", "photo")

### Step 4 — Present the plan

```markdown
## Image optimization plan for {site_url}

**Images scanned:** {n_total}
**Images needing optimization:** {n_optimize}
**Estimated total savings:** {savings_estimate} (from {current_total_size} to ~{projected_total_size})

### Breakdown

| Issue | Count | Est. savings |
|---|---|---|
| Oversized (resize needed) | {n} | {savings} |
| Uncompressed (recompress needed) | {n} | {savings} |
| No WebP version | {n} | {savings} |
| Poor filename | {n} | SEO win (no byte savings) |
| Missing alt text | {n} | accessibility win |

### Top 10 heaviest images

| ID | Filename | Current size | After opt (est.) | Savings |
|---|---|---|---|---|
| 42 | IMG_1234.jpg | 4.2MB | 380KB | 91% |
| ... | | | | |
```

Ask: *"Ready to optimize? I'll process all {n} images. This runs locally — no files leave your server."*

### Step 5 — Apply optimizations (only if approved)

For each image, apply the approved operations:

1. **Resize:** If the image is wider than the max width for its context, resize it. This is done server-side via Respira's image processing.
2. **Compress:** Re-encode the image at a target quality (85 for JPEG, lossless for PNG where possible).
3. **WebP convert:** Create a `.webp` version alongside the original.
4. **Rename:** If the filename is poor and alt text exists, rename to a slug derived from the alt text. If no alt text, derive from the parent page/post title + image context.
5. **Update alt text:** If alt text is missing and context is available (page title, surrounding headings), suggest alt text and apply it.

Use `respira_update_media` to update metadata (alt text, title, caption).
Use `respira_upload_media` to replace the file if the optimization produces a new file.

### Step 6 — Verify + report

After processing, re-scan the optimized images to confirm:
- File sizes actually decreased
- WebP versions exist
- Dimensions are within targets
- Alt text is populated

Output a before/after summary:

```markdown
## ✅ Optimization complete

**Images processed:** {n}
**Total size before:** {before}
**Total size after:** {after}
**Total savings:** {savings} ({pct}% reduction)

### Per-image results

| ID | Filename | Before | After | Savings | WebP | Alt text |
|---|---|---|---|---|---|---|
| 42 | ai-tools-malaysia.jpg | 4.2MB | 380KB | 91% | ✅ | ✅ "AI tools for Malaysian businesses" |
| ... | | | | | | |

### What changed
- Resized {n} images to max {max_width}px
- Compressed {n} images (avg quality 85)
- Created {n} WebP versions
- Renamed {n} files from generic to descriptive slugs
- Added alt text to {n} images

### Next steps
- Run a PageSpeed audit to see the impact on your scores
- Consider adding `loading="lazy"` to below-the-fold images (if not already set)
```

---

## Hard rules

- **Never delete originals without explicit permission.** The skill creates optimized versions; it does not delete the original files unless the user explicitly says "replace the originals."
- **SVG files are skipped.** SVGs are already vector and tiny. Don't try to compress or WebP-convert them.
- **GIF files are skipped for WebP conversion.** WebP doesn't support animation reliably. Compress GIFs if oversized, but don't convert.
- **External URLs cannot be optimized.** If an image is hosted on a CDN or external URL, flag it but don't try to process it.
- **Alt text generation is conservative.** Only suggest alt text when there's clear context (page title, surrounding heading, caption). If context is ambiguous, flag for manual review.
- **Filename renaming is opt-in.** Some users have workflows that depend on original filenames. Always ask before renaming.
- **Batch size matters.** Processing 500 images in one go can timeout. Default batch size is 50; paginate.

---

## Telemetry

Records: site URL hash, n_images scanned, n_images optimized, total savings (bytes), operations used (compress/webp/resize/rename/alt), success/failure, total duration. No image content, no filenames, no alt text sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
