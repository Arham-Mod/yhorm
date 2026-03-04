import faiss
import numpy as np
from typing import List


class FaissVectorStore:
    """
    Store embedding vectors using FAISS and perform similarity search
    """

    def __init__(self, metadata_store):

        self.index = None
        self.metadata_store = metadata_store
        self.current_id = 0

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        """
        Normalize vectors for cosine similarity
        """
        faiss.normalize_L2(vectors)
        return vectors

    def add_vectors(self, vectors: List[np.ndarray]):
        """
        Add multiple vectors to FAISS index
        """

        np_vectors = np.vstack(vectors)
        np_vectors = self._normalize(np_vectors)

        # Create index if it doesn't exist
        if self.index is None:

            dimension = np_vectors.shape[1]

            # Inner product index (works with normalized vectors = cosine similarity)
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(np_vectors)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        """
        Search similar vectors
        """

        query_vector = np.expand_dims(query_vector, axis=0)
        query_vector = self._normalize(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        return scores[0], indices[0]

    def save(self, path: str):

        faiss.write_index(self.index, path)

    def load(self, path: str):

        self.index = faiss.read_index(path)

    def add_chunk(self, embedding, chunk):

        embedding = np.expand_dims(embedding, axis=0)

        embedding = self._normalize(embedding)

        if self.index is None:

            dimension = embedding.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        vector_id = self.current_id

        self.index.add(embedding)

        self.metadata_store.add(vector_id, chunk)

        self.current_id += 1