# Live link evidence

Store one small JSON artifact per published post as
`<post-slug>.json`. Do not copy the article into the artifact.

The artifact records the live post ID, slug, current `link_hash`, and the
inbound scan decision:

- `links_found` with the live source post IDs; or
- `no_safe_context` with a specific reason when forcing a link would be
  irrelevant or awkward.

Generate or update the artifact after the Phase 7 internal-link-builder scan,
then run:

```bash
python scripts/verify-links.py --post-id <post-id> \
  --inbound-review content/link-reviews/<post-slug>.json \
  --check-destinations
```

Any changed link invalidates `link_hash` and requires a new scan. Rank Math
link checks are not a substitute for this evidence.
