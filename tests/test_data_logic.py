"""Small automated checks for the sample data and rule-based logic."""
import unittest
from pathlib import Path

from data_logic import find_plot_records, get_unique_plot_ids, get_warnings, load_records


class JomiCheckLiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_records(Path(__file__).resolve().parents[1] / "data" / "plots.json")

    def test_has_at_least_20_records_and_20_unique_plots(self):
        self.assertGreaterEqual(len(self.records), 20)
        self.assertGreaterEqual(len(get_unique_plot_ids(self.records)), 20)

    def test_clean_scenario_has_no_flags(self):
        found = find_plot_records(self.records, "P-1001")
        self.assertTrue(found)
        self.assertEqual(get_warnings(found), [])

    def test_pending_mutation_scenario_is_flagged(self):
        found = find_plot_records(self.records, "P-1002")
        warnings = get_warnings(found)
        self.assertTrue(any(item["code"] == "mutation_not_completed" for item in warnings))

    def test_conflicting_active_deeds_scenario_is_flagged(self):
        found = find_plot_records(self.records, "P-1018")
        warnings = get_warnings(found)
        self.assertGreaterEqual(len(found), 2)
        self.assertTrue(any(item["code"] == "active_deed_conflict" for item in warnings))

    def test_search_by_deed_id(self):
        found = find_plot_records(self.records, "d-2026-1001")
        self.assertTrue(found)
        self.assertEqual(found[0]["plot_id"], "P-1001")

    def test_unknown_id_returns_empty_list(self):
        self.assertEqual(find_plot_records(self.records, "P-9999"), [])

    def test_case_and_acquisition_flags_are_explained(self):
        case_record = find_plot_records(self.records, "P-1003")
        acquisition_record = find_plot_records(self.records, "P-1004")
        self.assertTrue(any(item["code"] == "pending_case" for item in get_warnings(case_record)))
        self.assertTrue(any(item["code"] == "acquisition_flag" for item in get_warnings(acquisition_record)))


if __name__ == "__main__":
    unittest.main()
