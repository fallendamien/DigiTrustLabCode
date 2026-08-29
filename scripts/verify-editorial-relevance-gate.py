"""Deterministic fixtures for DigiTrust Lab's editorial relevance gate.

The checker uses explicit family/cluster/intent/entity registries and exact
canonical URL identity. It does not attempt general NLP or query live systems.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
import re
from typing import Optional
from urllib.parse import urlsplit, urlunsplit


AS_OF = date(2026, 8, 29)
FRESHNESS_DAYS = 30
APPROVED_CATEGORIES = {
    "ai-tools": "AI Tools",
    "canva-design": "Canva & Design",
    "prompt-engineering": "Prompt Engineering",
    "digital-skills": "Digital Skills",
}

# These identifiers are the relevance contract. Text is evidence only; it
# cannot grant relevance without a registered family, intent, and entity set.
TOPIC_FAMILIES = {
    "ai-tools.chatgpt.poster": {
        "pillar_id": "ai-tools",
        "cluster_id": "ai-tools.chatgpt",
        "topic_intent_id": "intent.chatgpt.poster.creation",
        "subject_entity_allowlist": frozenset({"entity.chatgpt", "entity.poster"}),
        "forbidden_text_terms": frozenset(
            {"ranking", "google", "search", "visibility", "seo", "notion", "wordpress"}
        ),
        "requires_approval": False,
    },
    "digital-skills.notion.task-template": {
        "pillar_id": "digital-skills",
        "cluster_id": "digital-skills.notion",
        "topic_intent_id": "intent.notion.daily.task.management",
        "subject_entity_allowlist": frozenset(
            {"entity.notion", "entity.task-template"}
        ),
        "forbidden_text_terms": frozenset(
            {"ranking", "google", "search", "visibility", "seo", "wordpress"}
        ),
        "requires_approval": False,
    },
    # This family exists only to exercise the exact approval path. The fixture
    # is not evidence that the live calendar currently approves this pivot.
    "digital-skills.seo.wordpress-audit": {
        "pillar_id": "digital-skills",
        "cluster_id": "digital-skills.seo",
        "topic_intent_id": "intent.wordpress.seo.audit",
        "subject_entity_allowlist": frozenset(
            {"entity.wordpress", "entity.seo-audit"}
        ),
        "forbidden_text_terms": frozenset({"notion", "chatgpt", "poster"}),
        "requires_approval": True,
    },
}


@dataclass(frozen=True)
class Attestation:
    decision: str
    status: str
    evidence_ref: str
    checked_at: str
    owner: str
    topic_family_id: str
    pillar_id: str
    cluster_id: str
    topic_intent_id: str
    subject_entity_ids: frozenset[str]


@dataclass(frozen=True)
class OperationsEvidence:
    calendar_ref: str
    calendar_status: str
    calendar_urls: tuple[str, ...]
    published_parent_or_peer_urls: tuple[str, ...]
    published_parent_or_peer_status: str
    inbound_source_urls: tuple[str, ...]
    inbound_source_status: str
    link_feasibility_urls: tuple[str, ...]
    link_feasibility_ref: str
    link_feasibility_status: str
    checked_at: str
    owner: str


@dataclass(frozen=True)
class Candidate:
    topic: str
    seed: str
    category_id: str
    topic_family_id: str
    pillar_id: str
    cluster_id: str
    topic_intent_id: str
    subject_entity_ids: frozenset[str]
    declared_seed_intent: str
    reader_problem: str
    authenticity_basis: str
    inventory_check: str
    existing_cluster_map: str
    mapped_pillar_id: str
    mapped_cluster_id: str
    published_parent_or_peer_url: str
    inbound_source_url: str
    incremental_value: str
    anchor_context: str
    pivot_status: str
    user_approval_ref: str
    research: Optional[Attestation]
    seo: Optional[Attestation]
    operations: Optional[Attestation]
    operations_evidence: Optional[OperationsEvidence]
    metrics_positive: bool = False


def normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def tokens(value: str) -> set[str]:
    return set(normalize(value).split())


def canonical_url(value: str) -> Optional[str]:
    """Canonicalize scheme/host case, trailing slash, and fragment only."""

    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        return None
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
        return None
    # netloc.casefold() normalizes scheme/host casing while preserving query,
    # path, and any explicit port. Fragments are intentionally discarded.
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/") or "/"
    return urlunsplit(
        (parsed.scheme.casefold(), parsed.netloc.casefold(), path, parsed.query, "")
    )


def date_is_fresh(value: str) -> bool:
    try:
        checked = date.fromisoformat(value)
    except ValueError:
        return False
    age = (AS_OF - checked).days
    return 0 <= age <= FRESHNESS_DAYS


def validate_attestation(
    name: str, attestation: Optional[Attestation], candidate: Candidate
) -> list[str]:
    if attestation is None:
        return [f"missing {name} attestation"]

    failures: list[str] = []
    if attestation.decision != "PASS" or attestation.status != "PASS":
        failures.append(f"{name} attestation decision/status not PASS")
    if attestation.decision != attestation.status:
        failures.append(f"contradictory {name} attestation decision/status")
    if not attestation.evidence_ref.strip():
        failures.append(f"missing {name} attestation evidence reference")
    if not attestation.owner.strip():
        failures.append(f"missing {name} attestation owner")
    if not date_is_fresh(attestation.checked_at):
        failures.append(f"stale or invalid {name} attestation checked_at")
    if (
        attestation.topic_family_id != candidate.topic_family_id
        or attestation.pillar_id != candidate.pillar_id
        or attestation.cluster_id != candidate.cluster_id
        or attestation.topic_intent_id != candidate.topic_intent_id
        or attestation.subject_entity_ids != candidate.subject_entity_ids
    ):
        failures.append(f"contradictory {name} attestation structured classification")
    return failures


def exact_url_in(candidate_url: str, evidence_urls: tuple[str, ...]) -> bool:
    expected = canonical_url(candidate_url)
    if expected is None:
        return False
    return any(canonical_url(value) == expected for value in evidence_urls)


def validate_operations_evidence(candidate: Candidate) -> list[str]:
    evidence = candidate.operations_evidence
    if evidence is None:
        return ["missing Operations independent current-evidence record"]

    failures: list[str] = []
    required = {
        "calendar_ref": evidence.calendar_ref,
        "calendar_urls": evidence.calendar_urls,
        "published_parent_or_peer_urls": evidence.published_parent_or_peer_urls,
        "inbound_source_urls": evidence.inbound_source_urls,
        "link_feasibility_urls": evidence.link_feasibility_urls,
        "link_feasibility_ref": evidence.link_feasibility_ref,
        "owner": evidence.owner,
    }
    failures.extend(
        f"missing Operations evidence {field}"
        for field, value in required.items()
        if not value
    )
    if evidence.calendar_status != "verified-current":
        failures.append("Operations calendar evidence is not independently current")
    if evidence.published_parent_or_peer_status != "verified-published":
        failures.append("Operations parent/peer URL is not independently published")
    if evidence.inbound_source_status != "verified-published":
        failures.append("Operations inbound-source URL is not independently published")
    if evidence.link_feasibility_status != "feasible":
        failures.append("Operations link feasibility is not independently verified")
    if not exact_url_in(candidate.published_parent_or_peer_url, evidence.calendar_urls):
        failures.append("Operations calendar evidence does not identify exact candidate parent/peer URL")
    if not exact_url_in(candidate.inbound_source_url, evidence.calendar_urls):
        failures.append("Operations calendar evidence does not identify exact candidate inbound URL")
    if not exact_url_in(candidate.published_parent_or_peer_url, evidence.published_parent_or_peer_urls):
        failures.append("Operations parent/peer URL evidence does not exactly match candidate URL")
    if not exact_url_in(candidate.inbound_source_url, evidence.inbound_source_urls):
        failures.append("Operations inbound-source URL evidence does not exactly match candidate URL")
    if not exact_url_in(candidate.published_parent_or_peer_url, evidence.link_feasibility_urls):
        failures.append("Operations link evidence does not identify exact candidate parent/peer URL")
    if not exact_url_in(candidate.inbound_source_url, evidence.link_feasibility_urls):
        failures.append("Operations link evidence does not identify exact candidate inbound URL")
    if not date_is_fresh(evidence.checked_at):
        failures.append("stale or invalid Operations current-evidence checked_at")
    return failures


def validate_semantic_contract(candidate: Candidate) -> list[str]:
    family = TOPIC_FAMILIES.get(candidate.topic_family_id)
    if family is None:
        return ["unapproved topic-family ID"]

    failures: list[str] = []
    if candidate.category_id != family["pillar_id"] or candidate.pillar_id != family["pillar_id"]:
        failures.append("topic-family/pillar structured classification mismatch")
    if candidate.cluster_id != family["cluster_id"]:
        failures.append("declared cluster structured classification mismatch")
    if candidate.topic_intent_id != family["topic_intent_id"]:
        failures.append("topic intent ID is not allowed for topic family")
    unknown_entities = candidate.subject_entity_ids - family["subject_entity_allowlist"]
    if not candidate.subject_entity_ids:
        failures.append("subject entity set is empty")
    if unknown_entities:
        failures.append(f"subject entity set contains off-family IDs {sorted(unknown_entities)}")
    if candidate.mapped_pillar_id != candidate.pillar_id:
        failures.append("cluster/link map pillar ID does not match candidate pillar ID")
    if candidate.mapped_cluster_id != candidate.cluster_id:
        failures.append("cluster/link map cluster ID does not match candidate cluster ID")

    # Text can reject a known contradiction, but cannot grant relevance by
    # itself; the structured family/intent/entity checks above remain required.
    for label, value in (
        ("proposed topic", candidate.topic),
        ("reader problem", candidate.reader_problem),
        ("seed", candidate.seed),
        ("declared seed intent", candidate.declared_seed_intent),
        ("incremental value", candidate.incremental_value),
        ("anchor/context", candidate.anchor_context),
        ("existing-cluster/link map", candidate.existing_cluster_map),
    ):
        forbidden = family["forbidden_text_terms"] & tokens(value)
        if forbidden:
            failures.append(
                f"{label} semantic family contradiction: forbidden off-family concepts "
                f"{sorted(forbidden)}"
            )

    if family["requires_approval"]:
        expected = (
            "approval://user/2026-08-29/topic-family/"
            f"{candidate.topic_family_id}"
        )
        if candidate.pivot_status != "approved" or candidate.user_approval_ref != expected:
            failures.append("pivot lacks exact user approval reference")
    elif candidate.pivot_status != "none":
        failures.append("unapproved pivot from the approved topic family")
    elif candidate.user_approval_ref:
        failures.append("unexpected approval reference for non-pivot")
    return failures


def relevance(candidate: Candidate) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not candidate.topic.strip():
        failures.append("missing proposed topic")
    if not candidate.seed.strip():
        failures.append("missing seed")
    if candidate.category_id not in APPROVED_CATEGORIES:
        failures.append("unapproved category ID")
    for label, value in (
        ("reader problem", candidate.reader_problem),
        ("authenticity basis", candidate.authenticity_basis),
        ("inventory/cannibalization check", candidate.inventory_check),
        ("existing-cluster/link map", candidate.existing_cluster_map),
        ("published parent/peer URL", candidate.published_parent_or_peer_url),
        ("plausible inbound source URL", candidate.inbound_source_url),
        ("incremental reader value", candidate.incremental_value),
        ("planned anchor/context", candidate.anchor_context),
    ):
        if not value.strip():
            failures.append(f"missing {label}")
    failures.extend(validate_semantic_contract(candidate))
    failures.extend(validate_operations_evidence(candidate))
    failures.extend(validate_attestation("Research", candidate.research, candidate))
    failures.extend(validate_attestation("SEO", candidate.seo, candidate))
    failures.extend(validate_attestation("Operations", candidate.operations, candidate))
    return not failures, failures


def content_acceptance(candidate: Candidate) -> tuple[bool, list[str]]:
    passed, failures = relevance(candidate)
    if not passed:
        failures = [f"Content rejection: {failure}" for failure in failures]
    return passed, failures


def make_attestation(owner: str, candidate: Candidate, **changes: object) -> Attestation:
    return Attestation(
        decision=str(changes.get("decision", "PASS")),
        status=str(changes.get("status", "PASS")),
        evidence_ref=str(changes.get("evidence_ref", f"evidence://{owner.casefold()}/2026-08-29")),
        checked_at=str(changes.get("checked_at", "2026-08-29")),
        owner=str(changes.get("owner", owner)),
        topic_family_id=str(changes.get("topic_family_id", candidate.topic_family_id)),
        pillar_id=str(changes.get("pillar_id", candidate.pillar_id)),
        cluster_id=str(changes.get("cluster_id", candidate.cluster_id)),
        topic_intent_id=str(changes.get("topic_intent_id", candidate.topic_intent_id)),
        subject_entity_ids=frozenset(
            changes.get("subject_entity_ids", candidate.subject_entity_ids)
        ),
    )


def make_operations(
    *,
    parent_urls: tuple[str, ...] = ("https://digitrustlab.com/post-2",),
    inbound_urls: tuple[str, ...] = ("https://digitrustlab.com/post-2",),
    calendar_urls: Optional[tuple[str, ...]] = None,
    link_urls: Optional[tuple[str, ...]] = None,
    calendar_status: str = "verified-current",
    parent_status: str = "verified-published",
    inbound_status: str = "verified-published",
    link_status: str = "feasible",
) -> OperationsEvidence:
    calendar_urls = calendar_urls or tuple(dict.fromkeys(parent_urls + inbound_urls))
    link_urls = link_urls or tuple(dict.fromkeys(parent_urls + inbound_urls))
    return OperationsEvidence(
        calendar_ref="content/content-calendar.md#post-2",
        calendar_status=calendar_status,
        calendar_urls=calendar_urls,
        published_parent_or_peer_urls=parent_urls,
        published_parent_or_peer_status=parent_status,
        inbound_source_urls=inbound_urls,
        inbound_source_status=inbound_status,
        link_feasibility_urls=link_urls,
        link_feasibility_ref="evidence://operations/link-map/2026-08-29",
        link_feasibility_status=link_status,
        checked_at="2026-08-29",
        owner="Operations",
    )


def reissue(candidate: Candidate, *, operations_evidence: Optional[OperationsEvidence] = None) -> Candidate:
    return replace(
        candidate,
        research=make_attestation("Research", candidate),
        seo=make_attestation("SEO", candidate),
        operations=make_attestation("Operations", candidate),
        operations_evidence=operations_evidence or make_operations(),
    )


def base_candidate() -> Candidate:
    candidate = Candidate(
        topic="Cara Buat Poster Guna ChatGPT",
        seed="Cara Buat Poster Guna ChatGPT",
        category_id="ai-tools",
        topic_family_id="ai-tools.chatgpt.poster",
        pillar_id="ai-tools",
        cluster_id="ai-tools.chatgpt",
        topic_intent_id="intent.chatgpt.poster.creation",
        subject_entity_ids=frozenset({"entity.chatgpt", "entity.poster"}),
        declared_seed_intent="chatgpt poster creation",
        reader_problem="make a clear ChatGPT poster",
        authenticity_basis="explicitly planned first-use test of the ChatGPT workflow",
        inventory_check="distinct from the Canva-specific published Post #5",
        existing_cluster_map="extends approved cluster ai-tools.chatgpt under published Post #2",
        mapped_pillar_id="ai-tools",
        mapped_cluster_id="ai-tools.chatgpt",
        published_parent_or_peer_url="https://digitrustlab.com/post-2",
        inbound_source_url="https://digitrustlab.com/post-2",
        incremental_value="ChatGPT poster workflow distinct from Canva-specific Post #5",
        anchor_context="descriptive ChatGPT poster-workflow anchor in Post #2 context",
        pivot_status="none",
        user_approval_ref="",
        research=None,
        seo=None,
        operations=None,
        operations_evidence=None,
    )
    return reissue(candidate)


def build_cases() -> dict[str, Candidate]:
    relevant = base_candidate()
    ranking_google = reissue(
        replace(
            relevant,
            topic="Notion template to check ranking google visibility",
            seed="ranking google",
            category_id="digital-skills",
            topic_family_id="digital-skills.notion.task-template",
            pillar_id="digital-skills",
            cluster_id="digital-skills.notion",
            topic_intent_id="intent.notion.daily.task.management",
            subject_entity_ids=frozenset({"entity.notion", "entity.task-template"}),
            declared_seed_intent="notion daily task management",
            reader_problem="check ranking google visibility from a Notion task template",
            inventory_check="distinct from existing productivity posts",
            existing_cluster_map="extends approved cluster ai-tools.chatgpt under published Post #2",
            mapped_pillar_id="ai-tools",
            mapped_cluster_id="ai-tools.chatgpt",
            incremental_value="Notion task template for ranking google visibility",
            anchor_context="check ranking google visibility link from Post #2",
            metrics_positive=True,
        )
    )
    adjacent = replace(
        relevant,
        topic="WordPress SEO audit checklist",
        seed="audit seo wordpress",
        category_id="digital-skills",
        topic_family_id="digital-skills.seo.wordpress-audit",
        pillar_id="digital-skills",
        cluster_id="digital-skills.seo",
        topic_intent_id="intent.wordpress.seo.audit",
        subject_entity_ids=frozenset({"entity.wordpress", "entity.seo-audit"}),
        declared_seed_intent="wordpress seo audit",
        reader_problem="audit WordPress SEO issues with a practical checklist",
        inventory_check="documented as an approved pivot for the SEO audit family",
        existing_cluster_map="extends approved cluster digital-skills.seo",
        mapped_pillar_id="digital-skills",
        mapped_cluster_id="digital-skills.seo",
        incremental_value="practical WordPress SEO audit steps",
        anchor_context="WordPress SEO audit checklist in the technical audit section",
        pivot_status="outside-family",
    )
    adjacent = reissue(adjacent)
    approved_pivot = reissue(
        replace(
            adjacent,
            pivot_status="approved",
            user_approval_ref=(
                "approval://user/2026-08-29/topic-family/"
                "digital-skills.seo.wordpress-audit"
            ),
        )
    )
    notion_pass = reissue(
        replace(
            relevant,
            topic="Notion task template for daily work",
            seed="Notion task template",
            category_id="digital-skills",
            topic_family_id="digital-skills.notion.task-template",
            pillar_id="digital-skills",
            cluster_id="digital-skills.notion",
            topic_intent_id="intent.notion.daily.task.management",
            subject_entity_ids=frozenset({"entity.notion", "entity.task-template"}),
            declared_seed_intent="notion daily task management",
            reader_problem="organise daily work with a Notion task template",
            inventory_check="distinct from existing productivity posts",
            existing_cluster_map="extends approved cluster digital-skills.notion",
            mapped_pillar_id="digital-skills",
            mapped_cluster_id="digital-skills.notion",
            incremental_value="a practical Notion task template for daily work",
            anchor_context="Notion task template anchor in the daily-work section",
        )
    )
    return {
        "relevant_pass": relevant,
        "metrics_positive_ranking_google_fail": ranking_google,
        "unapproved_adjacent_pivot_fail": adjacent,
        "explicitly_approved_pivot_pass": approved_pivot,
        "registered_notion_task_template_pass": notion_pass,
        "ai_poster_padded_with_notion_fail": replace(
            notion_pass,
            subject_entity_ids=frozenset(
                {"entity.notion", "entity.task-template", "entity.chatgpt", "entity.poster"}
            ),
        ),
        "wordpress_seo_padded_with_notion_fail": replace(
            notion_pass,
            subject_entity_ids=frozenset(
                {"entity.notion", "entity.task-template", "entity.wordpress", "entity.seo-audit"}
            ),
        ),
        "missing_research_attestation": replace(relevant, research=None),
        "stale_seo_attestation": replace(
            relevant, seo=make_attestation("SEO", relevant, checked_at="2026-07-01")
        ),
        "contradictory_operations_attestation": replace(
            relevant,
            operations=make_attestation("Operations", relevant, status="FAIL"),
        ),
        "operations_current_evidence_fail": replace(
            relevant,
            operations_evidence=make_operations(calendar_status="not-verified-current"),
        ),
        "operations_exact_canonical_match_pass": replace(
            relevant,
            published_parent_or_peer_url="https://DIGITRUSTLAB.COM/post-2/",
            inbound_source_url="https://digitrustlab.com/post-2#parent",
            operations_evidence=make_operations(),
        ),
        "operations_post20_mismatch_fail": replace(
            relevant,
            operations_evidence=make_operations(
                parent_urls=("https://digitrustlab.com/post-20",)
            ),
        ),
    }


def main() -> int:
    cases = build_cases()
    expected_pass = {
        "relevant_pass",
        "explicitly_approved_pivot_pass",
        "registered_notion_task_template_pass",
        "operations_exact_canonical_match_pass",
    }
    outcomes: dict[str, bool] = {}
    for name, candidate in cases.items():
        passed, failures = content_acceptance(candidate)
        outcomes[name] = passed
        if name in expected_pass:
            assert passed, (name, failures)
        else:
            assert not passed, (name, "unexpected pass")

    ranking = cases["metrics_positive_ranking_google_fail"]
    ranking_failures = relevance(ranking)[1]
    assert ranking.metrics_positive
    assert all(
        value
        for value in (
            ranking.topic,
            ranking.seed,
            ranking.reader_problem,
            ranking.authenticity_basis,
            ranking.inventory_check,
            ranking.existing_cluster_map,
            ranking.published_parent_or_peer_url,
            ranking.inbound_source_url,
            ranking.incremental_value,
            ranking.anchor_context,
            ranking.research,
            ranking.seo,
            ranking.operations,
            ranking.operations_evidence,
        )
    )
    for record in (ranking.research, ranking.seo, ranking.operations):
        assert record is not None
        assert record.decision == record.status == "PASS"
        assert date_is_fresh(record.checked_at)
        assert record.evidence_ref and record.owner
    assert ranking.operations_evidence is not None
    assert ranking.operations_evidence.calendar_status == "verified-current"
    assert ranking.operations_evidence.published_parent_or_peer_status == "verified-published"
    assert ranking.operations_evidence.inbound_source_status == "verified-published"
    assert ranking.operations_evidence.link_feasibility_status == "feasible"
    assert "declared seed intent" not in " ".join(ranking_failures)
    assert any("proposed topic semantic family contradiction" in f for f in ranking_failures)
    assert any("reader problem semantic family contradiction" in f for f in ranking_failures)
    assert any("cluster/link map" in f for f in ranking_failures)
    assert any("cluster ID does not match" in f for f in ranking_failures)
    assert any("anchor/context semantic family contradiction" in f for f in ranking_failures)
    assert "missing Operations independent current-evidence record" not in ranking_failures
    assert "Operations parent/peer URL evidence does not exactly match candidate URL" in relevance(
        cases["operations_post20_mismatch_fail"]
    )[1]

    print(
        "PASS editorial relevance fixtures: "
        f"{len(cases)} scenarios; "
        f"{sum(outcomes.values())} pass / {len(cases) - sum(outcomes.values())} fail; "
        "canonical URLs, structured entities/intents, Operations evidence, "
        "and metric-positive rejection verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
