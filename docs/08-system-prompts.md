# Custom System Prompts

Learn how to customize AI behavior in TinyRag using system prompts. This is where TinyRag becomes truly powerful for domain-specific applications.

## 🎯 What Are System Prompts?

System prompts define how the AI assistant behaves and responds. They set the personality, expertise level, and response style for your RAG application.

## 🚀 Basic Usage

### Default System Prompt

```python
from tinyrag import Provider, TinyRag

provider = Provider(api_key="sk-your-key")
rag = TinyRag(provider=provider)

# Default prompt is:
# "You are a helpful assistant. Use the provided context to answer 
#  questions accurately. If the context doesn't contain relevant 
#  information, say so."
```

### Setting Custom Prompt

#### Method 1: During Initialization

```python
custom_prompt = "You are a technical expert. Provide detailed, accurate explanations with examples."

rag = TinyRag(
    provider=provider,
    system_prompt=custom_prompt
)
```

#### Method 2: After Initialization

```python
rag = TinyRag(provider=provider)

# Update prompt later
rag.set_system_prompt("You are a helpful coding assistant specializing in Python.")

# Check current prompt
current_prompt = rag.get_system_prompt()
print(current_prompt)
```

## 🎭 System Prompt Examples

### 1. Technical Documentation Assistant

```python
tech_prompt = """You are a technical documentation assistant. 
Provide clear, concise explanations with examples where helpful. 
Focus on practical implementation details and best practices. 
Use the provided context to give accurate technical information.
Format code examples with proper syntax highlighting."""

rag = TinyRag(provider=provider, system_prompt=tech_prompt)

# Add technical documentation
rag.add_documents([
    "api_documentation.pdf",
    "coding_standards.md",
    "architecture_guide.docx"
])

response = rag.chat("How do I implement user authentication?")
```

### 2. Customer Support Agent

```python
support_prompt = """You are a friendly and helpful customer support agent.
Always be polite, empathetic, and solution-focused.
Use the provided context to help resolve customer issues.
If you cannot find a solution in the context, apologize politely and 
suggest contacting technical support or escalating the issue.
Always end responses with asking if there's anything else you can help with."""

rag = TinyRag(provider=provider, system_prompt=support_prompt)

# Add support documentation
rag.add_documents([
    "faq.txt",
    "troubleshooting_guide.pdf",
    "user_manual.docx"
])

response = rag.chat("I can't log into my account")
```

### 3. Code Review Assistant

```python
code_review_prompt = """You are an expert code reviewer and software architect.
Analyze the provided code context and give constructive feedback.
Focus on:
- Code quality and readability
- Security vulnerabilities 
- Performance optimizations
- Best practices and design patterns
- Potential bugs or issues

Provide specific, actionable suggestions for improvement.
Be encouraging while being thorough in your analysis."""

rag = TinyRag(provider=provider, system_prompt=code_review_prompt)

# Add codebase
rag.add_codebase("my_project/")

response = rag.chat("Review the authentication module for security issues")
```

### 4. Educational Tutor

```python
tutor_prompt = """You are a patient and encouraging educational tutor.
Explain concepts clearly and break down complex topics into simple steps.
Use analogies and examples to help students understand difficult concepts.
Always encourage learning and ask follow-up questions to check understanding.
Adapt your explanation level based on the context provided.
End responses with a question to engage the student further."""

rag = TinyRag(provider=provider, system_prompt=tutor_prompt)

# Add educational content
rag.add_documents([
    "textbooks/",
    "lecture_notes/",
    "study_guides/"
])

response = rag.chat("Explain machine learning to me")
```

### 5. Medical Information Assistant

```python
medical_prompt = """You are a medical information assistant providing educational content.
Use the provided medical context to give accurate, evidence-based information.
Always include these important disclaimers:
- This information is for educational purposes only
- Always consult qualified healthcare professionals for medical advice
- Do not use this information for self-diagnosis or treatment

Be precise with medical terminology while keeping explanations accessible.
Emphasize the importance of professional medical consultation."""

rag = TinyRag(provider=provider, system_prompt=medical_prompt)

# Add medical literature
rag.add_documents([
    "medical_journals/",
    "health_guidelines.pdf",
    "treatment_protocols.docx"
])

response = rag.chat("What are the symptoms of hypertension?")
```

### 6. Legal Research Assistant

```python
legal_prompt = """You are a legal research assistant helping with legal document analysis.
Provide information based strictly on the legal documents and context provided.
Important disclaimers:
- This is not legal advice
- Consult qualified attorneys for legal matters
- Legal interpretations may vary by jurisdiction

Focus on:
- Relevant legal precedents and statutes
- Document analysis and key findings
- Factual legal information only
- Clear references to source materials"""

rag = TinyRag(provider=provider, system_prompt=legal_prompt)

# Add legal documents
rag.add_documents([
    "contracts/",
    "case_law.pdf", 
    "legal_opinions/"
])

response = rag.chat("What are the key terms in this contract?")
```

### 7. Creative Writing Assistant

```python
creative_prompt = """You are an enthusiastic creative writing assistant.
Help writers brainstorm ideas, develop characters, and improve their storytelling.
Be imaginative, inspiring, and constructive in your feedback.
Focus on:
- Story structure and plot development
- Character development and dialogue
- Setting and world-building
- Writing style and technique

Encourage creativity while providing practical writing advice.
Use the provided context to enhance creative projects."""

rag = TinyRag(provider=provider, system_prompt=creative_prompt)

# Add writing resources
rag.add_documents([
    "writing_guides/",
    "character_development.pdf",
    "plot_structures.txt"
])

response = rag.chat("Help me develop a compelling antagonist for my story")
```

### 8. Financial Advisor Assistant

