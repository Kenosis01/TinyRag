# Codebase Indexing

Learn how to index entire codebases and search for specific functions, classes, and code patterns with TinyRag.

## 🎯 What is Codebase Indexing?

TinyRag can analyze your entire codebase at the function level, making it searchable. This is perfect for:
- Code documentation and exploration
- Finding specific functions or patterns
- Onboarding new developers
- Code review and analysis

## 🚀 Basic Codebase Indexing

### Simple Project Indexing

```python
from tinyrag import TinyRag

# Create TinyRag instance
rag = TinyRag(vector_store="faiss")  # Faiss recommended for code

# Index entire project
rag.add_codebase("path/to/your/project/")

# Search for functions
results = rag.query("authentication function", k=5)
for text, score in results:
    print(f"Score: {score:.2f}")
    print(f"Code: {text[:200]}...")
    print("-" * 50)
```

### Specific Directory Indexing

```python
# Index specific directories
rag.add_codebase("src/")           # Source code only
rag.add_codebase("lib/auth/")      # Authentication module
rag.add_codebase("tests/")         # Test files

# Search across all indexed code
db_functions = rag.query("database connection")
auth_functions = rag.query("user login")
test_cases = rag.query("unit test for payment")
```

## 📁 Supported Languages

TinyRag supports function-level indexing for:

| Language   | File Extensions | Function Detection |
|------------|----------------|-------------------|
| Python     | `.py`          | `def function_name` |
| JavaScript | `.js`, `.ts`   | `function name`, `const name =` |
| Java       | `.java`        | `public/private type name()` |
| C++        | `.cpp`, `.h`   | `return_type function_name()` |
| Go         | `.go`          | `func functionName()` |
| Rust       | `.rs`          | `fn function_name()` |
| PHP        | `.php`         | `function functionName()` |

### Language Examples

```python
# Python project
rag = TinyRag()
rag.add_codebase("python_project/")
python_results = rag.query("data validation function")

# JavaScript project  
rag_js = TinyRag()
rag_js.add_codebase("frontend/src/")
js_results = rag_js.query("API call function")

# Mixed language project
rag_mixed = TinyRag()
rag_mixed.add_codebase("full_stack_app/")
backend_code = rag_mixed.query("database query Python")
frontend_code = rag_mixed.query("user interface JavaScript")
```

## 🔍 Advanced Search Patterns

### Function-Specific Searches

```python
rag = TinyRag()
rag.add_codebase("my_project/")

# Find specific function types
auth_functions = rag.query("authentication login function")
db_functions = rag.query("database query select")
api_endpoints = rag.query("REST API endpoint")
error_handlers = rag.query("exception error handling")
validators = rag.query("input validation")
```

### Pattern-Based Searches

```python
# Security-related code
security_code = rag.query("password hash encryption")
auth_code = rag.query("JWT token authentication") 
sql_code = rag.query("SQL injection prevention")

# Performance-related code
cache_code = rag.query("caching mechanism")
async_code = rag.query("async await function")
optimize_code = rag.query("performance optimization")

# Testing patterns
unit_tests = rag.query("unit test function")
mock_tests = rag.query("mock object testing")
integration_tests = rag.query("integration test API")
```

## 🎯 Practical Use Cases

### 1. Code Documentation Generator

```python
from tinyrag import TinyRag, Provider

# Setup with LLM for documentation
provider = Provider(api_key="sk-your-key")
rag = TinyRag(provider=provider)

# Index codebase
rag.add_codebase("src/")

# Generate documentation for modules
modules = ["authentication", "database", "API", "validation"]

for module in modules:
    print(f"\n=== {module.upper()} MODULE ===")
    
    # Find relevant functions
    functions = rag.query(f"{module} function", k=3)
    
    # Generate documentation
    context = "\n".join([func[0] for func in functions])
    doc = rag.chat(f"Document the {module} functions in this code:\n{context}")
    print(doc)
```

### 2. Code Review Assistant

```python
# Setup code review assistant
review_prompt = """You are a code reviewer. Analyze the provided code and suggest improvements for:
- Security vulnerabilities
- Performance issues  
- Code quality and readability
- Best practices"""

rag = TinyRag(provider=provider, system_prompt=review_prompt)
rag.add_codebase("src/")

# Review specific areas
areas_to_review = [
    "user input validation",
    "database query functions", 
    "authentication logic",
    "error handling"
]

for area in areas_to_review:
    print(f"\n=== REVIEWING: {area.upper()} ===")
    
    code_results = rag.query(area, k=2)
    if code_results:
        code_sample = code_results[0][0]  # Get top result
        review = rag.chat(f"Review this {area} code:\n{code_sample}")
        print(review)
```

### 3. Developer Onboarding

