#!/usr/bin/env python3
"""Block repetitive featured-image concepts before archive or upload.

The register is intentionally kept in content/image-prompts.md so the visual
decision remains visible beside the prompt library. This checker validates the
recorded decision and the six-entry history; the thumbnail comparison itself
must be attested by the worker after viewing the images together.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MODES = {
    "object-led",
    "abstract-symbolic",
    "diagrammatic",
    "environmental",
    "editorial-collage",
    "top-down",
    "split-transformation",
    "human-led",
}
TREATMENTS = {
    "flat-editorial-vector",
    "geometric-infographic",
    "isometric-systems-scene",
    "cut-paper-editorial-collage",
    "abstract-symbolic-composition",
    "cinematic-editorial-poster",
}
FORBIDDEN_MOTIF = ("person", "desk", "laptop", "robot")


def fail(message: str) -> int:
    print(f"FAIL featured-image-variety: {message}", file=sys.stderr)
    return 1


def parse_register(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"### Featured-image register .*?\n\n(.*?)\n\nAfter each publication,",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("featured-image register section is missing")
    rows: list[dict[str, str]] = []
    for line in match.group(1).splitlines():
        if not line.startswith("|") or line.startswith("|------"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 8 or cells[0] == "Post":
            continue
        rows.append(
            {
                "post": cells[0],
                "asset": cells[1],
                "mode": cells[2],
                "subject": cells[3],
                "composition": cells[4],
                "treatment": cells[5],
                "human": cells[6].lower(),
                "motif": cells[7].lower(),
            }
        )
    if len(rows) < 6:
        raise ValueError(f"register contains {len(rows)} entries; six are required")
    return rows[-6:]


def has_motif(value: str, tokens: tuple[str, ...] = FORBIDDEN_MOTIF) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return all(re.search(rf"\b{re.escape(token)}\b", normalized) for token in tokens)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--previous-six-inspected", action="store_true")
    parser.add_argument("--visual-mode", required=True, choices=sorted(MODES))
    parser.add_argument("--subject-class", required=True)
    parser.add_argument("--composition", required=True)
    parser.add_argument("--treatment", required=True, choices=sorted(TREATMENTS))
    parser.add_argument("--human-presence", required=True, choices=("yes", "no"))
    parser.add_argument("--motif", required=True)
    parser.add_argument("--difference-count", type=int, required=True)
    parser.add_argument(
        "--thumbnail-comparison", required=True, choices=("pass", "fail")
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.previous_six_inspected:
        return fail("previous six thumbnails were not explicitly inspected")
    if args.difference_count < 3 or args.difference_count > 5:
        return fail("immediate-prior difference count must be between 3 and 5")
    if args.thumbnail_comparison != "pass":
        return fail("thumbnail comparison is not PASS")
    if not args.subject_class.strip() or not args.composition.strip():
        return fail("subject class and composition must be nonblank")

    try:
        history = parse_register(args.register)
    except (OSError, ValueError) as exc:
        return fail(str(exc))

    prior_last_three_humans = sum(row["human"] == "yes" for row in history[-3:])
    if args.human_presence == "yes" and prior_last_three_humans > 0:
        return fail("human-led candidate would exceed one human-led image in the four-post window")
    if history[-1]["human"] == args.human_presence == "yes":
        return fail("human-led featured images may not be consecutive")

    if has_motif(args.motif) and any(has_motif(row["motif"]) for row in history):
        return fail("person+desk+laptop+robot motif repeats within the previous six images")

    print(
        "PASS featured-image-variety: six thumbnails inspected; "
        f"mode={args.visual_mode}; treatment={args.treatment}; "
        f"human={args.human_presence}; difference_count={args.difference_count}; "
        "thumbnail_comparison=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
