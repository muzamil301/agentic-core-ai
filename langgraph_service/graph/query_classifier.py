"""
Query Classifier for LangGraph RAG Service

This module classifies user queries into different types to determine
the appropriate response strategy.
"""

from enum import Enum
from typing import Dict, Tuple, List
import re


class QueryType(Enum):
    """Enumeration of query types."""
    
    RAG_REQUIRED = "rag_required"      # Needs knowledge base search
    DIRECT_ANSWER = "direct_answer"     # Can answer directly
    GREETING = "greeting"              # Simple greeting
    UNCLEAR = "unclear"                 # Needs clarification


class QueryClassifier:
    """
    Classifies user queries into different types.
    
    Uses keyword matching and pattern recognition to determine:
    - Whether RAG is needed (domain-specific questions)
    - Whether direct answer is sufficient (general questions)
    - Whether it's a greeting
    - Whether query is unclear
    """
    
    def __init__(self):
        """Initialize the query classifier with patterns and keywords."""
        
        # Keywords that indicate RAG is required (domain-specific)
        self.rag_keywords: List[str] = [
            # Payment/transaction related
            "transaction", "limit", "daily", "monthly", "card", "payment",
            "balance", "account", "transfer", "withdraw", "deposit",
            "fee", "charge", "refund", "block", "unblock", "pin", "cvv",
            "statement", "history", "merchant", "authorization",
            
            # Account related
            "account", "profile", "settings", "password", "security",
            "verification", "kyc", "document", "update",
            
            # Support related
            "support", "help", "issue", "problem", "error", "failed",
            "not working", "how to", "how do", "what is", "where is",
        ]
        
        # Keywords that indicate direct answer (general knowledge)
        self.direct_answer_keywords: List[str] = [
            "weather", "time", "date", "joke", "fun fact", "tell me about",
            "explain", "what is", "who is", "when did", "where is",
            "capital", "population", "definition", "meaning",
        ]
        
        # Greeting patterns
        self.greeting_patterns: List[str] = [
            r"^(hi|hello|hey|greetings|good morning|good afternoon|good evening|good night)",
            r"^(thanks|thank you|thx|appreciate)",
            r"^(bye|goodbye|see you|farewell)",
            r"^(how are you|how's it going|what's up)",
        ]
        
        # Question patterns
        self.question_patterns: List[str] = [
            r"\?$",  # Ends with question mark
            r"^(what|who|when|where|why|how|which|can|could|should|would|is|are|do|does|did)",
        ]
    
    def classify_query(self, query: str) -> Tuple[QueryType, float, Dict]:
        """
        Classify a user query.
        
        Args:
            query: The user's query string
            
        Returns:
            Tuple of:
            - QueryType: The classified type
            - float: Confidence score (0.0 to 1.0)
            - Dict: Additional metadata about the classification
        """
        if not query or not query.strip():
            return QueryType.UNCLEAR, 1.0, {
                "reason": "empty_query",
                "original_query": query
            }
        
        query_lower = query.lower().strip()
        query_length = len(query_lower)
        
        # Check for empty or very short queries
        if query_length < 2:
            return QueryType.UNCLEAR, 1.0, {
                "reason": "too_short",
                "original_query": query,
                "length": query_length
            }
        
        # Check for greetings first (simple greetings take priority)
        greeting_score = self._check_greeting(query_lower)
        
        # Check for RAG keywords (domain-specific)
        rag_score = self._check_rag_keywords(query_lower)
        
        # Check for direct answer keywords
        direct_score = self._check_direct_answer_keywords(query_lower)
        
        # If strong greeting pattern, prioritize greeting (unless very strong RAG signal)
        # This handles cases like "Thanks for your help" which should be greeting
        if greeting_score > 0.7:
            # Only override if RAG signal is very weak
            if rag_score < 0.5:
                return QueryType.GREETING, greeting_score, {
                    "reason": "greeting_pattern",
                    "original_query": query,
                    "matched_pattern": "greeting"
                }
            # If it's a simple acknowledgment phrase, still treat as greeting
            elif self._is_simple_acknowledgment(query_lower):
                return QueryType.GREETING, greeting_score, {
                    "reason": "greeting_acknowledgment",
                    "original_query": query,
                    "matched_pattern": "greeting"
                }
        
        # Check if it's a question
        is_question = self._is_question(query_lower)
        
        # Decision logic
        if rag_score > 0.5:
            # Strong RAG signal
            confidence = min(rag_score, 0.95)
            return QueryType.RAG_REQUIRED, confidence, {
                "reason": "rag_keywords_found",
                "original_query": query,
                "rag_score": rag_score,
                "is_question": is_question,
                "matched_keywords": self._get_matched_keywords(query_lower, self.rag_keywords)
            }
        
        elif direct_score > 0.5:
            # Direct answer signal
            confidence = min(direct_score, 0.95)
            return QueryType.DIRECT_ANSWER, confidence, {
                "reason": "direct_answer_keywords_found",
                "original_query": query,
                "direct_score": direct_score,
                "is_question": is_question,
                "matched_keywords": self._get_matched_keywords(query_lower, self.direct_answer_keywords)
            }
        
        elif is_question:
            # It's a question but unclear category - default to RAG
            # (safer to search knowledge base than guess)
            return QueryType.RAG_REQUIRED, 0.6, {
                "reason": "question_without_clear_category",
                "original_query": query,
                "is_question": True,
                "rag_score": rag_score,
                "direct_score": direct_score
            }
        
        else:
            # Unclear query
            return QueryType.UNCLEAR, 0.5, {
                "reason": "unclear_intent",
                "original_query": query,
                "rag_score": rag_score,
                "direct_score": direct_score,
                "is_question": is_question
            }
    
    def _check_greeting(self, query_lower: str) -> float:
        """Check if query matches greeting patterns."""
        # Check exact greeting patterns first
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return 0.9
        
        # Check for simple greetings (but not if they're part of a longer query)
        simple_greetings = ["hi", "hello", "hey", "thanks", "thank you", "bye"]
        for greeting in simple_greetings:
            # Only match if it's a standalone word or at the start
            if re.search(rf"^{greeting}\s|{greeting}$|^{greeting}\?", query_lower, re.IGNORECASE):
                return 0.8
        
        return 0.0
    
    def _check_rag_keywords(self, query_lower: str) -> float:
        """Check how many RAG keywords are present."""
        matches = sum(1 for keyword in self.rag_keywords if keyword in query_lower)
        
        if matches == 0:
            return 0.0
        elif matches == 1:
            return 0.5
        elif matches == 2:
            return 0.75
        else:
            return min(0.9, 0.5 + (matches * 0.1))
    
    def _check_direct_answer_keywords(self, query_lower: str) -> float:
        """Check how many direct answer keywords are present."""
        matches = sum(1 for keyword in self.direct_answer_keywords if keyword in query_lower)
        
        if matches == 0:
            return 0.0
        elif matches == 1:
            return 0.5
        elif matches >= 2:
            return 0.8
    
    def _is_question(self, query_lower: str) -> bool:
        """Check if query is a question."""
        # Check question mark
        if "?" in query_lower:
            return True
        
        # Check question patterns
        for pattern in self.question_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _get_matched_keywords(self, query_lower: str, keywords: List[str]) -> List[str]:
        """Get list of matched keywords."""
        return [kw for kw in keywords if kw in query_lower]
    
    def _is_simple_acknowledgment(self, query_lower: str) -> bool:
        """Check if query is a simple acknowledgment (thanks, etc.)."""
        acknowledgment_patterns = [
            r"^(thanks|thank you|thx|appreciate)",
            r"^(thanks|thank you|thx|appreciate)\s+for",
        ]
        for pattern in acknowledgment_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return True
        return False


def classify_query(query: str) -> Tuple[QueryType, float, Dict]:
    """
    Convenience function to classify a query.
    
    Args:
        query: The user's query string
        
    Returns:
        Tuple of (QueryType, confidence, metadata)
    """
    classifier = QueryClassifier()
    return classifier.classify_query(query)

