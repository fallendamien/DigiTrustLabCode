# Post #11 Revalidation — 2026-08-09

## Article status

Post #11 (`559`) remains published at:

`https://digitrustlab.com/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi/`

The live page was checked through the existing Chrome DevTools session. It returned the expected article title, a template-rendered H1, eight H2 headings, four images with alt text, a canonical URL, and `follow, index` robots metadata.

## Gates re-run

| Gate | Result | Evidence |
|---|---|---|
| Malay naturalness | PASS | Claude + OpenAI, 61 segments, high confidence; hash `dc96912efd4a884d009157e2221b2088e2ef144da1c5971836fc41e8306f45aa` |
| Mechanical Malay voice | PASS | Post 559, 0 errors and 0 warnings |
| Link quality | PASS | 2 contextual internal links, 3 external links, 1 dofollow, destinations checked; inbound `no_safe_context` |
| Rank Math essential checks | PASS | 13/13, computed score 100/A |
| SEO analysis | PASS with intentional template warning | 95/A; no content H1 is expected because the Bricks single-post template renders the H1 |
| Repository status | PASS | `verify-content-status.py`, `verify-imports.py`, 22 unit tests, and `git diff --check` |

## Critical finding: LiteSpeed serves stale child-sitemap 404s

The live Rank Math sitemap index returns HTTP 200 and references these child sitemaps. The Rank Math generator and WordPress rewrite rules have now been repaired: every child route returns valid XML with a cache-bypass query string. However, the clean canonical URLs still return the old LiteSpeed cached HTTP 404:

- `https://digitrustlab.com/post-sitemap.xml`
- `https://digitrustlab.com/page-sitemap.xml`
- `https://digitrustlab.com/category-sitemap.xml`
- `https://digitrustlab.com/author-sitemap.xml`

The index itself was last modified at `2026-08-08T08:09:14+00:00`. The article appears in the regenerated `post-sitemap.xml` with its four image URLs. This is a site-level crawl-discovery issue, separate from the article’s live `index, follow` directive and the Search Console URL Inspection result recorded on 8 August as `Page is indexed`.

### Current disposition

Documented as an open follow-up. Rank Math’s internal sitemap cache and WordPress rewrite-rule cache were invalidated through recoverable Respira option operations, and the rewrite rules regenerated correctly. LiteSpeed sitemap-cache exclusions are also configured and verified as the intended patterns. Direct LiteSpeed admin-IP purge requests were tried against every affected child route, but the clean URLs still return `x-litespeed-cache: hit` with the old 404, so that purge is not treated as successful. The remaining step requires the WordPress/Hostinger/Cloudflare cache-control surface that can clear the persistent public cache. The current Chrome session is signed out of the hidden WordPress login and Google Search Console, so no credential-dependent purge or Search Console submission was attempted.

### Safe repair sequence when authenticated

1. In the authenticated WordPress/Hostinger/Cloudflare cache controls, purge the stale sitemap routes or the site cache.
2. Confirm the sitemap index and every child sitemap return HTTP 200 XML without a query string and without `x-litespeed-cache: hit`.
3. Re-submit `https://digitrustlab.com/sitemap_index.xml` in Search Console.
4. Re-run the Post #11 URL Inspection and record the fresh status.
