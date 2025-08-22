# Chat Functionality

Build intelligent conversational interfaces with TinyRag's chat capabilities. Combine semantic search with LLM responses for powerful RAG applications.

## 🎯 What is Chat Functionality?

TinyRag's chat feature combines document search with AI language models to provide contextual, intelligent responses. It searches your documents and uses the relevant content to generate informed answers.

## 🚀 Basic Chat Setup

### Prerequisites

```python
from tinyrag import Provider, TinyRag

# Set up your AI provider first
provider = Provider(
    api_key="sk-your-openai-key",  # Replace with your key
    model="gpt-4",                 # or "gpt-3.5-turbo"
    base_url="https://api.openai.com/v1"
)

# Create TinyRag with chat capability
rag = TinyRag(provider=provider)
```

### First Chat Example

```python
# Add some documents
rag.add_documents([
    "TinyRag is a Python library for building RAG applications.",
    "It supports PDF, DOCX, CSV, and TXT file processing.",
    "Vector stores include Memory, Pickle, Faiss, and ChromaDB.",
    "The library works locally using embeddings from HuggingFace."
])

# Have a conversation
response = rag.chat("What is TinyRag and what can it do?")
print(response)

# Follow-up questions work naturally
response2 = rag.chat("What file formats does it support?")
print(response2)
```

### Understanding the Chat Process

```python
# The chat process involves:
# 1. Search your documents for relevant content
# 2. Provide that content as context to the AI
# 3. Generate a response based on the context
# 4. Return the AI's answer

# You can see this in action:
query = "How do vector stores work?"

# Step 1: See what documents are found
search_results = rag.query(query, k=3)
print("Found documents:")
for text, score in search_results:
    print(f"Score: {score:.2f} - {text[:100]}...")

# Step 2: Get AI response using those documents
chat_response = rag.chat(query)
print(f"\nAI Response: {chat_response}")
```

## 💬 Chat Patterns and Use Cases

### 1. Document Q&A System

```python
# Load comprehensive documentation
rag = TinyRag(provider=provider, vector_store="faiss")
rag.add_documents([
    "user_manual.pdf",
    "api_documentation/",
    "faq.txt",
    "troubleshooting_guide.docx"
])

# Interactive Q&A session
def interactive_qa():
    print("Document Q&A System - Ask me anything!")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("Question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            answer = rag.chat(question)
            print(f"Answer: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")

# interactive_qa()
```

### 2. Code Assistant

```python
# Set up code-focused assistant
code_prompt = """You are a helpful programming assistant. 
Analyze the provided code context and give practical, actionable advice.
Include code examples in your responses when helpful."""

code_rag = TinyRag(
    provider=provider,
    system_prompt=code_prompt,
    vector_store="faiss"
)

# Index codebase
code_rag.add_codebase("my_project/")

# Code-related conversations
coding_questions = [
    "How is user authentication implemented?",
    "Show me the database connection code",
    "What testing framework is used?",
    "How can I add a new API endpoint?",
    "Are there any security vulnerabilities in the auth code?"
]

print("=== Code Assistant ===")
for question in coding_questions:
    print(f"\nQ: {question}")
    answer = code_rag.chat(question)
    print(f"A: {answer}")
```

### 3. Customer Support Bot

```python
# Customer support configuration
support_prompt = """You are a friendly customer support representative.
Always be helpful, empathetic, and solution-focused.
Use the provided documentation to help resolve customer issues.
If you cannot find an answer, politely suggest contacting human support."""

support_rag = TinyRag(
    provider=provider,
    system_prompt=support_prompt,
    vector_store="memory"
)

# Load support knowledge base
support_rag.add_documents([
    "product_features.txt",
    "billing_information.pdf", 
    "technical_troubleshooting.docx",
    "shipping_policies.txt"
])

# Support conversation simulation
support_scenarios = [
    "I can't log into my account",
    "How do I cancel my subscription?", 
    "My order hasn't arrived yet",
    "The app keeps crashing on my phone",
    "I was charged twice for the same order"
]

print("=== Customer Support Bot ===")
for scenario in support_scenarios:
    print(f"\nCustomer: {scenario}")
    response = support_rag.chat(scenario)
    print(f"Support: {response}")
```

### 4. Research Assistant

