"""
Document model for file attachments.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:
    """Document information (simplified for future download feature)."""
    filename: str
    content_type: str  # Store as string, not enum
    size: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None