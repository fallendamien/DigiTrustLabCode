# NEXT — DigiTrust Lab

## Current State

- ✅ Blog is LIVE at https://blog.digitrustlab.com
- WordPress + Bricks Builder + Simply Static + Cloudflare Pages pipeline working
- Header (logo, nav, search bar, CTA) and footer configured
- Core pages: Homepage, Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami
- Post-process script handles Simply Static export bugs (form stripping, double-slash links)
- TROUBLESHOOTING.md documents 9 known issues with solutions

## Completed (Sessions 1-3, 2026-06-28 to 2026-07-01)

- ✅ Git repo initialized, Windsurf workspace bootstrapped
- ✅ Long-term revenue plan + affiliate research
- ✅ WordPress + Bricks installed on LocalWP
- ✅ Blog structure with all core pages
- ✅ Header/footer templates with nav, search bar, CTA
- ✅ Simply Static export → Cloudflare Pages deployment pipeline
- ✅ Post-process script (search bar injection, double-slash fix, category label removal)
- ✅ Nav labels standardized (Tentang Kami, Hubungi Kami, Polisi Privasi)
- ✅ Tentang page updated (Zed, 2022)
- ✅ Search bar resized (width 180px, height 32px)
- ✅ GUI-First Policy documented in AGENTS.md as Priority #1

## Next Steps (Priority Order)

1. **Write first blog post** — WriterZen keyword research → write → ClickRank optimization
2. **Set up Google Search Console + GA4** — verify ownership, submit sitemap
3. **Verify ClickRank ownership** — JS snippet on blog
4. **Add digitrustlab.com to Screpy** — monitoring
5. **Register Klikjer affiliate** — free, 50% commission, Malaysian eBooks
6. **Register JV Warrior affiliate** — Malaysian digital products
7. **Create Etsy shop** — choose clean shop name (NOT DigiTrust Lab)
8. **Create first Etsy listing** — "30 Prompt AI untuk Iklan FB & IG (Bahasa Melayu)"
9. **Set up MailerLite** — free account, newsletter form on blog
10. **Create lead magnet PDF** — "50 Prompt AI Percuma"

## Important Notes

- **GUI-First Policy**: Content/layout changes via Bricks/WordPress GUI, NOT code
- **Export workflow**: GUI edits → Simply Static export → post-process-static.ps1 → wrangler deploy
- **Code only for**: Simply Static export bugs, bulk file fixes, CLI deployment
