import os
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

"""
Append chunks into single line text which is appended into texts so that 'embed_batch' code runs 
"""

class Embedder:
    """
    Converts codechunks into vector embeddings using sentenee transformer
    Also the minilm model used here converts text to 384 dimensions
    So final size is 384
    Also save vector as float 32 as the FAISS is written in c++ which operates on 32 bit and optimised for float 32 bit
    """

    def __init__(self, model_name: str = "sentence-transformer/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self,text:str)-> np.array:
        """
        Embedding single tect
        """
        vector = self.model.encode(text, convert_to_numpy=True)
        return vector.astype("float32")
    
    def embed_batch(self, texts: List[str]) -> List[np.array]:
        '''
        Embedding multiple texts now
        '''
        vectors = self.model.encode(texts, convert_to_numpy=True)
        return [v.astype("float32") for v in vectors]