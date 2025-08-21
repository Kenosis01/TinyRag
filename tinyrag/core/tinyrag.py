"""
Main TinyRag class for Retrieval-Augmented Generation
"""

from typing import Union, List, Optional, Dict, Any, Tuple
from pathlib import Path

from .provider import Provider
from .text_utils import extract_text, chunk_text
from ..vector_stores import (
    FaissVectorStore, 
    MemoryVectorStore, 
    PickleVectorStore, 
    ChromaVectorStore
)


class TinyRag:
    def __init__(
        self, 
        provider: Provider, 
        vector_store: str = "faiss", 
        chunk_size: int = 500,
        vector_store_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize TinyRag with a provider and vector store
        
        Args:
            provider: Provider instance for API calls
            vector_store: Type of vector store ("faiss", "memory", "pickle", "chroma")
            chunk_size: Size of text chunks for embedding
            vector_store_config: Additional configuration for vector store
        """
        self.provider = provider
        self.chunk_size = chunk_size
        
        # Determine embedding dimension based on model
        if provider.embedding_model == "default":
            dimension = 384  # all-MiniLM-L6-v2 dimension
        else:
            dimension = 1536  # OpenAI embedding dimension (adjust as needed)
        
        vector_store_config = vector_store_config or {}
        
        if vector_store == "faiss":
            self.vector_store = FaissVectorStore(dimension=dimension, **vector_store_config)
        elif vector_store == "memory":
            self.vector_store = MemoryVectorStore(dimension=dimension, **vector_store_config)
        elif vector_store == "pickle":
            self.vector_store = PickleVectorStore(dimension=dimension, **vector_store_config)
        elif vector_store == "chroma":
            self.vector_store = ChromaVectorStore(dimension=dimension, **vector_store_config)
        else:
            raise ValueError(f"Unsupported vector store: {vector_store}. "
                           f"Supported options: faiss, memory, pickle, chroma")
    
    def add_documents(self, data: Union[str, Path, List[str]]) -> None:
        """Add documents from text, file path, or list of texts"""
        if isinstance(data, list):
            # Handle list of texts or file paths
            all_chunks = []
            for item in data:
                text = extract_text(item)
                chunks = chunk_text(text, self.chunk_size)
                all_chunks.extend(chunks)
        else:
            # Handle single text or file path
            text = extract_text(data)
            all_chunks = chunk_text(text, self.chunk_size)
        
        if all_chunks:
            # Generate embeddings for all chunks
            embeddings = self.provider.get_embeddings(all_chunks)
            
            # Add to vector store
            self.vector_store.add_vectors(embeddings, all_chunks)
    
    def query(self, query: str, k: int = 5, return_scores: bool = True) -> Union[List[str], List[Tuple[str, float]]]:
        """Query the vector store without using LLM - just return similar chunks
        
        Args:
            query: Query string to search for
            k: Number of similar chunks to return
            return_scores: If True, return (text, score) tuples; if False, return just text
            
        Returns:
            List of similar text chunks, optionally with similarity scores
        """
        # Generate embedding for the query
        query_embedding = self.provider.get_embeddings([query])[0]
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, k=k)
        
        if return_scores:
            return results  # Returns [(text, score), ...]
        else:
            return [text for text, score in results]  # Returns [text, ...]
    
    def chat(self, query: str, k: int = 3) -> str:
        """Retrieve relevant chunks and generate an answer using LLM"""
        # Generate embedding for the query
        query_embedding = self.provider.get_embeddings([query])[0]
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, k=k)
        
        if not results:
            context = "No relevant documents found."
        else:
            # Combine retrieved chunks as context
            context_chunks = [text for text, score in results]
            context = "\n\n".join(context_chunks)
        
        # Create messages for chat completion
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the provided context to answer questions accurately. If the context doesn't contain relevant information, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
        
        # Generate response using the provider
        response = self.provider.chat_completion(messages)
        return response
    
    def get_similar_chunks(self, text: str, k: int = 5) -> List[Tuple[str, float]]:
        """Get chunks similar to the provided text (alias for query with scores)"""
        return self.query(text, k=k, return_scores=True)
    
    def search_documents(self, query: str, k: int = 5, min_score: float = 0.0) -> List[Tuple[str, float]]:
        """Search documents with optional minimum similarity score filtering"""
        results = self.query(query, k=k, return_scores=True)
        return [(text, score) for text, score in results if score >= min_score]
    
    def get_all_chunks(self) -> List[str]:
        """Get all stored text chunks"""
        return self.vector_store.texts.copy()
    
    def get_chunk_count(self) -> int:
        """Get the number of stored chunks"""
        return self.vector_store.size()
    
    def clear_documents(self) -> None:
        """Clear all stored documents and embeddings"""
        self.vector_store.clear()
    
    def save_vector_store(self, filepath: str) -> None:
        """Save the vector store to disk"""
        self.vector_store.save(filepath)
    
    def load_vector_store(self, filepath: str) -> None:
        """Load the vector store from disk"""
        self.vector_store.load(filepath)