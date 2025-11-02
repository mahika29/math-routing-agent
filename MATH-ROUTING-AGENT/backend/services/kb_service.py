"""
Knowledge Base Service - RAG Retrieval from Qdrant
Searches vector database for similar math problems
"""

import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from config.settings import settings

# Load environment variables  # ADD THIS
load_dotenv()

class KnowledgeBaseService:
    """Manages knowledge base RAG operations"""
    
    def __init__(self):
        """Initialize Qdrant client and embedding model"""
        print("🔧 Initializing Knowledge Base Service...")
        
        # Connect to Qdrant Cloud
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        
        print(f"✅ Connected to Qdrant: {settings.QDRANT_COLLECTION_NAME}")
    
    async def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search knowledge base for relevant math problems
        
        Args:
            query: User's math question
            top_k: Number of results to return
            
        Returns:
            List of matching problems with solutions
        """
        try:
            # Create embedding for query
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )
            
            # Format results
            results = []
            for hit in search_results:
                result = {
                    "question": hit.payload.get("question", ""),
                    "solution": hit.payload.get("solution", ""),
                    "steps": hit.payload.get("steps", []),
                    "topic": hit.payload.get("topic", ""),
                    "difficulty": hit.payload.get("difficulty", ""),
                    "class": hit.payload.get("class", ""),
                    "board": hit.payload.get("board", []),
                    "score": hit.score,
                    "source": "knowledge_base"
                }
                results.append(result)
            
            print(f"✅ Found {len(results)} matches in KB")
            return results
            
        except Exception as e:
            print(f"❌ KB Search error: {str(e)}")
            return []
    
    async def add_document(self, document: Dict, metadata: Dict) -> bool:
        """
        Add new document to knowledge base
        
        Args:
            document: Problem data (question, solution, steps)
            metadata: Additional metadata (topic, class, board)
            
        Returns:
            Success boolean
        """
        try:
            # Combine question and solution for embedding
            text = f"{document['question']} {document['solution']}"
            embedding = self.embedding_model.encode(text).tolist()
            
            # Add to Qdrant
            from qdrant_client.models import PointStruct
            import uuid
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "question": document['question'],
                    "solution": document['solution'],
                    "steps": document.get('steps', []),
                    "topic": metadata.get('topic', ''),
                    "difficulty": metadata.get('difficulty', 'medium'),
                    "class": metadata.get('class', 10),
                    "board": metadata.get('board', [])
                }
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            print(f"✅ Added document to KB")
            return True
            
        except Exception as e:
            print(f"❌ Error adding document: {str(e)}")
            return False
    
    def check_relevance(self, query: str, results: List[Dict], threshold: float = 0.7) -> bool:
        """
        Check if KB results are relevant enough
        
        Args:
            query: Original query
            results: Search results
            threshold: Minimum score threshold
            
        Returns:
            True if results are relevant, False if web search needed
        """
        if not results:
            return False
        
        # Check if best match score is above threshold
        best_score = results[0].get("score", 0)
        
        print(f"📊 Best match score: {best_score:.3f} (threshold: {threshold})")
        
        if best_score >= threshold:
            print("✅ KB results are relevant")
            return True
        else:
            print("⚠️ KB results not relevant enough, need web search")
            return False

# Singleton instance
kb_service = KnowledgeBaseService()
