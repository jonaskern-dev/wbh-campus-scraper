"""
StudyProgram models for the complete program structure.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any

from .module import Module
from .element import Element


from typing import Optional

@dataclass
class StudyProgramInfo:
    """Basic study program information."""
    id: int
    number: str
    name: str
    degree_type: Optional[str] = None  # e.g. "Bachelor of Science", "Bachelor of Engineering"


@dataclass
class StudyProgram:
    """Complete study program data structure for JSON output."""
    study_program: StudyProgramInfo
    modules: Dict[str, Module]
    elements: List[Element]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "study_program": asdict(self.study_program),
            "modules": {
                module_id: asdict(module)
                for module_id, module in self.modules.items()
            },
            "elements": [asdict(element) for element in self.elements]
        }