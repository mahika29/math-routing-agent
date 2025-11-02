import dspy
from typing import List, Dict
import os

# Math Solution Signature
class MathSolutionSignature(dspy.Signature):
    """Generate step-by-step math solutions with educational clarity."""
    
    question: str = dspy.InputField(desc="Mathematical question to solve")
    context: str = dspy.InputField(desc="Additional context from knowledge base or web search")
    class_level: str = dspy.InputField(desc="Student class level (9-12 or JEE)")
    
    steps: List[str] = dspy.OutputField(desc="Step-by-step solution breakdown")
    final_answer: str = dspy.OutputField(desc="Final answer with units if applicable")
    explanation: str = dspy.OutputField(desc="Educational explanation for students")


class MathTutorModule(dspy.Module):
    """DSPy-powered Math Tutor with feedback optimization."""
    
    def __init__(self, groq_api_key: str):
        super().__init__()
        
        # Initialize Groq LLM via DSPy
        lm = dspy.LM(
            model='groq/llama-3.1-8b-instant',
            api_key=groq_api_key
        )
        dspy.configure(lm=lm)
        
        # Create predictor with Chain of Thought
        self.generate_solution = dspy.ChainOfThought(MathSolutionSignature)
    
    def forward(self, question: str, context: str, class_level: str):
        """Generate math solution using DSPy."""
        
        # Generate prediction
        prediction = self.generate_solution(
            question=question,
            context=context,
            class_level=class_level
        )
        
        # Quality assertions (DSPy auto-retries if fails)
        dspy.Suggest(
            len(prediction.steps) >= 2,
            "Solution must have at least 2 steps for clarity"
        )
        
        dspy.Suggest(
            len(prediction.final_answer) > 0,
            "Must provide a clear final answer"
        )
        
        return prediction


class FeedbackOptimizer:
    """Optimizes prompts based on human feedback."""
    
    def __init__(self, groq_api_key: str):
        self.tutor = MathTutorModule(groq_api_key)
        self.feedback_data = []
    
    async def collect_feedback(self, question: str, response: Dict, rating: str):
        """Collect user feedback (thumbs up/down)."""
        self.feedback_data.append({
            "question": question,
            "response": response,
            "rating": rating  # "up" or "down"
        })
    
    async def optimize_prompts(self):
        """Optimize DSPy prompts using collected feedback."""
        if len(self.feedback_data) < 5:
            return {
                "status": "insufficient_data",
                "message": f"Need at least 5 feedback samples. Current: {len(self.feedback_data)}"
            }
        
        # Filter positive examples
        good_examples = [
            {"question": item["question"], "answer": str(item["response"])}
            for item in self.feedback_data if item["rating"] == "up"
        ]
        
        if len(good_examples) < 3:
            return {
                "status": "insufficient_positive",
                "message": f"Need at least 3 positive examples. Current: {len(good_examples)}"
            }
        
        # Use DSPy optimizer (BootstrapFewShot)
        from dspy.teleprompt import BootstrapFewShot
        
        optimizer = BootstrapFewShot(metric=self.feedback_metric)
        optimized_tutor = optimizer.compile(
            student=self.tutor,
            trainset=good_examples[:5]  # Use top 5 good examples
        )
        
        self.tutor = optimized_tutor
        return {
            "status": "optimized",
            "examples_used": len(good_examples[:5]),
            "total_feedback": len(self.feedback_data)
        }
    
    def feedback_metric(self, example, prediction, trace=None):
        """Define what makes a good solution."""
        # Simple metric: check if steps exist and answer is non-empty
        return len(prediction.steps) >= 2 and len(prediction.final_answer) > 0


# Singleton instance - will be initialized in main.py
dspy_optimizer = None

def init_dspy_optimizer(groq_api_key: str):
    """Initialize the DSPy optimizer with API key."""
    global dspy_optimizer
    dspy_optimizer = FeedbackOptimizer(groq_api_key)
    return dspy_optimizer
