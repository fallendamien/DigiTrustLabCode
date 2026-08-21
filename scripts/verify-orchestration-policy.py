#!/usr/bin/env python3
"""Verify the repo-local orchestration policy and required pointers."""

from pathlib import Path
import argparse
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "ai" / "orchestration-policy.md"
if configured_policy := os.environ.get("TSOT_ORCHESTRATION_POLICY"):
    CANONICAL = Path(configured_policy)
else:
    canonical_candidates = (
        Path.home() / ".codeium" / "windsurf" / "agent-templates" / "workspace" / "rules" / "orchestration-policy.md",
        ROOT.parent / "agent-templates" / "workspace" / "rules" / "orchestration-policy.md",
    )
    CANONICAL = next((path for path in canonical_candidates if path.is_file()), canonical_candidates[0])
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
    ("Codex Sol", "gpt-5.6-luna"),
    ("Codex Sol", "high` effort"),
    ("Claude Opus", "claude-sonnet-4-6"),
    ("actual model ID", "reasoning effort"),
    ("host dispatch record", "worker self-description is not identity evidence"),
    ("gpt-5.5", "not a Claude worker"),
    ("Worker-context precedence", "bounded-worker"),
    ("Risk-based delegation", "approval-gated"),
    ("safe local", "reversible"),
    ("dispatch fails", "fallback"),
    ("runtime audits", "orchestrator turns"),
)

CONFIG_MODEL = "gpt-5.6-luna"
CONFIG_EFFORT = "high"


def codex_config_drift(path: Path):
    """Return configured Codex worker values that differ from Remy's contract."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    model_match = re.search(r'^\s*default_subagent_model\s*=\s*"([^"]+)"', text, re.MULTILINE)
    effort_match = re.search(r'^\s*default_subagent_reasoning_effort\s*=\s*"([^"]+)"', text, re.MULTILINE)
    drift = []
    if not model_match:
        drift.append("default_subagent_model is missing")
    elif model_match.group(1) != CONFIG_MODEL:
        drift.append(f"default_subagent_model={model_match.group(1)!r} (expected {CONFIG_MODEL!r})")
    if not effort_match:
        drift.append("default_subagent_reasoning_effort is missing")
    elif effort_match.group(1) != CONFIG_EFFORT:
        drift.append(f"default_subagent_reasoning_effort={effort_match.group(1)!r} (expected {CONFIG_EFFORT!r})")
    return drift


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-codex-config",
        action="store_true",
        help="fail when the machine-specific Codex worker config drifts from the shared contract",
    )
    args = parser.parse_args()
    failures = []
    if not POLICY.is_file():
        failures.append("missing repo-local policy adapter")
    if not CANONICAL.is_file():
        failures.append(f"missing canonical TSOT policy: {CANONICAL}")
    if failures:
        print("FAIL orchestration policy: " + "; ".join(failures))
        return 1
    adapter = POLICY.read_text(encoding="utf-8").lower()
    policy = CANONICAL.read_text(encoding="utf-8").lower()
    normalized_policy = " ".join(policy.split())
    for model, mapping in REQUIRED:
        if model.lower() not in normalized_policy or mapping.lower() not in normalized_policy:
            failures.append(f"missing mapping: {model} -> {mapping}")
    if "canonical policy" not in adapter or "thin" not in adapter:
        failures.append("repo-local policy is not a thin canonical adapter")
    pointers = 0
    for relative, target in POINTERS.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing pointer file: {relative}")
        elif target.lower() not in path.read_text(encoding="utf-8").lower():
            failures.append(f"missing policy pointer: {relative}")
        else:
            pointers += 1
    if "behavioral" not in policy or "not cryptographic" not in policy:
        failures.append("missing behavioral/non-cryptographic caveat")
    config_path = Path(os.environ.get("CODEX_CONFIG_PATH", Path.home() / ".codex" / "config.toml"))
    config_drift = codex_config_drift(config_path)
    if config_drift and args.strict_codex_config:
        failures.append(f"Codex config drift at {config_path}: " + "; ".join(config_drift))
    if failures:
        print("FAIL orchestration policy: " + "; ".join(failures))
        return 1
    if config_drift:
        print(f"WARN Codex config drift at {config_path}: " + "; ".join(config_drift))
        print("WARN shared guidance expects the documented Luna High value; update the user config explicitly and do not overwrite it silently")
    elif config_path.is_file():
        print(f"PASS Codex config: {config_path} matches {CONFIG_MODEL} at {CONFIG_EFFORT} effort")
    print(f"PASS orchestration policy: policy present; {len(REQUIRED)} mappings; {pointers} pointers; dispatch identity contract and caveat present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
