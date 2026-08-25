import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify-post-structure.py"
SPEC = importlib.util.spec_from_file_location("verify_post_structure", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PostStructureGateTests(unittest.TestCase):
    def test_template_title_duplicate_is_blocked(self):
        result = MODULE.check_html(
            "<h1>Cara Buat Nota Cantik dengan AI</h1><p>Isi artikel.</p>",
            title="Cara Buat Nota Cantik dengan AI",
            source="fixture",
        )
        self.assertFalse(result["passed"])
        self.assertEqual("duplicate-template-title", result["issues"][0]["code"])

    def test_any_body_h1_is_blocked_even_when_title_differs(self):
        result = MODULE.check_html(
            "<h1>Tajuk lain</h1><p>Isi artikel.</p>",
            title="Tajuk sebenar",
            source="fixture",
        )
        self.assertFalse(result["passed"])
        self.assertEqual("body-h1-present", result["issues"][0]["code"])

    def test_clean_body_with_h2_passes(self):
        result = MODULE.check_html(
            "<p>Pengenalan.</p><h2>Bahagian pertama</h2><p>Isi artikel.</p>",
            title="Tajuk halaman",
            source="fixture",
        )
        self.assertTrue(result["passed"], result["issues"])
        self.assertEqual(0, result["body_h1_count"])


if __name__ == "__main__":
    unittest.main()
