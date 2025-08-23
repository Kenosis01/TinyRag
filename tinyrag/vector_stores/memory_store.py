"""
In-memory vector store implementation using numpy
"""

import numpy as np
import pickle
from typing import List, Tuple, Dict, Any, Optional

from .base import BaseVectorStore


class MemoryVectorStore(BaseVectorStore):
    def __init__(self, dimension: int = 384):
        """Initialize in-memory vector store"""
        super().__init__(dimension)
        self.vectors = np.array([]).reshape(0, dimension)
    
    def add_vectors(self, embeddings: List[List[float]], texts: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Add vectors and corresponding texts to the store with optional metadata"""
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Normalize for cosine similarity
        norms = np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        embeddings_array = embeddings_array / (norms + 1e-8)
        
        if self.vectors.shape[0] == 0:
            self.vectors = embeddings_array
        else:
            self.vectors = np.vstack([self.vectors, embeddings_array])
        
        self.texts.extend(texts)
        self.embeddings.extend(embeddings)
        
        # Add metadata (default empty dict if not provided)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in texts])
    
    def search(self, query_embedding: List[float], k: int = 5, return_metadata: bool = False) -> List[Tuple[str, float, Optional[Dict[str, Any]]]]:
        """Search for similar vectors using cosine similarity with optional metadata"""
        if len(self.texts) == 0:
            return []
        
        query_array = np.array(query_embedding, dtype=np.float32)
        
        # Normalize query
        norm = np.linalg.norm(query_array)
        if norm > 0:
            query_array = query_array / norm
        
        # Calculate cosine similarities
        similarities = np.dot(self.vectors, query_array)
        
        # Get top k indices
        top_k = min(k, len(similarities))
        top_indices = np.argpartition(similarities, -top_k)[-top_k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]
        
        results = []
        for idx in top_indices:
            metadata = self.metadata[idx] if return_metadata and idx < len(self.metadata) else None
            results.append((self.texts[idx], float(similarities[idx]), metadata))
        
        return results
    
    def save(self, filepath: str):
        """Save the vector store to disk"""
        data = {
            'texts': self.texts,
            'embeddings': self.embeddings,
            'vectors': self.vectors,
            'dimension': self.dimension,
            'metadata': self.metadata
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
                self.vectors = data['vectors']
                self.dimension = data['dimension']
                self.metadata = data.get('metadata', [])  # Backward compatibility
        except FileNotFoundError:
            print(f"File {filepath}.pkl not found")
    
    def clear(self):
        """Clear all stored vectors and texts"""
        super().clear()
        self.vectors = np.array([]).reshape(0, self.dimension)