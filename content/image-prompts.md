# Image Prompts Library — DigiTrust Lab

> Copy-paste ready prompts for ChatGPT or Gemini image generation. Each post has 4 images: 1 featured + 3 in-content. Paste the prompt into the selected provider, download the result, and upload it to WordPress Media with the given filename.
>
> **Published posts** have content-derived prompts based on actual article text.
> **Planned posts** are marked TBD — prompts will be written after content is drafted.
>
> ⚠️ **`content/content-calendar.md` is the source of truth for post titles.** Section headings here are short labels for scanning, not authoritative titles. If a heading here names a *different topic* rather than a shortened version of the calendar title, the calendar wins — fix this file. (Audited 2026-07-29: Post #4 had genuinely diverged and was corrected; Posts #5, #7–#10 verified as consistent short forms.)

## 📸 Authentic screenshot standard for visual-software tutorials

When a post teaches a visual software app, dashboard, editor, plugin, or web
service, authentic interface screenshots are mandatory inline evidence for every
material action whose control, setting, state, or result matters. Capture one
coherent tested workflow with the same sample throughout. Keep screenshots
readable at article size, crop or blur account data and browser chrome before
upload, and record Malay alt text, an accurate caption where reader-visible
context is requested, platform/device/account-plan/date caveats, and the exact
article action covered. Generated illustrations may explain concepts or serve as
the separate featured hero; they must not imitate controls, menus, settings,
results, or proof of an interface action. Maintain a screenshot coverage map and
write an explicit reason for each material procedural action without a screenshot.

## 🎨 Design System (never change these)

| Element | Value |
|---------|-------|
| Style | DigiTrust Lab illustration family: flat editorial baseline with controlled treatments below |
| Background | Warm off-white `#FAFAF8` must be the dominant visible field; peach/cream accents are restrained supporting shapes, never a heavy full-bleed backdrop |
| Primary accent | Orange `#E8621A` |
| Dark elements | Dark charcoal `#1A1A1A` |
| Highlights | White |
| Aspect ratio | 16:9 (wide, min 1024×576) |
| Text in image | No readable text by default; clean intentional pseudo-writing, abstract lines, bullets, and checkboxes are allowed and should be preserved |

## 🛑 Mandatory image-mode choice (before every generation)

Before generating any featured, in-content, CTA/card, or replacement image,
pause and ask the owner to choose exactly one mode. Do not generate, refine, or
regenerate an image until the owner has made an explicit choice; never infer a
default from the treatment or the previous image.

| Mode | Binding visual direction |
|------|--------------------------|
| **More Depth** | Controlled 2.5D/isometric treatment: subtle perspective, layered forms, and gentle drop shadows. Keep the fixed DigiTrust Lab palette, 16:9 editorial framing, and no photorealism. |
| **Strict flat design** | Strict 2D vector treatment: solid fills and clean outlines only. No shadows, gradients, perspective, or depth cues. Keep the fixed DigiTrust Lab palette and 16:9 editorial framing. |

Record the selected mode in every image prompt. For a featured image, repeat the
same value in the variety record below. The mode controls rendering; the
approved treatment and variation guide still control subject and composition.
If a treatment conflicts with the chosen mode, change the brief or treatment
before generation rather than silently blending modes.

Controlled 2.5D is allowed as a bounded variety option, but it does not redefine
the DigiTrust Lab brand family. The fixed palette, 16:9 framing, editorial
restraint, previous-six check, treatment rotation, human/motif constraints, and
immediate-prior difference rule all remain in force.

## ⚖️ Background-weight and archive-uniformity gate (MANDATORY)

The palette is a hierarchy, not a list of interchangeable swatches. For every
featured image, the archive-card thumbnail must first read as a light,
warm-off-white/ivory image, consistent with the surrounding grid.

Hard visual requirements:

1. Keep warm off-white `#FAFAF8` (or a visually equivalent light ivory) as the
   dominant backdrop — target at least two-thirds of the visible background.
2. Use `#FFF3EE`, `#FFEADD`, restrained beige, and orange only as supporting
   shapes, panels, props, or accents. Do not use a large full-bleed tan, peach,
   brown, dark, saturated, muddy, or sepia field.
3. Review the candidate beside the previous six featured thumbnails at the
   actual archive-card size. If the background makes the candidate look darker,
   heavier, or like a different illustration family, mark the comparison FAIL.
4. A prompt that mentions the correct hex values is not visual evidence. The
   candidate must pass both the native-resolution audit and the archive-grid
   comparison before it can be archived, uploaded, or assigned as featured.

## Template 10 CTA card — AI skills and digital product creation

**Status:** GENERATED — ARCHIVED PENDING UPLOAD

**Filename:** `ai-skills-digital-product-creation-card.png`

**Archive path:** `G:\\Zamzam Biznez\\DigiTrustLab\\Blog images\\ai-skills-digital-product-creation-card.png`

**Alt text:** Ilustrasi komputer riba dengan aliran kerja AI dan penciptaan produk digital

```text
Use case: illustration-story. Asset type: WordPress CTA card image. Primary request: a generic flat editorial illustration of a clean desk with a laptop displaying abstract AI workflow cards, a notebook with simple geometric sketches, and modular digital product blocks. Scene/backdrop: warm uncluttered workspace. Style/medium: flat editorial illustration, warm trustworthy minimal. Composition/framing: wide 16:9, generous negative space, card-friendly crop. Lighting/mood: soft natural light, calm helpful peer. Color palette: documented DigiTrust Lab warm palette #FAFAF8, #FFF3EE, #FFEADD, #E8621A, #1A1A1A, white. Constraints: 800x450px intent, no readable text, no logos, no money symbols, no article-specific objects, no urgency or scarcity cues. Avoid: photorealistic sales imagery, currency, countdowns, badges, watermarks.
```

## 🚦 Featured-image variety gate (MANDATORY)

The archive grid is a visual product, not a row of interchangeable article
thumbnails. Before generating every new featured image, inspect the previous six
featured thumbnails together at archive-card size and record the comparison below.
This gate is blocking: if the thumbnail comparison or any rule fails, do not
archive, upload, or publish the image. Regenerate the concept first.

### Required pre-generation record

```text
Previous six thumbnails inspected: [six filenames or post numbers]
Image mode: [More Depth | Strict flat design — owner-selected; required]
Visual mode: [object-led | abstract-symbolic | diagrammatic | environmental |
              editorial-collage | top-down | split-transformation | human-led]
Subject class: [specific subject, not “AI”]
Composition: [specific layout and perspective]
Treatment: [approved treatment name below]
Planned background treatment: [dominant warm off-white / light ivory + restrained accents]
Background-weight target: [light dominant neutral]
Human presence: [yes | no]
Repeated motif check: [PASS | FAIL]
Immediate-prior difference count: [0–5 dimensions; must be ≥3]
Thumbnail comparison: [PASS | FAIL]
Background-weight review: [PASS | FAIL]
Archive-grid uniformity: [PASS | FAIL]
```

Run the deterministic record gate after the visual inspection and before
archiving. Replace the placeholders with the recorded values:

```powershell
python scripts/verify-featured-image-variety.py `
  --register content/image-prompts.md `
  --previous-six-inspected `
  --visual-mode <mode> `
  --subject-class "<specific subject>" `
  --composition "<layout and perspective>" `
  --treatment <approved-treatment> `
  --human-presence <yes|no> `
  --motif "<motif signals>" `
  --difference-count <3-5> `
  --thumbnail-comparison pass `
  --background-weight light-dominant-neutral `
  --background-review pass `
  --archive-grid-uniformity pass
```

The command checks the recorded history and blocks a failed or incomplete
decision. It cannot see the pixels itself, so `thumbnail-comparison pass`,
`background-weight light-dominant-neutral`, `background-review pass`, and
`archive-grid-uniformity pass` are valid only after the worker has actually
viewed the candidate at native resolution and beside the six thumbnails.

Hard rules:

1. Human-led featured images are exceptional. They must not appear
   consecutively, and there may be no more than one human-led image in any
   four consecutive posts.
2. The combined motif **person + desk + laptop + robot** is forbidden when it
   appears in any of the previous six featured images. Do not recreate it with
   minor prop or pose changes.
3. The new image must differ from the immediately previous featured image in at
   least three dimensions: subject, composition, perspective, treatment, and
   human presence.
4. Keep the DigiTrust Lab palette and 16:9 archive-safe framing, while rotating
   the approved treatments. Brand recognition comes from the palette, outlines,
   spacing, and editorial clarity, not from repeating one character scene.
5. View the candidate beside the previous six thumbnails. If it still reads as
   the same orange-shirt desk scene, mark `Thumbnail comparison: FAIL` and
   regenerate. A metadata PASS never overrides a visual FAIL.
6. The candidate's first thumbnail read must be light and neutral. A heavy
   colored background, even when it uses an approved peach or beige swatch,
   fails `Background-weight review` and blocks archive/upload.
7. `Background-weight review: PASS` and `Archive-grid uniformity: PASS` are
   required alongside the existing thumbnail comparison. Regenerate when the
   background competes with the subject, overwhelms the card, or looks unlike
   the recent set.

### Approved bounded treatment rotation

| Treatment | Visual boundary |
|-----------|-----------------|
| Flat editorial vector | Default geometric shapes and bold outlines; use only when the recent set is not already vector-heavy |
| Geometric infographic | Structured nodes, pathways, cards, or symbols; no human required |
| Isometric systems scene | Layered depth for processes and relationships; avoid a person at a laptop as the focal point |
| Cut-paper editorial collage | Overlapping paper-like planes and silhouettes using the fixed palette; no named-artist imitation |
| Abstract symbolic composition | One strong metaphor with generous negative space; no literal desk scene |
| Cinematic editorial poster | Selective framed vignette and silhouette treatment for cautionary or myth-busting topics |

The treatment is a bounded variation of the brand family, not permission to
change the palette, add readable text, imitate a named artist, or introduce
uncontrolled photorealism.

### Featured-image register (historical comparison set)

These recent entries document the repetition that this gate is designed to stop.
They are comparison evidence, not templates for the next image.

| Post | Featured asset | Visual mode | Subject class | Composition | Treatment | Human presence | Motif signals |
|------|----------------|-------------|---------------|-------------|-----------|------------------|----------------|
| #6 | `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-featured.png` | human-led | student, three AI robots | split | flat editorial vector | yes | student three robots chooser |
| #7 | `cara-buat-nota-cantik-dengan-ai-featured.png` | human-led | person, organised notes, laptop, AI sparkle | split | flat editorial vector | yes | person desk laptop robot |
| #9 | `prompt-gemini-ai-untuk-edit-foto-featured.png` | human-led | creator, portrait, editing interface | split | flat editorial vector | yes | creator portrait smartphone editing interface |
| #11 | `apa-itu-mcp-dalam-ai-dan-bagaimana-ia-berfungsi-featured.png` | diagrammatic | AI connection, files, database, app, human observer | split | flat editorial vector | yes | AI bridge files database app human observer |
| #12 | `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai-featured.png` | human-led | person, meeting notes, calendar | split | flat editorial vector | yes | person desk laptop calendar |
| #14 | `cara-buat-banner-guna-canva-featured.png` | object-led | modular banner canvas, safe-area frame, layout guides | centred direct-on canvas | geometric-infographic | no | banner canvas safe-area frame guide lines |

After each publication, append the new featured asset to this register, remove
the oldest entry, and preserve the six-entry comparison window.

## 📐 Variation Guide (rotate — avoid repeating the same composition)

| # | Variation | Use for |
|---|-----------|---------|
| 1 | Split composition | Featured images, comparisons |
| 2 | Minimalist negative space | Intro/overview sections |
| 3 | Isometric scene | Detailed comparison/breakdown sections |
| 4 | Top-down flat lay | Conclusion/summary sections |
| 5 | Icons floating around | Concept explainers |
| 6 | Geometric patterns | Technical/process articles |
| 7 | Abstract organic shapes | Creative/lifestyle topics |
| 8 | Cinematic editorial poster | Cautionary/myth-busting topics (selective) |

## 🧩 Prompt Template (authoritative — moved here from `write-post.md` 2026-07-30)

**Always provide BOTH the prompt AND the filename together.**

```
Prompt:
Owner-selected image mode: [More Depth | Strict flat design]. Apply the selected mode's binding direction above. [SUBJECT DESCRIPTION]. Simple geometric shapes, bold outlines. Background: predominantly warm off-white (#FAFAF8), with at least two-thirds of the visible field remaining light and neutral; use #FFF3EE/#FFEADD and orange (#E8621A) only as restrained supporting accents. Dark charcoal (#1A1A1A) outlines and elements, white highlights. [VISUAL ELEMENT — see Variation Guide above]. Clean, modern, minimal. No heavy full-bleed beige/peach/tan/dark background, no muddy or saturated backdrop, and no text or words in the image. Wide format 16:9.

Filename: {post-slug}-{image-description}.png
```

**Filename rule (MANDATORY):** lowercase, hyphens only, no underscores. Example: `apa-itu-ai-neural-network.png`. Applies to featured *and* in-content images.

**Composition rule:** Vary the visual element across images within the same post so they read as a curated collection, not a template repeat. The palette and brand illustration family stay fixed; the approved treatment, composition, perspective, and decorative elements change. Think "art lover's blog", not "corporate stock art". Never reuse the same scene layout (e.g. person at desk with screen) across posts.

### ⚠️ Anatomy Fix (MANDATORY for any human or robot)

AI generators routinely produce missing, deformed, or unnaturally positioned hands and arms. Always append:

> `Both person and robot have complete visible arms and hands with natural positioning.`

If hands are still wrong, regenerate with:

> `All hands fully rendered with five fingers each, arms complete from shoulder to fingertips, natural pose.`

### 🔍 Image audit gate (MANDATORY before archive or upload)

Inspect every generated image at native resolution twice: the full frame, then
each marked region (faces, hands/arms, figures, cropped edges, props, and any
pseudo-writing). Preserve clean intentional pseudo-writing, abstract lines,
bullets, and checkboxes. Reject distorted-looking letters, malformed glyphs,
wobbly/uneven/merged strokes, inconsistent spacing, accidental readable text or
numbers, logos, watermarks, orange blobs or halos behind or intersecting
people/arms, and anatomy artifacts. If any artifact appears, edit or regenerate
non-destructively from the best composition and repeat both inspections. Do not
“fix” the image by deleting all pseudo-writing. Record the pass before archive
or upload.

### 🔁 Cross-Provider Image-Reference Workflow (ChatGPT or Gemini)

When a generator produces a great composition but the wrong background colour or style, don't re-prompt from scratch — upload the image to the provider you are using and refine it there:

1. Upload the image you like to ChatGPT or Gemini
2. Ask the selected provider: *"Re-create this exact scene while preserving the owner-selected image mode recorded in the prompt. Use warm off-white (#FAFAF8) background, the documented DigiTrust Lab palette, and charcoal (#1A1A1A) outlines with orange (#E8621A) accents. All human hands must have five fingers. No text, labels, logos, or watermarks."*
3. The selected provider preserves the composition while fixing the brand colours
4. Save with the same SEO filename and re-upload to WordPress Media

### 🎬 Cinematic Editorial-Poster Variation (variation #8 — use selectively)

An accent style for high-concept articles, cautionary topics, myth-vs-reality explainers, or a dramatic visual metaphor. **Not the default.**

- Keep the standard palette: `#FAFAF8` / `#E8621A` / `#1A1A1A` / white
- Large irregular framed/vignette scene, strong outlines, foreground silhouettes, cinematic depth, slight retro print energy
- Add one simple adjacent symbolic object plus subtle dashed orbital lines or geometric accents
- **Never request imitation of a named living artist or a copy of a specific reference composition** — describe visual traits instead
- Avoid logos, watermarks, legible text, gore, or overly dark scenes

**Prompt addition:** `Cinematic editorial-poster composition: a large irregular framed vignette scene with dramatic orange-and-charcoal contrast, bold black outlines, foreground silhouettes, a simple symbolic object outside the frame, and subtle dashed orbital lines with small geometric accents. Flat, clean, text-free, with slight retro print energy.`

### 📚 Worked Examples

**Post #1 — "Apa Itu AI" — featured, icons floating:**
> Flat illustration style. A Malaysian man sitting at a desk with a glowing brain icon on a computer screen. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around: chat bubble, lightbulb, gears. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Post #2 — "Cara Guna ChatGPT" — split composition:**
> Flat illustration style. A split scene: left side shows a messy desk with scattered papers and a frustrated person, right side shows the same desk organized with a glowing ChatGPT interface on a tablet, tasks neatly sorted into folders. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Subtle geometric patterns connecting the two sides. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Post #1 in-content — "Bagaimana AI Berfungsi" — minimalist, illustrates the article's analogy:**
> Flat illustration style. A child pointing at different animals on flashcards — a cat, a dog, a bird — learning to recognize patterns, with a parallel digital grid showing the same concept with data points being sorted into categories. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist composition with generous negative space and a single focal element. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

**Cinematic editorial poster — myth-vs-reality explainer:**
> Flat cinematic editorial-poster illustration. A large irregular framed vignette shows a giant charcoal robot looming over a small city while human silhouettes run in the foreground, representing a fictional AI fear. Outside the frame, a simple calculator represents practical everyday AI. Connect the two scenes with subtle dashed orbital lines and small orange geometric accents. Bold black outlines, dramatic orange-and-charcoal contrast, warm off-white (#FAFAF8) background, orange (#E8621A) accents, charcoal (#1A1A1A) elements, white highlights, slight retro print energy. Clean, modern, minimal. No text, words, logos, or watermarks. Wide format 16:9.

> **Key lesson:** For in-content images, illustrate the *analogy or metaphor* used in that section's text — not the literal concept. This produces a unique visual per section and avoids repetitive imagery (don't use a brain icon for every AI-related image).

## 📝 How to Use This File

1. Before any generation, ask the owner to choose exactly one mode above; stop
   without a choice, and record it in every prompt and the featured variety record.
2. For a featured image, inspect the previous six thumbnails and complete the
   variety record.
3. Find the post you're working on below
4. Copy the **Prompt** block for each image
5. Paste into ChatGPT or Gemini
6. Download the generated image
7. Upload to WordPress Media Library with the exact **Filename**
8. Set Malay alt text (provided with each image)
9. Leave the WordPress Media Library **Image Caption** field empty by default
   for featured and inline images. Never copy the alt text or description into
   this field; add a reader-visible caption only when the user explicitly
   requests one. Keep alt text separate.
10. Assign featured image or insert into post content only after the thumbnail
    comparison and native-resolution audit both pass

## 🔄 Maintenance Rule

**🔢 KEEP SECTIONS IN NUMERICAL ORDER — Post #1, #2, #3 … #10.** Do NOT group by status (published first, planned last) and do NOT append new sections to the bottom. Insert each post at its numbered position. Mixed ordering makes the file hard to scan and hides which posts still need prompts.

> Fixed 2026-07-29: the order had drifted to `#1, #2, #3, #6, #4, #5, #7…` because published posts were appended as they shipped. Reordered numerically.

**When a post is published:** Replace TBD prompts with content-derived ones based on the actual article text. Update the post's status marker from PLANNED to PUBLISHED.

### Local Image Archive and Naming

After generating the images for a post, copy every final asset from its exact `C:\Users\Zamri\.codex\generated_images\<session-folder>` source folder into `G:\Zamzam Biznez\DigiTrustLab\Blog images`. Rename each file to the exact `Filename` stated in this library. Verify the destination copy with a SHA-256 comparison before uploading to WordPress or cleaning the source. Cleanup is limited to the verified files in that one session folder; if deletion is blocked by a safety guard, keep the source files and record that they remain.
When archiving a batch, copy the files in prompt order, from Image 1 to the final image. Do not rely on copy order for Explorer placement because NTFS can preserve or tie creation timestamps after deletion and recopy. Set distinct destination `CreationTime` values so Image 1 is newest, Image 2 is next, and the final image is oldest; then verify that sorting by `CreationTime` descending produces Image 1 → Image 2 → Image 3 → Image 4.

**When a new post is planned:** Add a new section with TBD prompts **at its numbered position**, not at the end of the file.

**Status markers:** `(PLANNED — TBD)` → `(READY TO GENERATE)` once prompts are written → `(GENERATED — PENDING UPLOAD)` once assets are archived and verified → `(UPLOADED — PENDING PUBLICATION)` once Media upload and alt text are verified → `(PUBLISHED ✅)` once live.

---

## Post #1 — Apa Itu AI? (PUBLISHED ✅)

**Slug:** `apa-itu-ai`
**URL:** https://digitrustlab.com/apa-itu-ai/
**Content summary:** Explains AI as a smart calculator (not movie robot), covers how AI learns patterns from data like a child learning animals, shows AI in daily life (YouTube, Google Maps, Netflix, Spotify), 3 types (chatbot, image, analysis), addresses job replacement fears, privacy warnings.

### Image 1 — Featured (Split Composition)

**Filename:** `apa-itu-ai-featured.png`

```
Flat illustration style. A split scene — on the left side a human brain made of geometric shapes, on the right side digital circuit patterns flowing from the brain, showing the evolution from human thinking to AI processing. A subtle dashed line connects the two halves. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split composition showing the transformation clearly. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Ilustrasi otak geometri berubah menjadi litar digital mewakili transformasi AI

### Image 2 — Neural Network / How AI Works (Minimalist Negative Space)

**Filename:** `apa-itu-ai-neural-network.png`

```
Flat illustration style. A child looking at flashcards with animal icons, with a parallel neural network diagram below showing nodes connected by lines, illustrating how AI learns patterns from examples just like a child learns. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist composition with generous negative space and a single focal element. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Konsep kecerdasan buatan (AI) dengan rangkaian neural

### Image 3 — AI in Daily Life (Icons Floating Around)

**Filename:** `apa-itu-ai-kehidupan-harian.png`

```
Flat illustration style. A smartphone in the center surrounded by floating app icons — a play button for YouTube, a map pin for Google Maps, a film strip for Netflix, a music note for Spotify, and a shopping bag for e-commerce — all connected by subtle dotted lines showing AI working behind the scenes. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around composition. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** AI dalam kehidupan harian — telefon, peta, muzik dan beli-belah

### Image 4 — AI vs Movie Robot (Cinematic Editorial Poster)

**Filename:** `apa-itu-ai-bukan-robot-filem.png`

```
Flat illustration style. An off-white editorial poster layout — on the left a dramatic movie projector casting a silhouette of a scary robot, on the right a simple friendly calculator icon, showing the contrast between AI in films and AI in reality. Dashed orbital lines and small geometric accents connect the two scenes. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Cinematic editorial poster variation with dramatic silhouettes and a simple adjacent symbolic object. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Perbezaan antara AI dalam filem dan AI dalam realiti — projektor wayang vs kalkulator

---

## Post #2 — Cara Guna ChatGPT (PUBLISHED ✅)

**Slug:** `cara-guna-chatgpt`
**URL:** https://digitrustlab.com/cara-guna-chatgpt/
**Content summary:** Beginner guide to ChatGPT — registration steps, interface navigation, 5 practical uses (write emails, summarize articles, plan tasks, learn topics, brainstorm), prompt tips (specific vs vague, open vs closed questions), privacy warnings.

### Image 1 — Featured / Intro (Split Composition)

**Filename:** `cara-guna-chatgpt-pengenalan.png`

```
Flat illustration style. A person sitting at a desk with a laptop, chat bubbles floating between them and the screen showing a conversation happening. A lightbulb icon above the person's head indicating ideas generated by AI. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split composition with person on left and chat interface on right. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Ilustrasi pengenalan ChatGPT — orang guna laptop dengan chat AI untuk meningkatkan produktiviti

### Image 2 — 5 Practical Uses (Top-Down Flat Lay)

**Filename:** `cara-guna-chatgpt-5-cara-praktikal.png`

```
Flat illustration style. A top-down flat lay of a desk with five distinct tool icons arranged in a row — an envelope for emails, a document with scissors for summarizing, a calendar for planning, a graduation cap for learning, and a lightbulb for brainstorming. Each icon connected to a central laptop by subtle dotted lines. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Top-down flat lay perspective of objects arranged on a surface. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Lima cara praktikal guna ChatGPT — menulis emel, meringkaskan, merancang, belajar, dan brainstorming

### Image 3 — Prompt Tips (Geometric Patterns)

**Filename:** `cara-guna-chatgpt-tips-prompt.png`

```
Flat illustration style. A magnifying glass examining a chat bubble, with dotted lines connecting to gears representing thought process and a checkmark representing clear results. Two paths shown — one straight and clear (specific prompt) and one winding and confused (vague prompt). Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Geometric patterns and dotted lines connecting elements. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Tips menulis prompt ChatGPT yang berkesan — kanta pembesar memeriksa kualiti arahan

---

## Post #3 — Cara Buat Prompt ChatGPT (PUBLISHED ✅)

**Slug:** `cara-buat-prompt-chatgpt`
**URL:** https://digitrustlab.com/cara-buat-prompt-chatgpt/
**Content summary:** Guide to writing effective ChatGPT prompts — clarity, specificity, context, open vs closed questions, giving examples, avoiding information overload. Practical examples for studying, work, daily life, and creativity. Common mistakes and tips.

### Image 1 — Effective Prompt (Minimalist Negative Space)

**Filename:** `cara-buat-prompt-chatgpt-prompt-efektif.png`

```
Flat illustration style. A magnifying glass examining a document with a checkmark, representing clarity and precision in writing prompts. A small chat bubble icon nearby. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist composition with generous negative space and a single focal element. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Cara buat prompt ChatGPT — kanta pembesar memeriksa dokumen dengan tanda semak, mewakili kejelasan dalam menulis prompt

### Image 2 — Daily Examples (Icons Floating Around)

**Filename:** `cara-buat-prompt-chatgpt-contoh-harian.png`

```
Flat illustration style. Four scenes arranged in a grid — a book for studying, a briefcase for work, a cooking pot for daily life, and a paint palette for creativity — each with a small chat bubble icon showing prompts can be used in all areas of life. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Icons floating around composition. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Cara buat prompt ChatGPT — empat bab kehidupan harian: belajar, bekerja, memasak, dan kreativiti dengan ikon chat

### Image 3 — Tips & Mistakes (Geometric Patterns)

**Filename:** `cara-buat-prompt-chatgpt-tips-kesalahan.png`

```
Flat illustration style. A winding path from a warning triangle on the left to a checkmark on the right, with small geometric obstacles along the way representing common prompt mistakes being avoided. Dotted lines guide the path. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Geometric patterns and dotted lines connecting elements. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Cara buat prompt ChatGPT — laluan berliku dari tanda amaran ke tanda semak, mewakili mengelak kesilapan prompt

---

## Post #4 — Cara Buat Gambar AI (READY TO GENERATE)

**Slug:** `cara-buat-gambar-ai`
**Focus keyword:** `cara buat gambar ai`

> ⚠️ **Title corrected 2026-07-29.** This entry previously read "5 AI Tools Percuma 2026" — a title that matched neither `content-calendar.md` nor the researched keyword. Three files carried three different titles for Post #4. `content-calendar.md` is the source of truth for post titles.

> Prompts below are derived from the actual article text in `content/drafts/post-4-cara-buat-gambar-ai.html`. Compositions are rotated per the variation guide so the set reads as a curated collection, not a template repeat.

### 1. Featured — split composition

**Filename:** `cara-buat-gambar-ai-featured.png`
**Alt text:** `Ilustrasi menunjukkan ayat arahan bertukar menjadi gambar yang dihasilkan oleh AI`

```
Flat illustration style. A split scene: on the left, a simple speech bubble containing three abstract text lines representing a written instruction; on the right, that same shape blooming into a finished framed picture of a landscape. A thin connecting line links the two halves across the centre. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### 2. Steps section — isometric scene

**Filename:** `cara-buat-gambar-ai-langkah-gemini.png`
**Alt text:** `Paparan isometrik komputer riba menunjukkan proses menjana gambar AI langkah demi langkah`

```
Flat illustration style. Isometric view of an open laptop on a desk, with three stacked translucent layers floating above the screen representing sequential steps, each layer slightly offset to show depth and progression. A small download arrow sits at the top layer. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### 3. Prompt-writing section — geometric patterns

**Filename:** `cara-buat-gambar-ai-tulis-prompt.png`
**Alt text:** `Ilustrasi kucing oren tidur di atas kerusi rotan dengan cahaya matahari petang`

> Illustrates the article's own example prompt, so the image and the text reinforce each other.

```
Flat illustration style. An orange cat sleeping curled on a rattan chair beside a window, warm late-afternoon light falling across the floor in soft geometric shafts. Subtle geometric patterns and dotted lines radiate outward from the chair, suggesting the descriptive details that produced the scene. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### 4. Limitations section — minimalist negative space

**Filename:** `cara-buat-gambar-ai-had-kekurangan.png`
**Alt text:** `Ilustrasi minimalis menggambarkan had penggunaan harian alat AI percuma`

> Deliberately avoids depicting hands, since the section text discusses AI rendering hands badly.

```
Flat illustration style. Minimalist composition with generous negative space: a single simple meter or gauge shape, partially filled, sitting alone in the frame with a small stack of three picture frames beside it — two complete, one faded and incomplete. Suggests a daily usage limit being reached. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

---

## Post #5 — Cara Buat Poster Guna Canva (PUBLISHED ✅)

**Slug:** `cara-buat-poster-guna-canva`
**Focus keyword:** `cara buat poster guna canva`
**Content summary:** Panduan praktikal memilih saiz poster, menggunakan *template* atau Magic Design, membina hierarki visual, menyemak cadangan AI, memastikan aksesibiliti dan mengeksport fail dengan betul.

> Semua imej dijana melalui built-in OpenAI image generation, diperiksa pada resolusi asal, dan diarkibkan. Pemeriksaan mendapati tiada teks boleh dibaca, logo Canva, watermark, UI palsu, artifak anatomi, atau halo/blob oren yang tidak diminta.

WordPress Media upload complete via Respira: featured **Media 625**, size **Media 626**, hierarchy **Media 627**, and export **Media 628**. Alt text was set in Malay and the three in-content URLs were used on the first published version of post **629**: https://digitrustlab.com/cara-buat-poster-guna-canva/.

**Screenshot refresh (23 August 2026):** The three generated in-content illustrations are retained below for provenance, but they are **superseded and must not be reinserted** into the live tutorial. The live article now uses authentic Canva UI captures from `content/assets/canva-post-5/`, with native lightboxes and Malay captions/alt text. The featured illustration (Media 625) remains the featured image; it is not presented as evidence of a Canva interface.

| Live tutorial coverage | Source capture | WordPress media | Use |
|---|---|---:|---|
| Choose poster size | `02-canva-print-poster-options.jpg` | 639 | Authentic Canva UI figure |
| Find a template | `09-canva-template-search-results.jpg` | 640 | Authentic Canva UI figure |
| Magic Design prompt | `11-canva-magic-design-prompt.jpg` | 641 | Authentic Canva UI figure |
| Magic Design result | `13-canva-magic-design-results-ready.jpg` | 642 | Authentic Canva UI figure |
| Visual hierarchy | `07-canva-heading-toolbar.jpg` | 643 | Authentic Canva UI figure |
| Elements/uploads workflow | `15-canva-elements-search.jpg` + `16-canva-uploads-panel.jpg` | 644 | Combined authentic Canva UI figure |
| Final export check | `06-canva-download-settings.jpg` / `08-canva-download-ready.jpg` | 628 (existing attachment) | Authentic Canva UI replacement |

The expanded live article contains nine in-content tutorial figures in total. Media 639–644 and the retained capture archive are the source of truth for future edits; do not publish from the older three-figure HTML draft without first refreshing it from the live article.

| Archived asset | SHA-256 |
|---|---|
| `cara-buat-poster-guna-canva-featured.png` | `EB37D8CBCA192E9DA245E2D4B59B2C56EDC2F802DC711BB6EA477C46A37B91A4` |
| `cara-buat-poster-guna-canva-pilih-saiz.png` | `FA6834C22AAA20898AD55F647A2283A27892879875A5025721A065640A891827` |
| `cara-buat-poster-guna-canva-hierarki-visual.png` | `89A428113FD1C4BB7080D68194ABC80153F6617C90357382FD737DA8079CBA13` |
| `cara-buat-poster-guna-canva-semak-sebelum-eksport.png` | `18D32D354F3A53E0564197C99A369F9BAFF0832153B522A90E55FC8CA16AFF35` |

### 1. Featured — split composition

**Filename:** `cara-buat-poster-guna-canva-featured.png`
**Alt text:** `Ilustrasi pereka menyusun poster dengan bantuan idea AI`

```text
Flat illustration style. Split composition: on the left, a person at a tidy desk reviewing an abstract poster layout on a laptop; on the right, a freestanding blank poster board with balanced geometric colour blocks, image frames and a small neutral sparkle symbol suggesting AI-assisted ideas. Keep the laptop display abstract and non-interface-like, with no buttons or screen text. Generous breathing room between the person and poster board. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, words, logos, Canva branding, fake UI, or watermark. Wide format 16:9. Both person and robot have complete visible arms and hands with natural positioning. No rounded orange blob, halo, disc or abstract orange shape behind or intersecting the person’s arm or body.
```

### 2. Choosing the size — top-down flat lay

**Filename:** `cara-buat-poster-guna-canva-pilih-saiz.png`
**Alt text:** `Lakaran tiga susunan poster dengan nisbah yang berbeza sebelum memilih saiz`

```text
Flat illustration style. Top-down flat lay showing three blank poster boards with clearly different proportions: portrait, square and landscape, arranged with a ruler, pencil, colour swatches and simple geometric paper shapes. The boards should communicate choosing a design size without any interface or labels. Balanced spacing, strong visual hierarchy and generous warm background space. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, words, numbers, dimensions, logos, fake UI, or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

### 3. Visual hierarchy — geometric poster

**Filename:** `cara-buat-poster-guna-canva-hierarki-visual.png`
**Alt text:** `Contoh susunan poster dengan tajuk, penerangan dan arahan yang mempunyai saiz berbeza`

```text
Flat illustration style. Front-facing geometric poster composition on a warm off-white surface: one large charcoal headline bar at the top, a medium orange supporting bar beneath it, several smaller aligned detail bars, and one simple image frame placed with clear spacing. The visual must show hierarchy through scale, contrast and alignment, while every text area remains abstract and completely unreadable. Use a calm editorial layout with generous negative space, not a social-media app screen. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, pseudo-writing, words, logos, fake UI, or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

### 4. Final export check — isometric scene

**Filename:** `cara-buat-poster-guna-canva-semak-sebelum-eksport.png`
**Alt text:** `Pemeriksaan poster pada komputer riba dan telefon sebelum dieksport`

```text
Flat illustration style. Isometric scene with a laptop and smartphone side by side, each showing the same abstract poster made from clean geometric blocks, with a magnifying glass, a simple checklist card and two crisp verification checkmarks nearby. The screens must look like blank design previews rather than software interfaces; no buttons, menus or labels. Show a clear final-review workflow through the arrangement of the objects and a subtle connecting arrow. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, words, numbers, logos, fake UI, or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

---

## Post #6 — ChatGPT vs Gemini vs Claude (PUBLISHED ✅)

**Slug:** `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026`
**URL:** https://digitrustlab.com/chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026/
**Content summary:** Comparison of ChatGPT (text generation, ease of use), Gemini (coding, complex tasks), Claude (security, privacy). Covers pricing, student suitability, platform availability. Conclusion table with pros/cons. Recommendations by user type.

### Image 1 — Featured (Split Composition)

**Filename:** `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-featured.png`

```
Flat illustration style. Three robot characters standing side by side representing ChatGPT, Gemini, and Claude — one with a chat bubble symbol, one with a diamond symbol, and one with a shield symbol. A student figure in front looking at all three trying to choose. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split composition showing the three options clearly. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Ilustrasi tiga robot AI mewakili ChatGPT, Gemini dan Claude dengan pelajar memilih yang terbaik

### Image 2 — Intro (Minimalist Negative Space)

**Filename:** `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-intro.png`

```
Flat illustration style. A person sitting at a desk with a laptop, three chat bubble icons floating above the screen — each with a distinct symbol inside (chat, diamond, shield) — representing the three AI platforms being considered. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist composition with generous negative space and a single focal element. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Orang duduk di meja dengan laptop dan tiga ikon chat bubble mewakili ChatGPT, Gemini dan Claude

### Image 3 — Comparison (Isometric Scene)

**Filename:** `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-comparison.png`

```
Flat illustration style. An isometric view of three platforms displayed as floating panels — one with a chat bubble icon, one with a diamond icon, one with a shield icon — each on a different level showing their unique strengths. Dotted lines connecting them showing comparison. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Isometric scene with layered depth. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Perbandingan isometrik tiga platform AI dengan simbol chat, berlian dan perisai

### Image 4 — Conclusion (Top-Down Flat Lay)

**Filename:** `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-conclusion.png`

```
Flat illustration style. A top-down flat lay of three cards arranged vertically — each card showing a distinct AI symbol (chat bubble, diamond, shield) — with a checklist icon and a graduation cap nearby, representing a student making their final choice. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Top-down flat lay perspective of objects arranged on a surface. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

**Alt text:** Susunan atas-bawah tiga kad AI dengan senarai semak dan topi graduasi untuk pelajar

---

## Post #7 — Cara Buat Nota Rapi dengan AI (DRAFTED — IMAGES GENERATED)

**Slug:** `cara-buat-nota-cantik-dengan-ai`
**Focus keyword:** `cara buat nota cantik`

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | `cara-buat-nota-cantik-dengan-ai-featured.png` | Flat illustration style. A polished wide featured illustration for an article about making neat, useful notes with AI for students and workers. Split composition: a person reviews organized notes beside a laptop while loose note cards transform into clean sections and a small abstract AI sparkle symbol communicates structure, review and human judgment. Simple geometric shapes, bold dark charcoal outlines, clean modern minimal editorial artwork. Warm off-white `#FAFAF8` background, orange `#E8621A` accents, dark charcoal `#1A1A1A` outlines and elements, white highlights. Wide 16:9. No readable text, logos or watermark. Both person and robot have complete visible arms and hands with natural positioning. No malformed anatomy, accidental pseudo-letters, rounded orange blobs, halos or discs. | Ilustrasi AI membantu menyusun nota yang kemas untuk pelajar dan pekerja |
| Intro | `cara-buat-nota-cantik-dengan-ai-alat.png` | Flat illustration style. Top-down flat lay showing the preparation stage for turning raw study or work material into useful notes with AI: notebook, laptop, phone, paper note cards, privacy shield and three abstract tool symbols represented by simple shapes. Balanced spacing, warm off-white `#FAFAF8` background, orange `#E8621A` accents, dark charcoal `#1A1A1A` outlines and elements, white highlights. Clean modern minimal editorial artwork, wide 16:9. No readable text, letters, numbers, logos or watermark. Clean abstract lines, bullets and checkboxes only. No clutter, rounded orange blobs, halos or discs. | Persediaan bahan dan pilihan alat AI untuk membuat nota |
| Fact-check | `cara-buat-nota-cantik-dengan-ai-semak-fakta.png` | Flat illustration style. Isometric left-to-right flow showing loose note cards moving through a magnifying glass and a shield/checkmark checkpoint, then becoming a short organized stack with bullet shapes, calendar and lock icons to suggest checking names, dates, figures and sensitive information. Warm off-white `#FAFAF8` background, orange `#E8621A` accents, dark charcoal `#1A1A1A` outlines and elements, white highlights. Clean modern minimal editorial artwork, wide 16:9. No readable text, letters, numbers, logos or watermark. Use only clean abstract lines, bullets and checkmarks. No clutter, rounded orange blobs, halos or discs. | Semakan fakta dan privasi sebelum nota AI dikongsi |
| Conclusion | TBD | Fourth in-content image remains deferred until the publication package is assembled. | TBD |

> **Generated and visually audited 24 August 2026.** All three assets use the DigiTrust Lab palette and were checked at native resolution for malformed anatomy, accidental readable text, logos, watermarks, orange blobs and halos. SHA-256 hashes are recorded in `content/content-calendar.md`.

> **WordPress staging (24 August 2026):** Media 653 is assigned as the featured image for draft Post 656; Media 654 and Media 655 are inserted in the draft body. The article remains unpublished. WriterZen's 0/3 image warning is retained as historical workflow evidence.

---

## Post #8 — Cara Buat Poster dengan ChatGPT (PUBLISHED — MEDIA REPAIR VERIFIED)

**Slug:** `cara-buat-poster-dengan-chatgpt`

**Focus keyword:** `poster chatgpt`

The native Malay draft is at `content/drafts/cara-buat-poster-dengan-chatgpt.html`. The original four assets were generated and visually inspected on 4 September 2026; project copies are in `content/assets/post-8/` and archive copies are under `G:\\Zamzam Biznez\\DigiTrustLab\\Blog images`. On 5 September 2026, the featured and idea-theme visuals were replaced after live review: the original featured image repeated in the body and used a pale human figure, while the original idea-theme image contained an ambiguous seated figure. The replacement assets below use the owner-selected **More Depth** mode and were inspected at native resolution before upload. A human-led candidate with a malformed hand was rejected and was not archived or uploaded.

| Archived asset | SHA-256 |
|----------------|---------|
| `cara-buat-poster-dengan-chatgpt-featured.png` | `BA85E3766E73F7DB12C3BD73B903C568BEA8DAE3BEABF1933EEBD1D500D054C0` |
| `cara-buat-poster-dengan-chatgpt-idea-tema.png` | `4884285CD7F4639F674CA24DA4D45CBF0DFA4636457C9A96C7F7996A719AC451` |
| `cara-buat-poster-dengan-chatgpt-chatgpt-vs-canva.png` | `D72523AF259A44006DD7816529CAE59286FB7F016DD0136EC9EAD20E508AB001` |
| `cara-buat-poster-dengan-chatgpt-semak-sebelum-eksport.png` | `F500EC0FC38B325D2F6D5BCCA9DF923DA63C31CC349F94335D793E95A6E5DC4D` |

| Replacement asset (More Depth) | SHA-256 |
|-------------------------------|---------|
| `cara-buat-poster-dengan-chatgpt-featured-v2.png` | `31B0EDEE3DFBBB367CD6B2756E14964384344C8B6F68313A16A482DAFD422BA3` |
| `cara-buat-poster-dengan-chatgpt-idea-tema-v2.png` | `09E3DD5E784EE093547F7355057F707E4D8F93BDE5F9D24CDA7540030A0D820C` |

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | `cara-buat-poster-dengan-chatgpt-featured.png` | Flat editorial illustration of a beginner at a desk reviewing a poster concept on a laptop, with a clean chat interface, a simple poster frame and small geometric idea cards connected in a calm workflow. Warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clear focal point, generous negative space, clean modern minimal composition. No readable text, logos, branded interface, watermark or numbers. Wide 16:9. No rounded orange blob, halo or disc behind a person. | Pemula merancang poster dengan bantuan ChatGPT |
| Idea tema | `cara-buat-poster-dengan-chatgpt-idea-tema.png` | Flat editorial illustration showing four abstract poster concept cards arranged in a neat comparison grid: minimal editorial, geometric modern, product visual and friendly illustration. Each card uses distinct shapes and composition without words. Warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Balanced spacing, clean modern minimal design. No readable text, logos, watermark or numbers. Wide 16:9. No rounded orange blobs, halos or discs. | Empat idea tema poster untuk dibandingkan sebelum memilih reka bentuk |
| ChatGPT dan Canva | `cara-buat-poster-dengan-chatgpt-chatgpt-vs-canva.png` | Flat editorial split composition showing the difference between AI visual exploration and controlled poster layout: on the left, abstract image ideas and a chat bubble; on the right, a tidy poster canvas with separate geometric text blocks and alignment guides, all without readable words. Warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clear visual contrast, clean modern minimal style. No branded logos, readable text, watermark or numbers. Wide 16:9. No rounded orange blob, halo or disc. | Perbandingan idea visual ChatGPT dan susun atur poster dalam editor reka bentuk |
| Semakan akhir | `cara-buat-poster-dengan-chatgpt-semak-sebelum-eksport.png` | Flat editorial illustration of a finished abstract poster being reviewed on a laptop and phone beside a checklist, magnifying glass, contrast symbol and export arrow. Use abstract lines and checkmarks only, no readable text. Warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean modern minimal composition with generous breathing room. No logos, watermark, readable text or numbers. Wide 16:9. No rounded orange blob, halo or disc. | Semakan visual dan kandungan poster sebelum mengeksport fail akhir |

### Replacement prompts (owner-selected More Depth mode)

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured replacement | `cara-buat-poster-dengan-chatgpt-featured-v2.png` | More Depth controlled 2.5D/isometric object-led editorial illustration. A large blank poster board with abstract orange and charcoal geometric shapes, three smaller concept cards, a chat-bubble token, colour swatches, pencil and export arrow arranged as a clear left-to-right workflow on a warm desk surface. DigiTrust Lab palette: #FAFAF8, #FFF3EE, #E8621A, #1A1A1A, white and restrained beige. Generous negative space, no people or anatomy, no readable text, letters, numbers, logos, branded UI, watermark, robot, halo or orange blob. Wide 16:9, clean and safe for thumbnail cropping. | Aliran kerja visual untuk merancang poster dengan ChatGPT |
| Idea tema replacement | `cara-buat-poster-dengan-chatgpt-idea-tema-v2.png` | More Depth controlled 2.5D comparison board with four abstract poster concept cards in a balanced 2x2 grid: minimal editorial, geometric modern, product visual and friendly illustration represented by shapes only. Use the DigiTrust Lab palette #FAFAF8, #FFF3EE, #E8621A, #1A1A1A, white and restrained beige. No people, faces, limbs, clothing, anatomy, readable text, letters, numbers, logos, branded UI, watermark or labels. Wide 16:9, spacious and calm. | Empat idea tema poster abstrak untuk dibandingkan sebelum memilih reka bentuk |

### Featured re-edit v3 — lighter background (LIVE; OWNER REPLACED MANUALLY)

**Filename:** `cara-buat-poster-dengan-chatgpt-featured-v3.png`

**Status:** Generated and reviewed at native resolution, then approved by the
owner on 2026-09-05; saved to the project asset archive and the external image
archive. The owner manually replaced the live WordPress featured image on
2026-09-07. Fresh Respira read-back confirms Post 721 now uses attachment
**Media 727** at the v3 URL below, with the planned Malay alt text. The direct
asset returned HTTP 200 (`image/png`, 138,714 bytes) on verification. The
manual replacement used a new filename and attachment ID, so it was not the
URL-preserving replacement path. The former attachment 723 is no longer
available, and confirmed-unused media 717 and 718 remain absent. No further
media cleanup is pending.

**SHA-256:** `213331300D756B36AB35EE428AACB09CE8ED749AB45FDC793D82A4EDA83ADA09`

**Prompt:** More Depth controlled 2.5D edit of the existing featured image. Keep
the poster board, abstract cards, chat token, colour swatches, pencil, export
arrow, object placement, shadows and 16:9 framing. Change only the broad
beige/tan background so warm off-white `#FAFAF8` is the dominant visible field
(at least two-thirds); keep peach/cream and restrained beige as small supporting
accents, with orange `#E8621A`, charcoal `#1A1A1A`, and white highlights. No
people, anatomy, text, letters, numbers, logos, branded UI, watermark, dark or
saturated backdrop, full-bleed peach/tan shapes, or orange blobs.

---

## Post #9 — 10 Prompt Gemini AI untuk Edit Foto dengan Mudah (PUBLISHED ✅)

**Slug:** `prompt-gemini-ai-untuk-edit-foto`

The article is live at `https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/` (Post ID 582). The controlled draft remains at `content/drafts/10-prompt-gemini-ai-edit-foto.html`. All four images were generated, visually checked, archived under `G:\\Zamzam Biznez\\DigiTrustLab\\Blog images`, and SHA-256 verified against their generated sources. Do not present any generated image as an actual Gemini edit result.

WordPress Media upload complete via Respira: featured **Media 578**, intro **Media 579**, comparison **Media 580**, conclusion **Media 581**. Fresh rendered verification confirms Media 579–581 resolve at 1672×941 with the planned Malay alt text.

| Archived asset | SHA-256 |
|----------------|---------|
| `prompt-gemini-ai-untuk-edit-foto-featured.png` | `21AA5A29916A4F9F4E4425A1D2881830211822F402ED0214F726679EC6876C8B` |
| `prompt-gemini-ai-edit-foto-upload.png` | `D3528C1CD6FAF1E23080CAFCC7FAAAF25A56793E196A99969C1EEF648178AD7E` |
| `prompt-gemini-ai-edit-foto-sebelum-selepas.png` | `DFE51787E5E16912D4BD9358465D2F4A0C6A07715CFB0275A3B7127B7BF13AF5` |
| `prompt-gemini-ai-edit-foto-prompt-dan-hasil.png` | `D52558A1271F90D837062AD6B0D518E2146A7EC7EA92A0C6643B0F3023250303` |

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | `prompt-gemini-ai-untuk-edit-foto-featured.png` | Flat illustration style. A creator holds a portrait photo while a friendly AI editing interface shows three visual possibilities: a changed background, improved lighting, and a realistic colour correction. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split composition with the original portrait on the left and polished editing options on the right. Clean, modern, minimal. No text or words in the image. Wide format 16:9. | Ilustrasi proses menggunakan prompt Gemini AI untuk mengedit foto |
| Intro | `prompt-gemini-ai-edit-foto-upload.png` | Flat illustration style. A smartphone portrait photo is being uploaded into a simple AI workspace, with a privacy shield and small image thumbnail beside it. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Minimalist negative space composition with the photo and privacy symbol as the focal point. Clean, modern, minimal. No text or words in the image. Wide format 16:9. | Persediaan foto dan privasi sebelum menggunakan Gemini AI |
| Comparison | `prompt-gemini-ai-edit-foto-sebelum-selepas.png` | Flat illustration style. A side-by-side comparison of the same portrait before and after careful AI editing: the left side has flat lighting and a cluttered background, while the right side has balanced lighting and a clean background, with the person's identity preserved. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split comparison composition with a subtle curved divider and no labels. Clean, modern, minimal. No text or words in the image. Wide format 16:9. | Perbandingan foto sebelum dan selepas suntingan Gemini AI |
| Conclusion | `prompt-gemini-ai-edit-foto-prompt-dan-hasil.png` | Flat illustration style. A top-down flat lay of a notebook with abstract prompt lines, a phone displaying a polished portrait, a small colour palette, and a consent/privacy card represented only by an icon. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Top-down flat lay composition with balanced spacing and gentle geometric accents. Clean, modern, minimal. No text or words in the image. Wide format 16:9. | Ringkasan prompt dan hasil suntingan foto dengan Gemini AI |

---

## Post #10 — Cara Menggunakan Canva AI Photo Editor untuk Menyunting Foto dengan Mudah (PUBLISHED ⚠️)

**Slug:** `cara-guna-canva-ai-photo-editor`

**URL:** https://digitrustlab.com/cara-guna-canva-ai-photo-editor/

**Focus keyword:** `canva ai photo editor`

**Status evidence:** Post 686 was published on 2026-08-26 08:38:24 (+08:00). Naturalness, voice, structure and link gates passed; Google Search Console later showed the exact URL indexed; both ClickRank tracker rows were verified; Screpy rank tracking remains pending/unverified.

**Prompt provenance:** The available repository evidence records the final assets, placements and instructional uses, but does not contain the original generation prompts or owner-selected image mode for this post. No prompt text or mode is inferred here.

### Evidence-backed asset record

The final evidence contains one separate DigiTrust Lab brand-color featured asset and four inline instructional assets. The published asset extensions and the local manifest names differ for the three safe screenshots, so both are recorded where evidence provides them.

| Placement | Evidence filename | Published asset / attachment | Alt text or evidence |
|-----------|------------------------|-----------------------------|---------------------|
| Featured | `canva-ai-photo-editor-featured.png` | Featured attachment 693 | Separate DigiTrust Lab brand-color hero asset; exact alt text is not captured in the cited local evidence. |
| Intro | `canva-ai-photo-editor-home-screen.png` | `canva-ai-photo-editor-home-screen.png` / attachment 692 | `Paparan halaman utama Canva dengan cadangan tugasan untuk memulakan suntingan foto` |
| Step 1 | `02-canva-ai-photo-editor-prompt-safe.jpg` | `02-canva-ai-photo-editor-prompt-safe.jpg` / attachment 683 | `Paparan Canva AI dengan pilihan “Help me edit a photo” untuk memulakan suntingan foto` |
| Step 2 | `03-canva-ai-photo-editor-upload-options-safe.jpg` | `03-canva-ai-photo-editor-upload-options-safe.jpg` / attachment 684 | `Pilihan “Upload” dan “Add from Canva” dalam Canva AI untuk memilih sumber foto` |
| Step 3 | `04-canva-ai-photo-editor-canva-sources-safe.jpg` | `04-canva-ai-photo-editor-canva-sources-safe.jpg` / attachment 685 | `Panel sumber Canva selepas memilih “Add from Canva” tanpa membuka sumber peribadi` |

The manifest confirms the three safe screenshots contain no account header, email, avatar or other personal identifier. Its quarantined intermediate captures remain excluded from article use.

---

## Post #11 — Apa Itu MCP dalam AI dan Bagaimana Ia Berfungsi? (PUBLISHED ✅)

**Slug:** `apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi`
**URL:** https://digitrustlab.com/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi/
**Focus keyword:** `mcp ai`
**Content summary:** Explains MCP as an open standard connecting AI applications with external systems, using the host, client and server architecture. Distinguishes MCP from APIs and covers tools, resources, prompts and access safety.

### Image 1 — Featured (Split Composition)

**Filename:** `apa-itu-mcp-dalam-ai-dan-bagaimana-ia-berfungsi-featured.png`
**Alt text:** Ilustrasi AI berhubung dengan fail, pangkalan data dan aplikasi melalui sambungan terkawal

```
Flat illustration style. An AI application connected through a clear bridge to three simple external sources: a folder for files, a database cylinder, and a small app window, with a human viewer on the side understanding the connection. The bridge represents controlled context exchange, not unrestricted access. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Split composition. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### Image 2 — Host, Client and Server (Isometric Scene)

**Filename:** `apa-itu-mcp-host-client-server.png`
**Alt text:** Ilustrasi host, klien dan pelayan MCP berhubung dalam susunan berlapis

```
Flat illustration style. An isometric scene with a central AI application panel connected to three distinct layers: a host at the top, a smaller client connection in the middle, and a server at the bottom providing file, database and app symbols. Use clear lines and spacing to show the connection hierarchy without labels. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Isometric scene with layered depth. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### Image 3 — MCP and API (Geometric Patterns)

**Filename:** `apa-itu-mcp-dan-api.png`
**Alt text:** Ilustrasi laluan MCP dan API yang berbeza tetapi saling berkaitan

```
Flat illustration style. Two clean communication paths crossing a geometric network: one path shows an AI application reaching a tool through a structured connector, while the other shows two system blocks connected by a direct API line. The paths meet at a small shared data point to suggest that an MCP server can use an API behind the scenes. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Geometric patterns and dotted lines connecting elements. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

### Image 4 — Safety and Permissions (Top-Down Flat Lay)

**Filename:** `apa-itu-mcp-keselamatan-kebenaran.png`
**Alt text:** Ilustrasi kebenaran akses dan keselamatan apabila menggunakan MCP

```
Flat illustration style. A top-down flat lay showing a small key, a shield, a folder, a database cylinder and a checklist arranged around a central connection point. Some paths are open and some are blocked, representing minimum permissions and checking actions before approval. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Top-down flat lay perspective of objects arranged on a surface. Clean, modern, minimal. No text or words in the image. Wide format 16:9.
```

---

## Post #12 — Contoh Minit Mesyuarat: Cara Susun Nota dengan AI (GENERATED + STAGED — WP DRAFT 605)

**Slug:** `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai`
**Focus keyword:** `contoh minit mesyuarat`
**Content summary:** Panduan menyediakan minit mesyuarat yang kemas, memisahkan perbincangan daripada keputusan dan menggunakan AI sebagai pembantu menyusun nota tanpa menggantikan semakan manusia.

> Semua imej menggunakan palet oren DigiTrust Lab. Tiada imej mengandungi bentuk oren bulat, halo atau blob di belakang atau bersilang dengan lengan/badan manusia. Setiap imej telah diperiksa secara visual untuk artefak anatomi, teks, logo dan watermark.

| Archived asset | SHA-256 |
|----------------|---------|
| `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai-featured.png` | `9B774AB0477E9BA85EE864853A584323B26CB2B13C7CAD944FE322ABB53EB179` |
| `contoh-minit-mesyuarat-struktur-nota.png` | `D00F68821B09EB3D4D49A3CB726AFF8FBF3747FD07C65F0CE9DCFFA55CAED601` |
| `contoh-minit-mesyuarat-susun-nota-dengan-ai.png` | `DB23397B91C7B31411AFFC024D178BE465370CF8A994CA5F3D490214EDC4A2A9` |
| `contoh-minit-mesyuarat-semak-sebelum-kongsi-clean.png` | `C4A607C9741F89FF91AD32D97EFAACF3B9B162A09905388FF2FC76C2FC99D12B` |

> Image 4 was regenerated after the first archive pass. The corrected
> `-clean.png` is the only archived and referenced asset; the superseded
> pre-correction file (`contoh-minit-mesyuarat-semak-sebelum-kongsi.png`,
> `091BD6342046B55E30C2F39A42E55EDE9734951968B2E476960798F20DBEF7DF`) is no
> longer present in the archive and must not be reused. Verified 2026-08-16:
> the repo copy at `content/assets/` and the archived source in
> `DigiTrustLab\Blog images` are byte-identical (1,120,488 bytes).

### Native-resolution visual audit

| Asset | Inspection coverage | Result |
|-------|---------------------|--------|
| Featured | Full frame + marked regions at native resolution | PASS — clean orange palette; no anatomy artifacts, blobs, halos, text, logos or watermark |
| Struktur nota | Full frame + marked regions at native resolution | PASS — clean geometric layout; no malformed pseudo-writing, blobs, halos, text, logos or watermark |
| Menyusun nota dengan AI | Full frame + marked regions at native resolution | PASS — intentional clean pseudo-writing only: straight parallel strokes, aligned bullets/checkboxes, consistent spacing; no malformed glyphs, readable text, blobs or halos |
| Semakan akhir | Full frame + marked regions at native resolution | PASS — clean geometric before-and-after; no malformed pseudo-writing, blobs, halos, text, logos or watermark |

**Audit rule:** Preserve intentional pseudo-writing, abstract lines, bullets and checkboxes when they are clean and designed. Reject malformed glyphs, wobbly or merged strokes, accidental readable text or numbers, logos, watermarks, orange blobs or halos behind/intersecting people or arms.

### Image 1 — Featured (Split Composition)

**Filename:** `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai-featured.png`
**Alt text:** Ilustrasi menyusun nota mesyuarat dengan bantuan AI dan kalendar tindakan

```
Flat illustration style. A polished wide illustration showing a person reviewing clear meeting notes on a laptop while a second panel shows organized bullet points and a calendar, representing AI helping structure meeting notes. One person at a desk, laptop, meeting notes, calendar and subtle AI sparkle icon. Split composition, person and laptop on the left, organized notes and calendar on the right, generous breathing room. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, logos or watermark. Wide format 16:9. Both person and robot have complete visible arms and hands with natural positioning. No rounded orange blob, halo, disc or abstract orange shape behind or intersecting any person’s arm or body.
```

### Image 2 — Struktur Nota (Top-Down Flat Lay)

**Filename:** `contoh-minit-mesyuarat-struktur-nota.png`
**Alt text:** Struktur asas untuk menyediakan minit mesyuarat yang kemas

```
Flat illustration style. Top-down flat lay of a meeting table with a notebook, agenda sheet, clock, checklist, folder and simple speech bubbles arranged around a central clean page, showing the parts of organized meeting minutes. Balanced spacing, no people. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, logos or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

### Image 3 — Menyusun Nota dengan AI (Isometric Scene)

**Filename:** `contoh-minit-mesyuarat-susun-nota-dengan-ai.png`
**WP media:** ID 604, `https://digitrustlab.com/wp-content/uploads/2026/08/contoh-minit-mesyuarat-susun-nota-dengan-ai-1.png` (clean corrected upload; the prior defective media ID 602 is not referenced).
**Alt text:** AI membantu menyusun kad nota mesyuarat kepada keputusan dan tindakan

```
Flat illustration style. Isometric scene showing a laptop receiving abstract meeting-note cards and sorting them into three clean stacks represented by icons for agenda, decisions and action items. Small AI sparkle symbol and arrows show the flow from loose notes to organized stacks. Layered depth, no people. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, logos or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

### Image 4 — Semakan Akhir (Geometric Before-and-After)

**Filename:** `contoh-minit-mesyuarat-semak-sebelum-kongsi-clean.png` (corrected regeneration)
**Alt text:** Senarai semak untuk menyemak minit mesyuarat sebelum dikongsi

```
Flat illustration style. Geometric before-and-after composition showing a messy page of scattered note cards transforming into a clean concise meeting-minutes page with checklist and verification marks. Clear left-to-right transformation, no people. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. No text, logos or watermark. Wide format 16:9. No rounded orange blob, halo, disc or abstract orange shape.
```

---

## Post #13 — Contoh Prompt AI: Cara Menulis Arahan yang Jelas dan Berkesan (PUBLISHED — 2026-09-13)

**Slug:** `contoh-prompt-ai`
**Focus keyword:** `contoh prompt`
**Content summary:** Panduan praktikal untuk mengenal pasti hasil, memberikan konteks, menetapkan format dan menguji prompt AI bagi tugasan pembelajaran, kandungan dan kerja harian.

### Image 1 — Featured (Prompt and Result Comparison)

**Filename:** `contoh-prompt-ai-featured.png`
**Alt text:** Ilustrasi membandingkan arahan prompt AI dengan hasil yang lebih tersusun

```
Flat illustration style. A polished wide editorial illustration showing a person at a desk comparing two clean prompt cards with two AI result panels: one vague and scattered, one structured and clear. Include a laptop, small abstract AI sparkle and a human hand marking the clearer result. Split composition with generous breathing room, no readable text. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. Wide format 16:9. No logos, watermark, letters, numbers, money symbols, rounded orange blob, halo or disc behind or intersecting the person.
```

### Image 2 — Prompt Structure (Layered Blocks)

**Filename:** `contoh-prompt-ai-struktur-arahan.png`
**Alt text:** Ilustrasi komponen prompt AI seperti tugas, konteks, format dan batasan

```
Flat illustration style. Isometric composition of four connected modular blocks representing a well-structured AI prompt: a target symbol for the task, a small folder for context, a document frame for output format and a shield for constraints. A subtle arrow flows from the four blocks into a simple AI assistant panel. Use abstract lines and icons only, no readable text. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. Wide format 16:9. No logos, watermark, letters, numbers, rounded orange blob, halo or disc.
```

### Image 3 — Before and After Prompt (Geometric Cards)

**Filename:** `contoh-prompt-ai-sebelum-selepas.png`
**Alt text:** Perbandingan prompt AI yang umum dengan arahan yang lebih khusus

```
Flat illustration style. Clear left-to-right before-and-after composition: on the left, a loose stack of plain prompt cards with scattered lines and a confused sparkle; on the right, one organized card with aligned abstract lines, a target icon and a verification checkmark. The transformation should communicate clarity without any letters or words. Simple geometric shapes, bold charcoal outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. Wide format 16:9. No readable text, logos, watermark, numbers, rounded orange blob, halo or disc.
```

### Image 4 — Test and Improve Loop (Top-Down Workspace)

**Filename:** `contoh-prompt-ai-uji-dan-baiki.png`
**Alt text:** Kitaran menguji dan memperbaiki prompt AI dengan semakan manusia

```
Flat illustration style. Top-down workspace showing a prompt card, an AI response page, a magnifying glass, a pencil and a circular arrow returning to a revised prompt card. Include three small abstract assistant symbols in separate panels to suggest comparison across tools, plus a human checklist at the edge. Use clean abstract lines and checkmarks only, no readable text. Balanced spacing, warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. Clean, modern, minimal. Wide format 16:9. No logos, watermark, letters, numbers, money symbols, rounded orange blob, halo or disc.
```

### Image audit requirements

- Inspect every candidate at native resolution and beside the previous six
  featured thumbnails at archive-card size before archiving or uploading.
- Warm off-white remains the dominant background; reject heavy, dark or
  saturated backdrops, readable text, logos, watermarks, malformed anatomy,
  orange blobs or halos.
- Archive only the verified final files under `G:\\Zamzam Biznez\\DigiTrustLab\\Blog images` using the exact filenames above.

### Generated asset audit — 2026-09-13

All four generated assets were inspected at native resolution and the featured
asset was compared beside the previous six archived featured thumbnails at
archive-card size. The family passed the warm off-white, flat geometric and
clean-markup review; no readable text, logo, watermark, malformed anatomy,
orange blob or halo was found.

| Asset | Native size | SHA-256 |
|---|---:|---|
| `contoh-prompt-ai-featured.png` | 1672×941 | `D93B849298DFC6349FBC7303659BCFA93E2279678049779DB64295E35E1B1252` |
| `contoh-prompt-ai-struktur-arahan.png` | 1672×941 | `70C14BB19AC8BA9E210C802BE67B2480DC6BB634C1409B3BDC183BE5AA4134EA` |
| `contoh-prompt-ai-sebelum-selepas.png` | 1672×941 | `9EEBECE437A8B1D649DDA6F3EC19171BBA590D7E6DBEDB52157E0E3E0A07E77F` |
| `contoh-prompt-ai-uji-dan-baiki.png` | 1672×941 | `EBC73F652DE1C4EA11F31335A40AAA988BA49A9B602995B30C211D736DCA057A` |

---

## Post #14 — Cara Buat Banner Guna Canva (AUTHENTIC SCREENSHOTS UPLOADED)

**Slug:** `cara-buat-banner-guna-canva`
**Focus keyword:** `cara buat banner guna canva`
**Draft:** `content/drafts/cara-buat-banner-guna-canva.html`
**Content-derived scope:** Memilih saiz dan platform, menyusun layout dengan grid serta alignment, kemudian menyemak keterbacaan dan tetapan eksport banner.

**Authentic screenshot evidence record — 2026-09-19:** The three generated
inline figures below are retained for provenance only and are superseded for
procedural guidance by authentic Canva captures from one coherent tested sample.
The featured hero remains a separate generated brand asset and is not replaced.

| Material action | Authentic candidate | Tested state | Malay alt text | Caption | Caveat | Status |
|---|---|---|---|---|---|---|
| Custom size/create | `content/assets/post-14/screenshots/cara-buat-banner-guna-canva-saiz-create.png` | Create a design → Custom size; `1200 × 628 px` | Paparan Canva untuk menetapkan saiz tersuai 1,200 × 628 piksel sebelum mencipta reka bentuk | Paparan Canva untuk menetapkan saiz tersuai 1,200 × 628 piksel sebelum mencipta reka bentuk. | Matching Facebook format displayed as `1200 × 630 px`; tested sample is `1200 × 628 px`. | Uploaded as Media 751, 1480×810 |
| Editor text/Position | `content/assets/post-14/screenshots/cara-buat-banner-guna-canva-editor-position.png` | Sample text selected; text toolbar and Position → Arrange/Advanced | Editor Canva yang menunjukkan teks contoh, bar alat teks dan panel Position untuk penjajaran | Editor Canva yang menunjukkan kotak teks dan panel Position untuk menyusun kedudukannya. | Controls and values can vary by design, device, and account plan. | Uploaded as Media 752, 1904×840 |
| Share → Download/export | `content/assets/post-14/screenshots/cara-buat-banner-guna-canva-share-download.png` | Download panel; PNG Suggested; `1200 × 628 px`; quality and transparency controls | Panel Canva Download selepas memilih Share, termasuk format PNG dan saiz 1,200 × 628 piksel | Panel Canva Download selepas memilih Share dan menyemak tetapan eksport. | Export formats and advanced options vary by design and plan. | Uploaded as Media 753, 1020×650 |

**Capture and privacy audit:** Authenticated Chrome Canva tab, desktop viewport,
2026-09-19. Browser chrome and visible account identity were excluded by crop;
no email, avatar, or personal identifier is intended for article use. The
authentic captures were exported locally and uploaded through Respira as Media
751–753; no fake screenshot or fabricated URL is recorded. Coverage map:
`content/assets/post-14/screenshots/README.md`.

**Owner-selected visual mode:** `Strict flat design` — 2D vector, warna rata, garisan bersih; tanpa bayang, gradien, perspektif atau kedalaman palsu.

### Pre-generation variety record — 2026-09-16

| Field | Evidence / decision |
|---|---|
| Previous six inspected | `cara-buat-poster-guna-canva-featured.png` (#5), `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-featured.png` (#6), `cara-buat-nota-cantik-dengan-ai-featured.png` (#7), `prompt-gemini-ai-untuk-edit-foto-featured.png` (#9), `apa-itu-mcp-dalam-ai-dan-bagaimana-ia-berfungsi-featured.png` (#11), `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai-featured.png` (#12); native inspection completed |
| Previous-six pattern | Mostly human-led split scenes with desk/laptop or robot motifs; warm off-white backgrounds and orange/charcoal accents |
| Subject class | Modular banner canvas with safe-area frame and layout guides |
| Composition | Centered horizontal banner strip with three modular panels, direct-on canvas view, generous negative space; no split scene |
| Treatment | `geometric-infographic` |
| Human presence | No |
| Motif | Blank banner canvas, safe-area frame, ruler/crop marks, guide lines, modular blocks |
| Background | Predominantly warm off-white `#FAFAF8`, light-dominant-neutral |
| Immediate-prior difference vs #12 | 5 dimensions: subject, composition, perspective, treatment and human presence |
| Repeated-motif check | PASS — no person, desk, laptop, robot or calendar motif |
| Thumbnail comparison | PASS — featured inspected beside #5, #6, #7, #9, #11 and #12 at archive-card size; new object-led composition reads distinctly |
| Background review | PASS — all four assets retain a light-dominant warm off-white field |
| Archive-grid uniformity | PASS — all four are 1672×941 (16:9), with consistent flat treatment and palette |

### Image 1 — Featured (Banner Workflow Canvas)

**Filename:** `cara-buat-banner-guna-canva-featured.png`
**Alt text:** Ilustrasi aliran kerja menyusun banner Canva daripada kanvas kosong kepada susun atur yang kemas

```
Strict flat design, 2D vector illustration in a wide 16:9 frame. Object-led diagrammatic composition viewed directly from the front: one large blank horizontal banner canvas in the centre, divided into three neat modular colour blocks with a visible inner safe-area frame, small ruler and crop marks, and one simple orange directional arrow showing the workflow from blank canvas to organised layout. Use solid fills and clean #1A1A1A outlines only. Dominant warm off-white #FAFAF8 background covering at least two thirds of the frame, with restrained #FFEADD and #E8621A accents and white highlights. No people, hands, desk, laptop, robot, calendar, poster board, photo-editing motif or pseudo-UI. No readable text, letters, numbers, logos, watermark, shadows, gradients, perspective, depth cues, orange blob, halo or disc. Keep every edge crisp and geometry intentional; leave comfortable breathing room around the banner.
```

**Placement status:** Retained as the separate featured hero candidate. It does
not provide interface evidence.

### Image 2 — Size and Platform Planning

**Placement status:** `SUPERSEDED FOR PROCEDURAL GUIDANCE` by the authentic
`cara-buat-banner-guna-canva-saiz-create.png` capture; retained below for
provenance only.

**Filename:** `cara-buat-banner-guna-canva-pilih-saiz.png`
**Alt text:** Tiga nisbah kanvas dan kawasan selamat untuk memilih saiz banner

```
Strict flat design, 2D vector illustration in a wide 16:9 frame. Show three blank canvases arranged horizontally in distinct wide, square-ish and tall aspect ratios, each with a smaller inner safe-area frame, simple ruler ticks and crop marks, plus one small SQUARE orange selector box containing an angular white checkmark beneath the canvases to communicate choosing a platform size. Direct-on flat view, solid fills, clean #1A1A1A outlines. Use only rectangular canvases, square corner marks and straight ruler lines; absolutely no circles, discs, blobs, halos, rounded badges or curved shapes. Dominant warm off-white #FAFAF8 background, restrained #FFEADD and #E8621A accents, white highlights. No readable text, letters, numbers, logos, watermark, people, desk, laptop, robot, poster scene, photo-editing interface, shadows, gradients, perspective or depth cues.
```

### Image 3 — Layout, Grid and Alignment

**Placement status:** `SUPERSEDED FOR PROCEDURAL GUIDANCE` by the authentic
`cara-buat-banner-guna-canva-editor-position.png` capture; retained below for
provenance only.

**Filename:** `cara-buat-banner-guna-canva-layout-grid.png`
**Alt text:** Grid dan panduan membantu menyusun elemen banner dengan kemas

```
Strict flat design, 2D vector illustration in a wide 16:9 frame. One blank horizontal banner canvas fills the centre, overlaid with a clean modular rectangular grid and guide lines. Place three abstract RECTANGULAR content blocks aligned to the grid, with small square anchor marks and short orange straight position arrows indicating consistent alignment. Use only rectangles, straight lines, square corner marks and tiny square anchors; absolutely no circles, discs, blobs, halos, rounded pills or curved shapes. Solid fills and crisp #1A1A1A outlines only, viewed directly on the canvas with no depth or perspective. Dominant warm off-white #FAFAF8 background, restrained #FFEADD and #E8621A accents, white highlights. No readable text, letters, numbers, logos, watermark, people, desk, laptop, robot, poster or photo-editing motif, pseudo-UI, shadows or gradients.
```

### Image 4 — Export, Readability and Final Check

**Placement status:** `SUPERSEDED FOR PROCEDURAL GUIDANCE` by the authentic
`cara-buat-banner-guna-canva-share-download.png` capture; retained below for
provenance only.

**Filename:** `cara-buat-banner-guna-canva-eksport-semak-akhir.png`
**Alt text:** Semakan keterbacaan, tepi dan format sebelum mengeksport banner

```
Strict flat design, 2D vector illustration in a wide 16:9 frame. Show a completed blank horizontal banner with one black outlined magnifying glass at the left, a square check box with an angular checkmark at the right, two small rectangular contrast swatches, crop and edge marks, and three small rectangular export-format tiles represented by a triangle, square and horizontal bar only. Arrange the elements as a calm final-check workflow around the banner, with no interface imitation. Use solid flat fills, crisp #1A1A1A outlines, direct-on 2D view. Dominant warm off-white #FAFAF8 background, restrained #FFEADD and #E8621A accents, white highlights. The only curved shape allowed is the black outlined magnifying lens; no orange circles, discs, blobs, halos, rounded badges or circular format marks. No readable text, letters, numbers, logos, watermark, people, desk, laptop, robot, poster or photo-editing motif, shadows, gradients, perspective or depth cues.
```

### Generated asset audit — 2026-09-16

All four generated assets were inspected at native resolution. The featured asset
was also compared beside the previous six featured thumbnails at archive-card size.
No readable text, accidental numbers, logo, watermark, pseudo-writing, orange blob,
halo or malformed geometry was found. Archive copies match repository hashes exactly.

| Asset | Native size | SHA-256 | Repo/archive parity |
|---|---:|---|---|
| `cara-buat-banner-guna-canva-featured.png` | 1672×941 | `03207DD14BE26A7B0CFE84B887B182465A27297EFCAD162AD78472E0A518CE53` | PASS |
| `cara-buat-banner-guna-canva-pilih-saiz.png` | 1672×941 | `ABEFAA52D2CE3AE9C50D7834C603D47B668CF82346FBC81E99FDFFEC5B8A36B4` | PASS |
| `cara-buat-banner-guna-canva-layout-grid.png` | 1672×941 | `B4ADE982A97A4484DB66EC90B9960FFDD1DFC157BA59FEDAFD4B5F7644BF1FEA` | PASS |
| `cara-buat-banner-guna-canva-eksport-semak-akhir.png` | 1672×941 | `62B234FE3F3B8C2BA8D7B69D43E571085637ADA55B1E05E33619F6C7BA22EC52` | PASS |

**Final audit:** Featured native visual audit PASS; featured six-thumbnail
comparison PASS; background review PASS; archive-grid uniformity PASS. The
three generated inline figures are **SUPERSEDED — RETAINED FOR PROVENANCE** by
the authentic screenshot coverage above. Screenshot local byte export and
WordPress upload are **COMPLETE**: the three coverage entries have durable
files, privacy review, alt/caption evidence and uploaded URLs/media IDs 751–753.

---

## Generic CTA Card — AI Skills and Digital Product Creation

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| CTA card | `ai-skills-digital-product-creation-card.png` | Flat editorial illustration of a clean desk with a laptop displaying abstract AI workflow cards, a notebook with simple geometric sketches, and modular digital product blocks; warm editorial, trustworthy, minimal, soft natural lighting; use the documented DigiTrust Lab warm palette (#FAFAF8, #FFF3EE, #FFEADD, #E8621A, #1A1A1A, white); wide 16:9 composition at card-friendly 800x450px, generous negative space, no readable text, no logos, no money symbols, no article-specific objects, no urgency or scarcity cues. | Ilustrasi komputer riba dengan aliran kerja AI dan penciptaan produk digital |
