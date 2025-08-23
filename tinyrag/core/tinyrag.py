"""
Main TinyRag class for Retrieval-Augmented Generation with multi-provider support and caching
"""

from typing import Union, List, Optional, Dict, Any, Tuple
from pathlib import Path
import concurrent.futures
from threading import Lock
import time
import os
from sentence_transformers import SentenceTransformer

from .provider import Provider
from .text_utils import extract_text, chunk_text
from .code_parser import CodeParser
from .document_cache import DocumentCache
from .structured_response import StructuredResponse, Source, ResponseFormatter
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
        system_prompt: Optional[str] = None,
        enable_cache: bool = True,
        cache_dir: str = ".tinyrag_cache"
    ):
        """Initialize TinyRag with optional provider, vector store, and caching
        
        Args:
            provider: Optional Provider instance for API calls. If None, uses local embeddings
            vector_store: Type of vector store ("faiss", "memory", "pickle", "chroma")
            chunk_size: Size of text chunks for embedding
            vector_store_config: Additional configuration for vector store
            max_workers: Maximum number of threads for parallel processing
            system_prompt: Custom system prompt for LLM chat
            enable_cache: Enable document caching to avoid re-processing
            cache_dir: Directory for cache files
        """
        # Initialize provider or create default one
        if provider is None:
            self.provider = Provider()  # Uses default local embedding model
        else:
            self.provider = provider
            
        self.chunk_size = chunk_size
        self.max_workers = max_workers
        self._lock = Lock()  # For thread-safe operations
        
        # Initialize caching
        if enable_cache:
            self.cache = DocumentCache(cache_dir)
            print(f"📦 Document cache enabled: {cache_dir}")
        else:
            self.cache = DocumentCache("").disable_cache()  # Null cache
            print("🚫 Document cache disabled")
        
        # Set system prompt
        self.system_prompt = system_prompt or (
            "You are a helpful assistant. Use the provided context to answer questions accurately. "
            "If the context doesn't contain relevant information, say so."
        )
        
        # Get embedding dimension from provider
        try:
            dimension = self.provider.get_embedding_dimension()
            print(f"🧠 Embedding dimension: {dimension}")
        except Exception as e:
            print(f"⚠️  Could not determine embedding dimension: {e}")
            # Fallback dimensions
            if hasattr(self.provider, 'embedding_provider'):
                if self.provider.embedding_provider == "openai":
                    dimension = 1536
                else:
                    dimension = 384  # Default local embedding dimension
            else:
                dimension = 384
        
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
    
    def _process_single_document(self, item: Union[str, Path]) -> Tuple[List[str], List[List[float]], List[Dict[str, Any]], bool]:
        """Process a single document and return its chunks, embeddings, metadata, and cache status"""
        try:
            # Check if document is cached
            if self.cache.is_cached(str(item), self.provider, self.chunk_size):
                cached_data = self.cache.get_cached_data(str(item), self.provider, self.chunk_size)
                if cached_data:
                    chunks, embeddings = cached_data
                    # Generate metadata for cached chunks
                    metadata = self._generate_metadata(item, chunks)
                    item_name = item if isinstance(item, str) and len(str(item)) < 50 else str(item)[:50] + '...'
                    print(f"📦 Loaded from cache: {item_name} ({len(chunks)} chunks)")
                    return chunks, embeddings, metadata, True
            
            # Process document if not cached
            text = extract_text(item, show_progress=True)
            if text and text.strip():
                chunks = chunk_text(text, self.chunk_size)
                if chunks:
                    # Generate embeddings
                    embeddings = self.provider.get_embeddings(chunks)
                    
                    # Generate metadata for chunks
                    metadata = self._generate_metadata(item, chunks)
                    
                    # Cache the results
                    self.cache.cache_document(str(item), chunks, embeddings, self.provider, self.chunk_size)
                    
                    item_name = item if isinstance(item, str) and len(str(item)) < 50 else str(item)[:50] + '...'
                    print(f"✓ Processed: {item_name} ({len(chunks)} chunks)")
                    return chunks, embeddings, metadata, False
                else:
                    print(f"⚠ No chunks created from: {item}")
            else:
                print(f"⚠ No text content found in: {item}")
        except Exception as e:
            print(f"⚠ Warning: Failed to process {item}: {e}")
        return [], [], [], False

    def _generate_metadata(self, item: Union[str, Path], chunks: List[str]) -> List[Dict[str, Any]]:
        """Generate metadata for chunks from a document"""
        metadata_list = []
        
        # Determine if item is a file path or raw text
        is_file = isinstance(item, (str, Path)) and os.path.isfile(str(item))
        
        for i, chunk in enumerate(chunks):
            metadata = {
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            
            if is_file:
                file_path = Path(item)
                metadata.update({
                    'source_file': file_path.name,
                    'source_path': str(file_path),
                    'document_type': file_path.suffix.lower().lstrip('.') if file_path.suffix else 'txt',
                    'file_size': file_path.stat().st_size if file_path.exists() else None
                })
            else:
                # Raw text input
                metadata.update({
                    'source_file': None,
                    'source_path': None,
                    'document_type': 'text',
                    'is_raw_text': True
                })
            
            metadata_list.append(metadata)
        
        return metadata_list

    def add_documents(self, data: Union[str, Path, List[Union[str, Path]]], use_threading: bool = True) -> None:
        """Add documents from text, file paths, or mixed list with intelligent caching
        
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
        all_embeddings = []
        all_metadata = []
        cached_count = 0
        processed_count = 0
        
        if isinstance(data, (list, tuple)):
            if use_threading and len(data) > 1:
                # Use multithreading for multiple documents
                print(f"Processing {len(data)} documents with multithreading (max_workers: {self.max_workers})...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    # Submit all documents for processing
                    future_to_item = {executor.submit(self._process_single_document, item): item for item in data}
                    
                    # Collect results as they complete
                    for future in concurrent.futures.as_completed(future_to_item):
                        chunks, embeddings, metadata, was_cached = future.result()
                        if chunks:
                            with self._lock:  # Thread-safe addition
                                all_chunks.extend(chunks)
                                all_embeddings.extend(embeddings)
                                all_metadata.extend(metadata)
                                if was_cached:
                                    cached_count += 1
                                else:
                                    processed_count += 1
            else:
                # Sequential processing
                print(f"Processing {len(data)} documents sequentially...")
                for item in data:
                    chunks, embeddings, metadata, was_cached = self._process_single_document(item)
                    if chunks:
                        all_chunks.extend(chunks)
                        all_embeddings.extend(embeddings)
                        all_metadata.extend(metadata)
                        if was_cached:
                            cached_count += 1
                        else:
                            processed_count += 1
        else:
            # Handle single text or file path
            chunks, embeddings, metadata, was_cached = self._process_single_document(data)
            all_chunks.extend(chunks)
            all_embeddings.extend(embeddings)
            all_metadata.extend(metadata)
            if was_cached:
                cached_count = 1
            else:
                processed_count = 1
        
        if all_chunks:
            # Add to vector store (embeddings are already generated)
            with self._lock:
                self.vector_store.add_vectors(all_embeddings, all_chunks, all_metadata)
            
            # Summary
            total_chunks = len(all_chunks)
            print(f"✅ Added {total_chunks} chunks to vector store")
            if cached_count > 0:
                print(f"📦 {cached_count} documents loaded from cache")
            if processed_count > 0:
                print(f"🔄 {processed_count} documents processed and cached")
        else:
            print("⚠ No valid content found to add")
    
    def query(self, query: str, k: int = 5, return_scores: bool = True, return_metadata: bool = False) -> Union[List[str], List[Tuple[str, float]], List[Tuple[str, float, Optional[Dict[str, Any]]]]]:
        """Query the vector store without using LLM - just return similar chunks
        
        Args:
            query: Query string to search for
            k: Number of similar chunks to return
            return_scores: If True, return (text, score) tuples; if False, return just text
            return_metadata: If True, return (text, score, metadata) tuples
            
        Returns:
            List of similar text chunks, optionally with similarity scores and metadata
        """
        # Generate embedding for the query
        query_embedding = self.provider.get_embeddings([query])[0]
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, k=k, return_metadata=True)
        
        if return_metadata:
            return results  # Returns [(text, score, metadata), ...]
        elif return_scores:
            return [(text, score) for text, score, metadata in results]  # Returns [(text, score), ...]
        else:
            return [text for text, score, metadata in results]  # Returns [text, ...]
    
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
    
    def query_structured(self, query: str, k: int = 5, format_type: str = "text") -> Union[str, Dict[str, Any], StructuredResponse]:
        """Query with structured output including sources and citations
        
        Args:
            query: Query string to search for
            k: Number of similar chunks to return
            format_type: Output format - "text", "json", "markdown", or "structured"
            
        Returns:
            Formatted response with sources and citations
        """
        start_time = time.time()
        
        # Get results with metadata
        results = self.query(query, k=k, return_metadata=True)
        
        processing_time = time.time() - start_time
        
        # Format using ResponseFormatter
        return ResponseFormatter.format_search_results(
            query=query,
            results=results,
            format_type=format_type
        )
    
    def chat_structured(self, query: str, k: int = 3, format_type: str = "text") -> Union[str, Dict[str, Any], StructuredResponse]:
        """Enhanced chat with structured output including sources and citations
        
        Args:
            query: Query string
            k: Number of context chunks to use
            format_type: Output format - "text", "json", "markdown", or "structured"
            
        Returns:
            Structured response with answer, sources, and citations
        """
        start_time = time.time()
        
        # Check if API key is available for chat completion
        if not self.provider.api_key:
            raise ValueError(
                "No API key provided. Chat functionality requires an API key. "
                "Initialize TinyRag with: Provider(api_key='your-key') or use query() method for similarity search only."
            )
        
        # Generate embedding for the query
        query_embedding = self.provider.get_embeddings([query])[0]
        
        # Search for relevant chunks with metadata
        results = self.vector_store.search(query_embedding, k=k, return_metadata=True)
        
        if not results:
            context = "No relevant documents found."
            sources = []
        else:
            # Combine retrieved chunks as context for LLM
            context_chunks = [text for text, score, metadata in results]
            context = "\n\n".join(context_chunks)
            sources = results
        
        # Enhanced system prompt for structured responses
        enhanced_prompt = f"""{self.system_prompt}
        
IMPORTANT: When providing answers:
1. Base your response strictly on the provided context
2. Be specific and detailed in your explanations
3. If information is not in the context, clearly state this
4. Organize your response in a clear, structured manner"""
        
        # Create messages for chat completion
        messages = [
            {
                "role": "system",
                "content": enhanced_prompt
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
        
        # Generate response using the provider
        response = self.provider.chat_completion(messages)
        
        processing_time = time.time() - start_time
        
        # Calculate confidence based on source relevance scores
        confidence = None
        if sources:
            avg_score = sum(score for _, score, _ in sources) / len(sources)
            confidence = min(avg_score * 1.2, 1.0)  # Scale and cap at 1.0
        
        # Format using ResponseFormatter
        return ResponseFormatter.format_chat_response(
            query=query,
            answer=response,
            sources=sources,
            confidence=confidence,
            processing_time=processing_time,
            format_type=format_type
        )
    
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
    
    def clear_cache(self) -> None:
        """Clear document cache"""
        self.cache.clear_cache()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the document cache"""
        return self.cache.get_cache_info()
    
    def cleanup_old_cache(self, days: int = 30) -> None:
        """Clean up cache entries older than specified days"""
        self.cache.cleanup_old_cache(days)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider configuration"""
        return {
            "embedding_provider": getattr(self.provider, 'embedding_provider', 'unknown'),
            "embedding_model": getattr(self.provider, 'embedding_model', 'unknown'),
            "chat_model": getattr(self.provider, 'model', 'unknown'),
            "embedding_dimension": getattr(self.provider, 'embedding_dimension', 'unknown'),
            "base_url": getattr(self.provider, 'base_url', ''),
            "ollama_base_url": getattr(self.provider, 'ollama_base_url', ''),
            "has_api_key": bool(getattr(self.provider, 'api_key', None))
        }
    
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