"""
Prompt templates for RAG.

This module contains all prompt templates used in the RAG pipeline.
"""

SYSTEM_PROMPT = """You are a helpful payment support assistant. 
Answer questions based ONLY on the provided context from the knowledge base.
If the context doesn't contain the answer to the user's question, politely say that you don't have that information available.
Be concise, accurate, and friendly in your responses.
"""

CONTEXT_FORMAT = """Context from knowledge base:

{context}

---

Please answer the following question based on the context above. If the context doesn't contain the answer, say "I don't have that information in my knowledge base."
"""

USER_QUERY_FORMAT = """Question: {query}"""

def build_rag_prompt(query: str, context: str, include_system: bool = True) -> str:
    """
    Build a complete RAG prompt with context and query.
    
    Args:
        query: User's question
        context: Retrieved context from knowledge base
        include_system: Whether to include system instructions
    
    Returns:
        Formatted prompt string
    """
    if include_system:
        prompt = f"{SYSTEM_PROMPT}\n\n{CONTEXT_FORMAT.format(context=context)}\n\n{USER_QUERY_FORMAT.format(query=query)}"
    else:
        prompt = f"{CONTEXT_FORMAT.format(context=context)}\n\n{USER_QUERY_FORMAT.format(query=query)}"
    
    return prompt




