from tinyrag import Provider, TinyRag

provider = Provider(
    api_key="sk-xxxxxx",
    model="gpt-4",
    embedding_model="default",
    base_url="https://api.openai.com/v1"
)

rag = TinyRag(provider=provider, vector_store="faiss")

rag.add_documents("path/to/docs_or_raw_text")

response = rag.chat("Summarize the documents.")

print(response)