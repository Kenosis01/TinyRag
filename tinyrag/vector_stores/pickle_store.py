"""
Simple pickle-based vector store implementation
"""

import pickle
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity

from .base import BaseVectorStore


class PickleVectorStore(BaseVectorStore):
    def __init__(self, dimension: int = 384, file_path: str = None, **kwargs):
        """Initialize pickle-based vector store
        
        Args:
            dimension: Embedding dimension
            file_path: Optional path to pickle file for automatic saving/loading
        """
        super().__init__(dimension)
        self.file_path = file_path
        
        # Load from file if it exists
        if self.file_path and self._file_exists():
            self.load(self.file_path)
    
    def _file_exists(self) -> bool:
        """Check if the pickle file exists"""
        if not self.file_path:
            return False
        
        import os
        return os.path.exists(f"{self.file_path}.pkl") or os.path.exists(self.file_path)
    
    def add_vectors(self, embeddings: List[List[float]], texts: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        """Add vectors and corresponding texts to the store with optional metadata"""
        self.embeddings.extend(embeddings)
        self.texts.extend(texts)
        
        # Add metadata (default empty dict if not provided)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in texts])
        
        # Auto-save if file path is configured
        if self.file_path:
            self.save(self.file_path)
    
    def search(self, query_embedding: List[float], k: int = 5, return_metadata: bool = False) -> List[Tuple[str, float, Optional[Dict[str, Any]]]]:
        """Search for similar vectors using cosine similarity with optional metadata"""
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
            metadata = self.metadata[idx] if return_metadata and idx < len(self.metadata) else None
            results.append((self.texts[idx], float(similarities[idx]), metadata))
        
        return results
    
    def save(self, filepath: str):
        """Save the vector store to disk"""
        data = {
            'texts': self.texts,
            'embeddings': self.embeddings,
            'dimension': self.dimension,
            'metadata': self.metadata
        }
        
        # Ensure .pkl extension
        if not filepath.endswith('.pkl'):
            filepath = f"{filepath}.pkl"
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            print(f"✓ Saved vector store to {filepath}")
        except Exception as e:
            print(f"⚠ Error saving to {filepath}: {e}")
    
    def load(self, filepath: str):
        """Load the vector store from disk"""
        # Try different file extensions
        possible_paths = [filepath, f"{filepath}.pkl"]
        
        for path in possible_paths:
            try:
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                    self.texts = data['texts']
                    self.embeddings = data['embeddings']
                    self.dimension = data['dimension']
                    self.metadata = data.get('metadata', [])  # Backward compatibility
                print(f"✓ Loaded vector store from {path}")
                return
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠ Error loading from {path}: {e}")
                continue
        
        print(f"⚠ Could not find pickle file: {filepath}")