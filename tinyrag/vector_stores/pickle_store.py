"""
Simple pickle-based vector store implementation
"""

import pickle
import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

from .base import BaseVectorStore


class PickleVectorStore(BaseVectorStore):
    def __init__(self, dimension: int = 384):
        """Initialize pickle-based vector store"""
        super().__init__(dimension)
    
    def add_vectors(self, embeddings: List[List[float]], texts: List[str]):
        """Add vectors and corresponding texts to the store"""
        self.embeddings.extend(embeddings)
        self.texts.extend(texts)
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """Search for similar vectors using cosine similarity"""
        if not self.embeddings:
            return []
        
        # Calculate cosine similarities
        query_array = np.array([query_embedding])
        embeddings_array = np.array(self.embeddings)
        
        similarities = cosine_similarity(query_array, embeddings_array)[0]
        
        # Get top k indices
        top_k = min(k, len(similarities))
        top_indices = np.argpartition(similarities, -top_k)[-top_k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]
        
        results = []
        for idx in top_indices:
            results.append((self.texts[idx], float(similarities[idx])))
        
        return results
    
    def save(self, filepath: str):
        """Save the vector store to disk"""
        data = {
            'texts': self.texts,
            'embeddings': self.embeddings,
            'dimension': self.dimension
        }
        
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """Load the vector store from disk"""
        try:
            with open(f"{filepath}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.embeddings = data['embeddings']
                self.dimension = data['dimension']
        except FileNotFoundError:
            print(f"File {filepath}.pkl not found")