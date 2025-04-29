from abc import ABC, abstractmethod
from typing import List

class SearchEngine(ABC):
    """Base class for search engine implementations"""
    
    @abstractmethod
    def search(self, keywords: List[str], max_results: int = 20) -> List[str]:
        """Search for URLs based on keywords"""
        pass
    
    def filter_urls(self, urls: List[str]) -> List[str]:
        """Filter out unwanted URLs (e.g., YouTube)"""
        pass