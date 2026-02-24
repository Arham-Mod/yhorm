from dataclasses import dataclass
from typing import List


@dataclass
class CodeChunk:
    """
    Represents a structured unit of code used in parsing
    """
    id: str
    file_path: str
    name: str
    type: str  # "function", "class", "method"
    start_line: int
    end_line: int
    source_code: str
    calls: List[str]