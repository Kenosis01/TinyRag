# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.5] - 2025-08-23

### Added
- **Multi-Provider Embedding Support**: Revolutionary embedding provider system
  - **Local Embeddings**: sentence-transformers integration (all-MiniLM-L6-v2, all-mpnet-base-v2, multilingual models)
  - **OpenAI Embeddings**: text-embedding-ada-002 support with API integration
  - **Ollama Embeddings**: Local Ollama server support for privacy-focused deployments
  - **Custom Embedding Functions**: Support for user-defined embedding providers
  - **Hybrid Configurations**: Mix local embeddings with cloud chat models for cost optimization

- **Structured Responses with Source Citations**: Game-changing output formatting
  - **Multiple Output Formats**: Text, JSON, Markdown, and structured object formats
  - **Automatic Source Citations**: [1], [2] citation numbering with detailed source tracking
  - **Source Metadata**: File names, document types, chunk positions, relevance scores
  - **Confidence Scoring**: Automatic confidence calculation based on source relevance
  - **Processing Metrics**: Response time tracking and performance analytics

- **Enhanced Query Methods**:
  - `query_structured()` - Search with structured output and citations (no LLM required)
  - `chat_structured()` - LLM chat with automatic citations and source attribution
  - `query(..., return_metadata=True)` - Enhanced search with metadata support

- **Intelligent Document Caching System**: Performance breakthrough for repeated operations
  - **Smart Cache Keys**: Content + modification time + embedding configuration hashing
  - **Configuration-Aware**: Separate cache entries for different embedding providers/models
  - **Automatic Invalidation**: Detects document changes and configuration modifications
  - **Cache Management**: `clear_cache()`, `get_cache_info()`, `cleanup_old_cache()` methods
  - **Thread-Safe Operations**: Concurrent cache access with proper locking

- **Enhanced Vector Store Architecture**: Extended all vector stores with metadata support
  - **Metadata Tracking**: Store and retrieve document metadata alongside embeddings
  - **Backward Compatibility**: Seamless upgrade path for existing vector stores
  - **Source Attribution**: Track original file paths, document types, and chunk positions

- **Advanced Provider Configuration**:
  - Factory methods: `create_local_provider()`, `create_openai_provider()`, `create_ollama_provider()`
  - Dynamic embedding dimension detection
  - Provider information utilities: `get_provider_info()`
  - Environment variable integration for secure API key management

### Enhanced
- **TinyRag Constructor**: New parameters for caching and multi-provider support
  - `enable_cache` - Toggle intelligent document caching
  - `cache_dir` - Custom cache directory location
  - Enhanced provider integration with automatic configuration detection

- **Document Processing Pipeline**: Complete metadata integration
  - Automatic metadata generation for all document types
  - Source file tracking with full path and basename information
  - Document type detection (PDF, DOCX, TXT, raw text)
  - Chunk position tracking within documents

- **Response Quality**: Dramatically improved output organization
  - Clean, structured formatting for better readability
  - Proper source attribution eliminates "messy text" issues
  - Professional citation format suitable for research and business use
  - Configurable output formats for different use cases

### Changed
- **Version Bump**: Updated from 0.2.0 to 0.3.5 to reflect major feature additions
- **Provider Architecture**: Complete rewrite to support multiple embedding backends
- **Vector Store Interface**: Extended base class with metadata support
- **Import Structure**: Added `StructuredResponse`, `Source`, `ResponseFormatter` to main imports

### Examples
- **Enhanced Demo Script**: `examples/structured_response_demo.py`
  - Comprehensive demonstration of all new features
  - Interactive examples with and without API keys
  - Format comparison (text, JSON, markdown)
  - Performance benchmarking and feature showcase

### Documentation
- **Updated Provider Configuration**: Complete rewrite of `docs/10-provider-config.md`
  - Multi-provider setup examples
  - Structured response documentation
  - Performance optimization guidelines
  - Environment-specific configurations
- **Enhanced Test Suite**: Updated `test.py` with structured response demonstrations

### Performance Improvements
- **Caching System**: Eliminates redundant document processing
- **Multi-Provider Architecture**: Optimized embedding generation
- **Structured Output**: Efficient formatting with minimal overhead
- **Metadata Tracking**: Lightweight source attribution system

### Technical Notes
- Maintains full backward compatibility with existing code
- All new features are opt-in through method selection
- Zero breaking changes to existing API
- Enhanced error handling and user feedback throughout

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