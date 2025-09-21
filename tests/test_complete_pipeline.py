#!/usr/bin/env python3
"""
Complete pipeline test - simulates actual usage.

This test verifies the complete workflow from HTML input to JSON output
exactly as a user would use it via the command line.
"""

import json
import subprocess
import tempfile
from pathlib import Path
import unittest


class TestCompletePipeline(unittest.TestCase):
    """Test the complete pipeline as used from command line."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.html_file = cls.fixtures_dir / "curriculum_informatik.html"
        cls.expected_json = cls.fixtures_dir / "expected_output_informatik.json"
        cls.main_script = Path(__file__).parent.parent / "main.py"

    def test_command_line_extraction(self):
        """Test extraction via command line interface."""
        # Create temp output file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            output_file = Path(tmp.name)

        try:
            # Run the main script
            result = subprocess.run(
                ["python3", str(self.main_script), str(self.html_file), "-o", str(output_file)],
                capture_output=True,
                text=True
            )

            # Check that command succeeded
            self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")

            # Verify output file was created
            self.assertTrue(output_file.exists(), "Output JSON file was not created")

            # Load and verify output
            with open(output_file, 'r', encoding='utf-8') as f:
                actual_data = json.load(f)

            with open(self.expected_json, 'r', encoding='utf-8') as f:
                expected_data = json.load(f)

            # Verify structure
            self.assertIn("study_program", actual_data)
            self.assertIn("modules", actual_data)
            self.assertIn("elements", actual_data)

            # Verify counts match
            self.assertEqual(
                len(actual_data["modules"]),
                len(expected_data["modules"]),
                "Module count doesn't match"
            )
            self.assertEqual(
                len(actual_data["elements"]),
                len(expected_data["elements"]),
                "Element count doesn't match"
            )

            # Verify study program info
            self.assertEqual(
                actual_data["study_program"],
                expected_data["study_program"],
                "Study program info doesn't match"
            )

        finally:
            # Clean up
            if output_file.exists():
                output_file.unlink()


    def test_pretty_vs_compact_json(self):
        """Test pretty print vs compact JSON output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pretty_file = Path(tmpdir) / "pretty.json"
            compact_file = Path(tmpdir) / "compact.json"

            # Generate pretty JSON
            subprocess.run(
                ["python3", str(self.main_script), str(self.html_file),
                 "-o", str(pretty_file), "--pretty"],
                check=True
            )

            # Generate compact JSON
            subprocess.run(
                ["python3", str(self.main_script), str(self.html_file),
                 "-o", str(compact_file), "--no-pretty"],
                check=True
            )

            # Load both files
            with open(pretty_file, 'r') as f:
                pretty_data = json.load(f)

            with open(compact_file, 'r') as f:
                compact_data = json.load(f)

            # Data should be identical
            self.assertEqual(pretty_data, compact_data, "Pretty and compact JSON have different data")

            # File sizes should be different (pretty is larger)
            pretty_size = pretty_file.stat().st_size
            compact_size = compact_file.stat().st_size
            self.assertGreater(pretty_size, compact_size, "Pretty JSON should be larger than compact")

            # Pretty file should have newlines
            with open(pretty_file, 'r') as f:
                pretty_content = f.read()
            self.assertIn('\n  ', pretty_content, "Pretty JSON should be indented")

            # Compact file should be single line (or minimal newlines)
            with open(compact_file, 'r') as f:
                compact_content = f.read()
            # Compact JSON should have way fewer lines
            self.assertLess(
                compact_content.count('\n'),
                pretty_content.count('\n') / 10,
                "Compact JSON should have significantly fewer newlines"
            )


if __name__ == '__main__':
    unittest.main()