```python
# Research-focused assistant
research_prompt = """You are a research assistant helping with academic and professional research.
Provide thorough, well-researched answers with proper context.
Cite the relevant information from the provided sources.
Be objective and analytical in your responses."""

research_rag = TinyRag(
    provider=provider,
    system_prompt=research_prompt,
    vector_store="chromadb"
)

# Add research materials
research_rag.add_documents([
    "research_papers/",
    "academic_journals/",
    "industry_reports/",
    "conference_proceedings/"
])

# Research queries
research_questions = [
    "What are the latest developments in machine learning?",
    "Summarize the key findings on climate change impacts",
    "What methodologies are used in user experience research?",
    "Compare different approaches to data privacy protection"
]

print("=== Research Assistant ===")
for question in research_questions:
    print(f"\nResearch Query: {question}")
    analysis = research_rag.chat(question)
    print(f"Analysis: {analysis}\n" + "="*50)
```

## 🎨 Advanced Chat Features

### Conversation Memory

```python
class ConversationManager:
    def __init__(self, rag):
        self.rag = rag
        self.conversation_history = []
    
    def chat_with_history(self, message, max_history=5):
        """Chat with conversation context."""
        
        # Add current message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Create context-aware prompt
        if len(self.conversation_history) > 1:
            recent_history = self.conversation_history[-max_history:]
            context = "\n".join([f"{msg['role']}: {msg['content']}" 
                               for msg in recent_history[:-1]])
            enhanced_message = f"Previous conversation:\n{context}\n\nCurrent question: {message}"
        else:
            enhanced_message = message
        
        # Get response
        response = self.rag.chat(enhanced_message)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

# Usage example
conversation = ConversationManager(rag)

# Multi-turn conversation
print("User: What is machine learning?")
response1 = conversation.chat_with_history("What is machine learning?")
print(f"Assistant: {response1}")

print("\nUser: How is it different from traditional programming?")
response2 = conversation.chat_with_history("How is it different from traditional programming?")
print(f"Assistant: {response2}")

print("\nUser: Can you give me a practical example?")
response3 = conversation.chat_with_history("Can you give me a practical example?")
print(f"Assistant: {response3}")
```

### Multi-Document Chat

```python
class MultiDocumentChat:
    def __init__(self, provider):
        self.provider = provider
        self.document_rags = {}
    
    def add_document_collection(self, name, documents):
        """Add a named collection of documents."""
        rag = TinyRag(provider=self.provider, vector_store="memory")
        rag.add_documents(documents)
        self.document_rags[name] = rag
    
    def chat_across_collections(self, question, collections=None):
        """Get responses from multiple document collections."""
        if collections is None:
            collections = list(self.document_rags.keys())
        
        responses = {}
        for collection_name in collections:
            if collection_name in self.document_rags:
                rag = self.document_rags[collection_name]
                response = rag.chat(question)
                responses[collection_name] = response
        
        return responses
    
    def compare_perspectives(self, question):
        """Compare answers across different document collections."""
        responses = self.chat_across_collections(question)
        
        comparison = f"Question: {question}\n\n"
        for collection, response in responses.items():
            comparison += f"=== {collection.title()} Perspective ===\n"
            comparison += f"{response}\n\n"
        
        return comparison

# Multi-document example
multi_chat = MultiDocumentChat(provider)

# Add different document collections
multi_chat.add_document_collection("technical_docs", [
    "technical_specifications.pdf",
    "api_reference.md",
    "architecture_guide.docx"
])

multi_chat.add_document_collection("user_guides", [
    "user_manual.pdf",
    "getting_started.txt",
    "tutorials/"
])

multi_chat.add_document_collection("business_docs", [
    "business_requirements.docx",
    "market_analysis.pdf",
    "strategy_document.txt"
])

# Compare perspectives
question = "What are the key benefits of our product?"
comparison = multi_chat.compare_perspectives(question)
print(comparison)
```

### Specialized Chat Modes

