# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release of TinyRag
- Core Provider class for API management and embeddings
- TinyRag class with document management and querying capabilities
- Multiple vector store backends:
  - Memory store (pure NumPy, no dependencies)
  - Faiss store (high-performance similarity search)
  - ChromaDB store (persistent vector database)
  - Pickle store (simple file-based storage)
- Text extraction support for multiple formats:
  - PDF files (via PyPDF2)
  - DOCX files (via python-docx)
  - TXT files
  - Raw text strings
- Text chunking with overlapping segments
- Embedding generation using:
  - Local Sentence Transformers (default)
  - Provider API endpoints (OpenAI, etc.)
- Query functionality without LLM requirement
- Chat completion with retrieved context
- Document persistence and loading
- Comprehensive examples and documentation

### Features
- `query()` method for similarity search without LLM
- `chat()` method for LLM-powered responses with context
- `search_documents()` with score filtering
- `get_similar_chunks()` for finding similar content
- Vector store save/load functionality
- Configurable chunk sizes and retrieval parameters
- Optional dependencies for different use cases

### Documentation
- Comprehensive README with examples
- API reference documentation
- Installation instructions for different use cases
- Usage examples for all major features