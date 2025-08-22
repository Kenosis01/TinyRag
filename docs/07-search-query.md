# Search & Query

Master TinyRag's search capabilities without LLM integration. Perfect for building search engines, document discovery, and content exploration systems.

## 🎯 What is Search & Query?

TinyRag's core search functionality finds the most similar documents to your query using semantic embeddings. No API keys required - everything runs locally.

## 🚀 Basic Search

### Simple Document Search

```python
from tinyrag import TinyRag

# Create TinyRag instance
rag = TinyRag()

# Add documents
rag.add_documents([
    "Python is a programming language known for simplicity.",
    "JavaScript runs in web browsers and servers.",
    "Machine learning algorithms learn from data patterns.",
    "Database systems store and retrieve structured information."
])

# Basic search
results = rag.query("programming language")
print(results)
# Output: [('Python is a programming language...', 0.85), ('JavaScript runs in web browsers...', 0.72)]
```

### Understanding Results

```python
# Query returns list of tuples: (text, similarity_score)
results = rag.query("data science", k=3)

for text, score in results:
    print(f"Similarity: {score:.2f}")
    print(f"Text: {text}")
    print("-" * 50)

# Similarity scores range from 0 (no similarity) to 1 (identical)
# Scores above 0.7 are typically very relevant
# Scores above 0.8 are highly relevant
```

## 🔍 Advanced Search Parameters

### Control Number of Results

```python
# Get different numbers of results
top_3 = rag.query("machine learning", k=3)      # Top 3 results
top_10 = rag.query("machine learning", k=10)    # Top 10 results
all_results = rag.query("machine learning", k=100)  # Up to 100 results

print(f"Found {len(top_3)} in top 3")
print(f"Found {len(all_results)} total relevant results")
```

### Similarity Threshold Filtering

```python
# Filter by minimum similarity score
def filter_by_threshold(results, min_score=0.7):
    """Keep only results above similarity threshold."""
    return [(text, score) for text, score in results if score >= min_score]

# Get all results, then filter
all_results = rag.query("database systems", k=50)
high_quality = filter_by_threshold(all_results, min_score=0.75)

print(f"All results: {len(all_results)}")
print(f"High quality (>0.75): {len(high_quality)}")
```

### Query Optimization

```python
# Different query strategies
queries = {
    "specific": "Python programming language features",
    "broad": "programming",
    "technical": "object-oriented programming paradigm",
    "conceptual": "software development best practices"
}

for query_type, query_text in queries.items():
    results = rag.query(query_text, k=5)
    print(f"\n{query_type.title()} Query: '{query_text}'")
    print(f"Found {len(results)} results, top score: {results[0][1]:.2f}")
```

## 📊 Search Result Analysis

### Result Quality Assessment

```python
def analyze_search_quality(rag, query, k=10):
    """Analyze the quality of search results."""
    results = rag.query(query, k=k)
    
    if not results:
        return {"status": "no_results"}
    
    scores = [score for _, score in results]
    
    analysis = {
        "query": query,
        "total_results": len(results),
        "avg_score": sum(scores) / len(scores),
        "max_score": max(scores),
        "min_score": min(scores),
        "high_quality_count": len([s for s in scores if s >= 0.8]),
        "medium_quality_count": len([s for s in scores if 0.6 <= s < 0.8]),
        "low_quality_count": len([s for s in scores if s < 0.6])
    }
    
    return analysis

# Test different queries
test_queries = [
    "machine learning algorithms",
    "web development",
    "data structures",
    "completely unrelated topic xyz123"
]

for query in test_queries:
    analysis = analyze_search_quality(rag, query)
    print(f"\nQuery: '{analysis['query']}'")
    print(f"Results: {analysis['total_results']}, Avg Score: {analysis['avg_score']:.2f}")
    print(f"High Quality: {analysis['high_quality_count']}, Medium: {analysis['medium_quality_count']}")
```

## 🎯 Practical Search Applications

### 1. Document Discovery System

