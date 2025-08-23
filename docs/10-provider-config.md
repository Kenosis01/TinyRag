# Provider Configuration

Configure AI providers and embedding models for TinyRag's enhanced functionality. Support for multiple embedding providers (local, OpenAI, Ollama), structured responses with citations, and intelligent caching.

## 🎯 What is a Provider?

A Provider in TinyRag handles both embedding generation and LLM communication. With the enhanced multi-provider system, you can:
- Choose embedding providers independently from chat models
- Use local embeddings with cloud LLM chat
- Get structured responses with source citations
- Benefit from intelligent document caching

## 🚀 Multi-Provider Setup

### Local Embeddings (Default - No API Key Required)

```python
from tinyrag import Provider, TinyRag

# Local embeddings with sentence-transformers (recommended for cost efficiency)
provider = Provider(
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2"  # Fast, accurate, 384 dimensions
)

# Use with TinyRag
rag = TinyRag(provider=provider)

# This works for search without any API keys!
rag.add_documents(["document.pdf", "text content"])
results = rag.query_structured("your question", format_type="json")
```

### OpenAI Embeddings + Chat

```python
# OpenAI embeddings with chat functionality
provider = Provider(
    api_key="sk-your-openai-key",
    model="gpt-4",
    embedding_provider="openai",
    embedding_model="text-embedding-ada-002"
)

rag = TinyRag(provider=provider)
rag.add_documents(["documents/"])

# Structured chat with citations
response = rag.chat_structured(
    "Explain the key concepts",
    format_type="markdown"
)
print(response)  # Shows answer with source citations
```

### Ollama Local Embeddings

```python
# Use local Ollama for embeddings
provider = Provider(
    embedding_provider="ollama",
    embedding_model="nomic-embed-text",
    ollama_base_url="http://localhost:11434"
)

rag = TinyRag(provider=provider)
```

### Hybrid Setup: Local Embeddings + Cloud Chat

```python
# Cost-effective: Local embeddings + OpenAI chat
provider = Provider(
    api_key="sk-your-key",
    model="gpt-3.5-turbo",          # Chat model
    embedding_provider="local",      # Local embeddings (free)
    embedding_model="all-MiniLM-L6-v2"
)

rag = TinyRag(
    provider=provider,
    enable_cache=True,  # Cache embeddings to avoid re-processing
    system_prompt="You are a helpful assistant that provides detailed answers with proper citations."
)
```

## 📊 Structured Responses & Citations

### Enhanced Output Formats

```python
# Setup provider (any embedding type works)
provider = Provider(
    api_key="sk-your-key",  # Optional for search-only
    embedding_provider="local"  # or "openai", "ollama"
)

rag = TinyRag(provider=provider)
rag.add_documents(["research.pdf", "manual.docx", "notes.txt"])

# Structured search results (no LLM needed)
query = "machine learning algorithms"

# Text format with citations
text_result = rag.query_structured(query, format_type="text")
print(text_result)
# Output includes:
# - Answer summary
# - Source files with relevance scores
# - Document types and chunk positions

# JSON format for APIs
json_result = rag.query_structured(query, format_type="json")
# Perfect for web applications and integrations

# Markdown format for documentation
md_result = rag.query_structured(query, format_type="markdown")
# Great for reports and documentation
```

### Chat with Citations (Requires API Key)

```python
# Setup with LLM for enhanced chat
provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",
    embedding_provider="local",  # Save costs on embeddings
)

rag = TinyRag(
    provider=provider,
    system_prompt="Provide detailed explanations with proper source attribution."
)

# Enhanced chat with automatic citations
response = rag.chat_structured(
    "What are the best practices for data preprocessing?",
    k=5,  # Use top 5 most relevant sources
    format_type="markdown"
)

print(response)
# Output includes:
# - Detailed LLM-generated answer
# - Automatic citation numbers [1], [2], etc.
# - Complete source list with file names, scores, and previews
# - Confidence scoring
# - Processing time metrics
```

## 🔑 Environment Variables & Security

```python
import os

# Set environment variable (more secure)
os.environ["OPENAI_API_KEY"] = "sk-your-openai-key"

# Provider automatically uses environment variable
provider = Provider(
    model="gpt-4",
    embedding_provider="local"  # Use local embeddings to save costs
    # api_key automatically loaded from OPENAI_API_KEY
)

# Complete configuration with caching
rag = TinyRag(
    provider=provider,
    vector_store="faiss",  # High-performance for large datasets
    enable_cache=True,     # Avoid re-processing documents
    cache_dir=".tinyrag_cache"
)
```

## 🤖 Embedding Model Comparison

