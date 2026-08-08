import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-links.py"
SPEC = importlib.util.spec_from_file_location("verify_links", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class LinkGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = MODULE.load_policy(ROOT / "content" / "link-policy.json")

    def check(self, html, source_url=""):
        return MODULE.validate_links(html, self.policy, source_url=source_url)

    def test_clean_editorial_links_pass(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> dan '
            '<a href="https://modelcontextprotocol.io/specification/2025-03-26/index" rel="noopener">spesifikasi rasmi MCP</a></p>',
            "https://digitrustlab.com/mcp/",
        )
        self.assertTrue(result["passed"], result["issues"])
        self.assertEqual(1, result["counts"]["internal"])
        self.assertEqual(1, result["counts"]["external_dofollow"])

    def test_generic_anchor_is_blocked(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">di sini</a> '
            '<a href="https://example.com">rujukan rasmi</a></p>'
        )
        self.assertFalse(result["passed"])
        self.assertTrue(any(issue["code"] == "generic-anchor" for issue in result["issues"]))

    def test_sponsored_external_is_blocked(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> '
            '<a href="https://example.com" rel="sponsored">rujukan rasmi</a></p>'
        )
        self.assertFalse(result["passed"])
        self.assertTrue(any(issue["code"] == "editorial-rel" for issue in result["issues"]))

    def test_nofollow_external_is_allowed_when_dofollow_exists(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> '
            '<a href="https://example.com" rel="nofollow">rujukan rasmi</a> '
            '<a href="https://example.org">rujukan kedua</a></p>'
        )
        self.assertTrue(result["passed"], result["issues"])

    def test_insecure_external_is_blocked(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> '
            '<a href="http://example.com">rujukan rasmi</a></p>'
        )
        self.assertFalse(result["passed"])
        self.assertTrue(any(issue["code"] == "https-required" for issue in result["issues"]))

    def test_toc_fragments_are_excluded_from_editorial_counts(self):
        result = self.check(
            '<nav><a href="#pengenalan">Pengenalan</a>'
            '<a href="https://digitrustlab.com/mcp/#Kesimpulan">Kesimpulan</a></nav>'
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> '
            '<a href="https://example.com">rujukan rasmi</a></p>',
            "https://digitrustlab.com/mcp/",
        )
        self.assertTrue(result["passed"], result["issues"])
        self.assertEqual(2, result["counts"]["fragments_excluded"])

    def test_missing_outbound_classes_is_blocked(self):
        result = self.check('<p>Artikel tanpa pautan.</p>')
        self.assertFalse(result["passed"])
        codes = {issue["code"] for issue in result["issues"]}
        self.assertIn("internal-links-missing", codes)
        self.assertIn("external-links-missing", codes)

    def test_self_link_is_blocked(self):
        result = self.check(
            '<p><a href="/mcp/">penerangan MCP</a> '
            '<a href="https://example.com">rujukan rasmi</a></p>',
            "https://digitrustlab.com/mcp/",
        )
        self.assertFalse(result["passed"])
        self.assertTrue(any(issue["code"] == "self-link" for issue in result["issues"]))

    def test_inbound_review_requires_current_hash_and_reason(self):
        result = self.check(
            '<p><a href="/apa-itu-ai/">pengenalan AI</a> '
            '<a href="https://example.com">rujukan rasmi</a></p>',
            "https://digitrustlab.com/mcp/",
        )
        post = {"id": 559, "slug": "mcp", "link": "https://digitrustlab.com/mcp/"}
        review = {
            "schema_version": 1,
            "post_id": 559,
            "slug": "mcp",
            "link_hash": result["link_hash"],
            "inbound": {"decision": "no_safe_context", "source_ids": [], "reason": "No safe contextual source exists yet."},
        }
        issues = MODULE.validate_inbound_review(review, post=post, link_result=result, sources=[])
        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
