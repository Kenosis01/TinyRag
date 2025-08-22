# Document Processing

Complete guide to processing different document formats with TinyRag. Learn how to handle PDF, DOCX, CSV, TXT files and optimize for large datasets.

## 📄 Supported Formats

TinyRag automatically detects and processes these formats:

- **PDF** - Research papers, reports, books
- **DOCX** - Word documents, proposals, documentation  
- **CSV** - Spreadsheets, data files, logs
- **TXT** - Plain text, markdown, code files
- **Raw Text** - Direct string input

## 🚀 Basic Document Processing

### Single Documents

```python
from tinyrag import TinyRag

rag = TinyRag()

# Different file types
rag.add_documents("research_paper.pdf")
rag.add_documents("project_proposal.docx") 
rag.add_documents("customer_data.csv")
rag.add_documents("meeting_notes.txt")

# Search across all documents
results = rag.query("project timeline")
```

### Multiple Documents

```python
# Process multiple files at once
documents = [
    "reports/annual_report.pdf",
    "docs/user_guide.docx",
    "data/sales_data.csv", 
    "notes/requirements.txt"
]

rag = TinyRag()
rag.add_documents(documents)

# Efficient parallel processing
rag.add_documents(documents, use_threading=True)
```

### Entire Directories

```python
# Process all files in a directory
rag.add_documents("document_folder/")

# Recursive directory processing
rag.add_documents("project_docs/")  # Includes subdirectories
```

## 📋 PDF Processing

### Basic PDF Handling

```python
# Simple PDF processing
rag = TinyRag()
rag.add_documents("technical_manual.pdf")

# Search PDF content
results = rag.query("installation procedure")
```

### Large PDF Files

```python
# Optimized for large PDFs
rag = TinyRag(
    chunk_size=400,     # Smaller chunks for large files
    max_workers=4       # Parallel processing
)

# Process large PDF efficiently
rag.add_documents("large_research_paper.pdf")
```

### Multiple PDF Processing

```python
# Process PDF collections
pdf_files = [
    "academic_papers/paper1.pdf",
    "academic_papers/paper2.pdf", 
    "academic_papers/paper3.pdf",
    # ... more PDFs
]

rag = TinyRag(vector_store="faiss")  # Better for large collections
rag.add_documents(pdf_files, use_threading=True)

# Search across all papers
ml_papers = rag.query("machine learning algorithms", k=5)
```

### PDF Processing Options

```python
# Different PDF processing backends available
# TinyRag automatically tries multiple extraction methods:

# 1. PyMuPDF (fastest, recommended)
# pip install PyMuPDF

# 2. pdfminer.six (fallback option)  
# pip install pdfminer.six

# TinyRag chooses the best available option automatically
```

## 📝 DOCX Processing

### Word Document Handling

```python
# Process Word documents
rag = TinyRag()

# Single document
rag.add_documents("project_specification.docx")

# Multiple documents
docx_files = [
    "contracts/agreement1.docx",
    "contracts/agreement2.docx", 
    "proposals/proposal_draft.docx"
]
rag.add_documents(docx_files)
```

### Complex DOCX Documents

```python
# DOCX with tables, images, formatting
rag = TinyRag(chunk_size=600)  # Larger chunks for formatted content

# TinyRag extracts:
# - Main text content
# - Table data
# - Header/footer text
# - (Images are not processed)

rag.add_documents("complex_report.docx")
results = rag.query("quarterly performance metrics")
```

## 📊 CSV Processing

### Structured Data Processing

```python
# CSV files are processed intelligently
rag = TinyRag()

# Add CSV data
rag.add_documents("customer_database.csv")
rag.add_documents("sales_records.csv")

# Search structured data
customer_info = rag.query("customer contact information")
sales_data = rag.query("revenue by product category")
```

### Large CSV Files

```python
# Efficient CSV processing
rag = TinyRag(
    chunk_size=300,     # Smaller chunks for tabular data
    vector_store="faiss"  # Better performance for large datasets
)

# Process large CSV files
rag.add_documents([
    "transactions_2023.csv",   # Large transaction log
    "user_behavior.csv",       # Analytics data
    "inventory_data.csv"       # Product information
])

# Search across all data
results = rag.query("user engagement metrics")
```

### CSV Processing Features

```python
# TinyRag intelligently handles:
# - Column headers as context
# - Row data formatting  
# - Numeric data representation
# - Missing values

# Example CSV content becomes searchable:
# "Product: iPhone 14, Category: Electronics, Price: $999, Stock: 50 units"
```

## 📄 Text File Processing

### Plain Text Files

```python
# Various text formats
text_files = [
    "README.md",
    "requirements.txt", 
    "config.ini",
    "log_file.log",
    "source_code.py"
]

rag = TinyRag()
rag.add_documents(text_files)

# Search text content
results = rag.query("configuration settings")
```

### Large Text Files

```python
# Process large text files efficiently
rag = TinyRag(
    chunk_size=500,
    max_workers=6
)

# Large log files, documentation, etc.
rag.add_documents([
    "application.log",      # 100MB log file
    "documentation.md",     # Large documentation
    "data_export.txt"       # Database export
])
```

