from dataclasses import dataclass
from typing import List


@dataclass
class CodeChunk:
    chunk_id: str
    file_path: str
    name: str
    type: str
    start_line: int
    end_line: int
    source_code: str
    called_functions: List[str]