```python
def create_specialized_chat(mode, provider, documents):
    """Create specialized chat instances for different purposes."""
    
    prompts = {
        "explainer": """You are an expert teacher. Explain complex topics in simple terms.
        Use analogies and examples to make concepts easy to understand.
        Break down complex ideas into digestible steps.""",
        
        "analyzer": """You are a critical analyst. Examine information thoroughly.
        Identify key points, patterns, and potential issues.
        Provide objective, detailed analysis based on the evidence.""",
        
        "problem_solver": """You are a practical problem solver.
        Focus on actionable solutions and step-by-step guidance.
        Prioritize practical, implementable approaches.""",
        
        "creative": """You are a creative thinking partner.
        Generate innovative ideas and alternative approaches.
        Think outside the box while staying grounded in the context."""
    }
    
    if mode not in prompts:
        raise ValueError(f"Unknown mode: {mode}")
    
    rag = TinyRag(
        provider=provider,
        system_prompt=prompts[mode],
        vector_store="memory"
    )
    rag.add_documents(documents)
    
    return rag

# Create different specialized assistants
documents = ["technical_documentation/", "user_guides/"]

explainer_bot = create_specialized_chat("explainer", provider, documents)
analyzer_bot = create_specialized_chat("analyzer", provider, documents) 
solver_bot = create_specialized_chat("problem_solver", provider, documents)

# Same question, different perspectives
question = "How does the authentication system work?"

print("=== Explainer Mode ===")
explanation = explainer_bot.chat(question)
print(explanation)

print("\n=== Analyzer Mode ===")
analysis = analyzer_bot.chat(question)
print(analysis)

print("\n=== Problem Solver Mode ===")
solution = solver_bot.chat(question)
print(solution)
```

## 🔧 Chat Configuration and Optimization

### Response Quality Control

```python
def enhance_chat_quality(rag, question, max_retries=3):
    """Improve chat response quality with retry logic."""
    
    for attempt in range(max_retries):
        try:
            # Get search results first
            search_results = rag.query(question, k=5)
            
            # Check if we have good search results
            if not search_results or search_results[0][1] < 0.6:
                # Try a broader search
                broader_question = f"information about {question}"
                search_results = rag.query(broader_question, k=5)
            
            # Get chat response
            response = rag.chat(question)
            
            # Basic quality checks
            if len(response) > 50 and "I don't know" not in response.lower():
                return {
                    "response": response,
                    "attempt": attempt + 1,
                    "search_quality": search_results[0][1] if search_results else 0
                }
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return {
                    "response": "I apologize, but I'm having trouble answering that question right now.",
                    "attempt": attempt + 1,
                    "error": str(e)
                }
    
    return None

# Quality-controlled chat
question = "How do I implement secure password storage?"
result = enhance_chat_quality(rag, question)

if result:
    print(f"Response (attempt {result['attempt']}):")
    print(result['response'])
    if 'search_quality' in result:
        print(f"Search quality: {result['search_quality']:.2f}")
```

### Chat Performance Monitoring

```python
import time
from datetime import datetime

class ChatMetrics:
    def __init__(self):
        self.chat_logs = []
    
    def monitored_chat(self, rag, question):
        """Chat with performance monitoring."""
        start_time = time.time()
        timestamp = datetime.now()
        
        try:
            # Search phase
            search_start = time.time()
            search_results = rag.query(question, k=3)
            search_time = time.time() - search_start
            
            # Chat phase
            chat_start = time.time()
            response = rag.chat(question)
            chat_time = time.time() - chat_start
            
            total_time = time.time() - start_time
            
            # Log metrics
            metrics = {
                "timestamp": timestamp,
                "question": question,
                "response_length": len(response),
                "search_time": search_time,
                "chat_time": chat_time,
                "total_time": total_time,
                "search_results_count": len(search_results),
                "top_search_score": search_results[0][1] if search_results else 0,
                "status": "success"
            }
            
            self.chat_logs.append(metrics)
            return response, metrics
            
        except Exception as e:
            error_metrics = {
                "timestamp": timestamp,
                "question": question,
                "error": str(e),
                "total_time": time.time() - start_time,
                "status": "error"
            }
            self.chat_logs.append(error_metrics)
            raise e
    
    def get_performance_summary(self):
        """Get performance statistics."""
        if not self.chat_logs:
            return "No chat data available."
        
        successful_chats = [log for log in self.chat_logs if log["status"] == "success"]
        
        if not successful_chats:
            return "No successful chats recorded."
        
        avg_total_time = sum(log["total_time"] for log in successful_chats) / len(successful_chats)
        avg_search_time = sum(log["search_time"] for log in successful_chats) / len(successful_chats)
        avg_chat_time = sum(log["chat_time"] for log in successful_chats) / len(successful_chats)
        avg_response_length = sum(log["response_length"] for log in successful_chats) / len(successful_chats)
        
        return f"""
Chat Performance Summary:
- Total chats: {len(self.chat_logs)}
- Successful: {len(successful_chats)}
- Average total time: {avg_total_time:.2f}s
- Average search time: {avg_search_time:.2f}s  
- Average chat time: {avg_chat_time:.2f}s
- Average response length: {avg_response_length:.0f} characters
"""

# Performance monitoring example
metrics = ChatMetrics()

test_questions = [
    "What is TinyRag?",
    "How do I install it?",
    "What are the main features?",
    "Can you show me an example?"
]

for question in test_questions:
    response, chat_metrics = metrics.monitored_chat(rag, question)
    print(f"Q: {question}")
    print(f"A: {response[:100]}...")
    print(f"Time: {chat_metrics['total_time']:.2f}s\n")

print(metrics.get_performance_summary())
```

