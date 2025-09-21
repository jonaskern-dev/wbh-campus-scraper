"""
Tests for data models.

Focus on testing the data structure and JSON serialization.
"""

import unittest
import json
from scraper.models import (
    StudyProgram, StudyProgramInfo, StudyProgramBuilder,
    Module, Element, Document, ExamInfo, SubElement
)


class TestDataModels(unittest.TestCase):
    """Test the data models and JSON structure."""

    def test_study_program_info(self):
        """Test StudyProgramInfo model."""
        info = StudyProgramInfo(
            id=46566,
            number="1110",
            name="Informatik (Bachelor)"
        )
        self.assertEqual(info.id, 46566)
        self.assertEqual(info.number, "1110")
        self.assertEqual(info.name, "Informatik (Bachelor)")

    def test_module_structure(self):
        """Test Module data structure."""
        module = Module(
            id=786,
            name="Mathematische Grundlagen für Informatiker",
            code="MATH01",
            credit_points=8.0,
            element_ids=[1, 2, 3],
            exam_ids=[3],
            study_material_ids=[1, 2]
        )
        self.assertEqual(module.id, 786)
        self.assertEqual(module.credit_points, 8.0)
        self.assertEqual(len(module.element_ids), 3)
        self.assertEqual(len(module.exam_ids), 1)

    def test_element_structure(self):
        """Test Element data structure."""
        element = Element(
            id=783,
            code="B-INF01XX",
            name="Einführungsprojekt für Informatiker",
            type="exam",
            semester=1,
            credit_points=2.0
        )
        self.assertEqual(element.id, 783)
        self.assertEqual(element.type, "exam")
        self.assertTrue(element.is_exam)
        self.assertEqual(element.credit_points, 2.0)

    def test_element_with_exam_info(self):
        """Test Element with ExamInfo."""
        exam_info = ExamInfo(
            exam_form="Klausur",
            prerequisites="Keine",
            allowed_aids="Taschenrechner",
            core_topics="Grundlagen der Informatik"
        )
        element = Element(
            id=100,
            code="TEST",
            name="Test Exam",
            type="exam",
            exam_info=exam_info
        )
        self.assertIsNotNone(element.exam_info)
        self.assertEqual(element.exam_info.exam_form, "Klausur")

    def test_document_structure(self):
        """Test Document data structure."""
        doc = Document(
            filename="test.pdf",
            content_type="pdf",
            size="1.5 MB",
            url="/download/test.pdf"
        )
        self.assertEqual(doc.filename, "test.pdf")
        self.assertEqual(doc.content_type, "pdf")
        self.assertEqual(doc.size, "1.5 MB")

    def test_study_program_builder(self):
        """Test StudyProgramBuilder functionality."""
        builder = StudyProgramBuilder(
            id=46566,
            number="1110",
            name="Informatik (Bachelor)"
        )

        # Add a module
        module = Module(id=1, name="Test Module", credit_points=6.0)
        builder.add_module(module)

        # Add an element
        element = Element(id=1, code="TEST", name="Test", type="exam")
        builder.add_element(element)

        # Build the program
        program = builder.build()

        self.assertIsInstance(program, StudyProgram)
        self.assertEqual(len(program.modules), 1)
        self.assertEqual(len(program.elements), 1)

    def test_json_serialization(self):
        """Test JSON serialization of complete structure."""
        # Create a simple study program
        info = StudyProgramInfo(id=1, number="1", name="Test")
        modules = {
            "1": Module(id=1, name="Module 1", credit_points=6.0)
        }
        elements = [
            Element(id=1, code="E1", name="Element 1", type="exam", credit_points=6.0)
        ]

        program = StudyProgram(
            study_program=info,
            modules=modules,
            elements=elements
        )

        # Convert to dict and ensure it's JSON serializable
        data_dict = program.to_dict()
        json_str = json.dumps(data_dict, ensure_ascii=False)
        self.assertIsNotNone(json_str)

        # Parse back and verify structure
        parsed = json.loads(json_str)
        self.assertIn("study_program", parsed)
        self.assertIn("modules", parsed)
        self.assertIn("elements", parsed)
        self.assertEqual(parsed["study_program"]["name"], "Test")

    def test_builder_analysis_methods(self):
        """Test analysis methods in StudyProgramBuilder."""
        builder = StudyProgramBuilder(id=1, number="1", name="Test")

        # Add modules with credit points
        builder.add_module(Module(id=1, name="M1", credit_points=6.0))
        builder.add_module(Module(id=2, name="M2", credit_points=8.0))

        # Add elements of different types and semesters
        builder.add_element(Element(id=1, code="E1", name="Exam 1", type="exam", semester=1))
        builder.add_element(Element(id=2, code="E2", name="Learning 1", type="learning_module", semester=1))
        builder.add_element(Element(id=3, code="E3", name="Seminar 1", type="seminar", semester=2))

        # Test total credit points
        self.assertEqual(builder.get_total_credit_points(), 14.0)

        # Test filtering by semester
        semester_1 = builder.get_elements_by_semester(1)
        self.assertEqual(len(semester_1), 2)

        # Test filtering by type
        exams = builder.get_elements_by_type("exam")
        self.assertEqual(len(exams), 1)


if __name__ == '__main__':
    unittest.main()