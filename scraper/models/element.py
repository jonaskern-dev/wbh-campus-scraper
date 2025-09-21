"""
Element model for study elements (courses, exams, seminars).
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .document import Document
from .exam_info import ExamInfo
from .mark_and_points import MarkAndPoints
from .sub_element import SubElement


@dataclass
class Element:
    """Study element (course, exam, seminar)."""
    id: int
    code: str
    name: str
    type: str  # Store as string for JSON
    study_month: int = 0
    semester: int = 0
    module_id: Optional[int] = None
    credit_points: Optional[float] = None
    is_passed: bool = False
    exam_info: Optional[ExamInfo] = None
    mark_and_points: Optional[MarkAndPoints] = None
    documents: List[Document] = field(default_factory=list)
    sub_elements: List[SubElement] = field(default_factory=list)

    @property
    def is_exam(self) -> bool:
        """Check if this element is an exam."""
        return self.type == "exam"