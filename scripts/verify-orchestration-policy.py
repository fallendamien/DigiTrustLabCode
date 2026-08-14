#!/usr/bin/env python3
"""Verify the repo-local orchestration policy and required pointers."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "ai" / "orchestration-policy.md"
POINTERS = {
    ".claude/rules/orchestration-gate.md": "../../docs/ai/orchestration-policy.md",
    "AGENTS.md": "docs/ai/orchestration-policy.md",
    "departments/README.md": "../docs/ai/orchestration-policy.md",
    "workspaces/executive-assistant/AGENTS.md": "../../docs/ai/orchestration-policy.md",
}
REQUIRED = (
    ("Codex Sol", "orchestrator"),
    ("Claude Opus", "orchestrator"),
    ("Luna XHigh", "Luna High"),
    ("Haiku", "simple"),
    ("Sonnet", "complex"),
    ("Luna High", "default"),
    ("Luna High", "gpt-5.6-luna"),
    ("Luna High", "high reasoning"),
)


def main():
    failures = []
    if not POLICY.is_file():
        failures.append("missing policy")
        print("FAIL orchestration policy: " + "; ".join(failures))
        return 1
    policy = POLICY.read_text(encoding="utf-8").lower()
    for model, mapping in REQUIRED:
        if model.lower() not in policy or mapping.lower() not in policy:
            failures.append(f"missing mapping: {model} -> {mapping}")
    pointers = 0
    for relative, target in POINTERS.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing pointer file: {relative}")
        elif target.lower() not in path.read_text(encoding="utf-8").lower():
            failures.append(f"missing policy pointer: {relative}")
        else:
            pointers += 1
    if "behavioral" not in policy or "not a cryptographic" not in policy:
        failures.append("missing behavioral/non-cryptographic caveat")
    if failures:
        print("FAIL orchestration policy: " + "; ".join(failures))
        return 1
    print(f"PASS orchestration policy: policy present; {len(REQUIRED)} mappings; {pointers} pointers; caveat present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
