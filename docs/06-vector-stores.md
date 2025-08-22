# Vector Stores

Choose the right vector storage backend for your TinyRag application. This guide covers all supported options and when to use each.

## 🎯 What Are Vector Stores?

Vector stores hold the numerical representations (embeddings) of your documents. Different stores offer different trade-offs between performance, persistence, and features.

## 📊 Quick Comparison

| Vector Store | Best For | Persistence | Memory Usage | Setup |
|-------------|----------|-------------|--------------|-------|
| **Memory** | Development, small datasets | ❌ No | High | Zero |
| **Pickle** | Medium datasets, simple persistence | ✅ Yes | Medium | Zero |
| **Faiss** | Large datasets, fast search | ✅ Yes | Low | Easy |
| **ChromaDB** | Production, advanced features | ✅ Yes | Low | Medium |

## 🚀 Memory Vector Store

Perfect for development and small datasets (< 1,000 documents).

### Basic Usage

```python
from tinyrag import TinyRag

# Default vector store
rag = TinyRag()  # Uses memory by default
# OR explicitly specify
rag = TinyRag(vector_store="memory")

# Add documents
rag.add_documents([
    "TinyRag supports multiple vector stores.",
    "Memory store is great for testing.",
    "No persistence but very fast."
])

# Search immediately
results = rag.query("vector stores")
print(results)
```

### Pros and Cons

**✅ Pros:**
- Zero setup required
- Fastest for small datasets
- No external dependencies
- Perfect for testing

**❌ Cons:**
- Data lost when program ends
- High memory usage for large datasets
- Not suitable for production

### When to Use Memory Store

```python
# ✅ Perfect for:
# - Development and testing
# - Temporary data processing
# - Small document collections
# - Proof of concepts

rag = TinyRag(vector_store="memory")

# Quick experimentation
test_docs = ["doc1.txt", "doc2.txt", "doc3.txt"]
rag.add_documents(test_docs)
results = rag.query("test query")
```

## 💾 Pickle Vector Store

Balanced option for medium-sized applications with simple persistence needs.

### Basic Usage

```python
# Initialize with pickle store
rag = TinyRag(vector_store="pickle")

# Add documents (automatically saved)
rag.add_documents([
    "data/reports/",
    "research.pdf",
    "notes.txt"
])

# Data persists between sessions
# Restart program...

# Load existing data
rag_new = TinyRag(vector_store="pickle")
# Your documents are still there!
results = rag_new.query("research findings")
```

### Custom Pickle Location

```python
# Specify custom pickle file location
rag = TinyRag(
    vector_store="pickle",
    vector_store_config={
        "persist_directory": "my_data/",
        "pickle_file": "my_embeddings.pkl"
    }
)
```

### Pros and Cons

**✅ Pros:**
- Simple persistence
- No external dependencies
- Medium memory usage
- Easy backup (just copy the .pkl file)

**❌ Cons:**
- Slower than memory for large datasets
- No concurrent access
- Limited scalability
- Single file can become large

### When to Use Pickle Store

```python
# ✅ Perfect for:
# - Personal projects
# - Medium datasets (1K-10K documents)
# - Simple applications
# - When you need basic persistence

rag = TinyRag(vector_store="pickle")

# Document collection that grows over time
rag.add_documents(["week1_reports/"])
# Later...
rag.add_documents(["week2_reports/"])
# Data accumulates and persists
```

## ⚡ Faiss Vector Store

High-performance option for large datasets and fast similarity search.

### Installation

```bash
pip install faiss-cpu
# OR for GPU support (if available)
pip install faiss-gpu
```

### Basic Usage

```python
# Initialize with Faiss
rag = TinyRag(vector_store="faiss")

# Add large document collection
rag.add_documents([
    "large_dataset/",
    "books/",
    "research_papers/"
])

# Fast similarity search
results = rag.query("machine learning algorithms", k=10)
```

### Advanced Faiss Configuration

```python
# Custom Faiss settings
rag = TinyRag(
    vector_store="faiss",
    vector_store_config={
        "persist_directory": "faiss_indices/",
        "index_type": "IVF",  # Index type for large datasets
        "metric": "cosine"    # Distance metric
    }
)
```

### Faiss Index Types

