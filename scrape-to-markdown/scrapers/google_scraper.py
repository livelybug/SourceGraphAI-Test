from typing import List
from scrapers.search_engine import SearchEngine
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

class GoogleScraper(SearchEngine):
    """Implementation of SearchEngine for Google"""
    
    def __init__(self, delay: int = 2):
        """
        Initialize Google scraper
        
        Args:
            delay: Time to wait between requests in seconds
        """
        # self.google_url = "https://www.google.com#search?udm=14&q="
        self.google_url = "https://www.google.com"
        
        # with sync_playwright() as p:
            # browser = p.chromium.launch(
            #     # executable_path = "/usr/bin/google-chrome",
            #     headless=False,
            # )
            # self.browser = p.chromium.connect_over_cdp('http://localhost:9222')
            # self.default_context = self.browser.contexts[0]
        
        pass
        
    def search(self, keywords: List[str], max_results: int = 20) -> List[str]:
        """
        Search Google for URLs based on keywords
        
        Args:
            keywords: List of search terms
            max_results: Maximum number of results to return
            
        Returns:
            List of URLs matching the search criteria
        """

        with sync_playwright() as p:
            self.browser = p.chromium.connect_over_cdp('http://localhost:9222')
            self.default_context = self.browser.contexts[0]

            page = self.default_context.pages[0]
            # page = browser.new_page(ignore_https_errors=True)
            page.goto(self.google_url, wait_until='networkidle')
            page.wait_for_load_state()
            page.fill("textarea[name='q']", "profitable memecoin trading strategies logic")
            page.press("textarea[name='q']", "Enter")
            page.wait_for_selector("#search")
            page = self.default_context.pages[1]
            page.goto(self.google_url, wait_until='networkidle')
            page.wait_for_load_state()
        pass