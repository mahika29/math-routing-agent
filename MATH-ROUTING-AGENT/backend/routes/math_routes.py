from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.vector_service import vector_service
from services.guardrail_service import GuardrailService
from services.dspy_module import dspy_optimizer
from services.feedback_service import feedback_service
from services.mcp_service import mcp_service
from services.llm_service import llm_service
from services.benchmark_service import benchmark_service
from services.output_guardrail_service import output_guardrail
from fastapi import UploadFile, File
from services.file_upload_service import file_upload_service


router = APIRouter()
guardrail = GuardrailService()


class SolveRequest(BaseModel):
    question: str
    board: str = "CBSE"
    class_level: int = 10


class SolutionResponse(BaseModel):
    question: str
    solution: str
    steps: List[str]
    source: str
    topic: str
    difficulty: str
    confidence: float


@router.post("/solve", response_model=SolutionResponse)
async def solve_math_problem(req: SolveRequest):
    """Solve a math problem using VectorDB"""
    print(f"📝 Question: {req.question}")

    # INPUT GUARDRAIL: Check if question is math-related
    is_valid, reason = guardrail.is_academic_question(req.question)
    if not is_valid:
        print(f"🚫 Input Guardrail blocked: {reason}")
        return SolutionResponse(
            question=req.question,
            solution=f"⚠️ {reason}",
            steps=[reason, "Please ask a Math question."],
            source="input_guardrail",
            topic="invalid",
            difficulty="none",
            confidence=0.0
        )

    # Search in VectorDB
    result = vector_service.search(req.question, n_results=1)
    print(f"🔍 VectorDB Result: {result}")
    print(f"🔍 Score: {result['score'] if result else 'None'}")

    if result and result["score"] >= 0.5:
        print(f"✅ VectorDB Match! Confidence: {result['score']:.2%}")
        return SolutionResponse(
            question=req.question,
            solution=result["solution"],
            steps=result["steps"],
            source="knowledge_base",
            topic=result["topic"],
            difficulty=result["difficulty"],
            confidence=result["score"]
        )

    # Low confidence - search web via MCP
    print(f"🔍 Low confidence, searching web via MCP...")
    search_results = mcp_service.search_web(req.question, max_results=3)

    if search_results['success'] and search_results['results']:
        # Combine web results
        web_context = "\n\n".join([
            f"Source {i+1}: {r['title']}\n{r['content']}\nURL: {r['url']}"
            for i, r in enumerate(search_results['results'])
        ])
        
        # Use Groq to format the web results
        formatted_response = llm_service.format_web_results(req.question, web_context)
        
        # OUTPUT GUARDRAIL: Validate LLM response before returning
        is_safe, reason = output_guardrail.validate_response(
            formatted_response['solution'], 
            req.question
        )

        if not is_safe:
            print(f"🚨 OUTPUT GUARDRAIL BLOCKED: {reason}")
            return SolutionResponse(
                question=req.question,
                solution=f"🚫 {reason}\n\nPlease ask a Math/Physics/Chemistry question(JEE).",
                steps=["Response safety validation failed", "Content was not academic"],
                source="output_guardrail",
                topic="blocked",
                difficulty="unknown",
                confidence=0.0
            )
        
        # Response is safe - return normally
        return SolutionResponse(
            question=req.question,
            solution=formatted_response['solution'],
            steps=formatted_response['steps'],
            source="web_search",
            topic=formatted_response.get('topic', 'General'),
            difficulty=formatted_response.get('difficulty', 'Medium'),
            confidence=0.75
        )

    print(f"❌ No results from VectorDB or web")
    return SolutionResponse(
        question=req.question,
        solution="Solution not found in knowledge base or web",
        steps=["This problem is not in our database", "Web search also returned no results"],
        source="none",
        topic="unknown",
        difficulty="unknown",
        confidence=0.0
    )


@router.get("/formulas/{class_level}")
async def get_formulas(class_level: str):
    """Get formulas for specific class level"""
    import json
    from pathlib import Path
    
    try:
        formulas_file = Path(__file__).parent.parent / "data" / "formulas_by_class.json"
        with open(formulas_file, 'r', encoding='utf-8') as f:
            all_formulas = json.load(f)
        if class_level not in all_formulas:
            return {"error": f"No formulas found for class {class_level}"}
        return {
            "class_level": class_level,
            "formulas": all_formulas[class_level]
        }
    except Exception as e:
        return {"error": str(e)}


@router.post("/feedback")
async def submit_feedback(
    question: str,
    rating: str,  # 'positive' or 'negative'
    solution: str,
    confidence: float
):
    """Submit user feedback for a solution"""
    feedback_data = {
        "question": question,
        "rating": rating,
        "response": {"solution": solution},
        "confidence": confidence
    }
    result = await feedback_service.save_feedback(feedback_data)
    return {
        "success": True,
        "message": "Thank you for your feedback!",
        "feedback_count": result.get("count", 0)
    }


@router.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    stats = feedback_service.get_feedback_stats()
    return stats


@router.get("/benchmark/jeebench")
async def benchmark_jeebench(num_questions: int = 10):
    """
    Test system on JEE Bench dataset
    Returns: accuracy, correct answers, detailed results
    """
    try:
        result = await benchmark_service.evaluate_sample(num_questions)
        return result
    except Exception as e:
        return {
            'error': str(e),
            'status': 'failed'
        }


@router.get("/benchmark/stats")
async def benchmark_stats():
    """Get JEE Bench dataset statistics"""
    try:
        stats = benchmark_service.get_dataset_stats()
        return stats
    except Exception as e:
        return {
            'error': str(e),
            'status': 'Dataset not loaded yet'
        }


# ============= DSPy OPTIMIZATION ENDPOINTS =============

@router.post("/optimize/dspy")
async def optimize_with_dspy():
    """Manually trigger DSPy prompt optimization."""
    if dspy_optimizer is None:
        return {"error": "DSPy optimizer not initialized"}
    
    result = await dspy_optimizer.optimize_prompts()
    return {
        "success": True,
        "optimization_result": result,
        "message": "DSPy prompts optimized based on feedback"
    }


@router.get("/optimize/stats")
async def get_optimization_stats():
    """Get DSPy optimization statistics."""
    if dspy_optimizer is None:
        return {"error": "DSPy optimizer not initialized"}
    
    feedback_stats = feedback_service.get_feedback_stats()
    
    return {
        "total_feedback": feedback_stats["total_feedback"],
        "positive_feedback": feedback_stats["positive"],
        "negative_feedback": feedback_stats["negative"],
        "positive_percentage": feedback_stats["positive_percentage"],
        "dspy_feedback_collected": len(dspy_optimizer.feedback_data)
    }

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload image with math problem"""
    try:
        content = await file.read()
        result = await file_upload_service.upload_image(content, file.filename)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload textbook PDF and extract chapters & formulas"""
    try:
        content = await file.read()
        result = await file_upload_service.upload_pdf(content, file.filename)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/upload/file-info")
async def get_file_info(filename: str, file_type: str = "pdf"):
    """Get info about uploaded file"""
    result = file_upload_service.get_file_info(filename, file_type)
    return result
