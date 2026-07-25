# Readability Pass — Breaking Up Walls of Text

## Trigger
- After publishing a post, if the content is dense paragraphs with no visual breaks
- When a post has 0 in-content images and Rank Math flags it
- When user says "sea of text", "wall of text", "too dense", "hard to read"
- Before starting a new post, if previous posts need a visual standard to follow

## Problem
Blog posts written by AI tend to produce uniform blocks: H2 → paragraph → paragraph → list → H2 → paragraph... The reader's eye has no resting points. This kills time-on-page and bounce rate.

## Solution: 4-Step Readability Pass

### Step 1: Audit the Post
1. Navigate to the live post URL with `?nocache=1`
2. Count images in `#brxe-bodycn` — if 0, images are needed
3. Scan for long sections (3+ paragraphs without any visual break)
4. Identify: warning/tip lists, example prompts, dense intro sections

### Step 2: Image Placement (if 0-1 images)
- **Above the fold:** Place first image right after the intro paragraph, before the first H2
- **Mid-content:** Place images under H2 section intros (not at the end)
- **Aim for 3 images minimum** for a 1500+ word post
- Use Gemini Nano Banana 2 with the standard DigiTrust Lab prompt template
- See `write-post.md` → Image Prompt Template section

### Step 3: Callout Boxes for Warnings/Tips
Convert plain warning/tip lists into styled callout boxes:

```html
<div style="background:#FFF8F5;border-left:3px solid #E8621A;border-radius:0 6px 6px 0;padding:12px 16px;margin:16px 0;">
<p><strong>⚠️ Amaran penting:</strong> [warning text]</p>
<p><strong>Tip:</strong> [tip text]</p>
</div>
```

**When to use:**
- Privacy/security warnings
- Accuracy disclaimers about AI
- Important tips that shouldn't be missed
- Combined short H4 sections that are related (e.g., "Pentingnya memeriksa" + "Cara mengelakkan")

**Colors:**
- Warning callout: `background:#FFF8F5` (light orange tint)
- Border: `3px solid #E8621A` (brand orange)

### Step 4: Blockquote Examples
Convert inline example text into visually distinct blockquotes:

```html
<blockquote style="border-left:3px solid #E8621A;padding:8px 16px;margin:12px 0;background:#F5F3EE;border-radius:0 6px 6px 0;">
<p><strong>Contoh soalan terbuka:</strong> <em>"[example text]"</em></p>
<p>[explanation of what AI does with this]</p>
</blockquote>
```

**When to use:**
- Example prompts/responses
- Before/after comparisons
- Copyable text snippets
- Any content the reader should visually distinguish from body text

**Colors:**
- Example blockquote: `background:#F5F3EE` (surface color)
- Border: `3px solid #E8621A` (brand orange)

## WordPress Editor Notes

- Posts using the classic editor appear as `core/freeform` blocks in Gutenberg
- Use `wp.data.dispatch('core/block-editor').updateBlockAttributes()` to modify content
- Always call `wp.data.dispatch('core/editor').savePost()` after changes
- `<div style="">` blocks may get stripped by WordPress content sanitizer — use `<blockquote style="">` instead (more reliable)
- Always verify on live site with `?nocache=1` after saving

## Verification Checklist

| Item | How to verify |
|------|--------------|
| Image above first H2 | `imgPos < h2Pos` in DOM |
| 3+ in-content images | `document.querySelectorAll('#brxe-bodycn figure img').length >= 3` |
| Callout boxes live | `document.querySelectorAll('#brxe-bodycn div[style*="border-left:3px solid #E8621A"]').length` |
| Blockquote examples live | `document.querySelectorAll('#brxe-bodycn blockquote[style*="border-left:3px solid #E8621A"]').length` |
| All images have Malay alt text | Check `img.alt` is non-empty and in Malay |

## Content Pattern Standard (for future posts)

Use this rhythm when writing new posts:

```
Intro paragraph (1-2)
→ Image (if section is long)
→ H2 heading
→ Short intro (1 paragraph)
→ Content (paragraphs, lists)
→ Callout box (if warnings/tips)
→ H3 subsections
→ Blockquote examples (if examples exist)
→ Image (break before next H2)
```

**Not every section needs an image.** 3 images + 2 callouts + 2 blockquotes is enough for a 1500-word post. The rest is formatting: short intros, clear lists, separated examples.