```python
class DocumentDiscovery:
    def __init__(self, documents_path):
        self.rag = TinyRag(vector_store="faiss")
        self.rag.add_documents([documents_path])
    
    def search(self, query, min_score=0.6):
        """Search with quality filtering."""
        results = self.rag.query(query, k=20)
        filtered = [(text, score) for text, score in results if score >= min_score]
        return filtered
    
    def explore_topics(self, topics):
        """Explore multiple related topics."""
        topic_results = {}
        for topic in topics:
            results = self.search(topic, min_score=0.7)
            topic_results[topic] = results[:5]  # Top 5 per topic
        return topic_results
    
    def find_similar_documents(self, sample_text):
        """Find documents similar to given text."""
        return self.search(sample_text, min_score=0.75)

# Usage example
discovery = DocumentDiscovery("research_papers/")

# Search for specific topics
ml_docs = discovery.search("machine learning")
ai_docs = discovery.search("artificial intelligence")

# Explore related topics
topics = ["neural networks", "deep learning", "computer vision"]
topic_exploration = discovery.explore_topics(topics)

# Find similar to existing document
sample = "This paper presents a novel approach to natural language processing..."
similar_docs = discovery.find_similar_documents(sample)
```

### 2. Content Recommendation Engine

```python
class ContentRecommender:
    def __init__(self):
        self.rag = TinyRag(vector_store="memory")
        self.user_history = {}
    
    def add_content(self, content_list):
        """Add content to recommendation system."""
        self.rag.add_documents(content_list)
    
    def recommend_based_on_interest(self, user_interests, k=5):
        """Recommend content based on user interests."""
        recommendations = {}
        
        for interest in user_interests:
            results = self.rag.query(interest, k=k)
            recommendations[interest] = [
                {"text": text[:100] + "...", "score": score}
                for text, score in results if score >= 0.6
            ]
        
        return recommendations
    
    def find_related_content(self, content_text, k=3):
        """Find content related to given text."""
        results = self.rag.query(content_text, k=k+1)  # +1 to exclude exact match
        # Filter out exact matches and low scores
        related = [(text, score) for text, score in results 
                  if score < 0.99 and score >= 0.7]
        return related[:k]

# Content recommendation example
recommender = ContentRecommender()

# Add content library
content = [
    "Introduction to Python programming and basic syntax",
    "Advanced JavaScript frameworks like React and Vue",
    "Machine learning with scikit-learn and pandas",
    "Database design principles and SQL optimization",
    "Web security best practices and authentication",
    "Mobile app development with React Native",
    "DevOps tools and continuous integration pipelines"
]

recommender.add_content(content)

# Get personalized recommendations
user_interests = ["web development", "mobile apps", "security"]
recommendations = recommender.recommend_based_on_interest(user_interests)

for interest, recs in recommendations.items():
    print(f"\n--- {interest.title()} Recommendations ---")
    for rec in recs:
        print(f"Score: {rec['score']:.2f} - {rec['text']}")
```

### 3. FAQ Search System