```python
# Help new developers understand codebase
onboarding_prompt = """You are helping a new developer understand this codebase. 
Explain code clearly with context about how it fits into the larger system."""

rag = TinyRag(provider=provider, system_prompt=onboarding_prompt)
rag.add_codebase("entire_project/")

# Common onboarding questions
onboarding_questions = [
    "How does user authentication work?",
    "Where is the database connection logic?",
    "How are API routes defined?",
    "What testing framework is used?",
    "How is error handling implemented?"
]

print("=== NEW DEVELOPER GUIDE ===\n")
for question in onboarding_questions:
    print(f"Q: {question}")
    answer = rag.chat(question)
    print(f"A: {answer}\n")
```

### 4. Code Migration Assistant

```python
# Help with code migration or refactoring
migration_prompt = """You are helping migrate code. Identify patterns, dependencies, 
and suggest migration strategies based on the code structure."""

rag = TinyRag(provider=provider, system_prompt=migration_prompt)
rag.add_codebase("legacy_system/")

# Migration analysis
migration_queries = [
    "deprecated function patterns",
    "database access patterns",
    "configuration management",
    "third party dependencies"
]

print("=== MIGRATION ANALYSIS ===\n")
for query in migration_queries:
    results = rag.query(query, k=3)
    analysis = rag.chat(f"Analyze these {query} for migration:\n" + 
                       "\n".join([r[0] for r in results]))
    print(f"**{query.title()}:**\n{analysis}\n")
```

## ⚙️ Configuration Options

### Chunking Strategy for Code

```python
# Optimize for code structure
rag = TinyRag(
    vector_store="faiss",
    chunk_size=800,        # Larger chunks for complete functions
    max_workers=8          # Parallel processing for large codebases
)

# Index with progress tracking
import os
def index_with_progress(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(('.py', '.js', '.java', '.cpp', '.go', '.rs', '.php')):
                files.append(os.path.join(root, filename))
    
    print(f"Found {len(files)} code files to index...")
    rag.add_codebase(directory)
    print("Indexing complete!")

index_with_progress("large_project/")
```

### Language-Specific Configuration

```python
# Python-focused indexing
python_rag = TinyRag(chunk_size=600)  # Good for Python functions
python_rag.add_codebase("python_app/", file_extensions=['.py'])

# JavaScript-focused indexing  
js_rag = TinyRag(chunk_size=500)      # Good for JS functions
js_rag.add_codebase("react_app/src/", file_extensions=['.js', '.jsx', '.ts', '.tsx'])
```

## 🚀 Performance Tips

### 1. Use Appropriate Vector Store

```python
# For small codebases (< 1000 functions)
rag = TinyRag(vector_store="memory")

# For medium codebases (1000-10000 functions)  
rag = TinyRag(vector_store="faiss")

# For large codebases (> 10000 functions)
rag = TinyRag(vector_store="chromadb")
```

### 2. Optimize Search Queries

```python
# ✅ Good: Specific and descriptive
specific_queries = [
    "user authentication login function",
    "database SELECT query with JOIN",
    "REST API POST endpoint validation",
    "async file upload handler"
]

# ❌ Avoid: Too generic
generic_queries = [
    "function",
    "code", 
    "method",
    "class"
]
```

### 3. Batch Processing

```python
# Process multiple directories efficiently
directories = ["src/auth/", "src/api/", "src/db/", "src/utils/"]

rag = TinyRag(vector_store="faiss", max_workers=4)

# Index all at once for better performance
for directory in directories:
    rag.add_codebase(directory)

# Now search across all indexed code
results = rag.query("authentication middleware", k=10)
```

## 🔧 Troubleshooting

### Common Issues

**Empty Results:**
```python
# Check if files were indexed
results = rag.query("any function", k=50)
if not results:
    print("No functions found. Check file paths and extensions.")
    
# Verify supported file types
import os
code_files = [f for f in os.listdir("src/") 
              if f.endswith(('.py', '.js', '.java', '.cpp', '.go', '.rs', '.php'))]
print(f"Found {len(code_files)} code files")
```

**Poor Search Results:**
```python
# Try broader queries first
broad_results = rag.query("function", k=10)
print(f"Total functions indexed: {len(broad_results)}")

# Then narrow down
specific_results = rag.query("authentication function", k=5)
```

**Memory Issues with Large Codebases:**
```python
# Use streaming approach for very large projects
def index_large_codebase(root_dir):
    rag = TinyRag(vector_store="chromadb", max_workers=2)
    
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            print(f"Indexing {subdir}...")
            rag.add_codebase(subdir_path)
    
    return rag
```

## 🎓 Next Steps

Ready to enhance your code search capabilities:

- [**Vector Stores**](06-vector-stores.md) - Choose the right storage for your codebase size
- [**Search & Query**](07-search-query.md) - Advanced search techniques
- [**Chat Functionality**](09-chat-functionality.md) - AI-powered code explanations
- [**Performance Optimization**](11-performance.md) - Handle large codebases efficiently

---

**Want to see codebase indexing in real applications?** Check [Real-world Examples](15-examples.md) for complete code search systems!