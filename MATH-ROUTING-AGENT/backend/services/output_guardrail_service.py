class OutputGuardrailService:
    """Validates LLM-generated responses for safety and academic relevance."""
    
    def __init__(self):
        # Academic keywords (more flexible)
        self.academic_keywords = [
            'formula', 'equation', 'solve', 'calculate', 'theorem', 'proof',
            'derivative', 'integral', 'area', 'volume', 'angle', 'triangle',
            'square', 'circle', 'rectangle', 'velocity', 'acceleration',
            'force', 'energy', 'mass', 'algebra', 'geometry', 'calculus',
            'trigonometry', 'physics', 'chemistry', 'mathematics', 'solution',
            'answer', 'step', 'method', 'process', 'value', 'result',
            'x =', 'y =', '=', '+', '-', '×', '÷', 'sin', 'cos', 'tan',
            'log', 'ln', 'sqrt', 'power', 'exponent', 'root'
        ]
        
        # Harmful content patterns
        self.harmful_patterns = [
            'kill', 'weapon', 'drug', 'illegal', 'hack', 'exploit',
            'bomb', 'violence', 'racist', 'hate', 'suicide'
        ]
    
    def validate_response(self, response: str, original_question: str) -> tuple[bool, str]:
        """
        Validate LLM response for safety and academic content.
        Returns: (is_safe: bool, reason: str)
        """
        
        if not response or len(response.strip()) < 10:
            return False, "Response is too short or empty"
        
        response_lower = response.lower()
        question_lower = original_question.lower()
        
        # Check for harmful content
        for pattern in self.harmful_patterns:
            if pattern in response_lower:
                return False, f"Response contains harmful content: {pattern}"
        
        # RELAXED CHECK: If response has math symbols or academic keywords → PASS
        academic_score = sum(1 for keyword in self.academic_keywords if keyword in response_lower)
        
        # Also check if question was academic (even with typos)
        question_academic_score = sum(1 for keyword in self.academic_keywords if keyword in question_lower)
        
        # If either response OR question has academic content → PASS
        if academic_score >= 2 or question_academic_score >= 1:
            return True, "Response is academic and safe"
        
        # Fallback: Check if response contains numbers or mathematical operations
        import re
        has_numbers = bool(re.search(r'\d+', response))
        has_math_ops = any(op in response for op in ['+', '-', '×', '÷', '=', '*', '/'])
        
        if has_numbers and has_math_ops:
            return True, "Response contains mathematical operations"
        
        return False, "⚠️ Response doesn't contain academic content. Must be Math/Physics/Chemistry"


# Singleton instance
output_guardrail = OutputGuardrailService()
