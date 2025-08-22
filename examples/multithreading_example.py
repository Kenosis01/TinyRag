"""
Multithreading example for TinyRag
"""

from tinyrag import TinyRag
import time

def main():
    print("=== TinyRag Multithreading Example ===\n")
    
    # Initialize TinyRag without provider (uses default all-MiniLM-L6-v2)
    rag = TinyRag(
        vector_store="memory",  # Fast for demo
        max_workers=4  # Use 4 threads for processing
    )
    
    # Sample documents to process
    documents = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning algorithms can automatically learn patterns from data without explicit programming.",
        "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently.",
        "Natural language processing enables computers to understand, interpret, and generate human language.",
        "Deep learning uses neural networks with multiple layers to model complex patterns in data.",
        "Retrieval-augmented generation combines information retrieval with language generation for better AI responses.",
        "Embeddings are dense vector representations that capture semantic meaning of text content.",
        "Similarity search finds the most relevant documents based on vector distance metrics and algorithms.",
        "Transformers are a type of neural network architecture particularly effective for NLP tasks.",
        "Large language models are trained on vast amounts of text data to understand language patterns."
    ]
    
    print("=== Processing with Multithreading ===")
    start_time = time.time()
    
    # Add documents with multithreading (default)
    rag.add_documents(documents, use_threading=True)
    
    threading_time = time.time() - start_time
    print(f"Multithreading processing time: {threading_time:.2f} seconds\n")
    
    # Clear and test sequential processing
    rag.clear_documents()
    
    print("=== Processing Sequentially ===")
    start_time = time.time()
    
    # Add documents without multithreading
    rag.add_documents(documents, use_threading=False)
    
    sequential_time = time.time() - start_time
    print(f"Sequential processing time: {sequential_time:.2f} seconds\n")
    
    # Test querying
    print("=== Testing Query Functionality ===")
    query = "What is machine learning?"
    
    results = rag.query(query, k=3, return_scores=True)
    print(f"Query: '{query}'")
    print("Top 3 similar chunks:")
    
    for i, (text, score) in enumerate(results, 1):
        print(f"{i}. Score: {score:.3f}")
        print(f"   Text: {text[:80]}...")
        print()
    
    # Performance comparison
    if sequential_time > 0:
        speedup = sequential_time / threading_time if threading_time > 0 else 1
        print(f"=== Performance Comparison ===")
        print(f"Speedup with multithreading: {speedup:.2f}x")
        print(f"Total chunks processed: {rag.get_chunk_count()}")
    
    print("\n=== Multithreading Example Complete ===")

if __name__ == "__main__":
    main()