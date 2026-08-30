"""Deterministic fixtures for the WriterZen AI-credit gate.

The checker validates workflow invariants only. It does not connect to
WriterZen, infer checkbox state, or claim how many credits optional keyword
suggestions consume.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional


# Fixture anchor only. Production validation uses the caller's `as_of` value or
# the current UTC time; it must not inherit this historical test date.
FIXTURE_REFERENCE = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)
MAX_UI_AGE_SECONDS = 5 * 60
MAX_OPERATIONS_AGE_SECONDS = 60
MAX_REVIEW_AGE_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class UiEvidence:
    outline_toggle: Optional[bool]
    whole_article_toggle: Optional[bool]
    keyword_suggestion_toggle: Optional[bool]
    keyword_set_status: str
    captured_at: str
    create_attempted_at: str
    evidence_ref: str
    ai_credit_status: str = "unknown"
    upgrade_attempted: Optional[bool] = None
    bypass_attempted: Optional[bool] = None
    suggestion_insufficiency: str = ""
    user_credit_authorization: str = ""
    displayed_suggestion_cost: str = ""


@dataclass(frozen=True)
class OperationsAttestation:
    decision: str
    status: str
    evidence_ref: str
    checked_at: str
    owner: str


@dataclass(frozen=True)
class Review:
    provider: str
    model: str
    status: str
    content_hash: str
    checked_at: str


@dataclass(frozen=True)
class Handoff:
    ui: UiEvidence
    operations: Optional[OperationsAttestation]
    writerzen_generation_mode: str = "outline_only"
    native_drafting_mode: str = "native"
    draft_status: str = "outline"
    dual_review_status: str = "PENDING"
    anthropic_review: Optional[Review] = None
    openai_review: Optional[Review] = None


def parse_timestamp(value: str) -> Optional[datetime]:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def is_actual_claude_sonnet(review: Review) -> bool:
    """Match the naturalness-review contract's provider/model envelope."""
    provider = review.provider.casefold()
    model = review.model.casefold()
    return provider in {"anthropic", "firstparty"} and model.startswith(
        "claude-"
    ) and "sonnet" in model


def validate_ui(ui: UiEvidence, as_of: Optional[datetime] = None) -> list[str]:
    reference = as_of or datetime.now(timezone.utc)
    failures: list[str] = []
    if ui.outline_toggle is not True:
        failures.append("outline-only toggle is not proven ON")
    if ui.whole_article_toggle is not False:
        failures.append("whole-article toggle is not proven OFF")
    if ui.keyword_suggestion_toggle is None:
        failures.append("keyword-suggestion toggle state is unknown")
    if ui.keyword_set_status not in {"adequate", "insufficient"}:
        failures.append("keyword-set status is missing or unknown")
    if ui.ai_credit_status not in {"adequate", "insufficient"}:
        failures.append("AI-credit status is missing or unknown")
    if not ui.evidence_ref.strip():
        failures.append("missing fresh WriterZen UI evidence reference")

    captured = parse_timestamp(ui.captured_at)
    attempted = parse_timestamp(ui.create_attempted_at)
    if captured is None or attempted is None:
        failures.append("missing or invalid WriterZen UI timestamps")
    elif not (
        captured <= attempted
        and attempted <= reference
        and (attempted - captured).total_seconds() <= MAX_UI_AGE_SECONDS
    ):
        failures.append("WriterZen UI evidence is stale or not immediately before Create")

    if ui.upgrade_attempted is not False:
        failures.append("Upgrade or plan-change attempt is not proven absent")
    if ui.bypass_attempted is not False:
        failures.append("AI-credit bypass attempt is not proven absent")
    if ui.ai_credit_status == "insufficient":
        failures.append("insufficient AI credits block the outline-only Create request")

    if ui.keyword_suggestion_toggle is True:
        if ui.keyword_set_status != "insufficient":
            failures.append("keyword suggestions enabled despite an adequate validated set")
        if not ui.suggestion_insufficiency.strip():
            failures.append("missing documented keyword insufficiency")
        if not ui.user_credit_authorization.strip():
            failures.append("missing explicit user authorization for optional credit spend")
        if not ui.displayed_suggestion_cost.strip():
            failures.append("optional keyword-suggestion cost is unknown")
    return failures