### Local Models (sentence-transformers)

```python
# Fast and lightweight (recommended)
fast_provider = Provider(
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2"  # 384 dim, 80MB, fast
)

# High accuracy
accurate_provider = Provider(
    embedding_provider="local", 
    embedding_model="all-mpnet-base-v2"  # 768 dim, 420MB, accurate
)

# Multilingual support
multilingual_provider = Provider(
    embedding_provider="local",
    embedding_model="paraphrase-multilingual-MiniLM-L12-v2"
)

# Compare models
models = {
    "Fast": fast_provider,
    "Accurate": accurate_provider,
    "Multilingual": multilingual_provider
}

query = "machine learning concepts"
for name, provider in models.items():
    rag = TinyRag(provider=provider)
    rag.add_documents(["ml_textbook.pdf"])
    
    result = rag.query_structured(query, k=3, format_type="json")
    print(f"{name}: {len(result['sources'])} sources found")
```

### OpenAI Embeddings

```python
# High-quality embeddings (paid)
openai_provider = Provider(
    api_key="sk-your-key",
    embedding_provider="openai",
    embedding_model="text-embedding-ada-002",  # 1536 dimensions
    model="gpt-4"  # For chat functionality
)

# Best for: Production applications requiring highest quality
# Cost: ~$0.0001 per 1K tokens
```

### Ollama Local Models

```python
# Self-hosted embeddings
ollama_provider = Provider(
    embedding_provider="ollama",
    embedding_model="nomic-embed-text",
    ollama_base_url="http://localhost:11434"
)

# Requires: ollama pull nomic-embed-text
# Best for: Privacy-focused applications, no internet dependency
```

## 📈 Provider Selection Guide

### Choose the Right Combination

```python
def get_recommended_setup(use_case, budget="medium", privacy="normal"):
    """Get recommended provider configuration"""
    
    configurations = {
        # Research & Development
        ("research", "low", "normal"): {
            "embedding_provider": "local",
            "embedding_model": "all-MiniLM-L6-v2",
            "chat_model": None,  # Search-only
            "description": "Fast local search, no API costs"
        },
        
        ("research", "medium", "normal"): {
            "embedding_provider": "local",
            "embedding_model": "all-mpnet-base-v2",
            "chat_model": "gpt-3.5-turbo",
            "description": "Accurate embeddings + affordable chat"
        },
        
        ("research", "high", "normal"): {
            "embedding_provider": "openai",
            "embedding_model": "text-embedding-ada-002",
            "chat_model": "gpt-4",
            "description": "Premium quality for critical applications"
        },
        
        # Privacy-focused
        ("private", "any", "high"): {
            "embedding_provider": "ollama",
            "embedding_model": "nomic-embed-text",
            "chat_model": None,
            "description": "Fully local, no data leaves your system"
        },
        
        # Production applications
        ("production", "medium", "normal"): {
            "embedding_provider": "local",
            "embedding_model": "all-MiniLM-L6-v2",
            "chat_model": "gpt-4",
            "description": "Cost-effective with premium chat quality"
        }
    }
    
    key = (use_case, budget, privacy)
    return configurations.get(key, configurations[("research", "low", "normal")])

# Usage examples
setups = [
    ("research", "low", "normal"),
    ("production", "medium", "normal"),
    ("private", "any", "high")
]

for use_case, budget, privacy in setups:
    config = get_recommended_setup(use_case, budget, privacy)
    print(f"\n{use_case.title()} ({budget} budget, {privacy} privacy):")
    print(f"  Embeddings: {config['embedding_provider']} - {config['embedding_model']}")
    print(f"  Chat: {config['chat_model'] or 'Search-only'}")
    print(f"  Notes: {config['description']}")
```

### Real-World Setup Examples

```python
# Startup/Research: Cost-effective with great results
startup_provider = Provider(
    api_key="sk-your-key",  # Only needed for chat
    model="gpt-3.5-turbo",
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2"
)

# Enterprise: High performance and reliability
enterprise_provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",
    embedding_provider="openai",
    embedding_model="text-embedding-ada-002",
    base_url="https://api.openai.com/v1"  # Or your custom endpoint
)

# Privacy-first: Everything local
privacy_provider = Provider(
    embedding_provider="ollama",
    embedding_model="nomic-embed-text",
    ollama_base_url="http://localhost:11434"
    # No API key needed - fully local
)

# Budget-conscious: Search without LLM costs
budget_provider = Provider(
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2"
    # No API key - search and structured output only
)
```

## ⚡ Performance & Caching Configuration

### Intelligent Document Caching

