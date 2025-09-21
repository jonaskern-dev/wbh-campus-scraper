"""
Integration tests for WBH Campus Scraper.

Tests the complete extraction pipeline using real HTML data from multiple
study programs and validates against expected JSON output.
"""

import json
import unittest
from pathlib import Path

from scraper import WBHScraper


class TestIntegrationInformatik(unittest.TestCase):
    """Integration tests using Informatik curriculum.html data."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.html_file = cls.fixtures_dir / "curriculum_informatik.html"
        cls.expected_json = cls.fixtures_dir / "expected_output_informatik.json"

        # Load expected output
        with open(cls.expected_json, 'r', encoding='utf-8') as f:
            cls.expected_data = json.load(f)

    def setUp(self):
        """Set up each test."""
        self.scraper = WBHScraper(debug=False)

    def test_complete_extraction(self):
        """Test complete extraction from curriculum_informatik.html."""
        # Extract data
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Basic assertions
        self.assertIsNotNone(study_program)
        self.assertEqual(study_program.study_program.id, 46566)
        self.assertEqual(study_program.study_program.number, "1110")
        self.assertEqual(study_program.study_program.name, "Informatik (Bachelor)")

    def test_module_count(self):
        """Test that all modules are extracted correctly."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Should have 25 modules
        self.assertEqual(len(study_program.modules), 25)

        # Check specific module
        self.assertIn("786", study_program.modules)
        module_786 = study_program.modules["786"]
        self.assertEqual(module_786.name, "Mathematische Grundlagen für Informatiker")
        self.assertEqual(module_786.credit_points, 8.0)

    def test_element_count_and_types(self):
        """Test that all elements are extracted with correct types."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Should have 135 elements total
        self.assertEqual(len(study_program.elements), 135)

        # Count by type
        exams = [e for e in study_program.elements if e.is_exam]
        learning_modules = [e for e in study_program.elements if e.type == "learning_module"]
        seminars = [e for e in study_program.elements if e.type == "seminar"]

        self.assertEqual(len(exams), 27)
        self.assertEqual(len(learning_modules), 99)
        self.assertEqual(len(seminars), 9)

    def test_credit_points_extraction(self):
        """Test that credit points are extracted when available."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Check that some elements have CP and some don't
        elements_with_cp = [e for e in study_program.elements if e.credit_points is not None]
        elements_without_cp = [e for e in study_program.elements if e.credit_points is None]

        self.assertGreater(len(elements_with_cp), 0, "Should have elements with credit points")
        self.assertGreater(len(elements_without_cp), 0, "Should have elements without credit points")

    def test_semester_assignment(self):
        """Test that elements have semester assignments."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Check semester distribution
        semester_counts = {}
        for element in study_program.elements:
            sem = element.semester
            semester_counts[sem] = semester_counts.get(sem, 0) + 1

        # Should have elements in multiple semesters
        self.assertGreater(len(semester_counts), 1, "Should have elements in multiple semesters")

        # Check specific known distribution
        self.assertEqual(semester_counts.get(0, 0), 5, "Should have 5 unassigned elements")
        self.assertEqual(semester_counts.get(1, 0), 32, "Should have 32 elements in semester 1")

    def test_document_extraction(self):
        """Test that documents are extracted correctly."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Count elements with documents
        elements_with_docs = [e for e in study_program.elements if e.documents]
        self.assertEqual(len(elements_with_docs), 71)

        # Count total documents
        total_docs = sum(len(e.documents) for e in study_program.elements)
        self.assertEqual(total_docs, 215)

    def test_json_serialization(self):
        """Test that the output can be serialized to JSON."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Convert to dict
        data_dict = study_program.to_dict()

        # Should be serializable
        json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
        self.assertIsNotNone(json_str)

        # Parse it back
        parsed = json.loads(json_str)
        self.assertEqual(parsed["study_program"]["id"], 46566)

    def test_output_structure_matches_expected(self):
        """Test that output structure matches expected data.json."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()
        output_dict = study_program.to_dict()

        # Check main structure
        self.assertIn("study_program", output_dict)
        self.assertIn("modules", output_dict)
        self.assertIn("elements", output_dict)

        # Check study program data
        self.assertEqual(
            output_dict["study_program"],
            self.expected_data["study_program"]
        )

        # Check module count
        self.assertEqual(
            len(output_dict["modules"]),
            len(self.expected_data["modules"])
        )

        # Check element count
        self.assertEqual(
            len(output_dict["elements"]),
            len(self.expected_data["elements"])
        )

        # Deep check: verify first element has all expected fields
        if output_dict["elements"]:
            first_element = output_dict["elements"][0]
            expected_first = self.expected_data["elements"][0]

            # Check all keys are present
            for key in expected_first.keys():
                self.assertIn(key, first_element, f"Missing key '{key}' in element")

            # Verify mark_and_points field exists
            self.assertIn("mark_and_points", first_element, "mark_and_points field missing")

    def test_mark_and_points_extraction(self):
        """Test that mark_and_points data is extracted correctly."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Find elements with grades
        elements_with_grades = [
            e for e in study_program.elements
            if e.mark_and_points and e.mark_and_points.mark
        ]

        # Should have at least some graded elements
        self.assertGreater(len(elements_with_grades), 0, "Should have graded elements")

        # Check structure of mark_and_points
        for element in elements_with_grades[:1]:  # Check first graded element
            mp = element.mark_and_points
            self.assertIsNotNone(mp.mark)
            self.assertIsNotNone(mp.mark_label)
            # Dates might be None, but if present should be strings
            if mp.esa_send_date:
                self.assertIsInstance(mp.esa_send_date, str)
            if mp.esa_grade_date:
                self.assertIsInstance(mp.esa_grade_date, str)

    def test_specific_elements(self):
        """Test specific important elements."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Find thesis element
        thesis = next(
            (e for e in study_program.elements if e.code == "Thesis"),
            None
        )
        self.assertIsNotNone(thesis, "Should find Thesis element")
        # Note: Thesis might not have credit_points in the current data

        # Find first semester programming course
        prog_course = next(
            (e for e in study_program.elements
             if e.code == "B-GOPB01XX" and e.semester == 1),
            None
        )
        self.assertIsNotNone(prog_course, "Should find B-GOPB01XX in semester 1")