```python
class FAQSearch:
    def __init__(self):
        self.rag = TinyRag(vector_store="pickle")
        self.faqs = {}
    
    def load_faqs(self, faq_data):
        """Load FAQ questions and answers."""
        questions = []
        for i, (question, answer) in enumerate(faq_data.items()):
            questions.append(question)
            self.faqs[i] = {"question": question, "answer": answer}
        
        self.rag.add_documents(questions)
    
    def search_faq(self, user_question, k=3):
        """Find most relevant FAQ entries."""
        results = self.rag.query(user_question, k=k)
        
        relevant_faqs = []
        for question_text, score in results:
            if score >= 0.6:  # Minimum relevance threshold
                # Find the FAQ entry
                for faq_id, faq_data in self.faqs.items():
                    if faq_data["question"] == question_text:
                        relevant_faqs.append({
                            "question": faq_data["question"],
                            "answer": faq_data["answer"],
                            "relevance": score
                        })
                        break
        
        return relevant_faqs

# FAQ system example
faq_system = FAQSearch()

# Sample FAQ data
faq_data = {
    "How do I install TinyRag?": "Use pip install tinyrag to install the library.",
    "What file formats are supported?": "TinyRag supports PDF, DOCX, CSV, and TXT files.",
    "Can I use TinyRag without an API key?": "Yes, TinyRag works locally without requiring API keys.",
    "How do I index my codebase?": "Use the add_codebase() method to index code files.",
    "What vector stores are available?": "Memory, Pickle, Faiss, and ChromaDB are supported.",
    "How do I improve search quality?": "Use specific queries and adjust similarity thresholds."
}

faq_system.load_faqs(faq_data)

# User questions
user_questions = [
    "How to setup TinyRag?",
    "Which documents can I process?", 
    "Do I need OpenAI API?",
    "How to search code files?"
]

for question in user_questions:
    print(f"\nUser: {question}")
    faqs = faq_system.search_faq(question)
    
    if faqs:
        best_match = faqs[0]
        print(f"Best Match (Score: {best_match['relevance']:.2f}):")
        print(f"Q: {best_match['question']}")
        print(f"A: {best_match['answer']}")
    else:
        print("No relevant FAQ found.")
```

### 4. Code Search Engine

```python
class CodeSearchEngine:
    def __init__(self, codebase_path):
        self.rag = TinyRag(vector_store="faiss", chunk_size=800)
        self.rag.add_codebase(codebase_path)
    
    def search_functions(self, query, k=5):
        """Search for specific functions or code patterns."""
        results = self.rag.query(query, k=k)
        return [(code, score) for code, score in results if score >= 0.6]
    
    def find_similar_code(self, code_snippet, k=3):
        """Find code similar to provided snippet."""
        results = self.rag.query(code_snippet, k=k+5)  # Get extra results
        # Filter out exact matches and very low scores
        similar = [(code, score) for code, score in results 
                  if score < 0.95 and score >= 0.7]
        return similar[:k]
    
    def search_by_category(self, categories):
        """Search for different categories of code."""
        categorized_results = {}
        
        for category, search_terms in categories.items():
            category_results = []
            for term in search_terms:
                results = self.search_functions(term, k=3)
                category_results.extend(results)
            
            # Remove duplicates and sort by score
            seen = set()
            unique_results = []
            for code, score in sorted(category_results, key=lambda x: x[1], reverse=True):
                if code not in seen:
                    seen.add(code)
                    unique_results.append((code, score))
            
            categorized_results[category] = unique_results[:5]  # Top 5 per category
        
        return categorized_results

# Code search example
# code_search = CodeSearchEngine("my_project/")

# Search for specific functionality
# auth_functions = code_search.search_functions("user authentication login")
# db_functions = code_search.search_functions("database query SELECT")

# Search by categories
# categories = {
#     "Authentication": ["login", "password", "token", "auth"],
#     "Database": ["query", "SELECT", "INSERT", "database"],
#     "API": ["endpoint", "route", "API", "request"],
#     "Testing": ["test", "unittest", "assert", "mock"]
# }

# categorized_code = code_search.search_by_category(categories)
```

## 🔧 Query Optimization Techniques

### 1. Multi-Query Expansion

```python
def expanded_search(rag, base_query, k=10):
    """Search using multiple related queries."""
    
    # Generate related queries
    related_queries = [
        base_query,
        f"{base_query} examples",
        f"{base_query} tutorial", 
        f"how to {base_query}",
        f"{base_query} best practices"
    ]
    
    all_results = []
    seen_texts = set()
    
    for query in related_queries:
        results = rag.query(query, k=k//len(related_queries))
        
        for text, score in results:
            if text not in seen_texts:
                seen_texts.add(text)
                all_results.append((text, score))
    
    # Sort by score and return top k
    all_results.sort(key=lambda x: x[1], reverse=True)
    return all_results[:k]

# Example usage
expanded_results = expanded_search(rag, "machine learning", k=10)
```

### 2. Semantic Query Enhancement

