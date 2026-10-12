import ast
import unittest
from pathlib import Path


def load_sanitizer():
    source = Path("api.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(source)

    function_node = next(
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "sanitize_report_explanation"
    )

    isolated_module = ast.Module(
        body=[function_node],
        type_ignores=[],
    )
    namespace = {}
    exec(compile(isolated_module, "api.py", "exec"), namespace)
    return namespace["sanitize_report_explanation"]


sanitize_report_explanation = load_sanitizer()


class TestReportSanitizer(unittest.TestCase):

    def test_thalassemia_claim_is_replaced(self):
        result = sanitize_report_explanation(
            "- High MCHC could indicate thalassemia."
        )
        self.assertNotIn("thalassemia", result.lower())
        self.assertIn("do not establish a diagnosis", result.lower())

    def test_iron_deficiency_claim_is_replaced(self):
        result = sanitize_report_explanation(
            "- This may suggest iron deficiency."
        )
        self.assertNotIn("iron deficiency", result.lower())

    def test_inflammatory_claim_is_cautioned(self):
        result = sanitize_report_explanation(
            "- High neutrophils suggest a possible inflammatory response."
        )
        self.assertIn("does not establish infection or", result.lower())

    def test_elevated_hemoglobin_claim_is_flagged(self):
        result = sanitize_report_explanation(
            "- Hemoglobin levels are elevated."
        )
        self.assertIn("verify the original report", result.lower())

    def test_duplicate_sanitized_lines_are_removed(self):
        result = sanitize_report_explanation(
            "- This may suggest iron deficiency.\n"
            "- This may suggest iron deficiency."
        )
        self.assertEqual(result.count("do not establish a diagnosis"), 1)

    def test_safe_plain_language_is_preserved(self):
        text = "- The platelet count is within the printed range."
        self.assertEqual(sanitize_report_explanation(text), text)


if __name__ == "__main__":
    unittest.main()