# Image Prompts Library — DigiTrust Lab

> Copy-paste ready prompts for ChatGPT or Gemini image generation. Each post has 4 images: 1 featured + 3 in-content. Paste the prompt into the selected provider, download the result, and upload it to WordPress Media with the given filename.
>
> **Published posts** have content-derived prompts based on actual article text.
> **Planned posts** are marked TBD — prompts will be written after content is drafted.
>
> ⚠️ **`content/content-calendar.md` is the source of truth for post titles.** Section headings here are short labels for scanning, not authoritative titles. If a heading here names a *different topic* rather than a shortened version of the calendar title, the calendar wins — fix this file. (Audited 2026-07-29: Post #4 had genuinely diverged and was corrected; Posts #5, #7–#10 verified as consistent short forms.)

## 🎨 Design System (never change these)

| Element | Value |
|---------|-------|
| Style | DigiTrust Lab illustration family: flat editorial baseline with controlled treatments below |
| Background | Warm off-white `#FAFAF8` |
| Primary accent | Orange `#E8621A` |
| Dark elements | Dark charcoal `#1A1A1A` |
| Highlights | White |
| Aspect ratio | 16:9 (wide, min 1024×576) |
| Text in image | No readable text by default; clean intentional pseudo-writing, abstract lines, bullets, and checkboxes are allowed and should be preserved |

## 🚦 Featured-image variety gate (MANDATORY)

The archive grid is a visual product, not a row of interchangeable article
thumbnails. Before generating every new featured image, inspect the previous six
featured thumbnails together at archive-card size and record the comparison below.
This gate is blocking: if the thumbnail comparison or any rule fails, do not
archive, upload, or publish the image. Regenerate the concept first.

### Required pre-generation record

```text
Previous six thumbnails inspected: [six filenames or post numbers]
Visual mode: [object-led | abstract-symbolic | diagrammatic | environmental |
              editorial-collage | top-down | split-transformation | human-led]
Subject class: [specific subject, not “AI”]
Composition: [specific layout and perspective]
Treatment: [approved treatment name below]
Human presence: [yes | no]
Repeated motif check: [PASS | FAIL]
Immediate-prior difference count: [0–5 dimensions; must be ≥3]
Thumbnail comparison: [PASS | FAIL]
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
  --thumbnail-comparison pass
```

The command checks the recorded history and blocks a failed or incomplete
decision. It cannot see the pixels itself, so `thumbnail-comparison pass` is
valid only after the worker has actually viewed the six thumbnails together.

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
| #5 | `cara-buat-poster-guna-canva-featured.png` | human-led | person, Canva board, laptop | split | flat editorial vector | yes | person laptop Canva board |
| #6 | `chatgpt-vs-gemini-vs-claude-panduan-pilihan-ai-2026-featured.png` | human-led | student, three AI robots | split | flat editorial vector | yes | student three robots chooser |
| #7 | `cara-buat-nota-cantik-dengan-ai-featured.png` | human-led | person, organised notes, laptop, AI sparkle | split | flat editorial vector | yes | person desk laptop robot |
| #9 | `prompt-gemini-ai-untuk-edit-foto-featured.png` | human-led | creator, portrait, editing interface | split | flat editorial vector | yes | creator portrait smartphone editing interface |
| #11 | `apa-itu-mcp-dalam-ai-dan-bagaimana-ia-berfungsi-featured.png` | diagrammatic | AI connection, files, database, app, human observer | split | flat editorial vector | yes | AI bridge files database app human observer |
| #12 | `contoh-minit-mesyuarat-cara-susun-nota-dengan-ai-featured.png` | human-led | person, meeting notes, calendar | split | flat editorial vector | yes | person desk laptop calendar |

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
Flat illustration style. [SUBJECT DESCRIPTION]. Simple geometric shapes, bold outlines. Color palette: warm off-white (#FAFAF8) background, orange (#E8621A) accents, dark charcoal (#1A1A1A) outlines and elements, white highlights. [VISUAL ELEMENT — see Variation Guide above]. Clean, modern, minimal. No text or words in the image. Wide format 16:9.

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
2. Ask the selected provider: *"Re-create this exact scene but with warm off-white (#FAFAF8) background, flat illustration style, charcoal (#1A1A1A) outlines, orange (#E8621A) accents, white highlights. All human hands must have five fingers. No text, labels, logos, or watermarks."*
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

1. Inspect the previous six featured thumbnails and complete the variety record
2. Find the post you're working on below
3. Copy the **Prompt** block for each image
4. Paste into ChatGPT or Gemini
5. Download the generated image
6. Upload to WordPress Media Library with the exact **Filename**
7. Set Malay alt text (provided with each image)
8. Assign featured image or insert into post content only after the thumbnail
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

## Post #8 — 5 Template Notion (PLANNED — TBD)

**Slug:** TBD

> Prompts will be written after content is drafted in WriterZen.

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | TBD | TBD | TBD |
| Intro | TBD | TBD | TBD |
| Comparison | TBD | TBD | TBD |
| Conclusion | TBD | TBD | TBD |

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

## Post #10 — AI vs Canva Design (PLANNED — TBD)

**Slug:** TBD

> Prompts will be written after content is drafted in WriterZen.

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | TBD | TBD | TBD |
| Intro | TBD | TBD | TBD |
| Comparison | TBD | TBD | TBD |
| Conclusion | TBD | TBD | TBD |

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
