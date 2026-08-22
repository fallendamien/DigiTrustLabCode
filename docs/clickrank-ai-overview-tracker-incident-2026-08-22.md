# ClickRank AI Overview Tracker Incident — 2026-08-22

## What happened

Post #5 (`cara buat poster guna canva`) was submitted to ClickRank's AI Overview Tracker using the existing authenticated Chrome session. The modal returned a generic error, then a later submission stayed on `Processing...`. No row was visible immediately, so the entry was initially treated as unverified.

## Root cause

The ClickRank tracker write is asynchronous. Its URL-search/submission path can return an HTML/error response while the frontend expects JSON, producing `Unexpected token '<'`. The dashboard login was valid, the keyword and URL were valid, and the request continued processing after the modal closed.

## Fresh evidence

- Reopening the same authenticated ClickRank tab later showed the row.
- Tracker count changed from 7 to 8.
- Row: `cara buat poster guna canva` · Malaysia/Malay · exact Post #5 URL.
- Current result: `Not Found`, AI/organic `N/A`, visibility `0%`.

## Prevention rule

After clicking **Start Tracking**:

1. Wait for processing to settle.
2. Reload or reopen the same authenticated tracker tab.
3. Check the tracked-keyword count.
4. Verify the exact keyword, URL, market and language row.
5. Only retry if the count and row are still absent after that check.

Do not treat a generic toast, an HTML-as-JSON error, or a temporary `Processing...` state as proof that no row exists. `Not Found`, `N/A`, and `0%` describe a tracked keyword with no detected result; they are not submission errors.
