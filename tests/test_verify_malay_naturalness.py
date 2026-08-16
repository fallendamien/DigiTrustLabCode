import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-malay-naturalness.py"
SPEC = importlib.util.spec_from_file_location("verify_malay_naturalness", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


CHECKS = {name: True for name in MODULE.REQUIRED_CHECKS}


def make_review(document, claude_family="anthropic", openai_family="openai", confidence="high", findings=None):
    reviewers = [
        {"id": "claude", "model_family": claude_family, "model": "sonnet"},
        {"id": "openai", "model_family": openai_family, "model": "gpt-5"},
    ]
    evaluation = lambda: {"checks": dict(CHECKS), "confidence": confidence, "findings": findings or []}
    return {
        "schema_version": 2,
        "post_id": 559,
        "slug": "fixture",
        "reviewed_at": "2026-08-08T00:00:00Z",
        "content_hash": document["content_hash"],
        "status": "pass",
        "reviewers": reviewers,
        "document_review": {"claude": evaluation(), "openai": evaluation()},
        "segments": [
            {
                "id": segment["id"],
                "hash": segment["hash"],
                "reviewers": {"claude": evaluation(), "openai": evaluation()},
            }
            for segment in document["segments"]
        ],
        "disagreements": [],
        "human_resolutions": [],
    }


class NaturalnessGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = MODULE.load_rules(ROOT / "content" / "malay-naturalness-rules.json")

    def document(self, html):
        return MODULE.build_document(html, title="Tajuk bersih")

    def test_clean_article_with_claude_and_openai_reviews_passes(self):
        document = self.document("<p>AI boleh membantu anda memahami tugasan ini.</p><img alt='Ilustrasi AI yang jelas'>")
        result = MODULE.evaluate(document, make_review(document), self.rules)
        self.assertTrue(result["passed"], result["issues"])

    def test_confirmed_alasan_sopan_regression_is_blocked(self):
        document = self.document("<p>Jawapan itu bukan sekadar alasan sopan.</p>")
        result = MODULE.evaluate(document, make_review(document), self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "rejected-phrase" for item in result["issues"]))

    def test_non_required_reviewer_family_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        result = MODULE.evaluate(document, make_review(document, openai_family="Gemini"), self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "reviewer-family" for item in result["issues"]))

    def test_two_claude_reviews_without_openai_are_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document, openai_family="anthropic")
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "reviewer-coverage" for item in result["issues"]))

    def test_more_than_two_reviewers_are_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["reviewers"].append({"id": "third", "model_family": "openai", "model": "gpt-5"})
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "reviewer-count" for item in result["issues"]))

    def test_missing_reviewer_model_identity_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["reviewers"][1]["model"] = ""
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "reviewer-identity" for item in result["issues"]))

    def test_missing_segment_coverage_is_blocked(self):
        document = self.document("<p>Ayat pertama jelas.</p><p>Ayat kedua juga jelas.</p>")
        review = make_review(document)
        review["segments"].pop()
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "segment-missing" for item in result["issues"]))

    def test_extra_segment_evidence_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["segments"].append(
            {
                "id": "seg-999",
                "hash": "unused",
                "reviewers": {},
            }
        )
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "segment-extra" for item in result["issues"]))

    def test_failed_binary_check_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["document_review"]["openai"]["checks"]["natural_usage"] = False
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "check-failed" for item in result["issues"]))

    def test_content_edit_invalidates_hash(self):
        original = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(original)
        edited = self.document("<p>Ayat ini sangat jelas dan semula jadi.</p>")
        result = MODULE.evaluate(edited, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "content-hash" for item in result["issues"]))

    def test_live_review_is_bound_to_exact_published_post(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        result = MODULE.evaluate(
            document,
            review,
            self.rules,
            expected_post_id=560,
            expected_slug="different-post",
            source_status="draft",
            require_published=True,
        )
        codes = {item["code"] for item in result["issues"]}
        self.assertFalse(result["passed"])
        self.assertTrue({"post-id", "post-slug", "post-status"}.issubset(codes))

    def test_unresolved_disagreement_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["disagreements"] = [{"segment_id": "seg-001", "detail": "Different wording"}]
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "disagreement-unresolved" for item in result["issues"]))

    def test_low_confidence_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document, confidence="medium")
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "confidence-not-high" for item in result["issues"]))

    def test_reviewer_finding_requires_rerun_after_correction(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document, findings=[{"phrase": "awkward"}])
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])

        rerun = make_review(document)
        rerun_result = MODULE.evaluate(document, rerun, self.rules)
        self.assertTrue(rerun_result["passed"], rerun_result["issues"])

    def test_alt_text_and_metadata_are_segmented(self):
        document = MODULE.build_document(
            "<meta name='description' content='Penerangan yang jelas'><p>Ayat yang jelas.</p><img alt='Ilustrasi yang jelas'>"
        )
        kinds = [segment["kind"] for segment in document["segments"]]
        self.assertIn("metadata", kinds)
        self.assertIn("alt", kinds)

    def test_final_package_file_can_match_live_title_excerpt_and_metadata(self):
        file_document = MODULE.build_document(
            "<title>Tajuk bersih</title>"
            "<p>Ayat yang jelas.</p>"
            "<p data-naturalness-kind='excerpt'>Ringkasan yang jelas.</p>"
            "<meta name='rank_math_title' content='Tajuk SEO yang jelas'>"
        )
        live_document = MODULE.build_document(
            "<p>Ayat yang jelas.</p>",
            title="Tajuk bersih",
            excerpt="Ringkasan yang jelas.",
            metadata={"rank_math_title": "Tajuk SEO yang jelas"},
        )
        self.assertEqual(file_document["content_hash"], live_document["content_hash"])
        self.assertEqual(file_document["segments"], live_document["segments"])

    def test_rendered_rest_excerpt_wrapper_matches_plain_manual_excerpt(self):
        self.assertEqual(
            MODULE.normalize_rendered_excerpt("<p>Ringkasan yang jelas.</p>\n"),
            "Ringkasan yang jelas.",
        )

    def test_missing_review_artifact_is_blocked(self):
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        result = MODULE.evaluate(document, None, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "review-missing" for item in result["issues"]))

    def test_cli_exit_codes_distinguish_failure_from_configuration_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            article = temp_path / "article.html"
            article.write_text("<p>Ayat ini jelas dan semula jadi.</p>", encoding="utf-8")
            invalid_review = temp_path / "review.json"
            invalid_review.write_text("{}", encoding="utf-8")

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                content_failure = MODULE.main(
                    ["--file", str(article), "--review", str(invalid_review)]
                )
                configuration_failure = MODULE.main(
                    ["--file", str(temp_path / "missing.html"), "--review", str(invalid_review)]
                )

            self.assertEqual(1, content_failure)
            self.assertEqual(2, configuration_failure)

    def test_struktur_jelas_rejected_phrase_is_blocked(self):
        """Regression: post 605 excerpt phrase caught by Zamri 2026-08-16, missed by both AI reviewers."""
        document = self.document("<p>Contoh minit mesyuarat yang kemas bermula dengan struktur jelas.</p>")
        result = MODULE.evaluate(document, make_review(document), self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "rejected-phrase" for item in result["issues"]))

    def test_grammatical_completeness_required_for_schema_v3(self):
        """schema_version 3 reviews must include grammatical_completeness; omitting it blocks publication."""
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)
        review["schema_version"] = 3
        # Simulate a reviewer that forgot the new check
        for reviewer_id in ("claude", "openai"):
            review["document_review"][reviewer_id]["checks"].pop("grammatical_completeness", None)
            for seg in review["segments"]:
                seg["reviewers"][reviewer_id]["checks"].pop("grammatical_completeness", None)
        result = MODULE.evaluate(document, review, self.rules)
        self.assertFalse(result["passed"])
        self.assertTrue(any(item["code"] == "checks-incomplete" for item in result["issues"]))

    def test_v2_artifact_does_not_require_grammatical_completeness(self):
        """Existing schema_version 2 artifacts remain valid without grammatical_completeness."""
        document = self.document("<p>Ayat ini jelas dan semula jadi.</p>")
        review = make_review(document)  # schema_version 2
        # Strip grammatical_completeness to simulate a real pre-v3 artifact
        for reviewer_id in ("claude", "openai"):
            review["document_review"][reviewer_id]["checks"].pop("grammatical_completeness", None)
            for seg in review["segments"]:
                seg["reviewers"][reviewer_id]["checks"].pop("grammatical_completeness", None)
        result = MODULE.evaluate(document, review, self.rules)
        self.assertTrue(result["passed"], result["issues"])

    def test_existing_mechanical_checker_remains_available(self):
        old_script = ROOT / "scripts" / "verify-malay-voice.py"
        spec = importlib.util.spec_from_file_location("verify_malay_voice", old_script)
        old = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(old)
        findings = old.scan(999, "fixture", "<p>AI boleh membantu anda dengan tugas ini.</p>")
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
