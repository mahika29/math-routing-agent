import json
import os
from datetime import datetime
from services.dspy_module import dspy_optimizer


class FeedbackService:
    def __init__(self, feedback_file="backend/data/feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_history = self._load_from_file()
    
    def _load_from_file(self):
        """Load feedback history from file."""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, "r") as f:
                return json.load(f)
        return []
    
    def _save_to_file(self):
        """Save feedback history to file."""
        os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
        with open(self.feedback_file, "w") as f:
            json.dump(self.feedback_history, f, indent=2)
    
    async def save_feedback(self, feedback_data: dict):
        """Save feedback and trigger DSPy optimization if threshold reached."""
        
        # Add timestamp
        feedback_data["timestamp"] = datetime.now().isoformat()
        
        # Save to history
        self.feedback_history.append(feedback_data)
        self._save_to_file()
        
        # NEW: Send feedback to DSPy optimizer
        if dspy_optimizer is not None:
            await dspy_optimizer.collect_feedback(
                question=feedback_data.get("question", ""),
                response=feedback_data.get("response", {}),
                rating=feedback_data.get("rating", "")  # "up" or "down"
            )
            
            # Auto-optimize after every 10 feedbacks
            if len(self.feedback_history) % 10 == 0:
                result = await dspy_optimizer.optimize_prompts()
                print(f"🔄 DSPy Optimization triggered: {result}")
        
        return {
            "status": "saved",
            "count": len(self.feedback_history),
            "feedback_id": len(self.feedback_history)
        }
    
    def get_feedback_stats(self):
        """Get feedback statistics."""
        positive = sum(1 for f in self.feedback_history if f.get("rating") == "up")
        negative = sum(1 for f in self.feedback_history if f.get("rating") == "down")
        
        return {
            "total_feedback": len(self.feedback_history),
            "positive": positive,
            "negative": negative,
            "positive_percentage": round((positive / len(self.feedback_history) * 100), 2) if self.feedback_history else 0
        }


# Singleton instance
feedback_service = FeedbackService()