## 🚀 Production Chat Systems

### Scalable Chat Service

```python
class ChatService:
    def __init__(self, provider, documents_path):
        self.rag = TinyRag(
            provider=provider,
            vector_store="chromadb",
            vector_store_config={
                "persist_directory": "chat_db/",
                "collection_name": "chat_documents"
            }
        )
        
        # Load documents once at startup
        print("Loading documents...")
        self.rag.add_documents([documents_path])
        print("Chat service ready!")
    
    def chat(self, message, user_id=None):
        """Handle chat requests with optional user tracking."""
        try:
            response = self.rag.chat(message)
            
            # Log for analytics (optional)
            if user_id:
                self.log_interaction(user_id, message, response)
            
            return {
                "status": "success",
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def log_interaction(self, user_id, message, response):
        """Log user interactions for analytics."""
        # Implementation depends on your logging system
        print(f"User {user_id}: {message[:50]}... -> {len(response)} chars")

# Production service example
# chat_service = ChatService(provider, "knowledge_base/")

# Handle user requests
# user_request = "How do I reset my password?"
# result = chat_service.chat(user_request, user_id="user123")
# print(result)
```

## 🔍 Debugging Chat Issues

### Common Problems and Solutions

```python
def debug_chat_issues(rag, question):
    """Diagnose common chat problems."""
    
    print(f"Debugging question: '{question}'")
    print("=" * 50)
    
    # 1. Check if documents are loaded
    try:
        search_test = rag.query("test", k=1)
        if not search_test:
            print("❌ No documents found. Check if documents are loaded.")
            return
        else:
            print(f"✅ Documents loaded: {len(search_test)} results for test query")
    except Exception as e:
        print(f"❌ Search error: {e}")
        return
    
    # 2. Check search quality for the question
    search_results = rag.query(question, k=5)
    if not search_results:
        print("❌ No relevant documents found for this question")
        print("Try broader or different keywords")
        return
    
    print(f"✅ Found {len(search_results)} relevant documents")
    print(f"Top similarity score: {search_results[0][1]:.2f}")
    
    if search_results[0][1] < 0.5:
        print("⚠️  Low similarity scores - question might not match document content")
    
    # 3. Check provider configuration
    try:
        if rag.provider is None:
            print("❌ No AI provider configured. Set up Provider with API key.")
            return
        else:
            print("✅ AI provider configured")
    except:
        print("❌ Provider check failed")
        return
    
    # 4. Test chat functionality
    try:
        response = rag.chat(question)
        print(f"✅ Chat successful: {len(response)} character response")
        print(f"Response preview: {response[:100]}...")
    except Exception as e:
        print(f"❌ Chat failed: {e}")
        print("Check API key, internet connection, and model availability")

# Debug example
# debug_chat_issues(rag, "How do I install Python packages?")
```

## 🎓 Next Steps

Ready to build production chat systems:

- [**Provider Configuration**](10-provider-config.md) - Advanced AI provider setup
- [**Performance Optimization**](11-performance.md) - Scale chat for high traffic
- [**Best Practices**](13-best-practices.md) - Production chat guidelines
- [**Real-world Examples**](15-examples.md) - Complete chat applications

---

**Want to see chat systems in action?** Check [Real-world Examples](15-examples.md) for complete conversational AI applications!