"""Guardrails for input/output filtering"""

from typing import Tuple
import re

class InputGuardrail:
    """Validates and filters user input"""
    
    MATH_KEYWORDS = {
        "algebra", "calculus", "geometry", "trigonometry", "matrix", "equation",
        "derivative", "integral", "solve", "prove", "evaluate", "simplify",
        "probability", "statistics", "linear", "quadratic", "polynomial",
        "function", "limit", "series", "number", "fraction", "percentage"
    }
    
    BLOCKED_KEYWORDS = {
        "hack", "exploit", "malware", "virus", "bomb", "illegal", "fraud",
        "steal", "harm", "hurt", "violence", "suicide", "drug"
    }
    
    @staticmethod
    def is_math_question(question: str) -> Tuple[bool, str]:
        """Check if question is math-related"""
        question_lower = question.lower()
        
        # Check for blocked content
        for keyword in InputGuardrail.BLOCKED_KEYWORDS:
            if keyword in question_lower:
                return False, f"Question contains blocked keyword: {keyword}"
        
        # Check if it's math-related
        has_math_keyword = any(
            keyword in question_lower 
            for keyword in InputGuardrail.MATH_KEYWORDS
        )
        
        if not has_math_keyword and len(question) < 20:
            return False, "Question is too short and doesn't appear to be math-related"
        
        return True, "Question is valid"
    
    @staticmethod
    def sanitize_question(question: str) -> str:
        """Clean and normalize question"""
        # Remove extra whitespace
        question = " ".join(question.split())
        # Remove special characters but keep mathematical ones
        question = re.sub(r'[<>{}|\\^]', '', question)
        return question


class OutputGuardrail:
    """Validates and filters model output"""
    
    @staticmethod
    def is_valid_solution(solution: str) -> Tuple[bool, str]:
        """Validate solution content"""
        
        if not solution or len(solution) < 10:
            return False, "Solution is too short"
        
        if len(solution) > 10000:
            return False, "Solution is too long"
        
        # Check for harmful content
        blocked_patterns = ["execute", "system call", "shell command"]
        for pattern in blocked_patterns:
            if pattern.lower() in solution.lower():
                return False, f"Solution contains suspicious content: {pattern}"
        
        return True, "Solution is valid"
    
    @staticmethod
    def sanitize_solution(solution: str) -> str:
        """Clean solution output"""
        # Remove extra newlines
        solution = re.sub(r'\n\n+', '\n\n', solution)
        # Strip leading/trailing whitespace
        solution = solution.strip()
        return solution