```python
def semantic_search_variants(rag, query, k=5):
    """Try different semantic variations of the query."""
    
    variants = [
        query,                                    # Original
        f"explain {query}",                      # Explanatory
        f"{query} concepts",                     # Conceptual
        f"{query} implementation",               # Implementation-focused
        f"introduction to {query}",              # Beginner-friendly
        f"advanced {query}",                     # Advanced
    ]
    
    variant_results = {}
    for variant in variants:
        results = rag.query(variant, k=k)
        if results:
            variant_results[variant] = results
    
    return variant_results

# Compare different query approaches
semantic_variants = semantic_search_variants(rag, "neural networks", k=3)

for variant, results in semantic_variants.items():
    print(f"\nVariant: '{variant}'")
    print(f"Top result score: {results[0][1]:.2f}" if results else "No results")
```

### 3. Contextual Search

```python
def contextual_search(rag, queries_with_context, k=5):
    """Search with context awareness."""
    
    results_by_context = {}
    
    for context, query in queries_with_context.items():
        # Combine context with query
        enhanced_query = f"{context}: {query}"
        results = rag.query(enhanced_query, k=k)
        
        # Also try just the query
        simple_results = rag.query(query, k=k)
        
        # Combine and deduplicate
        combined = results + simple_results
        seen = set()
        unique_results = []
        
        for text, score in combined:
            if text not in seen:
                seen.add(text)
                unique_results.append((text, score))
        
        # Sort by score
        unique_results.sort(key=lambda x: x[1], reverse=True)
        results_by_context[context] = unique_results[:k]
    
    return results_by_context

# Example with context
contextual_queries = {
    "Programming": "functions and methods",
    "Data Science": "data analysis techniques",
    "Web Development": "responsive design patterns"
}

contextual_results = contextual_search(rag, contextual_queries, k=3)
```

## 📊 Performance Monitoring

### Search Performance Metrics

```python
import time
from collections import defaultdict

class SearchMetrics:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def measure_query(self, rag, query, k=5):
        """Measure query performance."""
        start_time = time.time()
        results = rag.query(query, k=k)
        query_time = time.time() - start_time
        
        metrics = {
            "query": query,
            "response_time": query_time,
            "results_count": len(results),
            "avg_score": sum(score for _, score in results) / len(results) if results else 0,
            "max_score": max(score for _, score in results) if results else 0
        }
        
        self.metrics[query].append(metrics)
        return metrics
    
    def benchmark_queries(self, rag, test_queries, iterations=3):
        """Benchmark multiple queries."""
        results = {}
        
        for query in test_queries:
            query_metrics = []
            for i in range(iterations):
                metrics = self.measure_query(rag, query)
                query_metrics.append(metrics)
            
            # Calculate averages
            avg_metrics = {
                "query": query,
                "avg_response_time": sum(m["response_time"] for m in query_metrics) / iterations,
                "avg_results_count": sum(m["results_count"] for m in query_metrics) / iterations,
                "avg_score": sum(m["avg_score"] for m in query_metrics) / iterations
            }
            
            results[query] = avg_metrics
        
        return results

# Performance monitoring example
metrics = SearchMetrics()

test_queries = [
    "machine learning",
    "web development", 
    "database design",
    "software testing"
]

# benchmark_results = metrics.benchmark_queries(rag, test_queries)
# for query, metrics in benchmark_results.items():
#     print(f"Query: {query}")
#     print(f"  Avg Time: {metrics['avg_response_time']:.3f}s")
#     print(f"  Avg Results: {metrics['avg_results_count']:.1f}")
#     print(f"  Avg Score: {metrics['avg_score']:.2f}")
```

## 🚀 Next Steps

Ready to enhance your search capabilities:

- [**Custom System Prompts**](08-system-prompts.md) - Add AI-powered responses to search results
- [**Chat Functionality**](09-chat-functionality.md) - Build conversational search interfaces
- [**Performance Optimization**](11-performance.md) - Speed up search for large datasets
- [**Real-world Examples**](15-examples.md) - Complete search applications

---

**Need search inspiration?** Check [Use Case Patterns](16-use-cases.md) for domain-specific search implementations!