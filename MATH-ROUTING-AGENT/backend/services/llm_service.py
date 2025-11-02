"""
LLM Service - Groq integration
Generates solutions for math problems
"""

import os
from typing import Optional
from groq import Groq


class LLMService:
    """Manages LLM operations using Groq"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant"):

        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        
        if not self.api_key:
            print("⚠️  WARNING: No Groq API key provided")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            print(f"🤖 LLM Service initialized with Groq model: {model}")
    
    async def generate_solution(self, prompt: str, question: str) -> str:
        """
        Generate step-by-step solution using LLM
        
        Args:
            prompt: Full prompt with context
            question: Original question (for fallback)
            
        Returns:
            Solution text
        """
        
        if not self.client:
            print("⚠️  No LLM client available, returning placeholder")
            return f"Solution for: {question}\n\nPlease provide Groq API key to generate solutions."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful math tutor. Provide clear, step-by-step solutions to math problems."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ LLM error: {str(e)}")
            return f"Error generating solution: {str(e)}"
    
    def format_web_results(self, question: str, web_context: str) -> dict:
        """
        Format web search results into clean step-by-step solution
        
        Args:
            question: User's question
            web_context: Combined web search results
            
        Returns:
            dict with 'solution', 'steps', 'topic', 'difficulty'
        """
        
        if not self.client:
            return {
                'solution': web_context,
                'steps': ['Web search results (Groq API key needed for formatting)'],
                'topic': 'General',
                'difficulty': 'Unknown'
            }
        
        try:
            prompt = f"""You are a math tutor answering a student's question. Read the web search results and provide a clear, educational response.

Question: {question}

Web Search Results:
{web_context}

Provide:
1. A clear, natural explanation (NOT mentioning "web search" or "sources")
2. Educational step-by-step breakdown (3-5 content-focused steps that explain the concept or solution)
3. Topic and Difficulty

Important: 
- Steps should be ABOUT THE MATH CONTENT, not about the search process
- Write like a tutor explaining directly to a student
- NO steps like "Search performed" or "Review sources"

Format your response as JSON:
{{
    "solution": "Clear explanation of the concept or solution",
    "steps": [
        "Key point 1 about the math concept",
        "Key point 2 explaining further",
        "Key point 3 with examples"
    ],
    "topic": "Number Theory",
    "difficulty": "Easy"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful math tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            print(f"❌ Error formatting web results: {str(e)}")
            return {
                'solution': web_context,
                'steps': ['Search performed', 'Results retrieved', 'Review sources'],
                'topic': 'General',
                'difficulty': 'Unknown'
            }


# Initialize service
llm_service = LLMService()