```python
# Enable smart caching (recommended)
rag = TinyRag(
    provider=provider,
    enable_cache=True,
    cache_dir=".tinyrag_cache",  # Custom cache location
    vector_store="faiss",       # High-performance storage
    max_workers=4               # Parallel processing
)

# Cache automatically handles:
# - Document change detection
# - Embedding model changes 
# - Configuration changes
# - Efficient storage and retrieval

# Cache management
print("Cache info:", rag.get_cache_info())
rag.cleanup_old_cache(days=30)  # Remove old entries
rag.clear_cache()               # Clear all cache
```

### Advanced Provider Configuration

```python
# Fine-tune provider behavior
advanced_provider = Provider(
    # Embedding configuration
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2",
    
    # Chat configuration (optional)
    api_key="sk-your-key",
    model="gpt-4",
    temperature=0.3,        # Lower = more focused
    max_tokens=1500,        # Response length limit
    top_p=0.9,             # Nucleus sampling
    frequency_penalty=0.1,  # Reduce repetition
    presence_penalty=0.1    # Encourage topic diversity
)

# Optimized TinyRag configuration
rag = TinyRag(
    provider=advanced_provider,
    vector_store="faiss",
    chunk_size=400,           # Optimal for most documents
    enable_cache=True,
    system_prompt="""You are a knowledgeable assistant that provides 
    accurate answers based on the given context. Always cite your sources 
    and indicate confidence levels."""
)
```

### Multi-Environment Setup

```python
# Development environment
dev_provider = Provider(
    embedding_provider="local",
    embedding_model="all-MiniLM-L6-v2",
    # No API key needed for development
)

# Staging environment
staging_provider = Provider(
    api_key=os.getenv("STAGING_OPENAI_KEY"),
    model="gpt-3.5-turbo",
    embedding_provider="local"
)

# Production environment
production_provider = Provider(
    api_key=os.getenv("PROD_OPENAI_KEY"),
    model="gpt-4",
    embedding_provider="openai",
    embedding_model="text-embedding-ada-002"
)

# Environment-specific configuration
def get_provider(environment="dev"):
    providers = {
        "dev": dev_provider,
        "staging": staging_provider,
        "prod": production_provider
    }
    return providers.get(environment, dev_provider)

# Usage
current_env = os.getenv("ENVIRONMENT", "dev")
provider = get_provider(current_env)
rag = TinyRag(provider=provider, enable_cache=True)
```
    "search": "text-search-ada-doc-001",       # Optimized for search
    "similarity": "text-similarity-ada-001"    # Optimized for similarity
}

# Choose based on your use case
search_provider = Provider(
    model="gpt-3.5-turbo",
    embedding_model=embedding_configs["search"]
)
```

## 🌐 Alternative Providers

### Azure OpenAI

```python
# Azure OpenAI configuration
azure_provider = Provider(
    api_key="your-azure-key",
    model="gpt-4",
    base_url="https://your-resource.openai.azure.com/",
    api_version="2023-12-01-preview",
    deployment_name="gpt-4-deployment"  # Your Azure deployment name
)

azure_rag = TinyRag(provider=azure_provider)
```

### Anthropic Claude

```python
# Claude configuration (when supported)
claude_provider = Provider(
    api_key="sk-ant-your-key",
    model="claude-3-opus",
    base_url="https://api.anthropic.com/v1/messages"
)

# Note: Check TinyRag documentation for latest Anthropic support
```

### Local Models (Ollama, LM Studio)

```python
# Local model via Ollama
local_provider = Provider(
    model="llama2",                           # Local model name
    base_url="http://localhost:11434/v1",     # Ollama endpoint
    api_key="not-needed"                      # Local models don't need keys
)

# Local model via LM Studio
lm_studio_provider = Provider(
    model="local-model",
    base_url="http://localhost:1234/v1",      # LM Studio endpoint
    api_key="not-needed"
)

# Use local models
local_rag = TinyRag(provider=local_provider)
local_rag.add_documents(["docs/"])
response = local_rag.chat("Explain this documentation")
```

### Custom API Endpoints

```python
# Custom or self-hosted models
custom_provider = Provider(
    api_key="your-custom-key",
    model="custom-model-name",
    base_url="https://your-custom-endpoint.com/v1",
    headers={                                 # Custom headers if needed
        "Authorization": "Bearer your-token",
        "Custom-Header": "custom-value"
    }
)

