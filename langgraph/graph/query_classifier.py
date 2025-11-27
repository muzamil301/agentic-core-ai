"""
Query Classification for Intelligent Routing

This module classifies user queries to determine whether they should be:
1. Answered using RAG (knowledge base lookup)
2. Answered directly by LLM (general questions)
3. Handled with special logic (greetings, etc.)
"""

import re
from typing import Dict, List, Tuple
from enum import Enum


class QueryType(Enum):
    """Types of queries for routing decisions."""
    RAG_REQUIRED = "rag_required"      # Needs knowledge base lookup
    DIRECT_ANSWER = "direct_answer"    # Can be answered directly by LLM
    GREETING = "greeting"              # Simple greeting/social
    UNCLEAR = "unclear"                # Needs clarification


class QueryClassifier:
    """
    Classifies user queries to determine the best response strategy.
    """
    
    def __init__(self):
        """Initialize the classifier with patterns and keywords."""
        
        # Keywords that typically require RAG (knowledge base lookup)
        self.rag_keywords = [
            # Payment/Banking specific
            "transaction", "limit", "daily", "weekly", "monthly", "spending",
            "account", "tier", "basic", "premium", "metal",
            "card", "block", "freeze", "unfreeze", "lost", "stolen",
            "transfer", "international", "sepa", "wire", "remittance",
            "fee", "charge", "cost", "rate", "exchange",
            "balance", "statement", "history",
            
            # Support specific
            "how to", "how do i", "what is", "where can", "when does",
            "policy", "rule", "procedure", "process",
            "support", "help", "assistance", "contact",
        ]
        
        # Greeting patterns
        self.greeting_patterns = [
            r"^(hi|hello|hey|good morning|good afternoon|good evening)",
            r"^(thanks|thank you|bye|goodbye|see you)",
            r"^(how are you|what's up|how's it going)",
        ]
        
        # Direct answer patterns (general questions not requiring knowledge base)
        self.direct_patterns = [
            r"(what.*weather|weather.*like)",
            r"(what.*time|current time|time now)",
            r"(what.*date|today's date|current date)",
            r"(tell me.*joke|make me laugh)",
            r"(who are you|what are you|your name)",
            r"(how.*work|explain.*work|describe.*work)",
        ]
        
        # Question indicators that suggest RAG might be needed
        self.question_indicators = [
            "what is", "what are", "how do", "how to", "where can", "when does",
            "why does", "which", "who can", "can i", "should i", "may i",
            "tell me about", "explain", "describe", "show me"
        ]
    
    def classify_query(self, query: str) -> Tuple[QueryType, float, Dict]:
        """
        Classify a user query and return the type with confidence score.
        
        Args:
            query: User's input query
            
        Returns:
            Tuple of (QueryType, confidence_score, metadata)
        """
        query_lower = query.lower().strip()
        metadata = {
            "original_query": query,
            "processed_query": query_lower,
            "reasoning": []
        }
        
        # Check for greetings first
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower):
                metadata["reasoning"].append("Matched greeting pattern")
                return QueryType.GREETING, 0.9, metadata
        
        # Check for direct answer patterns
        for pattern in self.direct_patterns:
            if re.search(pattern, query_lower):
                metadata["reasoning"].append("Matched direct answer pattern")
                return QueryType.DIRECT_ANSWER, 0.8, metadata
        
        # Count RAG-related keywords
        rag_score = 0
        matched_keywords = []
        
        for keyword in self.rag_keywords:
            if keyword in query_lower:
                rag_score += 1
                matched_keywords.append(keyword)
        
        metadata["matched_rag_keywords"] = matched_keywords
        metadata["rag_keyword_count"] = rag_score
        
        # Check for question indicators
        question_score = 0
        for indicator in self.question_indicators:
            if indicator in query_lower:
                question_score += 1
                metadata["reasoning"].append(f"Found question indicator: {indicator}")
        
        # Decision logic
        if rag_score >= 2:  # Multiple RAG keywords
            metadata["reasoning"].append("Multiple RAG keywords found")
            return QueryType.RAG_REQUIRED, min(0.9, 0.6 + rag_score * 0.1), metadata
        
        elif rag_score >= 1 and question_score >= 1:  # RAG keyword + question
            metadata["reasoning"].append("RAG keyword + question indicator")
            return QueryType.RAG_REQUIRED, 0.7, metadata
        
        elif question_score >= 1:  # Question but no clear RAG keywords
            metadata["reasoning"].append("Question detected, trying RAG first")
            return QueryType.RAG_REQUIRED, 0.5, metadata
        
        elif len(query_lower.split()) <= 3:  # Very short queries
            metadata["reasoning"].append("Short query, unclear intent")
            return QueryType.UNCLEAR, 0.3, metadata
        
        else:  # Default to direct answer for general queries
            metadata["reasoning"].append("No clear RAG indicators, using direct answer")
            return QueryType.DIRECT_ANSWER, 0.6, metadata
    
    def should_use_rag(self, query: str, threshold: float = 0.5) -> bool:
        """
        Simple boolean check if RAG should be used.
        
        Args:
            query: User's input query
            threshold: Confidence threshold for RAG decision
            
        Returns:
            True if RAG should be used, False otherwise
        """
        query_type, confidence, _ = self.classify_query(query)
        
        if query_type == QueryType.RAG_REQUIRED and confidence >= threshold:
            return True
        
        return False

