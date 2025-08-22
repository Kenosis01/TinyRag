# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-08-22

### Added
- **Codebase Indexing**: Function-level indexing for multiple programming languages
  - Support for Python, JavaScript, Java, C/C++, Go, Rust, PHP
  - Automatic function and class extraction using regex patterns
  - Language detection based on file extensions
  - Metadata enrichment (file path, language, function name, type)
- **New Methods**:
  - `add_codebase(path)` - Index entire codebases or single files
  - `search_code(query, language=None)` - Search code functions with optional language filtering
  - `get_function_by_name(name)` - Find specific functions by name
- **Enhanced Processing**:
  - Multithreaded codebase processing for large projects
  - Smart directory scanning with exclusion of common non-source directories
  - Error handling for malformed code files
- **Examples**: New codebase indexing example with sample code files

### Changed
- Updated contact email to transformtrails@gmail.com
- Enhanced documentation with codebase indexing section
- Updated package description to include codebase indexing
- Added code-related keywords for better discoverability

## [0.2.0] -  2025-08-22

### Added
- **Optional Provider**: Provider is now optional, defaults to local embeddings
- **Multithreading Support**: Parallel document processing for faster indexing
- **Enhanced Error Handling**: Better progress feedback and error messages
- **Thread Safety**: Thread-safe operations with automatic locking
- **New Parameters**:
  - `max_workers` for controlling thread pool size
  - `use_threading` parameter in `add_documents()`

### Changed
- Provider API key is now optional (defaults to None)
- Default embedding model uses all-MiniLM-L6-v2 without API key requirement
- Improved document processing with detailed logging
- Enhanced chat method with API key validation

## [0.1.0] -  2025-08-21

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