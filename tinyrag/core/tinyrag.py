"""
Main TinyRag class for Retrieval-Augmented Generation
"""

from typing import Union, List, Optional, Dict, Any, Tuple
from pathlib import Path
import concurrent.futures
from threading import Lock
from sentence_transformers import SentenceTransformer

from .provider import Provider
from .text_utils import extract_text, chunk_text
from .code_parser import CodeParser
from ..vector_stores import (
    FaissVectorStore, 
    MemoryVectorStore, 
    PickleVectorStore, 
    ChromaVectorStore
)


class TinyRag:
    def __init__(
        self, 
        provider: Optional[Provider] = None, 
        vector_store: str = "faiss", 
        chunk_size: int = 500,
        vector_store_config: Optional[Dict[str, Any]] = None,
        max_workers: Optional[int] = None,
        system_prompt: Optional[str] = None
    ):
        """Initialize TinyRag with optional provider and vector store
        
        Args:
            provider: Optional Provider instance for API calls. If None, only local embeddings will be used
            vector_store: Type of vector store ("faiss", "memory", "pickle", "chroma")
            chunk_size: Size of text chunks for embedding
            vector_store_config: Additional configuration for vector store
            max_workers: Maximum number of threads for parallel processing. If None, uses default ThreadPoolExecutor behavior
            system_prompt: Custom system prompt for LLM chat. If None, uses default prompt
        """
        # Initialize provider or create default one
        if provider is None:
            self.provider = Provider()  # Uses default embedding model (all-MiniLM-L6-v2)
        else:
            self.provider = provider
            
        self.chunk_size = chunk_size
        self.max_workers = max_workers
        self._lock = Lock()  # For thread-safe operations
        
        # Set system prompt
        self.system_prompt = system_prompt or (
            "You are a helpful assistant. Use the provided context to answer questions accurately. "
            "If the context doesn't contain relevant information, say so."
        )
        
        # Determine embedding dimension based on model
        if self.provider.embedding_model == "default":
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
    
    def _process_single_document(self, item: Union[str, Path]) -> List[str]:
        """Process a single document and return its chunks"""
        try:
            # Use enhanced text extraction with progress indication
            text = extract_text(item, show_progress=True)
            if text and text.strip():
                chunks = chunk_text(text, self.chunk_size)
                if chunks:
                    item_name = item if isinstance(item, str) and len(str(item)) < 50 else str(item)[:50] + '...'
                    print(f"✓ Processed: {item_name} ({len(chunks)} chunks)")
                    return chunks
                else:
                    print(f"⚠ No chunks created from: {item}")
            else:
                print(f"⚠ No text content found in: {item}")
        except Exception as e:
            print(f"⚠ Warning: Failed to process {item}: {e}")
        return []

    def add_documents(self, data: Union[str, Path, List[Union[str, Path]]], use_threading: bool = True) -> None:
        """Add documents from text, file paths, or mixed list with optional multithreading
        
        Args:
            data: Can be:
                - Single file path: "document.pdf"
                - Single text string: "This is raw text"
                - List of files: ["doc1.pdf", "doc2.txt", "doc3.docx"]
                - List of texts: ["Text 1", "Text 2", "Text 3"]
                - Mixed list: ["document.pdf", "Raw text", "another.txt"]
            use_threading: Whether to use multithreading for processing multiple documents
        """
        all_chunks = []
        
        if isinstance(data, (list, tuple)):
            if use_threading and len(data) > 1:
                # Use multithreading for multiple documents
                print(f"Processing {len(data)} documents with multithreading (max_workers: {self.max_workers})...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    # Submit all documents for processing
                    future_to_item = {executor.submit(self._process_single_document, item): item for item in data}
                    
                    # Collect results as they complete
                    for future in concurrent.futures.as_completed(future_to_item):
                        chunks = future.result()
                        if chunks:
                            with self._lock:  # Thread-safe addition
                                all_chunks.extend(chunks)
            else:
                # Sequential processing
                print(f"Processing {len(data)} documents sequentially...")
                for item in data:
                    chunks = self._process_single_document(item)
                    all_chunks.extend(chunks)
        else:
            # Handle single text or file path
            chunks = self._process_single_document(data)
            all_chunks.extend(chunks)
        
        if all_chunks:
            print(f"Generating embeddings for {len(all_chunks)} chunks...")
            # Generate embeddings for all chunks
            embeddings = self.provider.get_embeddings(all_chunks)
            
            # Add to vector store (thread-safe)
            with self._lock:
                self.vector_store.add_vectors(embeddings, all_chunks)
            print(f"✓ Added {len(all_chunks)} chunks to vector store")
        else:
            print("⚠ No valid content found to add")
    
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
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt for LLM chat
        
        Args:
            prompt: New system prompt to use for chat completions
        """
        self.system_prompt = prompt
    
    def get_system_prompt(self) -> str:
        """Get the current system prompt
        
        Returns:
            Current system prompt string
        """
        return self.system_prompt
    
    def chat(self, query: str, k: int = 3) -> str:
        """Retrieve relevant chunks and generate an answer using LLM"""
        # Check if API key is available for chat completion
        if not self.provider.api_key:
            raise ValueError(
                "No API key provided. Chat functionality requires an API key. "
                "Initialize TinyRag with: Provider(api_key='your-key') or use query() method for similarity search only."
            )
        
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
                "content": self.system_prompt
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
    
    def add_code_file(self, file_path: str) -> None:
        """Add a single code file by parsing and indexing its functions
        
        Args:
            file_path: Path to the code file to process
        """
        from pathlib import Path
        
        file_path_obj = Path(file_path)
        
        # Check if file exists
        if not file_path_obj.exists():
            print(f"⚠ File not found: {file_path}")
            return
        
        # Check if it's a file (not directory)
        if not file_path_obj.is_file():
            print(f"⚠ Path is not a file: {file_path}")
            return
        
        # Check if it's a supported code file
        if not CodeParser.is_code_file(str(file_path)):
            print(f"⚠ Unsupported file type: {file_path}")
            return
        
        print(f"Processing code file: {file_path}")
        
        # Parse the file
        functions = CodeParser.parse_file(str(file_path))
        
        if functions and functions[0]['type'] != 'error':
            # Format functions for embedding
            formatted_chunks = []
            for func in functions:
                chunk = f"File: {func['file']}\nLanguage: {func['language']}\nType: {func['type']}\nName: {func['name']}\nCode:\n{func['content']}"
                formatted_chunks.append(chunk)
            
            print(f"Generating embeddings for {len(formatted_chunks)} code functions...")
            
            # Generate embeddings for all chunks
            embeddings = self.provider.get_embeddings(formatted_chunks)
            
            # Add to vector store
            self.vector_store.add_vectors(embeddings, formatted_chunks)
            
            print(f"✓ Added {len(formatted_chunks)} code functions from {file_path_obj.name} to vector store")
        else:
            print(f"⚠ No valid code functions found in: {file_path}")
    
    def add_codebase(self, path: str, recursive: bool = True, use_threading: bool = True) -> None:
        """Add codebase from directory or single file by parsing and indexing code functions
        
        Args:
            path: Path to directory containing code files OR path to a single code file
            recursive: Whether to scan subdirectories recursively (only applies to directories)
            use_threading: Whether to use multithreading for processing (only applies to directories with multiple files)
        
        Examples:
            # Process a single code file
            rag.add_codebase("path/to/my_file.py")
            
            # Process a directory
            rag.add_codebase("path/to/project/")
            
            # Process directory non-recursively
            rag.add_codebase("path/to/project/", recursive=False)
        """
        from pathlib import Path
        
        path_obj = Path(path)
        
        # Check if path exists
        if not path_obj.exists():
            print(f"⚠ Path not found: {path}")
            return
        
        # Handle single file
        if path_obj.is_file():
            self.add_code_file(str(path))
            return
        
        # Handle directory
        if not path_obj.is_dir():
            print(f"⚠ Path is neither a file nor a directory: {path}")
            return
        
        # Scan directory for code files
        code_files = CodeParser.scan_directory(path, recursive=recursive)
        
        if not code_files:
            print(f"⚠ No code files found in: {path}")
            return
        
        print(f"Found {len(code_files)} code files in {path}")
        
        all_functions = []
        
        if use_threading and len(code_files) > 1:
            # Use multithreading for multiple files
            print(f"Processing {len(code_files)} code files with multithreading...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all files for processing
                future_to_file = {executor.submit(CodeParser.parse_file, file_path): file_path for file_path in code_files}
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_file):
                    functions = future.result()
                    if functions and functions[0]['type'] != 'error':
                        with self._lock:  # Thread-safe addition
                            all_functions.extend(functions)
        else:
            # Sequential processing
            print(f"Processing {len(code_files)} code files sequentially...")
            for file_path in code_files:
                functions = CodeParser.parse_file(file_path)
                if functions and functions[0]['type'] != 'error':
                    all_functions.extend(functions)
        
        if all_functions:
            # Format functions for embedding
            formatted_chunks = []
            for func in all_functions:
                chunk = f"File: {func['file']}\nLanguage: {func['language']}\nType: {func['type']}\nName: {func['name']}\nCode:\n{func['content']}"
                formatted_chunks.append(chunk)
            
            print(f"Generating embeddings for {len(formatted_chunks)} code functions...")
            
            # Generate embeddings for all chunks
            embeddings = self.provider.get_embeddings(formatted_chunks)
            
            # Add to vector store (thread-safe)
            with self._lock:
                self.vector_store.add_vectors(embeddings, formatted_chunks)
            
            print(f"✓ Added {len(formatted_chunks)} code functions to vector store")
        else:
            print("⚠ No valid code functions found to add")
    
    def search_code(self, query: str, k: int = 5, language: Optional[str] = None, min_score: float = 0.0) -> List[Tuple[str, float]]:
        """Search for code functions
        
        Args:
            query: Search query
            k: Number of results to return
            language: Filter by programming language (optional)
            min_score: Minimum similarity score threshold
            
        Returns:
            List of (code_chunk, score) tuples
        """
        # Generate embedding for the query
        query_embedding = self.provider.get_embeddings([query])[0]
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, k=k * 2)  # Get more results for filtering
        
        # Filter by language if specified
        if language:
            filtered_results = []
            for text, score in results:
                if f"Language: {language.lower()}" in text.lower() and score >= min_score:
                    filtered_results.append((text, score))
                    if len(filtered_results) >= k:
                        break
            return filtered_results[:k]
        
        # Filter by minimum score
        return [(text, score) for text, score in results if score >= min_score][:k]
    
    def get_function_by_name(self, function_name: str, k: int = 5) -> List[Tuple[str, float]]:
        """Search for functions by name
        
        Args:
            function_name: Name of function to search for
            k: Number of results to return
            
        Returns:
            List of (code_chunk, score) tuples
        """
        # Generate embedding for the function name
        query_embedding = self.provider.get_embeddings([function_name])[0]
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, k=k)
        
        # Filter to only include exact name matches
        exact_matches = []
        for text, score in results:
            if f"Name: {function_name}" in text:
                exact_matches.append((text, score))
        
        return exact_matches[:k]