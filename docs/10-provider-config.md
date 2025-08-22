# Provider Configuration

Configure AI providers and models for TinyRag's chat functionality. Support for OpenAI, Anthropic, local models, and custom endpoints.

## 🎯 What is a Provider?

A Provider in TinyRag handles the connection to AI language models. It manages API keys, model selection, and communication with AI services.

## 🚀 Basic Provider Setup

### OpenAI Provider

```python
from tinyrag import Provider, TinyRag

# Basic OpenAI setup
provider = Provider(
    api_key="sk-your-openai-key",
    model="gpt-4",
    base_url="https://api.openai.com/v1"
)

# Use with TinyRag
rag = TinyRag(provider=provider)
```

### Environment Variables (Recommended)

```python
import os

# Set environment variable (more secure)
os.environ["OPENAI_API_KEY"] = "sk-your-openai-key"

# Provider automatically uses environment variable
provider = Provider(
    model="gpt-4"
    # api_key automatically loaded from OPENAI_API_KEY
)
```

### Complete Configuration Example

```python
# Full provider configuration
provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",
    embedding_model="text-embedding-ada-002",
    base_url="https://api.openai.com/v1",
    temperature=0.7,
    max_tokens=2000
)

rag = TinyRag(
    provider=provider,
    vector_store="faiss",
    system_prompt="You are a helpful assistant."
)
```

## 🤖 Supported Models

### OpenAI Models

```python
# GPT-4 Models (recommended for best quality)
gpt4_provider = Provider(
    model="gpt-4",              # Latest GPT-4
    api_key="sk-your-key"
)

gpt4_turbo_provider = Provider(
    model="gpt-4-turbo",        # Faster, cheaper GPT-4
    api_key="sk-your-key"
)

# GPT-3.5 Models (faster, cheaper)
gpt35_provider = Provider(
    model="gpt-3.5-turbo",      # Standard GPT-3.5
    api_key="sk-your-key"
)

gpt35_16k_provider = Provider(
    model="gpt-3.5-turbo-16k",  # Larger context window
    api_key="sk-your-key"
)

# Compare model performance
models = {
    "GPT-4": gpt4_provider,
    "GPT-4 Turbo": gpt4_turbo_provider,
    "GPT-3.5": gpt35_provider
}

question = "Explain machine learning in simple terms"

for model_name, provider in models.items():
    rag = TinyRag(provider=provider)
    rag.add_documents(["ml_docs.txt"])
    
    response = rag.chat(question)
    print(f"\n=== {model_name} ===")
    print(response[:200] + "...")
```

### Model Selection Guidelines

```python
def choose_model(use_case, budget="medium"):
    """Recommend model based on use case and budget."""
    
    recommendations = {
        ("high_quality", "high"): "gpt-4",
        ("high_quality", "medium"): "gpt-4-turbo", 
        ("high_quality", "low"): "gpt-3.5-turbo",
        
        ("fast_response", "high"): "gpt-4-turbo",
        ("fast_response", "medium"): "gpt-3.5-turbo",
        ("fast_response", "low"): "gpt-3.5-turbo",
        
        ("large_context", "high"): "gpt-4",
        ("large_context", "medium"): "gpt-4-turbo",
        ("large_context", "low"): "gpt-3.5-turbo-16k",
        
        ("code_analysis", "high"): "gpt-4",
        ("code_analysis", "medium"): "gpt-4-turbo",
        ("code_analysis", "low"): "gpt-3.5-turbo"
    }
    
    return recommendations.get((use_case, budget), "gpt-3.5-turbo")

# Usage examples
customer_support_model = choose_model("fast_response", "low")      # gpt-3.5-turbo
research_model = choose_model("high_quality", "high")             # gpt-4
code_review_model = choose_model("code_analysis", "medium")       # gpt-4-turbo

print(f"Customer Support: {customer_support_model}")
print(f"Research: {research_model}")
print(f"Code Review: {code_review_model}")
```

## 🔧 Advanced Provider Configuration

### Custom Parameters

```python
# Fine-tune model behavior
custom_provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",
    temperature=0.3,        # Lower = more focused, higher = more creative
    max_tokens=1500,        # Maximum response length
    top_p=0.9,             # Nucleus sampling parameter
    frequency_penalty=0.1,  # Reduce repetition
    presence_penalty=0.1    # Encourage topic diversity
)

# Different configurations for different purposes
configs = {
    "creative": Provider(
        model="gpt-4",
        temperature=0.9,    # High creativity
        top_p=0.95,
        max_tokens=2000
    ),
    
    "analytical": Provider(
        model="gpt-4",
        temperature=0.2,    # Low creativity, focused
        top_p=0.8,
        max_tokens=1500
    ),
    
    "balanced": Provider(
        model="gpt-4-turbo",
        temperature=0.7,    # Balanced
        max_tokens=1200
    )
}

# Use different configs for different tasks
creative_rag = TinyRag(provider=configs["creative"])
analytical_rag = TinyRag(provider=configs["analytical"])
```

### Embedding Model Configuration

```python
# Custom embedding models
provider = Provider(
    api_key="sk-your-key",
    model="gpt-4",
    embedding_model="text-embedding-ada-002",  # OpenAI embedding
    embedding_dimensions=1536                  # Optional: specify dimensions
)

# Different embedding models for different purposes
embedding_configs = {
    "standard": "text-embedding-ada-002",      # General purpose
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