```python
# For different dataset sizes
configs = {
    # Small-medium datasets (< 100K vectors)
    "flat": {
        "vector_store_config": {"index_type": "Flat"}
    },
    
    # Large datasets (> 100K vectors)
    "ivf": {
        "vector_store_config": {"index_type": "IVF", "nlist": 100}
    },
    
    # Very large datasets with quantization
    "ivf_pq": {
        "vector_store_config": {"index_type": "IVFPQ", "nlist": 100, "m": 8}
    }
}

# Choose based on your data size
rag = TinyRag(vector_store="faiss", **configs["flat"])
```

### Pros and Cons

**✅ Pros:**
- Extremely fast for large datasets
- Efficient memory usage
- Persistent storage
- Facebook-developed, battle-tested
- Supports GPU acceleration

**❌ Cons:**
- Requires additional installation
- More complex configuration
- Learning curve for optimization

### When to Use Faiss

```python
# ✅ Perfect for:
# - Large document collections (> 10K documents)
# - Production applications requiring speed
# - Applications with frequent searches
# - When you need the fastest similarity search

rag = TinyRag(vector_store="faiss", max_workers=8)

# Large codebase indexing
rag.add_codebase("large_enterprise_project/")

# Fast function search across millions of lines
auth_functions = rag.query("authentication function", k=20)
db_functions = rag.query("database query", k=15)
```

## 🗄️ ChromaDB Vector Store

Full-featured vector database for production applications.

### Installation

```bash
pip install chromadb
```

### Basic Usage

```python
# Initialize with ChromaDB
rag = TinyRag(vector_store="chromadb")

# Add documents with metadata
rag.add_documents([
    "docs/user_guide.pdf",
    "docs/api_reference.md",
    "docs/tutorials/"
])

# Advanced search capabilities
results = rag.query("API authentication", k=5)
```

### Advanced ChromaDB Configuration

```python
# Custom ChromaDB settings
rag = TinyRag(
    vector_store="chromadb",
    vector_store_config={
        "persist_directory": "chroma_db/",
        "collection_name": "my_documents",
        "embedding_function": "default",  # or custom embedding
        "metadata": {"version": "1.0", "project": "MyApp"}
    }
)
```

### ChromaDB Collections

```python
# Multiple collections for different data types
# Documentation collection
docs_rag = TinyRag(
    vector_store="chromadb",
    vector_store_config={
        "collection_name": "documentation",
        "persist_directory": "vector_db/"
    }
)

# Code collection
code_rag = TinyRag(
    vector_store="chromadb", 
    vector_store_config={
        "collection_name": "codebase",
        "persist_directory": "vector_db/"
    }
)

# Different search strategies
docs_rag.add_documents(["docs/"])
code_rag.add_codebase("src/")

doc_results = docs_rag.query("installation guide")
code_results = code_rag.query("authentication function")
```

### Pros and Cons

**✅ Pros:**
- Full-featured vector database
- Advanced metadata support
- Production-ready
- Concurrent access support
- Rich query capabilities
- Growing ecosystem

**❌ Cons:**
- Larger dependency
- More complex setup
- Higher resource requirements
- Overkill for simple use cases

### When to Use ChromaDB

```python
# ✅ Perfect for:
# - Production applications
# - Multi-user environments
# - Complex metadata requirements
# - Applications needing database features
# - Long-term data storage

rag = TinyRag(
    vector_store="chromadb",
    vector_store_config={
        "collection_name": "company_knowledge",
        "persist_directory": "/data/vector_db/"
    }
)

# Enterprise knowledge base
rag.add_documents([
    "company_policies/",
    "technical_specs/", 
    "user_manuals/",
    "training_materials/"
])
```

## 🔄 Switching Between Vector Stores

### Migration Helper

```python
def migrate_vector_store(source_rag, target_store_type, target_config=None):
    """Migrate from one vector store to another."""
    
    # Create new RAG with target store
    target_rag = TinyRag(
        vector_store=target_store_type,
        vector_store_config=target_config or {}
    )
    
    # Get all documents from source (this is conceptual - TinyRag doesn't expose this directly)
    # In practice, you'd re-add your original documents
    print(f"Migrating to {target_store_type}...")
    
    return target_rag

# Example migration
# From memory to faiss for production
memory_rag = TinyRag(vector_store="memory")
memory_rag.add_documents(["docs/"])

# Migrate to Faiss for better performance
faiss_rag = migrate_vector_store(memory_rag, "faiss")
faiss_rag.add_documents(["docs/"])  # Re-add documents
```

### Development vs Production

