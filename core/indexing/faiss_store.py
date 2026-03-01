import faiss
import numpy as np
from typing import List

class FaissVectorStore:
    """
    Store the embeddings vectors using FAISS and used for searching
    """

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFaltIP(dimension)
    
    @staticmethod
    def _normalize(vectors: np.darray) -> np.ndarray:
        """
        Normalize vectors for cosine similarity
        """
        faiss.normalize_L2(vectors)
        return vectors
    
    #Faiss expects 2d matrix so we stack vectors
    def add_vectors(self, vectors:List[np.ndarray]):
        """
        Add multiple vectors to index
        """
        np_vectors= np.vstack(vectors)
        np_vectors = self._normalize(np_vectors)

        self.index.add(np_vectors)

    def serach(self, query_vector: np.darray, top_k: int = 5):
        """
        Search similiar vectors.
        """
        query_vector = np.expand_dims(query_vector, axis=0)
        query_vector = self._normalize(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        return scores[0], indices[0]
    
    def save(self, path:str):
        faiss.write_index(self.index, path)

    def load(self, path: str):
        self.index = faiss.read_index(path)