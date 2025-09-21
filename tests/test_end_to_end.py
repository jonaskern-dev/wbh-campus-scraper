"""
End-to-end test for HTML to JSON conversion.

This test verifies that the complete pipeline from HTML input to JSON output
works correctly and produces the expected data structure.
"""

import json
import unittest
import tempfile
from pathlib import Path

from scraper import WBHScraper


class TestEndToEnd(unittest.TestCase):
    """Test the complete HTML to JSON conversion pipeline."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.html_file = cls.fixtures_dir / "curriculum_informatik.html"
        cls.expected_json = cls.fixtures_dir / "expected_output_informatik.json"

    def test_html_to_json_conversion(self):
        """Test that HTML is correctly converted to expected JSON structure."""
        # Initialize scraper with HTML file
        scraper = WBHScraper(self.html_file)

        # Transform to structured data
        study_program = scraper.transform()

        # Convert to JSON dict
        actual_output = study_program.to_dict()

        # Load expected output
        with open(self.expected_json, 'r', encoding='utf-8') as f:
            expected_output = json.load(f)

        # Deep comparison of the complete structure
        self._compare_json_structure(actual_output, expected_output)

    def test_save_and_load_json(self):
        """Test that saved JSON file matches expected output."""
        scraper = WBHScraper(self.html_file)

        # Transform to structured data
        study_program = scraper.transform()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            # Save extracted data
            scraper.save_to_file(tmp_path)

            # Load saved file
            with open(tmp_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)

            # Load expected data
            with open(self.expected_json, 'r', encoding='utf-8') as f:
                expected_data = json.load(f)

            # Compare complete structure
            self._compare_json_structure(saved_data, expected_data)

        finally:
            # Clean up temp file
            if tmp_path.exists():
                tmp_path.unlink()

    def _compare_json_structure(self, actual, expected):
        """Deep comparison of JSON structures."""

        # 1. Compare study_program
        self.assertEqual(
            actual["study_program"],
            expected["study_program"],
            "Study program data doesn't match"
        )

        # 2. Compare all modules
        self.assertEqual(
            set(actual["modules"].keys()),
            set(expected["modules"].keys()),
            "Module IDs don't match"
        )

        for module_id in expected["modules"]:
            actual_module = actual["modules"][module_id]
            expected_module = expected["modules"][module_id]

            # Compare each module field
            self.assertEqual(
                actual_module["id"],
                expected_module["id"],
                f"Module {module_id}: ID mismatch"
            )
            self.assertEqual(
                actual_module["name"],
                expected_module["name"],
                f"Module {module_id}: Name mismatch"
            )
            self.assertEqual(
                actual_module.get("credit_points"),
                expected_module.get("credit_points"),
                f"Module {module_id}: Credit points mismatch"
            )

            # Compare element lists
            self.assertEqual(
                set(actual_module.get("element_ids", [])),
                set(expected_module.get("element_ids", [])),
                f"Module {module_id}: Element IDs mismatch"
            )
            self.assertEqual(
                set(actual_module.get("exam_ids", [])),
                set(expected_module.get("exam_ids", [])),
                f"Module {module_id}: Exam IDs mismatch"
            )

        # 3. Compare all elements
        self.assertEqual(
            len(actual["elements"]),
            len(expected["elements"]),
            "Number of elements doesn't match"
        )

        # Create lookup dictionaries by element ID
        actual_elements = {e["id"]: e for e in actual["elements"]}
        expected_elements = {e["id"]: e for e in expected["elements"]}

        self.assertEqual(
            set(actual_elements.keys()),
            set(expected_elements.keys()),
            "Element IDs don't match"
        )

        # Compare each element
        for elem_id in expected_elements:
            actual_elem = actual_elements[elem_id]
            expected_elem = expected_elements[elem_id]

            # Core fields that must match exactly
            self.assertEqual(
                actual_elem["code"],
                expected_elem["code"],
                f"Element {elem_id}: Code mismatch"
            )
            self.assertEqual(
                actual_elem["name"],
                expected_elem["name"],
                f"Element {elem_id}: Name mismatch"
            )
            self.assertEqual(
                actual_elem["type"],
                expected_elem["type"],
                f"Element {elem_id}: Type mismatch"
            )
            self.assertEqual(
                actual_elem.get("semester"),
                expected_elem.get("semester"),
                f"Element {elem_id}: Semester mismatch"
            )
            self.assertEqual(
                actual_elem.get("credit_points"),
                expected_elem.get("credit_points"),
                f"Element {elem_id}: Credit points mismatch"
            )
            self.assertEqual(
                actual_elem.get("module_id"),
                expected_elem.get("module_id"),
                f"Element {elem_id}: Module ID mismatch"
            )

            # Compare document count (not full structure for simplicity)
            if "documents" in expected_elem:
                self.assertEqual(
                    len(actual_elem.get("documents", [])),
                    len(expected_elem["documents"]),
                    f"Element {elem_id}: Document count mismatch"
                )

    def test_statistics_match_json_output(self):
        """Test that statistics are consistent with actual JSON output."""
        scraper = WBHScraper(self.html_file)

        # Transform data
        study_program = scraper.transform()

        # Calculate statistics manually
        stats = {
            'total_modules': len(study_program.modules),
            'total_elements': len(study_program.elements),
            'total_documents': sum(len(e.documents) for e in study_program.elements)
        }

        # Convert to dict for verification
        output = study_program.to_dict()

        # Verify statistics match actual data
        self.assertEqual(
            stats["total_modules"],
            len(output["modules"]),
            "Module count in statistics doesn't match actual data"
        )

        self.assertEqual(
            stats["total_elements"],
            len(output["elements"]),
            "Element count in statistics doesn't match actual data"
        )

        # Calculate actual totals from output
        actual_exams = sum(1 for e in output["elements"] if e["type"] == "exam")
        actual_learning = sum(1 for e in output["elements"] if e["type"] == "learning_module")
        actual_seminars = sum(1 for e in output["elements"] if e["type"] == "seminar")

        # Verify counts match
        total_by_type = actual_exams + actual_learning + actual_seminars
        self.assertEqual(stats["total_elements"], total_by_type)


if __name__ == '__main__':
    unittest.main()