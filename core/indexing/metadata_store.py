from typing import Dict, List
from core.parsing.chunk_model import CodeChunk


class MetadataStore:
    """
    Stores mapping between FAISS vector IDs and CodeChunk metadata.
    Also maintains name-based lookup for dependency expansion.
    """

    def __init__(self):

        self.id_to_chunk: Dict[int, CodeChunk] = {}
        self.name_to_chunk_ids: Dict[str, List[int]] = {}

    def add(self, vector_id: int, chunk: CodeChunk):

        self.id_to_chunk[vector_id] = chunk

        if chunk.name not in self.name_to_chunk_ids:
            self.name_to_chunk_ids[chunk.name] = []

        self.name_to_chunk_ids[chunk.name].append(vector_id)

    def get_chunk(self, vector_id: int):

        return self.id_to_chunk.get(vector_id)

    def get_chunks_by_name(self, name: str):

        ids = self.name_to_chunk_ids.get(name, [])

        return [self.id_to_chunk[i] for i in ids]