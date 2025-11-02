"""Data models for Math Routing Agent"""

from pydantic import BaseModel
from typing import Optional, List

class QuestionRequest(BaseModel):
    """Request model for math questions"""
    question: str
    context: Optional[str] = None

class SolutionResponse(BaseModel):
    """Response model for solutions"""
    question: str
    solution: str
    source: str  # "knowledge_base" or "web_search"
    steps: List[str]
    confidence: float

class FeedbackRequest(BaseModel):
    """Request model for user feedback"""
    question_id: str
    feedback_text: str
    rating: int  # 1-5
