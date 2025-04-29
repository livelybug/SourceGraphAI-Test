from typing import List
from scrapers.search_engine import SearchEngine
import subprocess
import time
from browser_use_app.search_get_urls import search_get_urls
from utils.utils import _is_chrome_running_with_port, filter_urls

class GoogleScraper(SearchEngine):
    """Implementation of SearchEngine for Google"""
    
    def __init__(self, delay: int = 2):
        """
        Initialize Google scraper
        
        Args:
            delay: Time to wait between requests in seconds
        """
        self.google_url = "https://www.google.com"
        
        if not _is_chrome_running_with_port(12922):
            subprocess.Popen(
                ["/usr/bin/google-chrome", "--remote-debugging-port=12922"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Wait until Chrome is fully running
            time.sleep(delay)
                    
        pass
        
    async def search(self, keywords: List[str], max_results: int = 50) -> List[str]:
        """
        Search Google for URLs based on keywords
        
        Args:
            keywords: List of search terms
            max_results: Maximum number of results to return
            
        Returns:
            List of URLs matching the search criteria
        """
        all_urls = []
        for keyword in keywords:
            urls = await search_get_urls(keyword)
            urls = filter_urls(urls)
            all_urls.extend(urls)
            all_urls = list(dict.fromkeys(all_urls))
        return all_urls[:max_results]
    