custom_rag = TinyRag(provider=custom_provider)
```

## 🔄 Provider Management

### Multiple Providers

```python
class MultiProviderRAG:
    def __init__(self):
        self.providers = {
            "gpt4": Provider(model="gpt-4", api_key="sk-key1"),
            "gpt35": Provider(model="gpt-3.5-turbo", api_key="sk-key2"), 
            "local": Provider(model="llama2", base_url="http://localhost:11434/v1", api_key="not-needed")
        }
        self.rags = {}
        
    def setup_rag(self, provider_name, documents):
        """Setup RAG with specific provider."""
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        rag = TinyRag(provider=self.providers[provider_name])
        rag.add_documents(documents)
        self.rags[provider_name] = rag
        
    def chat_with_provider(self, provider_name, question):
        """Chat using specific provider."""
        if provider_name not in self.rags:
            raise ValueError(f"RAG not setup for provider: {provider_name}")
        
        return self.rags[provider_name].chat(question)
    
    def compare_providers(self, question, providers=None):
        """Compare responses from different providers."""
        if providers is None:
            providers = list(self.rags.keys())
        
        results = {}
        for provider in providers:
            if provider in self.rags:
                try:
                    response = self.chat_with_provider(provider, question)
                    results[provider] = {"response": response, "status": "success"}
                except Exception as e:
                    results[provider] = {"error": str(e), "status": "error"}
        
        return results

# Multi-provider example
multi_rag = MultiProviderRAG()

# Setup different providers
documents = ["technical_docs/"]
multi_rag.setup_rag("gpt4", documents)
multi_rag.setup_rag("gpt35", documents)

# Compare responses
question = "Explain the architecture of this system"
comparison = multi_rag.compare_providers(question, ["gpt4", "gpt35"])

for provider, result in comparison.items():
    print(f"\n=== {provider.upper()} ===")
    if result["status"] == "success":
        print(result["response"][:200] + "...")
    else:
        print(f"Error: {result['error']}")
```

### Provider Fallback

```python
class FallbackProvider:
    def __init__(self, primary_provider, fallback_providers):
        self.primary = primary_provider
        self.fallbacks = fallback_providers
        self.current_provider = primary_provider
    
    def chat_with_fallback(self, rag, question):
        """Try primary provider, fallback if needed."""
        
        # Try primary first
        try:
            rag.provider = self.primary
            response = rag.chat(question)
            self.current_provider = self.primary
            return {"response": response, "provider": "primary", "status": "success"}
        
        except Exception as primary_error:
            print(f"Primary provider failed: {primary_error}")
            
            # Try fallback providers
            for i, fallback in enumerate(self.fallbacks):
                try:
                    rag.provider = fallback
                    response = rag.chat(question)
                    self.current_provider = fallback
                    return {"response": response, "provider": f"fallback_{i+1}", "status": "success"}
                
                except Exception as fallback_error:
                    print(f"Fallback {i+1} failed: {fallback_error}")
            
            # All providers failed
            return {"error": "All providers failed", "status": "error"}

# Fallback example
primary = Provider(model="gpt-4", api_key="sk-primary-key")
fallback1 = Provider(model="gpt-3.5-turbo", api_key="sk-fallback-key")
fallback2 = Provider(model="llama2", base_url="http://localhost:11434/v1", api_key="not-needed")

fallback_system = FallbackProvider(primary, [fallback1, fallback2])

rag = TinyRag()  # Provider will be set dynamically
rag.add_documents(["docs/"])

result = fallback_system.chat_with_fallback(rag, "What is this about?")
print(f"Response from {result['provider']}: {result.get('response', result.get('error'))}")
```

## 🔒 Security and Best Practices

### API Key Management

```python
import os
from pathlib import Path