def validate_operations(
    handoff: Handoff, as_of: Optional[datetime] = None
) -> list[str]:
    reference = as_of or datetime.now(timezone.utc)
    attestation = handoff.operations
    if attestation is None:
        return ["missing Operations AI-credit attestation"]
    failures: list[str] = []
    if attestation.decision != "PASS" or attestation.status != "PASS":
        failures.append("Operations AI-credit decision/status is not PASS")
    if attestation.decision != attestation.status:
        failures.append("contradictory Operations AI-credit decision/status")
    if not attestation.owner.strip():
        failures.append("missing Operations AI-credit owner")
    if not attestation.evidence_ref.strip() or attestation.evidence_ref != handoff.ui.evidence_ref:
        failures.append("Operations attestation does not identify the exact UI evidence")
    captured = parse_timestamp(handoff.ui.captured_at)
    attempted = parse_timestamp(handoff.ui.create_attempted_at)
    checked = parse_timestamp(attestation.checked_at)
    if checked is None:
        failures.append("missing or invalid Operations AI-credit checked_at")
    elif captured is None or attempted is None:
        failures.append("Operations freshness cannot be compared with invalid UI timestamps")
    elif not (
        captured <= checked <= attempted
        and (attempted - checked).total_seconds() <= MAX_OPERATIONS_AGE_SECONDS
        and checked <= reference
    ):
        failures.append("Operations AI-credit attestation is stale or not immediately before Create")
    return failures


def validate_reviews(
    handoff: Handoff, as_of: Optional[datetime] = None
) -> list[str]:
    reference = as_of or datetime.now(timezone.utc)
    ready_statuses = {"complete", "ready", "publication_ready"}
    if handoff.draft_status not in ready_statuses:
        return []
    failures: list[str] = []
    if handoff.dual_review_status != "PASS":
        failures.append("native draft is marked ready without a dual-review PASS")
    reviews = (("Anthropic", handoff.anthropic_review), ("OpenAI", handoff.openai_review))
    for name, review in reviews:
        if review is None:
            failures.append(f"missing {name} independent review evidence")
            continue
        if review.status != "PASS":
            failures.append(f"{name} review is not PASS")
        if not review.provider.strip() or not review.model.strip():
            failures.append(f"{name} review provider/model identity is missing")
        elif name == "Anthropic" and not is_actual_claude_sonnet(review):
            failures.append("Anthropic review is not an actual Claude model")
        elif name == "OpenAI" and (
            review.provider.casefold() != "openai"
            or not review.model.casefold().startswith("gpt-")
        ):
            failures.append("OpenAI review is not an actual OpenAI model")
        if not review.content_hash.strip():
            failures.append(f"{name} review content hash is missing")
        checked = parse_timestamp(review.checked_at)
        if checked is None:
            failures.append(f"{name} review timestamp is invalid")
        elif not (
            checked <= reference
            and (reference - checked).total_seconds() <= MAX_REVIEW_AGE_SECONDS
        ):
            failures.append(f"{name} review is stale or future-dated")
    if handoff.anthropic_review and handoff.openai_review:
        if not is_actual_claude_sonnet(handoff.anthropic_review):
            failures.append("Anthropic lane is not an actual Anthropic review")
        if handoff.openai_review.provider.casefold() != "openai":
            failures.append("OpenAI lane is not an independent OpenAI review")
        if handoff.anthropic_review.content_hash != handoff.openai_review.content_hash:
            failures.append("dual reviews do not cover the same final content hash")
    return failures


