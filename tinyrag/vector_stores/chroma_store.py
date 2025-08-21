"""
ChromaDB vector store implementation
"""

import uuid
from typing import List, Tuple, Optional

from .base import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    def __init__(self, dimension: int = 384, collection_name: str = "tinyrag_collection", persist_directory: Optional[str] = None):
        """Initialize ChromaDB vector store"""
        super().__init__(dimension)
        
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError("chromadb required. Install with: pip install chromadb")
        
        self.collection_name = collection_name
        
        if persist_directory:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        else:
            self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        
        # Create or get collection
        try:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception:
            # Collection might already exist
            self.collection = self.client.get_collection(name=collection_name)
        
        self.doc_ids = []
    
    def add_vectors(self, embeddings: List[List[float]], texts: List[str]):
        """Add vectors and corresponding texts to the store"""
        # Generate unique IDs for each document
        ids = [str(uuid.uuid4()) for _ in texts]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids
        )
        
        self.doc_ids.extend(ids)
        self.texts.extend(texts)
        self.embeddings.extend(embeddings)
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """Search for similar vectors"""
        if len(self.texts) == 0:
            return []
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, len(self.texts))
        )
        
        # ChromaDB returns distances, convert to similarity scores
        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        # Convert distances to similarity scores (1 - distance for cosine)
        similarities = [1 - dist for dist in distances]
        
        return list(zip(documents, similarities))
    
    def save(self, filepath: str):
        """Save is handled automatically by ChromaDB if using persistent client"""
        # For persistent client, data is automatically saved
        # For in-memory client, we could export the collection
        pass
    
    def load(self, filepath: str):
        """Load is handled automatically by ChromaDB if using persistent client"""
        # For persistent client, data is automatically loaded
        # Update our local tracking
        try:
            count = self.collection.count()
            if count > 0:
                # Get all documents to update local state
                all_data = self.collection.get()
                self.texts = all_data['documents'] or []
                self.embeddings = all_data['embeddings'] or []
                self.doc_ids = all_data['ids'] or []
        except Exception as e:
            print(f"Error loading ChromaDB collection: {e}")
    
    def clear(self):
        """Clear all stored vectors and texts"""
        super().clear()
        self.doc_ids = []
        
        # Delete and recreate collection
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error clearing ChromaDB collection: {e}")
    
    def size(self) -> int:
        """Return the number of stored vectors"""
        try:
            return self.collection.count()
        except:
            return len(self.texts)