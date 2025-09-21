"""
Enumerations for WBH Campus Data types.
"""

from enum import Enum


class ElementType(Enum):
    """Types of study elements."""
    EXAM = "exam"
    LEARNING_MODULE = "learning_module"
    SEMINAR = "seminar"


class DocumentType(Enum):
    """Types of documents (for future download feature)."""
    PDF = "pdf"
    EPUB = "epub"
    HTML = "html"
    MP3 = "mp3"
    ZIP = "zip"
    UNKNOWN = "unknown"


class DegreeType(Enum):
    """Types of academic degrees."""
    BACHELOR = "Bachelor"
    BACHELOR_OF_SCIENCE = "Bachelor of Science"
    BACHELOR_OF_ENGINEERING = "Bachelor of Engineering"
    BACHELOR_OF_ARTS = "Bachelor of Arts"
    MASTER = "Master"
    MASTER_OF_SCIENCE = "Master of Science"
    MASTER_OF_ENGINEERING = "Master of Engineering"
    MASTER_OF_ARTS = "Master of Arts"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, text: str) -> 'DegreeType':
        """
        Determine degree type from text.

        Args:
            text: Text containing degree information

        Returns:
            Appropriate DegreeType enum value
        """
        text_lower = text.lower()

        # Check for specific degree types
        if 'b.sc.' in text_lower or 'bachelor of science' in text_lower:
            return cls.BACHELOR_OF_SCIENCE
        elif 'b.eng.' in text_lower or 'bachelor of engineering' in text_lower:
            return cls.BACHELOR_OF_ENGINEERING
        elif 'b.a.' in text_lower or 'bachelor of arts' in text_lower:
            return cls.BACHELOR_OF_ARTS
        elif 'm.sc.' in text_lower or 'master of science' in text_lower:
            return cls.MASTER_OF_SCIENCE
        elif 'm.eng.' in text_lower or 'master of engineering' in text_lower:
            return cls.MASTER_OF_ENGINEERING
        elif 'm.a.' in text_lower or 'master of arts' in text_lower:
            return cls.MASTER_OF_ARTS
        elif 'bachelor' in text_lower:
            return cls.BACHELOR
        elif 'master' in text_lower:
            return cls.MASTER
        else:
            return cls.UNKNOWN