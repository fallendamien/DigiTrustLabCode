---
name: readability-pass
description: Break up walls of text in blog posts by adding visual resting points — images, pull quotes, callouts, stat blocks, tables. Use after publishing a post with dense paragraphs and no visual breaks, when a post has 0 in-content images, when Rank Math flags density, or when user says "sea of text", "wall of text", "too dense", "hard to read", or before starting a new post to set a visual standard.
---

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
- **Prompt template, design system, and worked examples:** `content/image-prompts.md` (authoritative — do not copy the template into other files)

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

---

## Rich Formatting Toolkit (authoritative — moved here from `write-post.md` 2026-07-30)

AI-assisted drafting can produce walls of text: flat paragraphs with no visual
breaks. **Every article must be richly formatted.** No section should be a sea
of text. For DigiTrust Lab, the WriterZen full-article mode is prohibited; this
toolkit applies to the native draft produced after the outline-only workflow.

| Formatting Type | When to Use | HTML Pattern |
|----------------|-------------|--------------|
| **Bullet lists** | Enumerations, features, tips, reasons | `<ul><li>...</li></ul>` |
| **Numbered lists** | Steps, sequences, rankings | `<ol><li>...</li></ol>` |
| **Bold labels** | Start of each bullet for scannability | `<li><strong>Label</strong>: description</li>` ⚠️ use a **colon**, never an em dash |
| **Blockquotes** | Examples, key quotes, before/after comparisons | See Step 4 template above |
| **Contrast pairs** | Dos and don'ts, good vs bad | `<li><strong>Elakkan:</strong> ...</li><li><strong>Gunakan:</strong> ...</li>` |
| **Before/after blocks** | Instructional examples (bad vs good prompt) | Two blockquotes back-to-back with labelled headers |
| **Inline emphasis** | English terms in BM sentences | `<em>prompt</em>, <em>brainstorming</em>` |
| **Warning/tip boxes** | Important cautions, pro tips | See Step 3 template above |
| **Short paragraphs** | One idea per paragraph — never more than 3-4 sentences without a break | — |
| **Figures with captions** | In-content images | `<figure class="wp-block-image"><img ... /><figcaption>...</figcaption></figure>` |
| **Internal links** | Contextual anchor text to related posts | `<a href="...">natural anchor text</a>` |

> ⚠️ **Em dash conflict — resolved 2026-07-29.** This toolkit previously specified `<strong>Label</strong> — description` for bullets, which silently contradicted the AGENTS.md punctuation rule capping em dashes at **1 per post** (they read as an AI tell in Malay). A single 5-item list blew the whole budget. **Always use a colon in list items.** Reserve the one permitted em dash for prose, if used at all. Caught on Post #4, where the draft scored 10 dashes against a max of 1.

### Formatting Checklist (run after every AI draft)

- [ ] **Em/en dash count ≤ 1** across the whole post (list items use colons, not dashes)
- [ ] No section is a wall of text (3+ paragraphs without a list, blockquote, or visual break)
- [ ] All enumerations use bullet or numbered lists
- [ ] All examples use blockquotes (not plain paragraphs)
- [ ] All list items have bold labels where applicable
- [ ] Dos/don'ts sections use "Elakkan" vs "Gunakan" contrast pairs
- [ ] At least 2-3 blockquotes per instructional article
- [ ] English terms italicized with `<em>` tags
- [ ] Paragraphs are short (max 3-4 sentences)
- [ ] Warning/tip boxes used for important callouts

> **Formatting is structure only.** Language quality is a separate failure mode with its own authority: load `.claude/skills/malay-voice-guide/SKILL.md` and run its checks too. A perfectly formatted post can still be full of banned contractions and broken tatabahasa.

### Reference Standards

| Post | What to copy |
|------|-------------|
| Post #2 (`/cara-guna-chatgpt/`) | Blockquotes for examples, bullet lists with bold labels, warning boxes, FAQ section |
| Post #3 (`/cara-buat-prompt-chatgpt/`) | Before/after blockquote pairs, contrast pairs, bullet lists with bold labels |
| Post #1 (`/apa-itu-ai/`) | Clean paragraph flow with lists, figure captions, natural internal links |

**Why this matters:** Rich formatting improves time-on-page, reduces bounce rate, increases mobile readability, and matches the visual quality Google's helpful content system rewards. Walls of text get skipped; structured content gets read. This is a non-negotiable quality standard for DigiTrust Lab.
