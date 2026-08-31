"""Deterministic fixtures for the native originality/source-attribution gate.

This validator checks workflow evidence and invariant fields only. It does not
scan the web, call WriterZen, or claim to detect all plagiarism.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional


REFERENCE = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)
MAX_EVIDENCE_AGE_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class OperationsEvidence:
    decision: str
    evidence_ref: str
    checked_at: str
    owner: str
    writerzen_plagiarism_action: str
    writerzen_plagiarism_requirement: str
    writerzen_plagiarism_credit_spend: str


@dataclass(frozen=True)
class Handoff:
    native_drafting_mode: str
    draft_provenance: str
    source_attribution_status: str
    source_attribution_refs: tuple[str, ...]
    competitor_text_copied: bool
    uncredited_close_paraphrase: bool
    distinctive_overlap_status: str
    distinctive_overlap_findings: tuple[str, ...]
    draft_content_hash: str
    originality_evidence_content_hash: str
    writerzen_plagiarism_checker_used: bool
    writerzen_plagiarism_checker_required: bool
    writerzen_plagiarism_credit_spent: bool
    external_checker_attempted: bool
    external_checker_authorized: bool
    external_checker_provider: str
    external_checker_authorization_ref: str
    evidence_ref: str
    evidence_checked_at: str
    operations: Optional[OperationsEvidence]


def parse_timestamp(value: str) -> Optional[datetime]:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate(handoff: Handoff, as_of: Optional[datetime] = None) -> list[str]:
    reference = as_of or datetime.now(timezone.utc)
    failures: list[str] = []

    if handoff.native_drafting_mode != "native":
        failures.append("draft body is not marked as native drafting")
    if not handoff.draft_provenance.strip():
        failures.append("missing draft provenance")
    if handoff.source_attribution_status not in {"complete", "not_applicable"}:
        failures.append("source attribution status is missing or unknown")
    if handoff.source_attribution_status == "complete" and not handoff.source_attribution_refs:
        failures.append("complete source attribution has no source references")
    if handoff.source_attribution_status == "not_applicable" and handoff.source_attribution_refs:
        failures.append("not_applicable attribution contains source references")
    for label, value in (
        ("draft content hash", handoff.draft_content_hash),
        ("originality evidence content hash", handoff.originality_evidence_content_hash),
    ):
        if not value.strip():
            failures.append(f"missing {label}")
    if (
        handoff.draft_content_hash.strip()
        and handoff.originality_evidence_content_hash.strip()
        and handoff.draft_content_hash != handoff.originality_evidence_content_hash
    ):
        failures.append("originality evidence does not cover the exact draft hash")
    if handoff.competitor_text_copied:
        failures.append("competitor/source text is marked copied")
    if handoff.uncredited_close_paraphrase:
        failures.append("uncredited close paraphrase is marked present")
    if handoff.distinctive_overlap_status != "clear":
        failures.append("distinctive-overlap review is not clear")
    if handoff.distinctive_overlap_status == "clear" and handoff.distinctive_overlap_findings:
        failures.append("clear overlap status has unresolved findings")

    if handoff.writerzen_plagiarism_checker_used:
        failures.append("WriterZen plagiarism checker was used")
    if handoff.writerzen_plagiarism_checker_required:
        failures.append("WriterZen plagiarism checker is incorrectly required")
    if handoff.writerzen_plagiarism_credit_spent:
        failures.append("WriterZen plagiarism credits/words were spent")

    if not handoff.evidence_ref.strip():
        failures.append("missing originality evidence reference")
    evidence_time = parse_timestamp(handoff.evidence_checked_at)
    if evidence_time is None:
        failures.append("invalid originality evidence timestamp")
    elif evidence_time > reference or (reference - evidence_time).total_seconds() > MAX_EVIDENCE_AGE_SECONDS:
        failures.append("originality evidence is stale or future-dated")

    if handoff.external_checker_attempted:
        if not handoff.external_checker_authorized:
            failures.append("external checker was attempted without explicit user authorization")
        if not handoff.external_checker_provider.strip():
            failures.append("external checker provider is missing")
        if handoff.external_checker_provider.casefold() == "writerzen":
            failures.append("WriterZen cannot be re-enabled as an external checker")
        if not handoff.external_checker_authorization_ref.strip():
            failures.append("external checker authorization evidence is missing")
    elif handoff.external_checker_authorized or handoff.external_checker_provider.casefold() not in {"", "none"}:
        failures.append("external checker evidence is contradictory")

    operations = handoff.operations
    if operations is None:
        failures.append("missing Operations originality attestation")
    else:
        if operations.decision != "PASS":
            failures.append("Operations originality decision is not PASS")
        if operations.writerzen_plagiarism_action != "NOT_RUN":
            failures.append("Operations does not attest that WriterZen plagiarism action was not run")
        if operations.writerzen_plagiarism_requirement != "NOT_REQUIRED":
            failures.append("Operations does not attest that WriterZen plagiarism was not required")
        if operations.writerzen_plagiarism_credit_spend != "NONE":
            failures.append("Operations does not attest that WriterZen plagiarism credits were not spent")
        if not operations.evidence_ref.strip() or operations.evidence_ref != handoff.evidence_ref:
            failures.append("Operations evidence does not identify the exact originality evidence")
        if not operations.owner.strip():
            failures.append("missing Operations originality owner")
        checked = parse_timestamp(operations.checked_at)
        if checked is None:
            failures.append("invalid Operations originality timestamp")
        elif checked > reference or (reference - checked).total_seconds() > MAX_EVIDENCE_AGE_SECONDS:
            failures.append("Operations originality attestation is stale or future-dated")
    return failures


def operations(evidence_ref: str = "evidence://originality/post-8/2026-08-31") -> OperationsEvidence:
    return OperationsEvidence(
        decision="PASS",
        evidence_ref=evidence_ref,
        checked_at="2026-08-31T11:59:00+00:00",
        owner="Operations",
        writerzen_plagiarism_action="NOT_RUN",
        writerzen_plagiarism_requirement="NOT_REQUIRED",
        writerzen_plagiarism_credit_spend="NONE",
    )


def base() -> Handoff:
    evidence_ref = "evidence://originality/post-8/2026-08-31"
    return Handoff(
        native_drafting_mode="native",
        draft_provenance="native draft from approved WriterZen outline plus recorded first-use test and cited sources",
        source_attribution_status="complete",
        source_attribution_refs=("https://help.openai.com/",),
        competitor_text_copied=False,
        uncredited_close_paraphrase=False,
        distinctive_overlap_status="clear",
        distinctive_overlap_findings=(),
        draft_content_hash="sha256:final-draft",
        originality_evidence_content_hash="sha256:final-draft",
        writerzen_plagiarism_checker_used=False,
        writerzen_plagiarism_checker_required=False,
        writerzen_plagiarism_credit_spent=False,
        external_checker_attempted=False,
        external_checker_authorized=False,
        external_checker_provider="none",
        external_checker_authorization_ref="",
        evidence_ref=evidence_ref,
        evidence_checked_at="2026-08-31T11:58:00+00:00",
        operations=operations(evidence_ref),
    )


def authorized_external(base_handoff: Handoff) -> Handoff:
    return replace(
        base_handoff,
        external_checker_attempted=True,
        external_checker_authorized=True,
        external_checker_provider="approved-third-party",
        external_checker_authorization_ref="approval://user/2026-08-31/external-originality-check",
    )


def main() -> int:
    valid = base()
    cases = {
        "native_draft_no_writerzen_checker_pass": valid,
        "not_applicable_sources_pass": replace(
            valid, source_attribution_status="not_applicable", source_attribution_refs=()
        ),
        "explicitly_authorized_external_checker_pass": authorized_external(valid),
        "writerzen_checker_used_fail": replace(valid, writerzen_plagiarism_checker_used=True),
        "writerzen_checker_required_fail": replace(valid, writerzen_plagiarism_checker_required=True),
        "writerzen_checker_credit_spent_fail": replace(valid, writerzen_plagiarism_credit_spent=True),
        "copied_competitor_text_fail": replace(valid, competitor_text_copied=True),
        "uncredited_close_paraphrase_fail": replace(valid, uncredited_close_paraphrase=True),
        "missing_source_attribution_fail": replace(valid, source_attribution_refs=()),
        "mismatched_hash_fail": replace(valid, originality_evidence_content_hash="sha256:other"),
        "missing_provenance_fail": replace(valid, draft_provenance=""),
        "suspicious_overlap_fail": replace(
            valid,
            distinctive_overlap_status="flagged",
            distinctive_overlap_findings=("distinctive competitor phrase",),
        ),
        "unauthorized_external_checker_fail": replace(
            valid,
            external_checker_attempted=True,
            external_checker_provider="approved-third-party",
        ),
        "writerzen_external_checker_even_authorized_fail": replace(
            authorized_external(valid), external_checker_provider="WriterZen"
        ),
        "operations_checker_run_fail": replace(
            valid,
            operations=replace(operations(valid.evidence_ref), writerzen_plagiarism_action="RUN"),
        ),
        "operations_missing_attestation_fail": replace(valid, operations=None),
        "operations_evidence_mismatch_fail": replace(
            valid,
            operations=replace(operations(valid.evidence_ref), evidence_ref="evidence://other"),
        ),
    }
    expected_pass = {
        "native_draft_no_writerzen_checker_pass",
        "not_applicable_sources_pass",
        "explicitly_authorized_external_checker_pass",
    }
    outcomes: dict[str, bool] = {}
    for name, handoff in cases.items():
        passed = not validate(handoff, as_of=REFERENCE)
        outcomes[name] = passed
        if name in expected_pass:
            assert passed, (name, validate(handoff, as_of=REFERENCE))
        else:
            assert not passed, (name, "unexpected pass")
    print(
        "PASS native originality/source-attribution fixtures: "
        f"{len(cases)} scenarios; {sum(outcomes.values())} pass / "
        f"{len(cases) - sum(outcomes.values())} fail; no-credit WriterZen "
        "checker prohibition, provenance, attribution, overlap, hash, and "
        "explicit external-checker authorization invariants verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
