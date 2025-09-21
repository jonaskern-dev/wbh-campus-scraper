"""
Module model for study modules.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Module:
    """Study module containing elements."""
    id: int
    name: str
    code: Optional[str] = None
    credit_points: Optional[float] = None
    element_ids: List[int] = field(default_factory=list)
    exam_ids: List[int] = field(default_factory=list)
    study_material_ids: List[int] = field(default_factory=list)