"""
Data Models for WBH Campus Data

Organized structure with each model in its own file.
"""

from .enums import ElementType, DocumentType
from .document import Document
from .exam_info import ExamInfo
from .mark_and_points import MarkAndPoints
from .sub_element import SubElement
from .element import Element
from .module import Module
from .study_program import StudyProgramInfo, StudyProgram
from .builder import StudyProgramBuilder

__all__ = [
    # Enums
    'ElementType',
    'DocumentType',

    # Models
    'Document',
    'ExamInfo',
    'MarkAndPoints',
    'SubElement',
    'Element',
    'Module',
    'StudyProgramInfo',
    'StudyProgram',

    # Builder
    'StudyProgramBuilder',
]