"""Web Search Service - Tavily API integration"""

class WebSearchService:
    """Manages web search operations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def search(self, query: str, max_results: int = 5):
        """Search web for relevant information"""
        # TODO: Implement Tavily search
        pass
