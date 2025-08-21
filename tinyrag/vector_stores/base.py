"""
Base vector store interface
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class BaseVectorStore(ABC):
    """Abstract base class for vector stores"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.texts = []
        self.embeddings = []
    
    @abstractmethod
    def add_vectors(self, embeddings: List[List[float]], texts: List[str]) -> None:
        """Add vectors and corresponding texts to the store"""
        pass
    
    @abstractmethod
    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """Search for similar vectors and return (text, similarity_score) tuples"""
        pass
    
    @abstractmethod
    def save(self, filepath: str) -> None:
        """Save the vector store to disk"""
        pass
    
    @abstractmethod
    def load(self, filepath: str) -> None:
        """Load the vector store from disk"""
        pass
    
    def clear(self) -> None:
        """Clear all stored vectors and texts"""
        self.texts = []
        self.embeddings = []
    
    def size(self) -> int:
        """Return the number of stored vectors"""
        return len(self.texts)