## 🎭 Mixed Content Processing

### Combined Document Types

```python
# Process different formats together
mixed_documents = [
    "overview.pdf",              # PDF overview
    "detailed_specs.docx",       # Word specifications  
    "performance_data.csv",      # CSV metrics
    "Quick notes about the project",  # Raw text
    "configuration.txt",         # Text file
    "meeting_transcripts/"       # Directory of files
]

rag = TinyRag(vector_store="faiss")
rag.add_documents(mixed_documents, use_threading=True)

# Search across all content types
results = rag.query("system requirements")
```

### Content Type Analysis

```python
# Analyze what was processed
chunk_count = rag.get_chunk_count()
all_chunks = rag.get_all_chunks()

print(f"Total chunks processed: {chunk_count}")

# Sample some chunks to see content variety
for i, chunk in enumerate(all_chunks[:3]):
    print(f"Chunk {i+1}: {chunk[:100]}...")
```

## ⚡ Performance Optimization

### Chunking Strategies

```python
# Optimize chunk size for content type
document_types = {
    "academic_papers": TinyRag(chunk_size=800),    # Larger chunks for context
    "reference_docs": TinyRag(chunk_size=600),     # Medium chunks for lookup
    "quick_notes": TinyRag(chunk_size=300),        # Smaller chunks for precision
    "data_files": TinyRag(chunk_size=400)          # Optimal for structured data
}

# Use appropriate chunking for each content type
for doc_type, rag_instance in document_types.items():
    rag_instance.add_documents(f"{doc_type}/")
```

### Batch Processing

```python
# Process large document collections in batches
import os

def process_large_collection(directory, batch_size=50):
    rag = TinyRag(
        vector_store="faiss",
        max_workers=8,
        chunk_size=500
    )
    
    # Get all files
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.pdf', '.docx', '.csv', '.txt')):
                all_files.append(os.path.join(root, file))
    
    # Process in batches
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}: {len(batch)} files")
        rag.add_documents(batch, use_threading=True)
    
    return rag

# Process large document library
rag = process_large_collection("document_library/")
```

### Memory Management

```python
# For very large document collections
rag = TinyRag(
    vector_store="faiss",
    chunk_size=400,        # Smaller chunks use less memory
    max_workers=4,         # Limit concurrent processing
    vector_store_config={
        "index_type": "IVFFlat"  # Memory-efficient Faiss index
    }
)

# Process documents efficiently
large_document_list = ["doc1.pdf", "doc2.docx", ...]  # 1000+ documents
rag.add_documents(large_document_list, use_threading=True)
```

## 🔍 Content Analysis

### Processing Statistics

```python
# Monitor processing progress
def add_documents_with_stats(rag, documents):
    import time
    
    start_time = time.time()
    initial_chunks = rag.get_chunk_count()
    
    rag.add_documents(documents, use_threading=True)
    
    end_time = time.time()
    final_chunks = rag.get_chunk_count()
    
    print(f"Processing completed in {end_time - start_time:.2f} seconds")
    print(f"Added {final_chunks - initial_chunks} new chunks")
    print(f"Total chunks: {final_chunks}")

# Use with monitoring
rag = TinyRag()
add_documents_with_stats(rag, ["large_collection/"])
```

### Content Quality Check

```python
# Verify document processing quality
results = rag.query("test query", k=10)

print("Content quality check:")
for i, (text, score) in enumerate(results, 1):
    length = len(text)
    has_structure = any(char in text for char in ['.', ':', ';'])
    
    print(f"{i}. Length: {length:3d} chars, "
          f"Score: {score:.3f}, "
          f"Structured: {has_structure}")
    print(f"   Preview: {text[:60]}...")
```

## 🛠️ Advanced Features

### Custom Text Extraction

```python
# For specialized document types, you can preprocess content
def preprocess_technical_docs(file_path):
    # Custom preprocessing logic
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove unwanted sections, format code blocks, etc.
    processed_content = content.replace("CONFIDENTIAL", "")
    return processed_content

# Add preprocessed content
rag = TinyRag()
processed_text = preprocess_technical_docs("technical_spec.txt")
rag.add_documents([processed_text])
```

### Document Metadata

```python
# Track document sources in results
def search_with_sources(rag, query, k=5):
    results = rag.query(query, k=k)
    
    print(f"Results for: '{query}'")
    for i, (text, score) in enumerate(results, 1):
        # Extract potential source information from text
        lines = text.split('\n')
        context = lines[0] if lines else "Unknown source"
        
        print(f"{i}. Score: {score:.3f}")
        print(f"   Source: {context[:40]}...")
        print(f"   Content: {text[:80]}...")
        print()

# Use with source tracking
search_with_sources(rag, "project requirements")
```

## 🚀 Next Steps

Master document processing and move to advanced features:

- [**Codebase Indexing**](05-codebase-indexing.md) - Search through source code
- [**Vector Stores**](06-vector-stores.md) - Choose optimal storage
- [**Performance**](11-performance.md) - Optimization techniques
- [**Best Practices**](13-best-practices.md) - Production recommendations

---

**Ready for code search?** Try [Codebase Indexing](05-codebase-indexing.md) to search through your source code!