class TestIntegrationMaschinenbau(unittest.TestCase):
    """Integration tests for Maschinenbau-Informatik study program."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.html_file = cls.fixtures_dir / "curriculum_maschinenbau_informatik.html"
        cls.expected_json = cls.fixtures_dir / "expected_output_maschinenbau_informatik.json"

        # Load expected output
        with open(cls.expected_json, 'r', encoding='utf-8') as f:
            cls.expected_data = json.load(f)

    def setUp(self):
        """Set up each test."""
        self.scraper = WBHScraper(debug=False)

    def test_complete_extraction(self):
        """Test complete extraction from curriculum_maschinenbau_informatik.html."""
        # Extract data
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Basic assertions
        self.assertIsNotNone(study_program)
        self.assertEqual(study_program.study_program.id, 26397)
        self.assertEqual(study_program.study_program.number, "1320")
        self.assertEqual(study_program.study_program.name, "Maschinenbau-Informatik")

    def test_module_count(self):
        """Test that all modules are extracted correctly."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Should have 29 modules
        self.assertEqual(len(study_program.modules), 29)

    def test_element_count_and_types(self):
        """Test that all elements are extracted with correct types."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Should have 153 elements total
        self.assertEqual(len(study_program.elements), 153)

        # Count by type
        exams = [e for e in study_program.elements if e.is_exam]
        learning_modules = [e for e in study_program.elements if e.type == "learning_module"]
        seminars = [e for e in study_program.elements if e.type == "seminar"]

        self.assertEqual(len(exams), 44)
        self.assertEqual(len(learning_modules), 97)
        self.assertEqual(len(seminars), 12)

    def test_credit_points_extraction(self):
        """Test that credit points are extracted when available."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Check that some elements have CP and some don't
        elements_with_cp = [e for e in study_program.elements if e.credit_points is not None]
        elements_without_cp = [e for e in study_program.elements if e.credit_points is None]

        self.assertGreater(len(elements_with_cp), 0, "Should have elements with credit points")
        self.assertGreater(len(elements_without_cp), 0, "Should have elements without credit points")

    def test_document_extraction(self):
        """Test that documents are extracted correctly."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Count elements with documents
        elements_with_docs = [e for e in study_program.elements if e.documents]
        self.assertEqual(len(elements_with_docs), 87)

        # Count total documents
        total_docs = sum(len(e.documents) for e in study_program.elements)
        self.assertEqual(total_docs, 220)

    def test_json_serialization(self):
        """Test that the output can be serialized to JSON."""
        self.scraper.file_path = self.html_file
        study_program = self.scraper.transform()

        # Convert to dict
        data_dict = study_program.to_dict()

        # Should be serializable
        json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
        self.assertIsNotNone(json_str)

        # Parse it back
        parsed = json.loads(json_str)
        self.assertEqual(parsed["study_program"]["id"], 26397)


class TestIntegrationAllPrograms(unittest.TestCase):
    """Test that all study programs can be parsed."""

    def test_all_html_files_parseable(self):
        """Test that all HTML fixtures can be parsed without errors."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        html_files = [
            "curriculum_informatik.html",
            "curriculum_maschinenbau_informatik.html",
            "curriculum_maschinenbau.html"
        ]

        for html_file in html_files:
            file_path = fixtures_dir / html_file
            if file_path.exists():
                with self.subTest(file=html_file):
                    scraper = WBHScraper(file_path)
                    study_program = scraper.transform()

                    # Basic checks
                    self.assertIsNotNone(study_program)
                    self.assertIsNotNone(study_program.study_program.name)
                    self.assertIsNotNone(study_program.study_program.number)
                    self.assertGreater(len(study_program.elements), 0)
                    self.assertGreater(len(study_program.modules), 0)


if __name__ == '__main__':
    unittest.main()