# Basic Usage

Learn TinyRag fundamentals without needing API keys or LLM integration. This guide covers core functionality using only local embeddings.

## 🎯 Core Concepts

TinyRag works in three simple steps:
1. **Initialize** - Create a TinyRag instance
2. **Add Content** - Load documents or text
3. **Search** - Find relevant information

## 📝 Simple Text Processing

### Basic Example

```python
from tinyrag import TinyRag

# Create TinyRag instance (uses local embeddings)
rag = TinyRag()

# Add text content
rag.add_documents([
    "Python is a programming language.",
    "Machine learning uses algorithms to find patterns.",
    "TinyRag helps build RAG applications quickly."
])

# Search for relevant content
results = rag.query("programming")
print(results)
```

**Output:**
```
[('Python is a programming language.', 0.72)]
```

### Working with Larger Text

```python
# Add longer content
long_text = """
TinyRag is designed for Retrieval-Augmented Generation applications.
It supports multiple vector stores including Memory, Faiss, and ChromaDB.
The library can process various document formats like PDF and DOCX.
Local embeddings work without requiring API keys.
"""

rag = TinyRag()
rag.add_documents([long_text])

# Search with different queries
queries = [
    "vector stores",
    "document formats", 
    "API keys"
]

for query in queries:
    results = rag.query(query, k=1)
    print(f"Query: '{query}'")
    print(f"Result: {results[0][0][:60]}... (Score: {results[0][1]:.3f})")
    print()
```

## 📁 File Processing

### Single Files

```python
from tinyrag import TinyRag

rag = TinyRag()

# Process individual files
rag.add_documents("document.pdf")
rag.add_documents("notes.txt")
rag.add_documents("research.docx")

# Search across all added files
results = rag.query("machine learning", k=3)
```

### Multiple Files

```python
# Process multiple files at once
file_list = [
    "reports/annual_report.pdf",
    "docs/user_manual.docx",
    "data/customer_feedback.csv",
    "notes/meeting_notes.txt"
]

rag = TinyRag()
rag.add_documents(file_list)

# Search with relevance filtering
results = rag.search_documents(
    query="customer satisfaction",
    k=5,
    min_score=0.6  # Only high-relevance results
)
```

### Mixed Content

```python
# Mix files and raw text
mixed_data = [
    "important_document.pdf",
    "Raw text: This is important information.",
    "presentation.docx",
    "Quick note: Remember to update the database."
]

rag = TinyRag()
rag.add_documents(mixed_data)

# TinyRag automatically handles different input types
results = rag.query("database")
```

## 🚀 Performance Options

### Multithreading

```python
# Enable multithreading for faster processing
rag = TinyRag(max_workers=4)

# Process many files efficiently
large_file_list = ["file1.pdf", "file2.docx", "file3.txt", ...]
rag.add_documents(large_file_list, use_threading=True)
```

### Chunk Size Optimization

```python
# Smaller chunks = more precise search
rag = TinyRag(chunk_size=300)

# Larger chunks = more context per result  
rag = TinyRag(chunk_size=800)

# Default is 500 characters
```

## 🎛️ Vector Store Options

### Memory Store (Default)

```python
# Fast, temporary storage
rag = TinyRag(vector_store="memory")

# Good for: Development, testing, small datasets
```

### Persistent Storage

```python
# Automatically saves to disk
rag = TinyRag(
    vector_store="pickle",
    vector_store_config={"file_path": "my_knowledge_base"}
)

# Data persists between sessions
rag.add_documents(["important_docs/"])

# Later sessions automatically load existing data
rag2 = TinyRag(
    vector_store="pickle", 
    vector_store_config={"file_path": "my_knowledge_base"}
)
# rag2 now contains previously added documents
```

### High-Performance Storage

```python
# Faiss vector store (requires: pip install faiss-cpu)
rag = TinyRag(vector_store="faiss")

# Best for: Large datasets, production use
```

## 🔍 Search Options

### Basic Search

```python
# Simple similarity search
results = rag.query("search term")
# Returns: [('text chunk', score), ...]
```

### Relevance Filtering

