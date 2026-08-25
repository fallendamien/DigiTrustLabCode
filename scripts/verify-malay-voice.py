#!/usr/bin/env python3
"""
verify-malay-voice.py — mechanical half of the DigiTrust Lab Malay voice policy.

Checks published WordPress content against the mechanically-checkable rules in
`.devin/skills/malay-voice-guide/SKILL.md`. Fetches live content from the public
WP REST API, so it always measures what readers actually see.

WHY THIS EXISTS
    The 2026-07-30 audit was done by eye and got the numbers badly wrong: it
    reported 3 em dashes in Post #1 (actual: 16), graded Post #6 "nearly clean"
    (actual: 15 em dashes), and listed findings for words that were not in the
    content at all. Counting is a machine's job. Judgement is a human's job.
    This script does the counting so the human can spend attention on judgement.

IMPORTANT
    This script is not the naturalness gate. Run verify-malay-naturalness.py
    with a current two-model-family review artifact before publication and
    against the live post after publication.

WHAT IT CANNOT CHECK
    Register, tone, tatabahasa/verb completeness, read-aloud flow, humour, and
    heading typos. A clean run is NOT a pass — it only means the countable
    defects are gone. Sections 1, 5, 6, 7, 9 and 11d of the skill still need a
    human read.

USAGE
    python scripts/verify-malay-voice.py                # all tracked content
    python scripts/verify-malay-voice.py 256 437        # specific post IDs
    python scripts/verify-malay-voice.py --json         # machine-readable
    python scripts/verify-malay-voice.py --baseline     # write baseline file

EXIT CODES
    0 = no violations   1 = violations found   2 = fetch/network error
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

SITE = "https://digitrustlab.com"

# id -> (label, endpoint). Add new posts here when they publish.
CONTENT = {
    256: ("Post #1  Apa Itu AI", "posts"),
    351: ("Post #2  Cara Guna ChatGPT", "posts"),
    437: ("Post #3  Cara Buat Prompt", "posts"),
    536: ("Post #4  Cara Buat Gambar AI", "posts"),
    490: ("Post #6  ChatGPT vs Gemini vs Claude", "posts"),
    559: ("Post #11 Apa Itu MCP dalam AI", "posts"),
    582: ("Post #9  Prompt Gemini AI untuk Edit Foto", "posts"),
    605: ("Post #12 Contoh Minit Mesyuarat", "posts"),
    629: ("Post #5  Cara Buat Poster Guna Canva", "posts"),
    656: ("Post #7  Cara Buat Nota Cantik dengan AI", "posts"),
    72:  ("Page     Tentang Kami", "pages"),
    73:  ("Page     Privasi", "pages"),
    74:  ("Page     Disclaimer", "pages"),
}

# Core pages are held to a higher register (skill §11e).
CORE_PAGES = {72, 73, 74}

EM_DASH = "—"
EN_DASH = "–"

# Banned contractions and slang — skill §3 and §11.
BANNED = {
    r"\btak\b": "tidak",
    r"\bnak\b": "akan / hendak",
    r"\bdah\b": "sudah / telah",
    r"\bje\b": "sahaja (or remove)",
    r"\btakleh\b": "tidak boleh",
    r"\bkorang\b": "anda",
    r"\bkau\b": "anda",
    r"\bawak\b": "anda",
    r"\bmacam mana\b": "bagaimana",
    r"\bkat sini\b": "di sini",
    r"\bboleh je\b": "anda boleh",
    r"\bsenang je\b": "mudah",
    r"\bianya\b": "ia",
    r"\bmerbahaya\b": "berbahaya",
    r"\bdi kalangan\b": "dalam kalangan",
}

# Non-baku loanwords where a standard BM word exists — skill §11c.
# NOTE: `efektif` is DBP-recognized (prpm.dbp.gov.my) and allowed in formal/semi-formal BM.
NON_BAKU = {
    r"\befisien\b": "cekap",
    r"\bkalau\b": "jika",
    r"\bperasan\b": "sedari / menyedari",
}

# English words with natural BM equivalents — skill §11c.
# NOT the §4b retention list (copy & paste, deadline, brainstorm stay English).
ENGLISH_WITH_BM = {
    r"\bcheck\b": "semak",
    r"\bresult\b": "hasil / keputusan",
    r"\beffort\b": "usaha",
    r"\brecommend\b": "mengesyorkan",
}

# Bahasa Indonesia forms that are NOT valid Malay — skill §4f.
#
# WHY: AI models routinely emit Indonesian when asked for Malay. The languages
# share most vocabulary, so an Indonesian word inside Malay prose reads as a
# slightly odd word choice rather than an error — it survives proofreading.
# Found live 2026-07-30: `mencoba` had been in Post #1 since publication, and
# the skill file itself was teaching `menyadarinya` in three example tables.
#
# DO NOT over-extend this list. Many words are valid in both languages
# (paham/faham, kamu, sekarang, jam), and `efektif` was wrongly banned on
# 2026-07-30 before DBP confirmed it valid. Verify at prpm.dbp.gov.my first.
INDONESIAN = {
    # -tas / -ti suffix family (highest-yield systematic check)
    r"\baktivitas\b": "aktiviti",
    r"\bkualitas\b": "kualiti",
    r"\bkomunitas\b": "komuniti",
    r"\bidentitas\b": "identiti",
    r"\brealitas\b": "realiti",
    r"\buniversitas\b": "universiti",
    r"\bfasilitas\b": "fasiliti / kemudahan",
    r"\bprioritas\b": "prioriti / keutamaan",
    r"\bkreativitas\b": "kreativiti",
    r"\bproduktivitas\b": "produktiviti",
    # root-vowel families: sadar->sedar, coba->cuba, pikir->fikir
    r"\bmenyadari\w*": "menyedari…",
    r"\bkesadaran\b": "kesedaran",
    r"\bsadar\b": "sedar",
    r"\bmencoba\w*": "mencuba…",
    r"\bdicoba\b": "dicuba",
    r"\bpercobaan\b": "percubaan",
    r"\bpikiran\b": "fikiran",
    r"\bmemikirkan\b": "memikirkan (BM: fikir root)",
    r"\bpemikiran\b": "pemikiran (BM: fikir root)",
    # Indonesian-only vocabulary
    r"\bbutuh\w*": "perlu / memerlukan",
    r"\bkarena\b": "kerana",
    r"\bkayak\b": "seperti",
    r"\bgimana\b": "bagaimana",
    r"\b(?:nggak|enggak)\b": "tidak",
    r"\bbanget\b": "sangat",
    r"\bbikin\w*": "buat / membuat",
    # spelling variants
    r"\bresiko\b": "risiko",
    r"\bpraktek\b": "praktik",
    r"\bsilahkan\b": "sila",
    r"\bnasehat\b": "nasihat",
    r"\bmerubah\b": "mengubah",
}

# `bisa` is a REAL Malay word meaning venom ("bisa ular"). Flagged as WARN only,
# because the Indonesian sense ("can") is far likelier in this content but a
# legitimate use must not fail the build. Read the sentence before replacing.
INDONESIAN_AMBIGUOUS = {
    r"\bbisa\b": "boleh (unless you mean venom — 'bisa ular')",
}

# Informal nouns/verbs — flagged everywhere, ERROR on core pages (§11e).
INFORMAL = {
    r"\bbenda\b": "produk / alat / perkara",
    r"\btengok\b": "melihat / memantau",
}

# Brand names that must never appear lowercase in body text — skill §4d.
BRANDS = [
    "ChatGPT", "Gemini", "Claude", "OpenAI", "Google", "Microsoft",
    "Canva", "Notion", "Midjourney", "Netflix", "Spotify", "WhatsApp",
    "YouTube", "Shopee", "Lazada", "Anthropic",
]

# English terms that must be wrapped in <em> when code-switched — skill §4c.
# Excludes brand names, acronyms, and absorbed loans (online, email, blog...).
NEEDS_ITALIC = [
    "chatbot", "prompt", "brainstorm", "brainstorming", "feedback",
    "deadline", "drag & drop", "copy & paste", "natural", "template",
    "dashboard", "workflow", "debugging", "codebase",
]


def fetch(cid, endpoint):
    url = f"{SITE}/wp-json/wp/v2/{endpoint}/{cid}?_fields=id,slug,title,content"
    req = urllib.request.Request(url, headers={"User-Agent": "digitrustlab-voice-check"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def strip_toc(html):
    """Remove the Easy Table of Contents block — it duplicates headings and
    would double-count any defect that appears in an H2/H3."""
    return re.sub(r"<div id=.ez-toc-container.*?</nav>\s*</div>", "", html, flags=re.S)


def visible_text(html):
    """Body copy only: no tags, no attribute values."""
    return re.sub(r"<[^>]+>", " ", html)


def strip_urls(text):
    """Brand-case checking must ignore URLs and filenames: 'gemini.google.com'
    and 'apa-itu-ai-neural-network.png' are correctly lowercase (skill §4d
    exempts URL slugs and image filenames)."""
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b[\w.-]+\.(?:com|my|ai|org|net|io|google|png|jpe?g|webp)\b", " ", text)
    return text


def alt_and_captions(html):
    """Alt text and figcaptions are reader-facing and in scope for the voice
    policy (AGENTS.md metadata rule), but are invisible to a plain-text strip."""
    alts = re.findall(r'alt="([^"]*)"', html)
    caps = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", html, flags=re.S)
    return " ".join(alts + [re.sub(r"<[^>]+>", " ", c) for c in caps])


def snippet(text, pos, width=42):
    s = text[max(0, pos - width):pos + width]
    return " ".join(s.split())


def scan(cid, label, html):
    """Return a list of (severity, rule, detail) tuples."""
    html = strip_toc(html)
    body = visible_text(html)
    meta = alt_and_captions(html)
    is_core = cid in CORE_PAGES
    out = []

    # -- Em/en dashes: max 1 per piece (skill §10) ------------------------
    body_dashes = [m.start() for m in re.finditer(f"[{EM_DASH}{EN_DASH}]", body)]
    meta_dashes = len(re.findall(f"[{EM_DASH}{EN_DASH}]", meta))

    li_dashes = sum(
        len(re.findall(f"[{EM_DASH}{EN_DASH}]", blk))
        for blk in re.findall(r"<li>.*?</li>", html, flags=re.S)
    )
    total = len(body_dashes) + meta_dashes
    if total > 1:
        fixable = f", {li_dashes} in <li> (swap for a colon)" if li_dashes else ""
        inmeta = f", {meta_dashes} in alt/caption" if meta_dashes else ""
        out.append(("ERROR", "em-dash",
                    f"{total} dashes, policy allows 1{fixable}{inmeta}"))
        for p in body_dashes[:40]:
            out.append(("  ", "", f"...{snippet(body, p)}..."))

    # -- Banned contractions and slang ------------------------------------
    for pat, fix in BANNED.items():
        for m in re.finditer(pat, body, re.I):
            out.append(("ERROR", "banned",
                        f"'{m.group()}' -> {fix}  ...{snippet(body, m.start())}..."))

    # -- Non-baku loanwords ------------------------------------------------
    for pat, fix in NON_BAKU.items():
        hits = list(re.finditer(pat, body, re.I))
        if hits:
            out.append(("ERROR", "non-baku",
                        f"'{hits[0].group()}' x{len(hits)} -> {fix}"))

    # -- Bahasa Indonesia forms (skill §4f) --------------------------------
    for pat, fix in INDONESIAN.items():
        for m in re.finditer(pat, body, re.I):
            out.append(("ERROR", "indonesian",
                        f"'{m.group()}' is Indonesian -> {fix}  ...{snippet(body, m.start())}..."))

    for pat, fix in INDONESIAN_AMBIGUOUS.items():
        for m in re.finditer(pat, body, re.I):
            out.append(("WARN", "indonesian?",
                        f"'{m.group()}' -> {fix}  ...{snippet(body, m.start())}..."))

    # -- English where a BM word exists ------------------------------------
    for pat, fix in ENGLISH_WITH_BM.items():
        hits = list(re.finditer(pat, body, re.I))
        if hits:
            out.append(("ERROR", "use-BM",
                        f"'{hits[0].group()}' x{len(hits)} -> {fix}"))

    # -- Informal register (hard error on core pages) ----------------------
    for pat, fix in INFORMAL.items():
        hits = list(re.finditer(pat, body, re.I))
        if hits:
            sev = "ERROR" if is_core else "WARN"
            note = " (core page: higher register required)" if is_core else ""
            out.append((sev, "informal",
                        f"'{hits[0].group()}' x{len(hits)} -> {fix}{note}"))

    # -- Brand capitalisation (URLs/filenames exempt, skill §4d) -----------
    body_nourl = strip_urls(body)
    for brand in BRANDS:
        for m in re.finditer(rf"\b{re.escape(brand)}\b", body_nourl, re.I):
            if m.group() != brand:
                out.append(("ERROR", "brand-case",
                            f"'{m.group()}' -> '{brand}'  ...{snippet(body_nourl, m.start())}..."))

    # -- Italic policy for code-switched English ---------------------------
    for term in NEEDS_ITALIC:
        total_n = len(re.findall(rf"\b{re.escape(term)}\b", body, re.I))
        if not total_n:
            continue
        ital = len(re.findall(rf"<em>\s*{re.escape(term)}\b", html, re.I))
        ital += len(re.findall(rf"<em>[^<]*\b{re.escape(term)}\b[^<]*</em>", html, re.I))
        if total_n > ital:
            out.append(("WARN", "italic",
                        f"'{term}': {total_n - min(ital, total_n)} of {total_n} not in <em>"))

    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", type=int, help="content IDs (default: all)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    targets = args.ids or list(CONTENT)
    report, errors, warns = {}, 0, 0

    for cid in targets:
        if cid not in CONTENT:
            print(f"!! unknown id {cid} — add it to CONTENT in this script", file=sys.stderr)
            return 2
        label, endpoint = CONTENT[cid]
        try:
            data = fetch(cid, endpoint)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"!! fetch failed for {cid}: {e}", file=sys.stderr)
            return 2
        findings = scan(cid, label, data["content"]["rendered"])
        report[cid] = {"label": label, "findings": findings}
        errors += sum(1 for s, _, _ in findings if s == "ERROR")
        warns += sum(1 for s, _, _ in findings if s == "WARN")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    for cid, r in report.items():
        hard = [f for f in r["findings"] if f[0] in ("ERROR", "WARN")]
        mark = "FAIL" if any(f[0] == "ERROR" for f in hard) else ("WARN" if hard else "PASS")
        print(f"\n{'='*72}\n[{mark}] {r['label']}  (id {cid})\n{'='*72}")
        if not hard:
            print("  no countable violations")
        for sev, rule, detail in r["findings"]:
            print(f"  {sev:<6} {rule:<11} {detail}" if sev.strip() else f"         {detail}")

    print(f"\n{'='*72}")
    print(f"TOTAL: {errors} error(s), {warns} warning(s) across {len(targets)} piece(s)")
    print("Countable checks only. Register, tatabahasa, flow and HEADING TYPOS")
    print("still require a human read against malay-voice-guide/SKILL.md.")
    print("=" * 72)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
