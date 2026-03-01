import pickle
from typing import Dict
from pathlib import Path

class MetadataStore:
    """
    stores mapping between FAISS vector IDs and CodeChunk metadata
    """
    def __init__(self):
        self.id_to_chunk: Dict[int,dict] = {}

    def add(self, vector_id: int, chunk_metadata: dict):
        self.id_to_chunk[vector_id] = chunk_metadata

    def get(self,vector_id: int):
        return self.id_to_chunk(vector_id)
    
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.id_to_chunk,f)
    
    def load(self, path:str):
        with open(path, "rb") as f:
            self.id_to_chunk = pickle.load(f)