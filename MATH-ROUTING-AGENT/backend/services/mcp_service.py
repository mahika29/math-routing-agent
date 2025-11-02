from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

class MCPService:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in .env")
        self.client = TavilyClient(api_key=api_key)
    
    def search_web(self, query: str, max_results: int = 3):
        """Search web using Tavily MCP"""
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )
            
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'url': result.get('url', '')
                })
            
            return {
                'success': True,
                'results': results,
                'query': query
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query
            }

# Initialize service
mcp_service = MCPService()
