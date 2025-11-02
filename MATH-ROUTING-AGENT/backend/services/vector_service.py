import chromadb
from chromadb.config import Settings
import json
from pathlib import Path

class VectorService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="math_problems",
            metadata={"description": "Mathematical problems and solutions"}
        )
        
        # Initialize if empty
        if self.collection.count() == 0:
            self._load_initial_data()
    
    def _load_initial_data(self):
        """Load problems from JSON into ChromaDB"""
        json_file = Path(__file__).parent.parent / "data" / "math_dataset.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        # Prepare data for ChromaDB
        documents = [p["question"] for p in problems]
        metadatas = [
            {
                "solution": p["solution"],
                "topic": p["topic"],
                "difficulty": p["difficulty"],
                "steps": json.dumps(p["steps"])
            }
            for p in problems
        ]
        ids = [str(i) for i in range(len(problems))]
        
        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Loaded {len(problems)} problems into ChromaDB")
    
    def search(self, query: str, n_results: int = 1):
        """Search for similar questions"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'][0]:
            return None
        
        # Get best match
        metadata = results['metadatas'][0][0]
        distance = results['distances'][0][0]
        
        # Convert distance to confidence (0-1)
        confidence = max(0, 1 - distance)
        
        return {
            "question": results['documents'][0][0],
            "solution": metadata['solution'],
            "steps": json.loads(metadata['steps']),
            "topic": metadata['topic'],
            "difficulty": metadata['difficulty'],
            "score": confidence
        }

# Global instance
vector_service = VectorService()
