"""
Mark and points information for graded elements.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MarkAndPoints:
    """Grade and evaluation information for an element."""
    mark: Optional[str] = None
    mark_label: Optional[str] = None
    esa_send_date: Optional[str] = None
    esa_grade_date: Optional[str] = None
    mark_and_points_tooltip: Optional[str] = None
    exam_css_class: Optional[str] = None
    show_tick_mark: Optional[bool] = None