```python
# Only get high-relevance results
good_results = rag.search_documents(
    query="artificial intelligence",
    k=10,
    min_score=0.7
)
```

### Score Analysis

```python
results = rag.query("machine learning", k=5)

for text, score in results:
    relevance = "High" if score > 0.8 else "Medium" if score > 0.5 else "Low"
    print(f"{relevance} relevance ({score:.3f}): {text[:60]}...")
```

### Different Result Formats

```python
# With scores (default)
results_with_scores = rag.query("data science", return_scores=True)
# Returns: [('text', 0.85), ('text', 0.72), ...]

# Just text
just_text = rag.query("data science", return_scores=False) 
# Returns: ['text', 'text', ...]
```

## 📊 Information Management

### Check Status

```python
# See how many chunks are stored
chunk_count = rag.get_chunk_count()
print(f"Stored chunks: {chunk_count}")

# Get all stored text
all_chunks = rag.get_all_chunks()
print(f"First chunk: {all_chunks[0][:100]}...")
```

### Clear Data

```python
# Remove all stored documents
rag.clear_documents()
print(f"Chunks after clearing: {rag.get_chunk_count()}")
```

### Save and Load

```python
# Save current state
rag.save_vector_store("my_backup.pkl")

# Load into new instance
rag2 = TinyRag()
rag2.load_vector_store("my_backup.pkl")
```

## 🧪 Practical Examples

### Document Q&A System

```python
from tinyrag import TinyRag

# Create knowledge base
rag = TinyRag(vector_store="pickle", 
              vector_store_config={"file_path": "company_kb"})

# Add company documents
rag.add_documents([
    "policies/hr_handbook.pdf",
    "docs/technical_specs.docx", 
    "guides/user_manual.txt"
])

# Interactive search
while True:
    question = input("Ask a question (or 'quit'): ")
    if question.lower() == 'quit':
        break
        
    results = rag.search_documents(question, k=3, min_score=0.6)
    
    if results:
        print("\nRelevant information found:")
        for i, (text, score) in enumerate(results, 1):
            print(f"{i}. Score: {score:.3f}")
            print(f"   {text[:150]}...")
            print()
    else:
        print("No relevant information found.")
```

### Content Discovery

```python
# Build searchable content library
rag = TinyRag(vector_store="faiss")

# Add diverse content
content_types = [
    "research_papers/",
    "blog_posts/", 
    "documentation/",
    "meeting_transcripts/"
]

for content_dir in content_types:
    rag.add_documents(content_dir)

# Explore content with different queries
exploration_queries = [
    "machine learning algorithms",
    "user experience design", 
    "data visualization",
    "project management"
]

for query in exploration_queries:
    print(f"\n=== {query.title()} ===")
    results = rag.query(query, k=3)
    
    for text, score in results:
        print(f"• {text[:100]}... ({score:.3f})")
```

## ⚡ Performance Tips

### Batch Processing

```python
# Process files in batches for memory efficiency
import os

def process_directory_in_batches(directory, batch_size=20):
    rag = TinyRag(vector_store="faiss")
    files = [f for f in os.listdir(directory) if f.endswith(('.pdf', '.txt', '.docx'))]
    
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        batch_paths = [os.path.join(directory, f) for f in batch]
        
        print(f"Processing batch {i//batch_size + 1}")
        rag.add_documents(batch_paths, use_threading=True)
    
    return rag

# Use for large document collections
rag = process_directory_in_batches("large_document_collection/")
```

### Memory Management

```python
# For large datasets, use appropriate chunk sizes
rag = TinyRag(
    vector_store="faiss",
    chunk_size=400,  # Smaller chunks for better memory usage
    max_workers=4    # Limit concurrent processing
)
```

## 🚀 Next Steps

Now that you understand the basics:

- [**Document Processing**](04-document-processing.md) - Deep dive into file handling
- [**Codebase Indexing**](05-codebase-indexing.md) - Search through code
- [**Vector Stores**](06-vector-stores.md) - Choose the right storage
- [**System Prompts**](08-system-prompts.md) - Add AI capabilities

---

**Ready for AI features?** Check out [System Prompts](08-system-prompts.md) to add LLM functionality!