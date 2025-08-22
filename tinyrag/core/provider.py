"""
Provider class for handling API interactions and embeddings
"""

import requests
import json
from typing import List, Optional
from sentence_transformers import SentenceTransformer


class Provider:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        embedding_model: str = "default",
        base_url: str = "https://api.openai.com/v1"
    ):
        self.api_key = api_key
        self.model = model
        self.embedding_model = embedding_model
        self.base_url = base_url.rstrip('/')
        
        # Initialize local embedding model if using default
        if self.embedding_model == "default":
            self.local_embedder = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.local_embedder = None
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        if self.embedding_model == "default":
            return self.local_embedder.encode(texts).tolist()
        else:
            # Use provider's embedding API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "input": texts,
                "model": self.embedding_model
            }
            
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return [item["embedding"] for item in result["data"]]
            else:
                raise Exception(f"Embedding API error: {response.text}")
    
    def chat_completion(self, messages: List[dict]) -> str:
        """Generate chat completion using the provider's API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Chat API error: {response.text}")