```python
financial_prompt = """You are a financial education assistant providing general financial information.
Use the provided financial context to explain concepts and provide educational content.
Important disclaimers:
- This is educational information only, not financial advice
- Consult certified financial advisors for personalized advice
- Past performance does not guarantee future results
- Consider your personal financial situation and risk tolerance

Focus on explaining financial concepts clearly and providing general guidance based on established financial principles."""

rag = TinyRag(provider=provider, system_prompt=financial_prompt)

# Add financial resources
rag.add_documents([
    "investment_guides/",
    "financial_planning.pdf",
    "market_analysis/"
])

response = rag.chat("Explain diversification in investment portfolios")
```

## 🎨 Advanced Prompt Techniques

### Dynamic Prompts Based on Content

```python
def create_domain_specific_prompt(domain):
    prompts = {
        "technical": "You are a senior software engineer. Focus on implementation details and best practices.",
        "business": "You are a business analyst. Focus on strategic insights and practical applications.",
        "academic": "You are a research assistant. Provide scholarly analysis with proper citations.",
        "creative": "You are a creative consultant. Think outside the box and inspire innovation."
    }
    return prompts.get(domain, "You are a helpful assistant.")

# Use different prompts for different content types
domain = "technical"
rag = TinyRag(
    provider=provider,
    system_prompt=create_domain_specific_prompt(domain)
)
```

### Context-Aware Prompts

```python
context_prompt = """You are an adaptive assistant. Analyze the context provided and adjust your response style:

- If context contains code: Act as a programming expert
- If context contains business documents: Focus on business insights  
- If context contains academic papers: Provide scholarly analysis
- If context contains technical specs: Give implementation guidance

Always match your expertise level to the complexity of the context provided."""

rag = TinyRag(provider=provider, system_prompt=context_prompt)
```

### Multi-Language Support

```python
multilingual_prompt = """You are a multilingual assistant. 
Respond in the same language as the user's question.
If the context is in a different language than the question, 
translate relevant information while maintaining accuracy.
Clearly indicate when you're translating content."""

rag = TinyRag(provider=provider, system_prompt=multilingual_prompt)
```

## 🔧 Best Practices

### 1. Be Specific

```python
# ❌ Vague
vague_prompt = "You are helpful."

# ✅ Specific  
specific_prompt = "You are a Python development expert specializing in web frameworks. Provide code examples and explain best practices for Django and Flask applications."
```

### 2. Set Clear Boundaries

```python
bounded_prompt = """You are a technical support assistant for our software product.
ONLY answer questions about:
- Installation and setup
- Basic troubleshooting
- Feature explanations
- Configuration options

For complex technical issues, billing questions, or feature requests, 
direct users to contact our specialized support teams."""
```

### 3. Include Format Instructions

```python
formatted_prompt = """You are a documentation assistant.
Format your responses as follows:
1. Brief summary (1-2 sentences)
2. Detailed explanation with examples
3. Additional resources or next steps
4. Use bullet points for lists
5. Include code examples in markdown blocks"""
```

### 4. Handle Missing Information

```python
comprehensive_prompt = """You are a research assistant.
When the provided context doesn't contain enough information:
1. Clearly state what information is missing
2. Provide what you can based on available context
3. Suggest specific questions or resources for finding missing information
4. Never make up or assume information not in the context"""
```

## 📊 Testing Your Prompts

### A/B Testing Different Prompts

```python
# Test different prompts with same query
prompts = {
    "formal": "You are a formal business consultant. Provide professional analysis.",
    "casual": "You are a friendly advisor. Keep explanations simple and conversational.",
    "technical": "You are a technical expert. Provide detailed implementation guidance."
}

query = "How should we implement user authentication?"

for style, prompt in prompts.items():
    rag = TinyRag(provider=provider, system_prompt=prompt)
    rag.add_documents(["auth_documentation.pdf"])
    
    response = rag.chat(query)
    print(f"\n=== {style.title()} Style ===")
    print(response[:200] + "...")
```

### Measuring Response Quality

```python
# Evaluate prompt effectiveness
def evaluate_prompt(prompt, test_queries, documents):
    rag = TinyRag(provider=provider, system_prompt=prompt)
    rag.add_documents(documents)
    
    results = []
    for query in test_queries:
        response = rag.chat(query)
        # Evaluate: length, relevance, helpfulness, etc.
        results.append({
            "query": query,
            "response": response,
            "length": len(response),
            "contains_examples": "```" in response
        })
    
    return results
```

## 🚀 Real-World Applications

### Customer Service Bot

```python
# Complete customer service implementation
service_prompt = """You are a customer service representative for TechCorp.
Be friendly, professional, and solution-oriented.
Always:
1. Acknowledge the customer's concern
2. Provide clear, step-by-step solutions
3. Offer additional help
4. Use the customer's name if provided

For complex issues, escalate to human support with ticket number."""

rag = TinyRag(provider=provider, system_prompt=service_prompt)
rag.add_documents(["support_kb/", "product_manuals/"])

# Interactive support session
def customer_support_chat():
    print("TechCorp Support Chat - How can I help you today?")
    while True:
        question = input("\nCustomer: ")
        if question.lower() in ['exit', 'quit', 'bye']:
            print("Support: Thank you for contacting TechCorp! Have a great day!")
            break
        
        response = rag.chat(question)
        print(f"Support: {response}")

# customer_support_chat()
```

## 📈 Next Steps

Ready to build more complex applications:

- [**Chat Functionality**](09-chat-functionality.md) - Build conversational interfaces
- [**Real-world Examples**](15-examples.md) - Complete application examples  
- [**Best Practices**](13-best-practices.md) - Production recommendations
- [**Integration Guide**](17-integration.md) - Connect with other tools

---

**Want to see system prompts in action?** Check out [Real-world Examples](15-examples.md) for complete applications!