def validate(
    handoff: Handoff, as_of: Optional[datetime] = None
) -> tuple[bool, list[str]]:
    reference = as_of or datetime.now(timezone.utc)
    failures = validate_ui(handoff.ui, as_of=reference)
    failures.extend(validate_operations(handoff, as_of=reference))
    if handoff.writerzen_generation_mode != "outline_only":
        failures.append("WriterZen generation mode is not outline_only")
    if handoff.native_drafting_mode != "native":
        failures.append("article body is not assigned to native drafting")
    failures.extend(validate_reviews(handoff, as_of=reference))
    return not failures, failures


def ui_base(*, suggestions: bool = False) -> UiEvidence:
    return UiEvidence(
        outline_toggle=True,
        whole_article_toggle=False,
        keyword_suggestion_toggle=suggestions,
        keyword_set_status="insufficient" if suggestions else "adequate",
        captured_at="2026-08-31T11:59:00+00:00",
        create_attempted_at="2026-08-31T12:00:00+00:00",
        evidence_ref="evidence://writerzen/create-modal/2026-08-31T11-59Z",
        ai_credit_status="adequate",
        upgrade_attempted=False,
        bypass_attempted=False,
    )


def operations(
    ui: UiEvidence,
    checked_at: str = "2026-08-31T11:59:30+00:00",
) -> OperationsAttestation:
    return OperationsAttestation(
        decision="PASS",
        status="PASS",
        evidence_ref=ui.evidence_ref,
        checked_at=checked_at,
        owner="Operations",
    )


def review(provider: str, model: str, content_hash: str = "sha256:final") -> Review:
    return Review(
        provider=provider,
        model=model,
        status="PASS",
        content_hash=content_hash,
        checked_at="2026-08-31T12:00:00+00:00",
    )


def build_cases() -> dict[str, Handoff]:
    ui = ui_base()
    valid = Handoff(ui=ui, operations=operations(ui))
    suggestion_ui = replace(
        ui_base(suggestions=True),
        suggestion_insufficiency="validated cluster lacks the poster-format question",
        user_credit_authorization="approval://user/2026-08-31/writerzen-keyword-suggestions",
        displayed_suggestion_cost="shown in current WriterZen confirmation",
    )
    suggestion_valid = Handoff(ui=suggestion_ui, operations=operations(suggestion_ui))
    complete_reviews = Handoff(
        ui=ui,
        operations=operations(ui),
        draft_status="complete",
        dual_review_status="PASS",
        anthropic_review=review("anthropic", "claude-sonnet-4-6"),
        openai_review=review("openai", "gpt-5.6-luna"),
    )
    return {
        "outline_only_pass": valid,
        "suggestions_default_off_pass": valid,
        "authorized_suggestions_pass": suggestion_valid,
        "whole_article_enabled_fail": replace(
            valid, ui=replace(ui, whole_article_toggle=True)
        ),
        "outline_toggle_unknown_fail": replace(valid, ui=replace(ui, outline_toggle=None)),
        "whole_article_toggle_unknown_fail": replace(
            valid, ui=replace(ui, whole_article_toggle=None)
        ),
        "stale_ui_evidence_fail": replace(
            valid, ui=replace(ui, captured_at="2026-08-31T11:40:00+00:00")
        ),
        "insufficient_credits_fail": replace(
            valid, ui=replace(ui, ai_credit_status="insufficient")
        ),
        "insufficient_credits_attempted_bypass_fail": replace(
            valid,
            ui=replace(
                ui,
                ai_credit_status="insufficient",
                upgrade_attempted=True,
                bypass_attempted=True,
            ),
        ),
        "missing_operations_attestation_fail": replace(valid, operations=None),
        "stale_operations_attestation_fail": replace(
            valid,
            operations=replace(
                operations(ui), checked_at="2026-08-31T11:45:00+00:00"
            ),
        ),
        "conflicting_operations_evidence_fail": replace(
            valid,
            operations=replace(
                operations(ui), evidence_ref="evidence://writerzen/other-snapshot"
            ),
        ),
        "suggestions_without_authorization_fail": replace(
            suggestion_valid,
            ui=replace(suggestion_ui, user_credit_authorization=""),
        ),
        "suggestions_without_insufficiency_fail": replace(
            suggestion_valid,
            ui=replace(suggestion_ui, suggestion_insufficiency=""),
        ),
        "suggestions_without_displayed_cost_fail": replace(
            suggestion_valid,
            ui=replace(suggestion_ui, displayed_suggestion_cost=""),
        ),
        "suggestions_with_adequate_set_fail": replace(
            valid,
            ui=replace(ui, keyword_suggestion_toggle=True),
        ),
        "native_draft_without_dual_reviews_fail": replace(valid, draft_status="complete"),
        "native_draft_ready_without_dual_reviews_fail": replace(
            valid, draft_status="ready"
        ),
        "native_draft_mismatched_hash_fail": replace(
            complete_reviews,
            openai_review=review("openai", "gpt-5.6-luna", "sha256:other"),
        ),
        "native_draft_stale_review_fail": replace(
            complete_reviews,
            anthropic_review=replace(
                complete_reviews.anthropic_review,
                checked_at="2026-08-29T12:00:00+00:00",
            ),
        ),
        "native_draft_dual_reviews_pass": complete_reviews,
        "native_draft_first_party_claude_pass": replace(
            complete_reviews,
            anthropic_review=review("firstParty", "claude-sonnet-5"),
        ),
        "native_draft_mislabeled_first_party_fail": replace(
            complete_reviews,
            anthropic_review=review("firstParty", "gpt-5.6-luna"),
        ),
        "native_draft_same_family_fail": replace(
            complete_reviews,
            openai_review=review("anthropic", "claude-sonnet-4-6"),
        ),
    }


