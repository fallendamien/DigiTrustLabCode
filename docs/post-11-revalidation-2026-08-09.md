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

## Critical finding: child sitemaps return 404

The live Rank Math sitemap index returns HTTP 200 and references these child sitemaps, but each child route currently returns HTTP 404:

- `https://digitrustlab.com/post-sitemap.xml`
- `https://digitrustlab.com/page-sitemap.xml`
- `https://digitrustlab.com/category-sitemap.xml`
- `https://digitrustlab.com/author-sitemap.xml`

The index itself was last modified at `2026-08-08T08:09:14+00:00`. This is a site-level crawl-discovery issue, separate from the article’s live `index, follow` directive and the Search Console URL Inspection result recorded on 8 August as `Page is indexed`.

### Current disposition

Documented as an open follow-up. Repair requires authenticated WordPress access to flush/rebuild Rank Math sitemap rewrite rules and then purge cache. The current Chrome session is signed out of the hidden WordPress login, so no credential-dependent change was attempted.

### Safe repair sequence when authenticated

1. Re-save WordPress Permalinks to flush rewrite rules.
2. Purge LiteSpeed Cache and any Cloudflare cache for the sitemap routes.
3. Confirm the sitemap index and every child sitemap return HTTP 200 XML.
4. Re-submit `https://digitrustlab.com/sitemap_index.xml` in Search Console.
5. Re-run the Post #11 URL Inspection and record the fresh status.
