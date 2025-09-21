"""
WBH Campus Scraper

A Python package for extracting and processing study data from WBH Online Campus HTML exports.
"""

__version__ = "0.5.2"
__author__ = "Jonas Kern"
__email__ = "info@jonaskern.de"

from .scraper import WBHScraper
from .models import (
    StudyProgram, StudyProgramInfo, StudyProgramBuilder,
    Module, Element, Document,
    ElementType, DocumentType, ExamInfo, SubElement
)

__all__ = [
    "WBHScraper",
    "StudyProgram",
    "StudyProgramInfo",
    "StudyProgramBuilder",
    "Module",
    "Element",
    "Document",
    "ElementType",
    "DocumentType",
    "ExamInfo",
    "SubElement"
]