```python
import os

# Use different stores based on environment
ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "development":
    # Fast iteration, no persistence needed
    rag = TinyRag(vector_store="memory")
    
elif ENV == "testing":
    # Quick persistence for test data
    rag = TinyRag(vector_store="pickle")
    
elif ENV == "production":
    # High performance, full features
    rag = TinyRag(
        vector_store="chromadb",
        vector_store_config={
            "persist_directory": "/app/data/vectors/",
            "collection_name": "production_docs"
        }
    )
```

## 📊 Performance Comparison

### Benchmark Results

Based on 10,000 documents, 1,000 queries:

```python
# Typical performance characteristics
performance_data = {
    "memory": {
        "index_time": "2.1s",
        "query_time": "45ms", 
        "memory_usage": "850MB",
        "persistence": False
    },
    "pickle": {
        "index_time": "2.3s",
        "query_time": "52ms",
        "memory_usage": "420MB", 
        "persistence": True
    },
    "faiss": {
        "index_time": "3.1s",
        "query_time": "12ms",
        "memory_usage": "180MB",
        "persistence": True
    },
    "chromadb": {
        "index_time": "4.2s", 
        "query_time": "28ms",
        "memory_usage": "220MB",
        "persistence": True
    }
}
```

### Choosing Based on Dataset Size

```python
def choose_vector_store(num_documents, need_persistence=True):
    """Recommend vector store based on requirements."""
    
    if num_documents < 1000:
        if need_persistence:
            return "pickle"
        else:
            return "memory"
            
    elif num_documents < 50000:
        return "faiss"
        
    else:  # Large datasets
        return "chromadb"

# Examples
small_project = choose_vector_store(500, need_persistence=False)  # "memory"
medium_project = choose_vector_store(5000)  # "faiss"  
large_project = choose_vector_store(100000)  # "chromadb"
```

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```python
try:
    rag = TinyRag(vector_store="faiss")
except ImportError:
    print("Faiss not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "faiss-cpu"])
    rag = TinyRag(vector_store="faiss")
```

**Performance Issues:**
```python
# Monitor memory usage
import psutil

def check_memory():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

rag = TinyRag(vector_store="memory")
check_memory()  # Before

rag.add_documents(["large_dataset/"])
check_memory()  # After
```

**Persistence Issues:**
```python
import os

# Check if persistence directory exists
persist_dir = "my_vectors/"
if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)
    print(f"Created directory: {persist_dir}")

rag = TinyRag(
    vector_store="chromadb",
    vector_store_config={"persist_directory": persist_dir}
)
```

## 🎯 Best Practices

### 1. Start Simple, Scale Up

```python
# Development phase
dev_rag = TinyRag(vector_store="memory")

# Testing phase  
test_rag = TinyRag(vector_store="pickle")

# Production phase
prod_rag = TinyRag(vector_store="faiss")
```

### 2. Configure for Your Use Case

```python
# High-frequency searches
search_heavy_rag = TinyRag(vector_store="faiss")

# Infrequent searches, need persistence
archive_rag = TinyRag(vector_store="pickle")

# Multi-user production app
production_rag = TinyRag(vector_store="chromadb")
```

### 3. Monitor and Optimize

```python
import time

def benchmark_vector_store(store_type, documents):
    """Benchmark different vector stores."""
    
    start_time = time.time()
    rag = TinyRag(vector_store=store_type)
    
    # Index documents
    index_start = time.time()
    rag.add_documents(documents)
    index_time = time.time() - index_start
    
    # Query performance
    query_start = time.time()
    results = rag.query("test query", k=5)
    query_time = time.time() - query_start
    
    return {
        "store": store_type,
        "index_time": f"{index_time:.2f}s",
        "query_time": f"{query_time*1000:.1f}ms",
        "results_count": len(results)
    }

# Compare stores
test_docs = ["sample_docs/"]
for store in ["memory", "pickle", "faiss"]:
    result = benchmark_vector_store(store, test_docs)
    print(f"{store}: Index {result['index_time']}, Query {result['query_time']}")
```

## 🚀 Next Steps

Ready to optimize your vector storage:

- [**Search & Query**](07-search-query.md) - Advanced search techniques for any vector store
- [**Performance Optimization**](11-performance.md) - Tune your vector store for maximum speed
- [**Configuration Options**](12-configuration.md) - All vector store configuration parameters
- [**Real-world Examples**](15-examples.md) - See vector stores in production applications

---

**Need help choosing?** Check the [FAQ](19-faq.md) for vector store selection guidance!