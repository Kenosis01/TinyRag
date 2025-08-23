# Quick Start

Get started with TinyRag in less than 5 minutes! This guide shows the absolute basics.

## 🚀 Super Quick Example

```python
from tinyrag import TinyRag

# 1. Create TinyRag instance (no API key needed!)
rag = TinyRag()

# 2. Add some documents
rag.add_documents([
    "TinyRag is a Python library for RAG applications.",
    "It supports PDF, DOCX, and text files.",
    "Vector stores include Memory, Faiss, and ChromaDB."
])

# 3. Search for information
results = rag.query("What file formats are supported?")
print(results)
```

**Output:**
```
[('It supports PDF, DOCX, and text files.', 0.87)]
```

## 📦 Installation

```bash
pip install tinyrag
```

That's it! No complicated setup required.

## 🎯 What Just Happened?

1. **No API Key**: TinyRag works locally using free embeddings
2. **Instant Search**: Added text and searched immediately
3. **Relevance Score**: Results include similarity scores (0-1)

## 🔥 Next Steps

### Add Real Documents

```python
from tinyrag import TinyRag

rag = TinyRag()

# Add actual files
rag.add_documents([
    "path/to/document.pdf",
    "path/to/notes.txt",
    "path/to/research.docx"
])

# Search across all documents
results = rag.query("machine learning", k=3)
for text, score in results:
    print(f"Score: {score:.2f} - {text[:100]}...")
```

### Add Your Codebase

```python
# Index your entire codebase
rag.add_codebase("path/to/project/")

# Find specific functions
auth_code = rag.query("authentication function")
db_code = rag.query("database connection")
```

### Use AI Chat (Optional)

```python
from tinyrag import Provider, TinyRag

# Set up AI provider
provider = Provider(api_key="sk-your-key")
rag = TinyRag(provider=provider)

# Add documents
rag.add_documents(["docs/", "research.pdf"])

# Get AI-powered answers
response = rag.chat("Summarize the key findings")
print(response)
```

## 🎨 Customize System Prompt

```python
# Create expert assistant
custom_prompt = "You are a technical expert. Provide detailed, accurate explanations."

rag = TinyRag(
    provider=provider,
    system_prompt=custom_prompt
)

# Or update later
rag.set_system_prompt("You are a helpful coding assistant.")
```

## 🔧 Multiple Embedding Providers

```python
from tinyrag import Provider

# Local models (no API key needed)
provider = Provider.create_local_provider("all-mpnet-base-v2")  # Higher quality
rag = TinyRag(provider=provider)

# OpenAI embeddings (requires API key)
provider = Provider.create_openai_provider("sk-your-key")
rag = TinyRag(provider=provider)

# Ollama local server (requires Ollama running)
provider = Provider.create_ollama_provider("nomic-embed-text")
rag = TinyRag(provider=provider)
```

## 📦 Smart Document Caching

```python
# Caching is enabled by default - speeds up repeated operations
rag = TinyRag(enable_cache=True)  # Default: True

# First time - processes and caches documents
rag.add_documents(["large_dataset/"])

# Second time - loads from cache (up to 10x faster!)
rag.add_documents(["large_dataset/"])  # Uses cached version

# Check cache status
cache_info = rag.get_cache_info()
print(f"Cached documents: {cache_info['total_documents']}")
print(f"Cache size: {cache_info['cache_size_mb']:.1f} MB")
```

## ⚡ Performance Tips

```python
# For large datasets
rag = TinyRag(
    vector_store="faiss",    # Faster for large datasets
    max_workers=8           # More parallel processing
)

# Process many documents efficiently
rag.add_documents(file_list, use_threading=True)
```

## 🏃‍♂️ Ready to Learn More?

- **[Multi-Provider Embeddings](11-multi-provider-embeddings.md)** - Local, OpenAI, Ollama, custom
- **[Basic Usage](03-basic-usage.md)** - More examples without AI
- **[System Prompts](08-system-prompts.md)** - Customize AI behavior
- **[Document Processing](04-document-processing.md)** - Work with different file types
- **[Vector Stores](06-vector-stores.md)** - Choose the right storage

---

**Need help?** Check the [FAQ](19-faq.md) or [Troubleshooting](14-troubleshooting.md) guide.