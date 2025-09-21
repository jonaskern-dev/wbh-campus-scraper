"""
HTML Scraper for WBH Campus Data

Extracts embedded JSON and study program information from HTML exports.
"""

import json
import re
from pathlib import Path
from pathlib import Path
from typing import Dict, Any, Optional, List


from .models import (
    StudyProgram, StudyProgramBuilder, Module, Element, Document,
    ElementType, DocumentType, ExamInfo, SubElement, MarkAndPoints
)


class WBHScraper:
    """
    Scraper for extracting and transforming WBH Campus HTML data.

    Usage:
        # Get raw JSON (default):
        scraper = WBHScraper("curriculum.html")
        raw_data = scraper.raw_json  # Direct access to extracted JSON

        # Get transformed data:
        scraper = WBHScraper("curriculum.html")
        study_program = scraper.transform()  # Structured StudyProgram object
    """

    # Pattern to find the embedded JSON (handles both spaces and tabs)
    JSON_PATTERN = r'WL\.DEBUG\.iCurriculumJSON[\s\t]*=[\s\t]*(\{.*?\});'

    # Pattern to extract study program info from encoded URLs
    # More flexible pattern that works for ALL study programs
    STUDY_PROGRAM_PATTERN = r'5374756469656e67616e67[0-9a-fA-F\s]+42616368656c6f72|5374756469656e67616e67[0-9a-fA-F\s]+4d6173746572'
    # Explanation:
    # 5374756469656e67616e67 = "Studiengang"
    # [0-9a-fA-F\s]+ = any hex characters and spaces
    # 42616368656c6f72 = "Bachelor" OR 4d6173746572 = "Master"

    def __init__(self, file_path: Optional[Path] = None, debug: bool = False):
        """
        Initialize the scraper.

        Args:
            file_path: Optional path to HTML file to scrape
            debug: If True, saves raw JSON to debug_raw.json
        """
        self.file_path = file_path
        self.debug = debug
        self.data = None  # Stores the current data (raw JSON)
        self.study_program = None
        self.builder: Optional[StudyProgramBuilder] = None

        # Auto-load data if file path is provided
        if self.file_path:
            self.data = self.parse_file(self.file_path)

    def extract_json_from_html(self, html_content: str) -> Dict[str, Any]:
        """
        Extract curriculum JSON data from HTML content.

        Args:
            html_content: HTML content as string

        Returns:
            Parsed JSON data

        Raises:
            ValueError: If JSON extraction fails
        """
        # Find JSON in HTML
        match = re.search(self.JSON_PATTERN, html_content, re.DOTALL)

        if not match:
            raise ValueError("No curriculum JSON data found in HTML")

        json_str = match.group(1)

        try:
            # Parse JSON
            data = json.loads(json_str)
            self.data = data

            # Try to extract study program info
            self._extract_study_program_info(html_content, data)

            # Save debug output if requested
            if self.debug:
                self._save_debug_json(data)

            return data

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    def _extract_study_program_info(self, html_content: str, data: Dict[str, Any]):
        """
        Extract study program information from encoded URLs.

        Args:
            html_content: The HTML content
            data: The JSON data dictionary to update
        """
        # Try to find encoded study program info
        hex_matches = re.findall(self.STUDY_PROGRAM_PATTERN, html_content, re.IGNORECASE)

        if hex_matches:
            for hex_match in hex_matches[:3]:  # Try first 3 matches
                try:
                    # Clean hex string (remove spaces if any)
                    hex_str = ''.join(hex_match.split())

                    # Limit length and decode
                    hex_str = hex_str[:300]  # Increased limit for longer names
                    decoded = bytes.fromhex(hex_str).decode('utf-8', errors='ignore')

                    # Clean up HTML entities
                    decoded = decoded.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')

                    # Extract study program info with more flexible pattern
                    # Pattern: "Studiengang" + number + name + "(Bachelor)" or "(Master)"
                    patterns = [
                        r'Studiengang\s+(\d+)\s+([^>&]+?)(?:\s*>|\s*\(?\s*)(Bachelor|Master)',
                        r'Studiengang\s+(\d+)\s+([^>&]+)',
                        r'(\d{4})\s+([^>&]+?)(?:\s*>|\s*\(?\s*)(Bachelor|Master)'
                    ]

                    for pattern in patterns:
                        studiengang_match = re.search(pattern, decoded, re.IGNORECASE)
                        if studiengang_match:
                            number = studiengang_match.group(1)
                            name = studiengang_match.group(2).strip()

                            # Clean up name - remove trailing whitespace and dashes
                            name = name.rstrip(' -')

                            # Add degree type if found
                            if studiengang_match.lastindex >= 3:
                                degree = studiengang_match.group(3)
                                # Format as "Name (Bachelor)" or "Name (Master)"
                                if not name.endswith(')'):
                                    name = f"{name} ({degree})"

                            data['studiengang_nummer'] = number
                            data['studiengang_name'] = name
                            return
                except Exception:
                    continue

        # Fallback to defaults if nothing found
        # Try to guess from the JSON content
        self._apply_fallback_study_program(data)

    def _apply_fallback_study_program(self, data: Dict[str, Any]):
        """
        Apply fallback logic to determine study program.

        Args:
            data: The JSON data dictionary to update
        """
        # Check if we can infer from course data
        courses = data.get('iCourseList', [])

        # Common patterns in course names
        if any('Informatik' in str(c.get('name', '')) for c in courses[:10]):
            data['studiengang_nummer'] = '1110'
            data['studiengang_name'] = 'Informatik (Bachelor)'
        elif any('Wirtschaftsinformatik' in str(c.get('name', '')) for c in courses[:10]):
            data['studiengang_nummer'] = '1120'
            data['studiengang_name'] = 'Wirtschaftsinformatik (Bachelor)'
        elif any('Maschinenbau' in str(c.get('name', '')) for c in courses[:10]):
            data['studiengang_nummer'] = '2110'
            data['studiengang_name'] = 'Maschinenbau (Bachelor)'
        else:
            # Ultimate fallback
            data['studiengang_nummer'] = '0000'
            data['studiengang_name'] = 'Unbekannter Studiengang'

    def _save_debug_json(self, data: Dict[str, Any]):
        """Save raw JSON for debugging purposes."""
        debug_file = Path('debug_raw.json')
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Debug: Raw JSON saved to {debug_file}")

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse an HTML file and extract JSON data.

        Args:
            file_path: Path to the HTML file

        Returns:
            Extracted JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If parsing fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        return self.extract_json_from_html(html_content)

    @property
    def raw_json(self) -> Optional[Dict[str, Any]]:
        """Get the raw JSON data (default output without transform)."""
        return self.data

    def transform(self) -> StudyProgram:
        """
        Transform the raw JSON data into structured StudyProgram.

        Returns:
            StudyProgram object with all extracted data

        Raises:
            ValueError: If no raw data is available
        """
        if not self.data:
            if self.file_path:
                self.data = self.parse_file(self.file_path)
            else:
                raise ValueError("No data available. Load a file first or provide file_path in constructor.")

        if not self.study_program:
            self.study_program = self._process_raw_data(self.data)

        return self.study_program

    def _process_raw_data(self, raw_data: Dict[str, Any]) -> StudyProgram:
        """
        Process raw JSON data into structured models.

        Args:
            raw_data: Raw JSON data from parser

        Returns:
            Populated StudyProgram object
        """
        # Create builder for study program
        self.builder = StudyProgramBuilder(
            id=raw_data.get("ilgid", 0),
            number=raw_data.get("studiengang_nummer", ""),
            name=raw_data.get("studiengang_name", "")
        )

        # Process modules and elements
        modules_data = {}
        element_to_module = {}

        # First pass: collect modules and map elements
        for course in raw_data.get("iCourseList", []):
            testarea = course.get("testarea", {})

            # Check if element belongs to a module
            if testarea and testarea.get("id", -1) != -1:
                module_id = testarea["id"]

                # Create module if not exists
                if module_id not in modules_data:
                    modules_data[module_id] = Module(
                        id=module_id,
                        name=testarea.get("name", ""),
                        code=testarea.get("sname")
                    )

                element_to_module[course["id"]] = module_id

        # Second pass: create elements and populate modules
        for course in raw_data.get("iCourseList", []):
            element = self._create_element(course, element_to_module)
            self.builder.add_element(element)

            # Add to module if applicable
            if element.module_id and element.module_id in modules_data:
                module = modules_data[element.module_id]
                module.element_ids.append(element.id)

                if element.is_exam:
                    module.exam_ids.append(element.id)
                    # Update module credit points from exam
                    if element.credit_points and element.credit_points > 0:
                        if not module.credit_points or module.credit_points < element.credit_points:
                            module.credit_points = element.credit_points
                else:
                    module.study_material_ids.append(element.id)

        # Add all modules to builder
        for module in modules_data.values():
            self.builder.add_module(module)

        return self.builder.build()

    def _create_element(self, course: Dict[str, Any], element_to_module: Dict[int, int]) -> Element:
        """
        Create an Element object from course data.

        Args:
            course: Course data from JSON
            element_to_module: Mapping of element IDs to module IDs

        Returns:
            Populated Element object
        """
        # Determine element type
        if course.get("isExam", False):
            element_type = "exam"
        elif course.get("isSeminar", False):
            element_type = "seminar"
        else:
            element_type = "learning_module"

        # Calculate semester from study month
        study_month = course.get("studyMonth", 0)
        semester = 0 if study_month == 0 else ((study_month - 1) // 6) + 1

        # Create element
        element = Element(
            id=course.get("id"),
            code=course.get("sName", ""),
            name=course.get("name", ""),
            type=element_type,
            study_month=study_month,
            semester=semester,
            module_id=element_to_module.get(course.get("id")),
            credit_points=course.get("cp"),
            is_passed=course.get("isPassed", False)
        )

        # Add exam info if present
        if element_type == "exam" and course.get("examInformations"):
            exam_info = course["examInformations"]
            element.exam_info = ExamInfo(
                exam_form=exam_info.get("examForm"),
                prerequisites=exam_info.get("participationRequirements"),
                allowed_aids=exam_info.get("allowedAuxiliaryMeans"),
                core_topics=exam_info.get("coreTopics")
            )

        # Add documents if present
        if course.get("courseActions") and course["courseActions"].get("docFolder"):
            for doc in course["courseActions"]["docFolder"]:
                document = Document(
                    filename=doc.get("filename", ""),
                    content_type=doc.get("contentType", "unknown").lower(),
                    size=doc.get("sizeLabel"),
                    url=doc.get("url"),
                    description=doc.get("contentTypeDescription")
                )
                element.documents.append(document)

        # Add sub-elements and extract markAndPoints if present
        if course.get("iContents"):
            for content in course["iContents"]:
                # Check for markAndPoints data
                if content.get("markAndPoints") and not element.mark_and_points:
                    mp = content["markAndPoints"]
                    element.mark_and_points = MarkAndPoints(
                        mark=mp.get("mark"),
                        mark_label=mp.get("markLabel"),
                        esa_send_date=mp.get("esaSendDate"),
                        esa_grade_date=mp.get("esaGradeDate"),
                        mark_and_points_tooltip=mp.get("markAndPointsTooltip"),
                        exam_css_class=mp.get("examCssClass"),
                        show_tick_mark=mp.get("showTickMark")
                    )

                # Create sub-element
                sub_element = self._create_sub_element(content, course.get("sName", ""))
                if sub_element:
                    element.sub_elements.append(sub_element)

        return element

    def _create_sub_element(self, content: Dict[str, Any], parent_code: str) -> Optional[SubElement]:
        """Create a SubElement from content data."""
        # Get ID and name
        content_id = content.get("id") or content.get("contentid")
        name = content.get("name", "")

        # Skip if no ID or name
        if not content_id or not name:
            return None

        sub_element = SubElement(
            id=content_id,
            code=parent_code,  # Use parent's code
            name=name,
            type="repetitorium" if "repetitorium" in name.lower() else "content"
        )

        # Check for documents in sub-element
        if content.get("docFolder"):
            for doc in content["docFolder"]:
                document = Document(
                    filename=doc.get("filename", ""),
                    content_type=doc.get("contentType", "unknown").lower(),
                    size=doc.get("sizeLabel"),
                    url=doc.get("url")
                )
                sub_element.documents.append(document)

        return sub_element

    def save_to_file(self, output_path: Path, pretty: bool = True) -> None:
        """
        Save the transformed data to a JSON file.

        Args:
            output_path: Path to save the JSON file
            pretty: Whether to pretty-print the JSON
        """
        if not self.study_program:
            self.transform()

        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(self.study_program.to_dict(), f, ensure_ascii=False, indent=2)
            else:
                json.dump(self.study_program.to_dict(), f, ensure_ascii=False)