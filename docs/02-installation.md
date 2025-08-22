# Installation Guide

Complete guide to installing TinyRag and its dependencies.

## 📦 Basic Installation

### Quick Install

```bash
pip install tinyrag
```

This installs the core library with basic functionality.

### What's Included

- Core TinyRag library
- Local embeddings (all-MiniLM-L6-v2)
- Memory vector store
- Basic text processing

## 🔧 Optional Dependencies

### Document Processing

```bash
# For PDF support
pip install PyMuPDF
# OR alternative PDF processor
pip install pdfminer.six

# For DOCX support
pip install python-docx

# For CSV support
pip install pandas
```

### Vector Stores

```bash
# For Faiss (recommended for production)
pip install faiss-cpu
# OR for GPU support
pip install faiss-gpu

# For ChromaDB
pip install chromadb
```

### API Integration

```bash
# For OpenAI API
pip install openai

# For other APIs (future support)
pip install anthropic
```

## 🎯 Complete Installation

### All Features

```bash
# Install everything at once
pip install tinyrag PyMuPDF python-docx pandas faiss-cpu chromadb openai
```

### Development Setup

```bash
# Clone repository
git clone https://github.com/Kenosis01/TinyRag.git
cd TinyRag

# Install in development mode
pip install -e .

# Install all dependencies
pip install -r requirements.txt
```

## 🏗️ Installation Options

### Minimal (No External Dependencies)

```bash
pip install tinyrag
```

**Use case**: Basic text processing, memory vector store only

### Standard (Document Processing)

```bash
pip install tinyrag PyMuPDF python-docx pandas
```

**Use case**: Process PDF, DOCX, CSV files with local embeddings

### Performance (High-Speed Vector Store)

```bash
pip install tinyrag PyMuPDF python-docx pandas faiss-cpu
```

**Use case**: Large document collections, production applications

### Complete (All Features)

```bash
pip install tinyrag PyMuPDF python-docx pandas faiss-cpu chromadb openai
```

**Use case**: Full RAG applications with AI chat

## 🐍 Python Version Requirements

- **Python 3.8+** (required)
- **Python 3.9-3.11** (recommended)
- **Python 3.12** (compatible)

### Check Your Python Version

```bash
python --version
```

## 🖥️ Operating System Support

### Windows

```bash
# Standard installation
pip install tinyrag

# For Faiss on Windows
pip install faiss-cpu
```

### macOS

```bash
# Standard installation
pip install tinyrag

# For Apple Silicon (M1/M2)
pip install faiss-cpu
```

### Linux

```bash
# Standard installation
pip install tinyrag

# For CUDA support (optional)
pip install faiss-gpu
```

## 🔍 Verify Installation

### Quick Test

```python
# test_installation.py
from tinyrag import TinyRag

# Create instance
rag = TinyRag()
print("✅ TinyRag installed successfully!")

# Test basic functionality
rag.add_documents(["Test document for verification"])
results = rag.query("test")
print(f"✅ Basic functionality working: {len(results)} results found")
```

### Run Test

```bash
python test_installation.py
```

**Expected Output:**
```
✅ TinyRag installed successfully!
✓ Processed: Test document for verification (1 chunks)
Generating embeddings for 1 chunks...
✓ Added 1 chunks to vector store
✅ Basic functionality working: 1 results found
```

### Test with Documents

```python
# test_documents.py
from tinyrag import TinyRag

rag = TinyRag()

# Test different input types
test_data = [
    "TinyRag supports multiple document formats.",
    "It works with PDF, DOCX, and text files.",
    "Vector stores provide efficient similarity search."
]

rag.add_documents(test_data)
results = rag.query("document formats", k=2)

print("✅ Document processing test passed!")
for text, score in results:
    print(f"Score: {score:.3f} - {text}")
```

## 🚨 Troubleshooting

### Common Issues

#### ImportError: No module named 'sentence_transformers'

```bash
pip install sentence-transformers
```

#### PDF Processing Not Working

```bash
# Try different PDF processors
pip install PyMuPDF
# OR
pip install pdfminer.six
```

#### Faiss Installation Fails

```bash
# Try conda instead of pip
conda install -c conda-forge faiss-cpu

# Or use alternative vector store
# TinyRag works with memory/pickle stores too
```

#### Memory Issues with Large Files

```python
# Use smaller chunk sizes
rag = TinyRag(chunk_size=300)

# Enable multithreading
rag.add_documents(files, use_threading=True)
```

### Getting Help

If you encounter issues:

1. Check [Troubleshooting Guide](14-troubleshooting.md)
2. Search [GitHub Issues](https://github.com/Kenosis01/TinyRag/issues)
3. Create a new issue with error details

## 🚀 Next Steps

After successful installation:

- [**Quick Start**](01-quick-start.md) - Your first TinyRag application
- [**Basic Usage**](03-basic-usage.md) - Core functionality examples
- [**Document Processing**](04-document-processing.md) - Working with files

---

**Installation complete?** Try the [Quick Start](01-quick-start.md) guide!