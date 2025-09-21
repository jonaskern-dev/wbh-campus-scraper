"""
SubElement model for content within elements.
"""

from dataclasses import dataclass, field
from typing import List

from .document import Document


@dataclass
class SubElement:
    """Sub-elements within an element."""
    id: int
    code: str
    name: str
    type: str
    documents: List[Document] = field(default_factory=list)