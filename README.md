<p align="center">
  <img src="logo.jpg" alt="Tinyrag Logo" width="200"/>
</p>


# TinyRag 🚀

[![PyPI version](https://badge.fury.io/py/tinyrag.svg)](https://badge.fury.io/py/tinyrag)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://tinyrag-docs.netlify.app/docs)
[![PyPI Downloads](https://static.pepy.tech/badge/tinyrag)](https://pepy.tech/projects/tinyrag)



A **lightweight, powerful Python library** for **Retrieval-Augmented Generation (RAG)** that works locally without API keys. Features advanced codebase indexing, multiple document formats, and flexible vector storage backends.

> **🎯 Perfect for developers who need RAG capabilities without complexity or mandatory cloud dependencies.**

## 🌟 Key Features

### 🚀 **Works Locally - No API Keys Required**
- **🧠 Local Embeddings**: Uses all-MiniLM-L6-v2 by default
- **🔍 Direct Search**: Query documents without LLM costs
- **⚡ Zero Setup**: Works immediately after installation

### 📚 **Advanced Document Processing** 
- **📄 Multi-Format**: PDF, DOCX, CSV, TXT, and raw text
- **💻 Code Intelligence**: Function-level indexing for 7+ programming languages
- **🧵 Multithreading**: Parallel processing for faster indexing
- **📊 Chunking Strategies**: Smart text segmentation

### 🗄️ **Flexible Storage Options**
- **🔌 Multiple Backends**: Memory, Pickle, Faiss, ChromaDB
- **💾 Persistence**: Automatic or manual data saving
- **⚡ Performance**: Choose speed vs. memory trade-offs
- **🔧 Configuration**: Customizable for any use case

### 💬 **Optional AI Integration**
- **🤖 Custom System Prompts**: Tailor AI behavior for your domain
- **🔗 Provider Support**: OpenAI, Azure, Anthropic, local models
- **💰 Cost Control**: Use only when needed
- **🎯 RAG-Powered Chat**: Contextual AI responses

## 🚀 Quick Start

> **💡 New to TinyRag?** Check out our comprehensive [📖 Documentation](https://tinyrag-docs.netlify.app/docs) with step-by-step guides!

### Installation

```bash
# Basic installation
pip install tinyrag

# With all optional dependencies
pip install tinyrag[all]

# Specific vector stores
pip install tinyrag[faiss]    # High performance
pip install tinyrag[chroma]   # Persistent storage
pip install tinyrag[docs]     # Document processing
```

### Usage Examples

### 🏃‍♂️ 30-Second Example (No API Key Required)

```python
from tinyrag import TinyRag

# 1. Create TinyRag instance
rag = TinyRag()

# 2. Add your content  
rag.add_documents([
    "TinyRag makes RAG simple and powerful.",
    "docs/user_guide.pdf",
    "research_papers/"
])

# 3. Search your content
results = rag.query("How does TinyRag work?", k=3)
for text, score in results:
    print(f"Score: {score:.2f} - {text[:100]}...")
```

**Output:**
```
Score: 0.89 - TinyRag makes RAG simple and powerful.
Score: 0.76 - TinyRag is a lightweight Python library for...
Score: 0.72 - The system processes documents using semantic...
```

### 🤖 AI-Powered Chat (Optional)

```python
from tinyrag import Provider, TinyRag

# Set up AI provider
provider = Provider(
    api_key="sk-your-openai-key",
    model="gpt-4"
)

# Create smart assistant
rag = TinyRag(
    provider=provider,
    system_prompt="You are a helpful technical assistant."
)

# Add knowledge base
rag.add_documents(["technical_docs/", "api_guides/"])
rag.add_codebase("src/")  # Index your codebase

# Get intelligent answers
response = rag.chat("How do I implement user authentication?")
print(response)
# AI response based on your specific docs and code!
```

## 📖 Complete Documentation

**📚 [Full Documentation](docs/README.md)** - Comprehensive guides from beginner to expert

### 🚀 **Getting Started**
- [**Quick Start**](docs/01-quick-start.md) - 5-minute introduction
- [**Installation**](docs/02-installation.md) - Complete setup guide  
- [**Basic Usage**](docs/03-basic-usage.md) - Core features without AI

### 🔧 **Core Features**
- [**Document Processing**](docs/04-document-processing.md) - PDF, DOCX, CSV, TXT
- [**Codebase Indexing**](docs/05-codebase-indexing.md) - Function-level code search
- [**Vector Stores**](docs/06-vector-stores.md) - Choose the right storage
- [**Search & Query**](docs/07-search-query.md) - Similarity search techniques

### 🤖 **AI Integration**
- [**System Prompts**](docs/08-system-prompts.md) - Customize AI behavior
- [**Chat Functionality**](docs/09-chat-functionality.md) - Build conversations
- [**Provider Configuration**](docs/10-provider-config.md) - AI model setup

---

## 🔧 Core API Reference

### Provider Class

```python
from tinyrag import Provider

# 🆓 No API key needed - works locally
provider = Provider(embedding_model="default")

# 🤖 With AI capabilities
provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",                           # GPT-4, GPT-3.5, local models
    embedding_model="text-embedding-ada-002", # or "default" for local
    base_url="https://api.openai.com/v1"     # OpenAI, Azure, custom
)
```

### TinyRag Class

```python
from tinyrag import TinyRag

# 🎛️ Choose your vector store
rag = TinyRag(
    provider=provider,               # Optional: for AI chat
    vector_store="faiss",           # memory, pickle, faiss, chromadb
    chunk_size=500,                 # Text chunk size
    max_workers=4,                  # Parallel processing
    system_prompt="Custom prompt"   # AI behavior
)
```

### 🗄️ Vector Store Comparison

| Store | Performance | Persistence | Memory | Dependencies | Best For |
|-------|-------------|-------------|---------|--------------|----------|
| **Memory** | ⚡ Fast | ❌ None | 📈 High | ✅ None | Development, testing |
| **Pickle** | 🐌 Fair | 💾 Manual | 📊 Medium | ✅ Minimal | Simple projects |
| **Faiss** | 🚀 Excellent | 💾 Manual | 📉 Low | 📦 faiss-cpu | Large datasets, speed |
| **ChromaDB** | ⚡ Good | 🔄 Auto | 📊 Medium | 📦 chromadb | Production, features |

> **💡 Recommendation:** Start with `memory` for development, use `faiss` for production performance.

## 🔧 Essential Methods

```python
# 📄 Document Management
rag.add_documents(["file.pdf", "text"])   # Add any documents
rag.add_codebase("src/")                   # Index code functions
rag.clear_documents()                      # Reset everything

# 🔍 Search & Query (No AI needed)
results = rag.query("search term", k=5)   # Find similar content
code = rag.query("auth function")          # Search code too

# 🤖 AI Chat (Optional)
response = rag.chat("Explain this code")   # Get AI answers
rag.set_system_prompt("Be helpful")        # Customize AI

# 💾 Persistence
rag.save_vector_store("my_data.pkl")       # Save your work
rag.load_vector_store("my_data.pkl")       # Load it back
```

> **📖 [Complete API Reference](docs/18-api-reference.md)** - Full method documentation

## 💻 Code Intelligence

TinyRag indexes your codebase at the **function level** for intelligent code search:

### 🌐 Supported Languages

| Language | Extensions | Detection |
|----------|------------|----------|
| **Python** | `.py` | `def function_name` |
| **JavaScript** | `.js`, `.ts` | `function name()`, `const name =` |
| **Java** | `.java` | `public/private type name()` |
| **C/C++** | `.c`, `.cpp`, `.h` | `return_type function_name()` |
| **Go** | `.go` | `func functionName()` |
| **Rust** | `.rs` | `fn function_name()` |
| **PHP** | `.php` | `function functionName()` |

### 🔍 Code Search Examples

```python
# Index your entire project
rag.add_codebase("my_app/")

# Find authentication code
auth_code = rag.query("user authentication login")

# Database functions
db_code = rag.query("database query SELECT")

# API endpoints
api_code = rag.query("REST API endpoint")

# Get AI explanations (with API key)
response = rag.chat("How does user authentication work?")
# AI analyzes your actual code and explains it!
```

> **💡 [Learn More](docs/05-codebase-indexing.md)** - Advanced code search techniques


## ⚙️ Configuration Examples

### 🚀 Performance Optimized
```python
# Large datasets, maximum speed
rag = TinyRag(
    vector_store="faiss",
    chunk_size=800,
    max_workers=8  # Parallel processing
)
```

### 💾 Production Setup
```python
# Persistent, multi-user ready
rag = TinyRag(
    provider=provider,
    vector_store="chromadb",
    vector_store_config={
        "collection_name": "company_docs",
        "persist_directory": "/data/vectors/"
    }
)
```

### 🤖 Custom AI Assistant
```python
# Domain-specific AI behavior
rag = TinyRag(
    provider=provider,
    system_prompt="""You are a senior software engineer.
    Provide detailed technical explanations with code examples."""
)
```

> **🔧 [Full Configuration Guide](docs/12-configuration.md)** - All options explained

## 📦 Installation

### 🎯 Choose Your Setup

```bash
# 🚀 Quick start (works immediately)
pip install tinyrag

# ⚡ High performance (recommended)
pip install tinyrag[faiss]

# 📄 Document processing (PDF, DOCX)
pip install tinyrag[docs]

# 🗄️ Production database
pip install tinyrag[chroma]

# 🎁 Everything included
pip install tinyrag[all]
```

### 🔧 What Each Option Includes

| Option | Includes | Use Case |
|--------|----------|----------|
| **Base** | Memory store, local embeddings | Development, testing |
| **[faiss]** | + High-performance search | Large datasets |
| **[docs]** | + PDF/DOCX processing | Document analysis |
| **[chroma]** | + Persistent database | Production apps |
| **[all]** | + Everything | Full features |

> **💡 [Installation Guide](docs/02-installation.md)** - Detailed setup instructions

## 🎯 Real-World Use Cases

### 🏢 **Business Applications**
- **📋 Customer Support**: Query company docs and policies
- **📚 Knowledge Management**: Searchable internal documentation
- **🔍 Research Tools**: Semantic search through research papers
- **📊 Report Analysis**: Find insights across business reports

### 👨‍💻 **Developer Tools**
- **🔧 Code Documentation**: Auto-generate code explanations
- **🔍 Legacy Code Explorer**: Understand large codebases
- **📖 API Assistant**: Query technical documentation
- **🧪 Testing Helper**: Find relevant test patterns

### 🎓 **Educational & Research**
- **📚 Study Assistant**: Query textbooks and notes
- **📝 Writing Helper**: Research paper analysis
- **🧠 Learning Companion**: Personalized explanations
- **📊 Data Analysis**: Explore datasets semantically

> **💡 [See Complete Examples](docs/15-examples.md)** - Production-ready applications

---

## 🛠️ Contributing

We welcome contributions! Here's how to get started:

```bash
# 1. Fork and clone
git clone https://github.com/Kenosis01/TinyRag.git
cd TinyRag

# 2. Install development dependencies  
pip install -e ".[all,dev]"

# 3. Run tests
python -m pytest

# 4. Make your changes and submit a PR!
```

### 📋 **Development Setup**
- **Python 3.7+** required
- **Core dependencies**: sentence-transformers, requests, numpy
- **Optional**: faiss-cpu, chromadb, PyPDF2, python-docx

> **🔧 [Development Guide](CONTRIBUTING.md)** - Detailed contributor guidelines

## 🤝 Community & Support

### 📞 **Get Help**
- **📖 [Complete Documentation](docs/README.md)** - Comprehensive guides
- **🐛 [GitHub Issues](https://github.com/Kenosis01/TinyRag/issues)** - Bug reports & feature requests
- **💬 [Discussions](https://github.com/Kenosis01/TinyRag/discussions)** - Community Q&A
- **📋 [FAQ](docs/19-faq.md)** - Common questions answered

### 🎉 **Show Your Support**
- ⭐ **Star this repo** if TinyRag helps you!
- 🐦 **Share on Twitter** - spread the word
- ☕ **[Buy me a coffee](https://buymeacoffee.com/kenosis)** - support development
- 🤝 **Contribute** - help make TinyRag better

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**🚀 TinyRag - Making RAG Simple, Powerful, and Accessible! 🚀**

*Build intelligent search and Q&A systems in minutes, not hours*

[![GitHub stars](https://img.shields.io/github/stars/Kenosis01/TinyRag?style=social)](https://github.com/Kenosis01/TinyRag)
[![PyPI downloads](https://img.shields.io/pypi/dm/tinyrag)](https://pypi.org/project/tinyrag/)
[![GitHub last commit](https://img.shields.io/github/last-commit/Kenosis01/TinyRag)](https://github.com/Kenosis01/TinyRag)

</div>
