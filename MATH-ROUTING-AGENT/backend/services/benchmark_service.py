import json
import httpx
import asyncio
import re
from typing import List, Dict, Optional
from datasets import load_dataset


class BenchmarkService:
    """Evaluates system on JEE Bench dataset"""
    
    def __init__(self):
        self.dataset = None
        self.dataset_stats = None
    
    async def load_jeebench(self):
        """Load JEE Bench dataset from Hugging Face"""
        try:
            print("📥 Loading JEE Bench dataset...")
            self.dataset = load_dataset("daman1209arora/jeebench", split="train")
            self.dataset_stats = {
                "total_questions": len(self.dataset),
                "dataset_name": "daman1209arora/jeebench",
                "status": "loaded"
            }
            print(f"✅ Loaded {len(self.dataset)} JEE questions")
            return True
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def get_dataset_stats(self) -> Dict:
        """Get dataset statistics"""
        if self.dataset_stats:
            return self.dataset_stats
        return {"error": "Dataset not loaded", "status": "not_loaded"}
    
    async def evaluate_sample(self, num_questions: int = 10) -> Dict:
        """
        Evaluate system on JEE Bench questions
        Actually calls /api/solve for each question
        Returns real accuracy metrics
        """
        
        # Load dataset if not already loaded
        if self.dataset is None:
            loaded = await self.load_jeebench()
            if not loaded:
                return {
                    "error": "Failed to load JEE Bench dataset",
                    "status": "failed"
                }
        
        # Get random sample
        import random
        sample_size = min(num_questions, len(self.dataset))
        sample_indices = random.sample(range(len(self.dataset)), sample_size)
        
        results = []
        correct = 0
        partial_correct = 0
        
        print(f"\n🧪 Testing {sample_size} JEE Bench questions...\n")
        
        # Call /api/solve for each question
        async with httpx.AsyncClient(timeout=60.0) as client:
            for idx, sample_idx in enumerate(sample_indices, 1):
                item = self.dataset[sample_idx]
                question = item.get('question', '')
                correct_answer = item.get('answer', '')
                
                try:
                    print(f"[{idx}/{sample_size}] Testing: {question[:80]}...")
                    
                    # Call actual /api/solve endpoint
                    response = await client.post(
                        "http://localhost:8000/api/solve",
                        json={
                            "question": question,
                            "board": "JEE",
                            "class_level": 12
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        system_answer = data.get('solution', '')
                        confidence = data.get('confidence', 0.0)
                        source = data.get('source', 'unknown')
                        
                        # Compare answers
                        is_correct, match_score = self._compare_answers(
                            system_answer, 
                            correct_answer
                        )
                        
                        if is_correct:
                            correct += 1
                            status = "✅ CORRECT"
                        elif match_score > 0.5:
                            partial_correct += 1
                            status = "⚠️ PARTIAL"
                        else:
                            status = "❌ WRONG"
                        
                        print(f"   {status} | Confidence: {confidence:.0%} | Source: {source}")
                        
                        results.append({
                            "q_number": idx,
                            "question": question[:100],
                            "expected_answer": correct_answer[:100],
                            "system_answer": system_answer[:100],
                            "is_correct": is_correct,
                            "match_score": match_score,
                            "confidence": confidence,
                            "source": source,
                            "status": status
                        })
                    else:
                        print(f"   ❌ API ERROR: {response.status_code}")
                        results.append({
                            "q_number": idx,
                            "question": question[:100],
                            "error": f"API error {response.status_code}"
                        })
                
                except asyncio.TimeoutError:
                    print(f"   ⏱️ TIMEOUT")
                    results.append({
                        "q_number": idx,
                        "question": question[:100],
                        "error": "Timeout - API took too long"
                    })
                except Exception as e:
                    print(f"   💥 ERROR: {str(e)}")
                    results.append({
                        "q_number": idx,
                        "question": question[:100],
                        "error": str(e)
                    })
        
        # Calculate metrics
        accuracy = (correct / sample_size) * 100 if sample_size > 0 else 0
        partial_accuracy = ((correct + partial_correct) / sample_size) * 100 if sample_size > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"📊 BENCHMARK RESULTS")
        print(f"{'='*60}")
        print(f"Total Questions: {sample_size}")
        print(f"Fully Correct: {correct} ({accuracy:.2f}%)")
        print(f"Partial Correct: {partial_correct}")
        print(f"Partial + Full Accuracy: {partial_accuracy:.2f}%")
        print(f"{'='*60}\n")
        
        return {
            "status": "completed",
            "total_questions": sample_size,
            "fully_correct": correct,
            "partial_correct": partial_correct,
            "accuracy_percentage": f"{accuracy:.2f}%",
            "partial_accuracy_percentage": f"{partial_accuracy:.2f}%",
            "results": results,
            "summary": {
                "total": sample_size,
                "correct": correct,
                "accuracy": accuracy,
                "partial_accuracy": partial_accuracy
            }
        }
    
    def _compare_answers(self, system_answer: str, correct_answer: str) -> tuple[bool, float]:
        """
        Compare system answer with correct answer
        Returns: (is_correct: bool, match_score: float 0-1)
        
        Strategies:
        1. Extract numbers and compare
        2. Check for key terms
        3. Fuzzy string matching
        """
        
        if not system_answer or not correct_answer:
            return False, 0.0
        
        system_lower = system_answer.lower()
        correct_lower = correct_answer.lower()
        
        # Strategy 1: Exact match
        if system_lower.strip() == correct_lower.strip():
            return True, 1.0
        
        # Strategy 2: Extract numbers and compare
        system_nums = self._extract_numbers(system_answer)
        correct_nums = self._extract_numbers(correct_answer)
        
        if system_nums and correct_nums:
            # Compare first number
            try:
                sys_val = float(system_nums[0])
                corr_val = float(correct_nums[0])
                
                # Allow 5% tolerance for numerical answers
                if corr_val != 0:
                    error_percent = abs(sys_val - corr_val) / abs(corr_val) * 100
                    if error_percent < 5:
                        return True, 1.0
                    elif error_percent < 15:
                        return False, 0.7
                else:
                    if abs(sys_val - corr_val) < 0.1:
                        return True, 1.0
            except:
                pass
        
        # Strategy 3: Check if correct answer appears in system answer
        if correct_lower in system_lower or system_lower in correct_lower:
            return True, 0.9
        
        # Strategy 4: Fuzzy string matching (simple similarity)
        similarity = self._string_similarity(system_lower, correct_lower)
        
        if similarity > 0.8:
            return True, similarity
        elif similarity > 0.5:
            return False, similarity
        
        return False, similarity
    
    def _extract_numbers(self, text: str) -> List[str]:
        """Extract all numbers from text"""
        return re.findall(r'-?\d+\.?\d*', text)
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """
        Simple string similarity (0-1)
        Based on common substring length
        """
        from difflib import SequenceMatcher
        return SequenceMatcher(None, s1, s2).ratio()


# Singleton instance
benchmark_service = BenchmarkService()
