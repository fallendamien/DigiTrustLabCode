#!/usr/bin/env python3
"""
verify-imports.py — assert the project's doctrine actually loads.

Checks that every file an AI agent is supposed to read at session start exists
and resolves. Run it before starting work, and after ANY change to symlinks,
`.gitignore`, or the `.devin/` / `.windsurf/` trees.

WHY THIS EXISTS
    On 2026-07-30 a symlink migration replaced `.devin/rules` with a link to the
    global agent-templates. Three of the four rules `CLAUDE.local.md` imports
    stopped resolving. Nothing errored. No warning appeared. Agents simply ran
    without the Bricks-Only Policy, the content-planning rule, and the
    browser-preview rule for a full working day before anyone noticed.

    That is the failure mode this guards: doctrine does not fail loudly, it just
    goes quiet. A missing `@import` is indistinguishable from a satisfied one
    unless something checks.

USAGE
    python scripts/verify-imports.py           # human-readable
    python scripts/verify-imports.py --quiet   # only failures

EXIT CODES
    0 = everything resolves    1 = something is missing
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Files that may contain `@import` lines. Both are gitignored and per-device,
# which is exactly why they go missing (fresh clone, new machine, git worktree).
IMPORT_SOURCES = ["CLAUDE.local.md", "CLAUDE.md"]

# Directories that are symlinks by design. A symlink that resolves to nothing,
# or to a tree missing its expected file, is the 2026-07-30 failure exactly.
SYMLINK_EXPECTATIONS = {
    ".devin/skills":     "malay-voice-guide/SKILL.md",
    # .devin/workflows removed 2026-08-01 — it duplicated .windsurf/workflows
    # (both pointed at the same TSOT folder) and Devin is no longer in use.
    # .windsurf/workflows is KEPT as the single browsable view of the global
    # workflow set. Claude Code still loads commands from ~/.claude/commands,
    # not from here; this symlink exists so the 31 workflows are visible and
    # editable in the editor alongside the other TSOT trees.
    ".windsurf/workflows": "commit.md",
    ".windsurf/skills":  None,
    ".windsurf/rules":   "verification-protocol.md",
}

# Project rules whose GLOBAL copy, if one exists, must not drift.
#
# WHY: `.devin/rules/` is a real git-tracked directory (authoritative).
# `.windsurf/rules/` is a symlink into the shared Google Drive TSOT.
#
# These two rules used to be duplicated across both trees and had silently
# DRIFTED by 2026-07-30: the global bricks copy still described the Bricks MCP
# endpoint decommissioned on 2026-07-05, and the global Malay copy still claimed
# "13 semi-formal sections" against an actual 14.
#
# The global copies were removed from the TSOT on 2026-07-30 by decision: the
# authoritative versions live in `.devin/rules/`, in git, and the project no
# longer needs them mirrored into the shared folder.
#
# The check is therefore CONDITIONAL, not mandatory:
#   - global copy absent  -> fine, that is the current intended state
#   - global copy present -> it must match `.devin/rules/` byte for byte
#
# That way a stale copy reappearing (a Drive restore, another machine syncing,
# a future decision to re-mirror) is caught, without failing on the state we
# deliberately chose.
DUPLICATED_RULES = [
    "bricks-mcp-absolute.md",
    "malay-skill-sync.md",
]
GLOBAL_RULES_DIR = ".windsurf/rules"   # symlink -> shared TSOT
LOCAL_RULES_DIR = ".devin/rules"       # real dir, git-tracked, authoritative

# Load-bearing files referenced by AGENTS.md / the pipeline. Cheap to assert.
CRITICAL = [
    "AGENTS.md",
    ".devin/skills/write-post/SKILL.md",
    ".devin/skills/malay-voice-guide/SKILL.md",
    ".devin/skills/readability-pass/SKILL.md",
    ".devin/skills/writerzen-keyword-research/SKILL.md",
    "content/image-prompts.md",
    "content/content-calendar.md",
    "scripts/verify-malay-voice.py",
]


def rel(p):
    return os.path.relpath(p, REPO).replace("\\", "/")


def collect_imports():
    """Return (source_file, import_target) pairs found across IMPORT_SOURCES."""
    found, missing_sources = [], []
    for src in IMPORT_SOURCES:
        path = os.path.join(REPO, src)
        if not os.path.exists(path):
            missing_sources.append(src)
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.match(r"^@(\S+)", line.strip())
                if m:
                    found.append((src, m.group(1)))
    return found, missing_sources


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args()

    failures, notes = [], []
    say = (lambda *a: None) if args.quiet else print

    # -- 1. import sources present ----------------------------------------
    imports, missing_sources = collect_imports()

    say("\n== import sources ==")
    for src in IMPORT_SOURCES:
        if src in missing_sources:
            # CLAUDE.md/CLAUDE.local.md are gitignored. Absent in a fresh clone
            # or a git worktree — which silently strips project doctrine.
            failures.append(f"{src} is missing — doctrine will not load "
                            f"(expected: gitignored, so absent in fresh clones and worktrees)")
            say(f"  MISSING  {src}")
        else:
            say(f"  ok       {src}")

    # -- 2. every @import target resolves ---------------------------------
    say("\n== @import targets ==")
    if not imports and not missing_sources:
        notes.append("no @import lines found — is the import block still present?")
    for src, target in imports:
        path = os.path.join(REPO, target)
        if os.path.exists(path):
            say(f"  ok       {target}")
        else:
            failures.append(f"@import target missing: {target}  (imported by {src})")
            say(f"  MISSING  {target}   <- imported by {src}")

    # -- 3. symlinked trees resolve ---------------------------------------
    say("\n== symlinked trees ==")
    for d, expected in SYMLINK_EXPECTATIONS.items():
        path = os.path.join(REPO, d)
        if not os.path.exists(path):
            failures.append(f"{d} does not resolve (broken symlink or deleted)")
            say(f"  BROKEN   {d}")
            continue
        kind = "symlink" if os.path.islink(path) else "real dir"
        if expected:
            probe = os.path.join(path, expected)
            if not os.path.exists(probe):
                failures.append(f"{d} resolves but is missing {expected} "
                                f"— pointing at the wrong tree?")
                say(f"  WRONG    {d} ({kind}) — no {expected}")
                continue
        say(f"  ok       {d} ({kind})")

    # -- 3b. project rules: authoritative copy present, global copy not stale --
    say("\n== project rules (.devin authoritative) ==")
    for name in DUPLICATED_RULES:
        local = os.path.join(REPO, LOCAL_RULES_DIR, name)
        glob_ = os.path.join(REPO, GLOBAL_RULES_DIR, name)
        if not os.path.exists(local):
            failures.append(f"{LOCAL_RULES_DIR}/{name} missing (authoritative copy)")
            say(f"  MISSING  {LOCAL_RULES_DIR}/{name}")
            continue
        if not os.path.exists(glob_):
            # Intended state since 2026-07-30. Not a failure.
            say(f"  ok       {name} (project-only, no global copy)")
            continue
        with open(local, "rb") as a, open(glob_, "rb") as b:
            if a.read() != b.read():
                failures.append(
                    f"{name} has DRIFTED between {LOCAL_RULES_DIR} and {GLOBAL_RULES_DIR}. "
                    f"Devin and Windsurf are reading different rules. "
                    f"The .devin copy is authoritative (git-tracked); copy it over the other.")
                say(f"  DRIFTED  {name}")
            else:
                say(f"  in sync  {name}")

    # -- 4. load-bearing files --------------------------------------------
    say("\n== critical files ==")
    for f in CRITICAL:
        if os.path.exists(os.path.join(REPO, f)):
            say(f"  ok       {f}")
        else:
            failures.append(f"critical file missing: {f}")
            say(f"  MISSING  {f}")

    # -- report ------------------------------------------------------------
    print()
    if notes:
        for n in notes:
            print(f"note: {n}")
    # NOTE: ASCII only in output. The Windows console defaults to cp1252 and
    # mangles em dashes, which is how this line looked on first run.
    if failures:
        print(f"FAIL - {len(failures)} problem(s):\n")
        for f in failures:
            print(f"  * {f}")
        print("\nDoctrine is incomplete. Agents will run without it and will NOT warn you.")
        print("If a symlink is involved, inspect before repairing:")
        print("  Get-Item .devin\\rules | Select-Object LinkType, Target")
        print("Remove a symlink with `cmd /c rmdir <path>` (removes the link, never the target).")
        return 1

    print(f"PASS - {len(imports)} imports, "
          f"{len(SYMLINK_EXPECTATIONS)} trees, {len(CRITICAL)} critical files all resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
