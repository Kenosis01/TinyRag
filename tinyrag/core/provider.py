"""
Provider class for handling API interactions and embeddings with multi-provider support
"""

import requests
import json
import os
from typing import List, Optional, Dict, Any
from sentence_transformers import SentenceTransformer


class Provider:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        embedding_model: str = "default",
        embedding_provider: str = "local",  # New: "local", "openai", "ollama", "custom"
        base_url: str = "https://api.openai.com/v1",
        ollama_base_url: str = "http://localhost:11434",
        custom_embedding_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Provider with support for multiple embedding backends
        
        Args:
            api_key: API key for cloud providers (OpenAI, etc.)
            model: Chat model name (for LLM functionality)
            embedding_model: Embedding model name
            embedding_provider: Type of embedding provider:
                - "local": Use local sentence-transformers models
                - "openai": Use OpenAI embeddings API
                - "ollama": Use local Ollama embeddings
                - "custom": Use custom embedding function
            base_url: Base URL for OpenAI-compatible APIs
            ollama_base_url: Base URL for Ollama server
            custom_embedding_config: Configuration for custom embedding providers
        """
        self.api_key = api_key
        self.model = model
        self.embedding_model = embedding_model
        self.embedding_provider = embedding_provider.lower()
        self.base_url = base_url.rstrip('/')
        self.ollama_base_url = ollama_base_url.rstrip('/')
        self.custom_embedding_config = custom_embedding_config or {}
        
        # Initialize embedding backend
        self._init_embedding_backend()
    
    def _init_embedding_backend(self):
        """Initialize the appropriate embedding backend based on provider type"""
        
        if self.embedding_provider == "local":
            # Local sentence-transformers models
            try:
                if self.embedding_model == "default":
                    model_name = 'all-MiniLM-L6-v2'
                else:
                    model_name = self.embedding_model
                
                print(f"Loading local embedding model: {model_name}")
                self.local_embedder = SentenceTransformer(model_name)
                self.embedding_dimension = self.local_embedder.get_sentence_embedding_dimension()
                print(f"✅ Local embedder loaded (dimension: {self.embedding_dimension})")
                
            except Exception as e:
                print(f"❌ Error loading local embedding model: {e}")
                print("Falling back to all-MiniLM-L6-v2")
                self.local_embedder = SentenceTransformer('all-MiniLM-L6-v2')
                self.embedding_dimension = 384
                
        elif self.embedding_provider == "openai":
            # OpenAI embeddings API
            self.local_embedder = None
            if self.embedding_model == "default":
                self.embedding_model = "text-embedding-ada-002"
            self.embedding_dimension = 1536  # OpenAI embedding dimension
            
        elif self.embedding_provider == "ollama":
            # Ollama local embeddings
            self.local_embedder = None
            if self.embedding_model == "default":
                self.embedding_model = "nomic-embed-text"  # Popular Ollama embedding model
            # Dimension will be determined dynamically
            self.embedding_dimension = None
            
        elif self.embedding_provider == "custom":
            # Custom embedding function
            self.local_embedder = None
            self.custom_embedding_function = self.custom_embedding_config.get('function')
            self.embedding_dimension = self.custom_embedding_config.get('dimension', 768)
            
        else:
            raise ValueError(f"Unsupported embedding provider: {self.embedding_provider}. "
                           f"Supported: local, openai, ollama, custom")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding model"""
        return self.embedding_dimension
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using the configured provider"""
        
        if self.embedding_provider == "local":
            return self._get_local_embeddings(texts)
            
        elif self.embedding_provider == "openai":
            return self._get_openai_embeddings(texts)
            
        elif self.embedding_provider == "ollama":
            return self._get_ollama_embeddings(texts)
            
        elif self.embedding_provider == "custom":
            return self._get_custom_embeddings(texts)
            
        else:
            raise ValueError(f"Unknown embedding provider: {self.embedding_provider}")
    
    def _get_local_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings using local sentence-transformers"""
        try:
            embeddings = self.local_embedder.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            raise Exception(f"Local embedding error: {e}")
    
    def _get_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings using OpenAI API"""
        if not self.api_key:
            raise ValueError("API key required for OpenAI embeddings")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "input": texts,
            "model": self.embedding_model
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return [item["embedding"] for item in result["data"]]
            else:
                raise Exception(f"OpenAI API error {response.status_code}: {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"OpenAI API request failed: {e}")
    
    def _get_ollama_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings using Ollama local server"""
        try:
            embeddings = []
            for text in texts:
                data = {
                    "model": self.embedding_model,
                    "prompt": text
                }
                
                response = requests.post(
                    f"{self.ollama_base_url}/api/embeddings",
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    embedding = result["embedding"]
                    embeddings.append(embedding)
                    
                    # Set dimension on first successful call
                    if self.embedding_dimension is None:
                        self.embedding_dimension = len(embedding)
                else:
                    raise Exception(f"Ollama API error {response.status_code}: {response.text}")
            
            return embeddings
            
        except requests.RequestException as e:
            raise Exception(f"Ollama API request failed: {e}. Make sure Ollama is running.")
    
    def _get_custom_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings using custom function"""
        if not self.custom_embedding_function:
            raise ValueError("Custom embedding function not provided")
        
        try:
            return self.custom_embedding_function(texts)
        except Exception as e:
            raise Exception(f"Custom embedding error: {e}")
    
    def chat_completion(self, messages: List[dict], temperature: float = 0.7) -> str:
        """Generate chat completion using the provider's API"""
        if not self.api_key:
            raise ValueError("API key required for chat completion")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Chat API error {response.status_code}: {response.text}")
                
        except requests.RequestException as e:
            raise Exception(f"Chat API request failed: {e}")
    
    @classmethod
    def create_local_provider(cls, model_name: str = "all-MiniLM-L6-v2") -> 'Provider':
        """Create a provider with local embeddings only"""
        return cls(
            embedding_provider="local",
            embedding_model=model_name
        )
    
    @classmethod
    def create_openai_provider(cls, api_key: str, 
                              chat_model: str = "gpt-3.5-turbo",
                              embedding_model: str = "text-embedding-ada-002") -> 'Provider':
        """Create a provider with OpenAI embeddings and chat"""
        return cls(
            api_key=api_key,
            model=chat_model,
            embedding_model=embedding_model,
            embedding_provider="openai"
        )
    
    @classmethod
    def create_ollama_provider(cls, 
                              embedding_model: str = "nomic-embed-text",
                              chat_model: str = "llama2",
                              ollama_url: str = "http://localhost:11434") -> 'Provider':
        """Create a provider with Ollama embeddings"""
        return cls(
            model=chat_model,
            embedding_model=embedding_model,
            embedding_provider="ollama",
            ollama_base_url=ollama_url
        )
    
    @classmethod
    def create_custom_provider(cls, embedding_function, dimension: int,
                              api_key: Optional[str] = None,
                              chat_model: str = "gpt-3.5-turbo") -> 'Provider':
        """Create a provider with custom embedding function"""
        return cls(
            api_key=api_key,
            model=chat_model,
            embedding_provider="custom",
            custom_embedding_config={
                'function': embedding_function,
                'dimension': dimension
            }
        )