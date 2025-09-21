"""
StudyProgramBuilder for constructing the study program.
"""

from typing import Dict, List, Optional

from .module import Module
from .element import Element
from .study_program import StudyProgramInfo, StudyProgram


class StudyProgramBuilder:
    """Helper to build StudyProgram from scraped data."""

    def __init__(self, id: int, number: str, name: str):
        """
        Initialize the builder with study program info.

        Args:
            id: Program ID
            number: Program number
            name: Program name
        """
        self.info = StudyProgramInfo(id=id, number=number, name=name)
        self.modules: Dict[str, Module] = {}
        self.elements: List[Element] = []

    def add_module(self, module: Module):
        """Add a module."""
        self.modules[str(module.id)] = module

    def add_element(self, element: Element):
        """Add an element."""
        self.elements.append(element)

    def get_module(self, module_id: int) -> Optional[Module]:
        """Get a module by ID."""
        return self.modules.get(str(module_id))

    def build(self) -> StudyProgram:
        """Build the final StudyProgram object."""
        return StudyProgram(
            study_program=self.info,
            modules=self.modules,
            elements=self.elements
        )

    # Analysis methods (for statistics)
    def get_total_credit_points(self) -> float:
        """Calculate total credit points."""
        total = 0
        for module in self.modules.values():
            if module.credit_points:
                total += module.credit_points
        return total

    def get_elements_by_semester(self, semester: int) -> List[Element]:
        """Get elements for a specific semester."""
        return [e for e in self.elements if e.semester == semester]

    def get_elements_by_type(self, element_type: str) -> List[Element]:
        """Get elements of a specific type."""
        return [e for e in self.elements if e.type == element_type]