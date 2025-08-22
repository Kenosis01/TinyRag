from tinyrag import Provider, TinyRag

# Example 1: Basic usage without LLM (no API key needed)
rag = TinyRag()  # Uses default all-MiniLM-L6-v2 embeddings

# Add multiple documents with multithreading
rag.add_documents([
    "path/to/doc1.pdf",
    "path/to/doc2.txt", 
    "Raw text content here"
])

# Query without LLM
results = rag.query("What is this about?")
print("Similar chunks:", results)

# Example 2: Index codebase at function level
rag.add_codebase("path/to/your/codebase")  # Index entire codebase

# Search for specific functions
code_results = rag.search_code("authentication function", k=3)
print("Code functions:", code_results)

# Search by programming language
python_funcs = rag.search_code("user management", language="python")
print("Python functions:", python_funcs)

# Example 3: With LLM for chat functionality
provider = Provider(
    api_key="sk-xxxxxx",
    model="gpt-4",
    embedding_model="default",
    base_url="https://api.openai.com/v1"
)

rag_with_llm = TinyRag(provider=provider, vector_store="faiss", max_workers=4)

rag_with_llm.add_documents([
    "path/to/docs_or_raw_text",
    "Another document",
    "More content"
])

# Also index codebase for code-aware chat
rag_with_llm.add_codebase("path/to/codebase")

response = rag_with_llm.chat("Summarize the documents and explain the main functions in the codebase.")
print(response)