def main() -> int:
    cases = build_cases()
    expected_pass = {
        "outline_only_pass",
        "suggestions_default_off_pass",
        "authorized_suggestions_pass",
        "native_draft_dual_reviews_pass",
        "native_draft_first_party_claude_pass",
    }
    outcomes: dict[str, bool] = {}
    for name, handoff in cases.items():
        passed, failures = validate(handoff, as_of=FIXTURE_REFERENCE)
        outcomes[name] = passed
        if name in expected_pass:
            assert passed, (name, failures)
        else:
            assert not passed, (name, "unexpected pass")

    assert any(
        "whole-article toggle" in f
        for f in validate(
            replace(
                valid_case(),
                ui=replace(valid_case().ui, whole_article_toggle=True),
            ),
            as_of=FIXTURE_REFERENCE,
        )[1]
    )

    september_ui = replace(
        valid_case().ui,
        captured_at="2026-09-01T11:59:00+00:00",
        create_attempted_at="2026-09-01T12:00:00+00:00",
        evidence_ref="evidence://writerzen/create-modal/2026-09-01T11-59Z",
    )
    september_case = Handoff(
        ui=september_ui,
        operations=operations(
            september_ui, checked_at="2026-09-01T11:59:30+00:00"
        ),
    )
    fresh_pass, fresh_failures = validate(
        september_case,
        as_of=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
    )
    assert fresh_pass, ("september_1_fresh_attestation_pass", fresh_failures)
    stale_case = replace(
        september_case,
        operations=operations(
            september_ui, checked_at="2026-09-01T11:55:00+00:00"
        ),
    )
    stale_pass, stale_failures = validate(
        stale_case,
        as_of=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
    )
    assert not stale_pass, ("september_1_stale_attestation_fail", stale_failures)
    print(
        "PASS WriterZen AI-credit fixtures: "
        f"{len(cases)} scenarios + date-rollover regression; "
        f"{sum(outcomes.values())} pass / "
        f"{len(cases) - sum(outcomes.values())} fail; outline-only, exact fresh "
        "Operations evidence, optional keyword-suggestion authorization, and "
        "dual-review content-hash invariants verified"
    )
    return 0


def valid_case() -> Handoff:
    ui = ui_base()
    return Handoff(ui=ui, operations=operations(ui))


if __name__ == "__main__":
    raise SystemExit(main())
