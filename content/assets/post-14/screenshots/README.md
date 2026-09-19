# Post #14 authentic Canva screenshot evidence

Status: `CAPTURED, PRIVACY-CROPPED AND UPLOADED`

Capture date: 2026-09-19 (Asia/Kuala_Lumpur)

## Tested workflow and sample

- Product: Canva web editor, desktop browser
- Account/plan: authenticated user account, Canva free workflow; no Pro-only
  control was required
- Sample design: `Banner Praktikal - Post 14`
- Canvas: 1,200 × 628 px, unit `px`
- Sample text: `Banner Praktikal` and `Satu mesej, satu susunan yang jelas`
- Editor URL: `https://www.canva.com/design/DAHVofvYPYo/sEf7_NLsSpNo1KXDFDqRow/edit?ui=e30`

## Coverage map

| Material action | Candidate filename | Authentic UI state captured | Malay alt text | Caption | Caveat | Status |
|---|---|---|---|---|---|---|
| Set a custom size and create the design | `cara-buat-banner-guna-canva-saiz-create.png` | Canva Create a design → Custom size; Width `1200`, Height `628`, Units `px`, matching format shown | Paparan Canva untuk menetapkan saiz tersuai 1,200 × 628 piksel sebelum mencipta reka bentuk | Paparan Canva untuk menetapkan saiz tersuai 1,200 × 628 piksel sebelum mencipta reka bentuk. | Matching format displayed as Facebook Post (Landscape) `1200 × 630 px`; the tested sample remains `1200 × 628 px`. | Media 751, 1480×810 |
| Select text and use editor text controls plus Position | `cara-buat-banner-guna-canva-editor-position.png` | Real editor with the sample text selected; Canva Sans, size 18, text controls and Position → Arrange/Advanced visible | Editor Canva yang menunjukkan teks contoh, bar alat teks dan panel Position untuk penjajaran | Editor Canva yang menunjukkan kotak teks dan panel Position untuk menyusun kedudukannya. | Values are sample-specific; labels and available controls can vary by design, device, and plan. | Media 752, 1904×840 |
| Share → Download and inspect export settings | `cara-buat-banner-guna-canva-share-download.png` | Real Share panel → Download; PNG Suggested, `1,200 × 628 px`, quality controls and transparent-background toggle visible | Panel Canva Download selepas memilih Share, termasuk format PNG dan saiz 1,200 × 628 piksel | Panel Canva Download selepas memilih Share dan menyemak tetapan eksport. | Current sample exposed PNG Suggested; other formats/options vary by design and account/plan. | Media 753, 1020×650 |

## Privacy and readability audit

The browser viewport was captured through the authenticated Canva tab and then
cropped to the editor/dialog region. Browser chrome was excluded. The editor
capture excluded the account area and the export capture excluded the sharing
identity area. No personal email, avatar, or account identifier appears in the
article assets. All three native captures were exported to this folder and
uploaded through Respira as WordPress Media 751–753; no fabricated or synthetic
interface screenshot was used.

## Explicit no-screenshot reasons

The draft's non-procedural principles, colour advice, accessibility explanation,
and final checklist do not need their own interface screenshot because they are
conceptual or outcome-focused rather than dependent on a specific control
location. The three material UI actions above require authentic screenshots and
are now covered by the uploaded media.

## Mental test cases for the workflow rule

1. Canva editor tutorial: screenshots required for size/create, editor controls,
   and export because a reader needs authentic control and state evidence.
2. Conceptual AI explainer: generated illustration allowed when it explains an
   idea and does not imitate a control, menu, setting, result, or proof of use.
3. API/CLI guide: screenshots optional when text/code is the primary evidence;
   the draft must record why a material action does not depend on visual UI.

Propagation decision: this is a project-local authoritative change in the
existing `.claude/skills/write-post/SKILL.md` and related project content
standards. No new global TSOT rule or pointer was created; parity propagation is
therefore intentionally not applicable.
