"""
ExamInfo model for exam-specific information.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExamInfo:
    """Exam-specific information."""
    exam_form: Optional[str] = None
    prerequisites: Optional[str] = None
    allowed_aids: Optional[str] = None
    core_topics: Optional[str] = None