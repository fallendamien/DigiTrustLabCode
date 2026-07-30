# Image Prompts Library — DigiTrust Lab

> Copy-paste ready prompts for Gemini Nano Banana 2. Each post has 4 images: 1 featured + 3 in-content. Paste the prompt into Gemini, download the result, upload to WordPress Media with the given filename.
>
> **Published posts** have content-derived prompts based on actual article text.
> **Planned posts** are marked TBD — prompts will be written after content is drafted.
>
> ⚠️ **`content/content-calendar.md` is the source of truth for post titles.** Section headings here are short labels for scanning, not authoritative titles. If a heading here names a *different topic* rather than a shortened version of the calendar title, the calendar wins — fix this file. (Audited 2026-07-29: Post #4 had genuinely diverged and was corrected; Posts #5, #7–#10 verified as consistent short forms.)

## 🎨 Design System (never change these)

| Element | Value |
|---------|-------|
| Style | Flat illustration, simple geometric shapes, bold outlines |
| Background | Warm off-white `#FAFAF8` |
| Primary accent | Orange `#E8621A` |
| Dark elements | Dark charcoal `#1A1A1A` |
| Highlights | White |
| Aspect ratio | 16:9 (wide, min 1024×576) |
| Text in image | NEVER |

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

**Composition rule:** Vary the visual element across images within the same post so they read as a curated collection, not a template repeat. The palette and flat style stay fixed; the composition and decorative elements change. Think "art lover's blog", not "corporate stock art". Never reuse the same scene layout (e.g. person at desk with screen) across posts.

### ⚠️ Anatomy Fix (MANDATORY for any human or robot)

AI generators routinely produce missing, deformed, or unnaturally positioned hands and arms. Always append:

> `Both person and robot have complete visible arms and hands with natural positioning.`

If hands are still wrong, regenerate with:

> `All hands fully rendered with five fingers each, arms complete from shoulder to fingertips, natural pose.`

### 🔁 Gemini Image-Reference Workflow (fixing background or style drift)

When a generator produces a great composition but the wrong background colour or style, don't re-prompt from scratch — use Gemini's image reference:

1. Upload the image you like to Gemini
2. Ask: *"Re-create this exact scene but with warm off-white (#FAFAF8) background, flat illustration style, charcoal (#1A1A1A) outlines, orange (#E8621A) accents, white highlights. All human hands must have five fingers. No text, labels, logos, or watermarks."*
3. Gemini preserves the composition while fixing the brand colours
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

1. Find the post you're working on below
2. Copy the **Prompt** block for each image
3. Paste into Gemini Nano Banana 2
4. Download the generated image
5. Upload to WordPress Media Library with the exact **Filename**
6. Set Malay alt text (provided with each image)
7. Assign featured image or insert into post content

## 🔄 Maintenance Rule

**🔢 KEEP SECTIONS IN NUMERICAL ORDER — Post #1, #2, #3 … #10.** Do NOT group by status (published first, planned last) and do NOT append new sections to the bottom. Insert each post at its numbered position. Mixed ordering makes the file hard to scan and hides which posts still need prompts.

> Fixed 2026-07-29: the order had drifted to `#1, #2, #3, #6, #4, #5, #7…` because published posts were appended as they shipped. Reordered numerically.

**When a post is published:** Replace TBD prompts with content-derived ones based on the actual article text. Update the post's status marker from PLANNED to PUBLISHED.

**When a new post is planned:** Add a new section with TBD prompts **at its numbered position**, not at the end of the file.

**Status markers:** `(PLANNED — TBD)` → `(READY TO GENERATE)` once prompts are written → `(PUBLISHED ✅)` once live.

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

## Post #5 — Canva Poster dengan AI (PLANNED — TBD)

**Slug:** TBD

> Prompts will be written after content is drafted in WriterZen.

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | TBD | TBD | TBD |
| Intro | TBD | TBD | TBD |
| Comparison | TBD | TBD | TBD |
| Conclusion | TBD | TBD | TBD |

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

## Post #7 — Cara Buat Nota Rapi dengan AI (PLANNED — TBD)

**Slug:** TBD

> Prompts will be written after content is drafted in WriterZen.

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | TBD | TBD | TBD |
| Intro | TBD | TBD | TBD |
| Comparison | TBD | TBD | TBD |
| Conclusion | TBD | TBD | TBD |

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

## Post #9 — Cara Buat AI Art dengan Gemini (PLANNED — TBD)

**Slug:** TBD

> Prompts will be written after content is drafted in WriterZen.

| Image | Filename | Prompt | Alt Text |
|-------|----------|--------|----------|
| Featured | TBD | TBD | TBD |
| Intro | TBD | TBD | TBD |
| Comparison | TBD | TBD | TBD |
| Conclusion | TBD | TBD | TBD |

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
