import unittest

from cbc_range_checker import extract_reference_comparisons


class TestCBCReferenceComparisons(unittest.TestCase):

    def test_value_within_range(self):
        report = "Hemoglobin 14 g/dL 13.5-17.5 NORMAL"
        result = extract_reference_comparisons(report)
        self.assertIn("WITHIN the printed range", result)

    def test_value_below_range(self):
        report = "Hemoglobin 10 g/dL 13.5-17.5 LOW"
        result = extract_reference_comparisons(report)
        self.assertIn("BELOW the printed range", result)

    def test_value_above_range(self):
        report = "Hemoglobin 18 g/dL 13.5-17.5 HIGH"
        result = extract_reference_comparisons(report)
        self.assertIn("ABOVE the printed range", result)

    def test_conflicting_lab_status_is_flagged(self):
        report = "Hemoglobin 10 g/dL 13.5-17.5 NORMAL"
        result = extract_reference_comparisons(report)
        self.assertIn("WARNING", result)
        self.assertIn("conflicts with the numeric comparison", result)

    def test_unrecognized_report_does_not_invent_results(self):
        result = extract_reference_comparisons(
            "This document contains no recognizable CBC rows."
        )
        self.assertIn("No reliable CBC range comparisons", result)

    def test_multiple_results_are_extracted(self):
        report = (
            "Hemoglobin 14 g/dL 13.5-17.5 NORMAL\n"
            "Hematocrit 35.6 % 41-50 LOW"
        )
        result = extract_reference_comparisons(report)
        self.assertIn("Hemoglobin:", result)
        self.assertIn("Hematocrit:", result)
        self.assertIn("WITHIN the printed range", result)
        self.assertIn("BELOW the printed range", result)

    def test_inconsistent_differential_percentages_are_flagged(self):
        report = (
            "Neutrophils % 79 % 40-70 HIGH\n"
            "Lymphocytes % 43 % 20-45 NORMAL\n"
            "Monocytes % 6 % 2-10 NORMAL\n"
            "Eosinophils % 6 % 1-6 NORMAL\n"
            "Basophils % 1 % 0-1 NORMAL"
        )

        result = extract_reference_comparisons(report)

        self.assertIn("total 135%", result)
        self.assertIn("verify the original report", result)
        self.assertIn("values have not been corrected", result)

    def test_partial_differential_does_not_trigger_sum_warning(self):
        report = (
            "Neutrophils % 60 % 40-70 NORMAL\n"
            "Lymphocytes % 30 % 20-45 NORMAL"
        )

        result = extract_reference_comparisons(report)

        self.assertNotIn("Differential percentage consistency", result)
if __name__ == "__main__":
    unittest.main()