class SecureProviderConfig:
    @staticmethod
    def load_from_env():
        """Load provider config from environment variables."""
        return Provider(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
    
    @staticmethod
    def load_from_file(config_file="config/openai.json"):
        """Load provider config from secure file."""
        import json
        
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        with open(config_path) as f:
            config = json.load(f)
        
        return Provider(
            api_key=config["api_key"],
            model=config.get("model", "gpt-3.5-turbo"),
            base_url=config.get("base_url", "https://api.openai.com/v1")
        )
    
    @staticmethod
    def validate_provider(provider):
        """Validate provider configuration."""
        if not provider.api_key or provider.api_key == "sk-your-key":
            raise ValueError("Invalid or placeholder API key")
        
        if not provider.model:
            raise ValueError("Model not specified")
        
        return True

# Secure configuration examples
try:
    # Method 1: Environment variables (recommended)
    provider = SecureProviderConfig.load_from_env()
    SecureProviderConfig.validate_provider(provider)
    print("✅ Provider loaded from environment")
    
except Exception as e:
    print(f"❌ Environment config failed: {e}")
    
    try:
        # Method 2: Secure config file
        provider = SecureProviderConfig.load_from_file()
        SecureProviderConfig.validate_provider(provider)
        print("✅ Provider loaded from config file")
    
    except Exception as e:
        print(f"❌ File config failed: {e}")
        provider = None
```

### Rate Limiting and Error Handling

```python
import time
from datetime import datetime, timedelta

class RateLimitedProvider:
    def __init__(self, base_provider, requests_per_minute=60):
        self.base_provider = base_provider
        self.requests_per_minute = requests_per_minute
        self.request_times = []
    
    def _can_make_request(self):
        """Check if we can make a request without hitting rate limits."""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Remove old requests
        self.request_times = [t for t in self.request_times if t > one_minute_ago]
        
        return len(self.request_times) < self.requests_per_minute
    
    def _wait_for_rate_limit(self):
        """Wait until we can make a request."""
        while not self._can_make_request():
            time.sleep(1)
    
    def chat_with_rate_limit(self, rag, question):
        """Chat with automatic rate limiting."""
        self._wait_for_rate_limit()
        
        try:
            response = rag.chat(question)
            self.request_times.append(datetime.now())
            return response
        
        except Exception as e:
            if "rate limit" in str(e).lower():
                print("Rate limit hit, waiting...")
                time.sleep(60)  # Wait a minute
                return self.chat_with_rate_limit(rag, question)
            else:
                raise e

# Rate limiting example
base_provider = Provider(model="gpt-3.5-turbo", api_key="sk-your-key")
rate_limited_provider = RateLimitedProvider(base_provider, requests_per_minute=30)

rag = TinyRag(provider=base_provider)
rag.add_documents(["docs/"])

# This will automatically respect rate limits
questions = ["Question 1", "Question 2", "Question 3"]
for question in questions:
    response = rate_limited_provider.chat_with_rate_limit(rag, question)
    print(f"Q: {question}\nA: {response[:100]}...\n")
```

## 📊 Provider Performance Monitoring

### Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.usage_log = []
        
        # Approximate costs per 1K tokens (update with current pricing)
        self.model_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
        }
    
    def estimate_tokens(self, text):
        """Rough token estimation (4 characters ≈ 1 token)."""
        return len(text) // 4
    
    def log_usage(self, model, input_text, output_text):
        """Log API usage for cost tracking."""
        input_tokens = self.estimate_tokens(input_text)
        output_tokens = self.estimate_tokens(output_text)
        
        if model in self.model_costs:
            costs = self.model_costs[model]
            estimated_cost = (
                (input_tokens / 1000) * costs["input"] +
                (output_tokens / 1000) * costs["output"]
            )
        else:
            estimated_cost = 0
        
        usage = {
            "timestamp": datetime.now(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost": estimated_cost
        }
        
        self.usage_log.append(usage)
        return usage
    
    def get_cost_summary(self, days=7):
        """Get cost summary for recent usage."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_usage = [u for u in self.usage_log if u["timestamp"] > cutoff]
        
        if not recent_usage:
            return "No recent usage data."
        
        total_cost = sum(u["estimated_cost"] for u in recent_usage)
        total_requests = len(recent_usage)
        avg_cost_per_request = total_cost / total_requests if total_requests > 0 else 0
        
        return f"""
Cost Summary (last {days} days):
- Total requests: {total_requests}
- Estimated total cost: ${total_cost:.4f}
- Average cost per request: ${avg_cost_per_request:.4f}
- Most expensive model used: {max(recent_usage, key=lambda x: x['estimated_cost'])['model'] if recent_usage else 'N/A'}
"""

# Cost tracking example
cost_tracker = CostTracker()

def monitored_chat(rag, question):
    """Chat with cost monitoring."""
    response = rag.chat(question)
    
    # Log usage
    usage = cost_tracker.log_usage(
        model=rag.provider.model,
        input_text=question,
        output_text=response
    )
    
    print(f"Estimated cost: ${usage['estimated_cost']:.4f}")
    return response

# Usage
provider = Provider(model="gpt-4", api_key="sk-your-key")
rag = TinyRag(provider=provider)
rag.add_documents(["docs/"])

response = monitored_chat(rag, "Explain the main concepts")
print(cost_tracker.get_cost_summary())
```

## 🚀 Next Steps

Ready to optimize your AI providers:

- [**Performance Optimization**](11-performance.md) - Speed up provider responses
- [**Best Practices**](13-best-practices.md) - Production provider guidelines
- [**Troubleshooting**](14-troubleshooting.md) - Solve provider issues
- [**Real-world Examples**](15-examples.md) - Production provider setups

---

**Need help with specific providers?** Check the [FAQ](19-faq.md) for provider-specific guidance!