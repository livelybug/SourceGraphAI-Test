from typing import List
from scrapers.search_engine import SearchEngine
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import subprocess
import psutil
import time

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
            # Wait until Chrome is running
            time.sleep(delay)
                
        # with sync_playwright() as p:
            # browser = p.chromium.launch(
            #     # executable_path = "/usr/bin/google-chrome",
            #     headless=False,
            # )
        
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
        query_url = self.google_url + "#search?udm=14&q=" + keywords[0]
        with sync_playwright() as p:
            self.browser = p.chromium.connect_over_cdp('http://localhost:12922')
            self.default_context = self.browser.contexts[0]

            page = self.default_context.pages[0]
            page.goto(self.google_url, wait_until='networkidle')
            page.wait_for_load_state()
            page.get_by_role("combobox").fill("profitable memecoin trading strategies logic")
            page.get_by_title("Search").press("Enter")
            page.wait_for_selector("#search")
            
            page1 = self.default_context.pages[0]
            page1.goto(query_url, wait_until='networkidle')
            page1.wait_for_load_state()
        pass
    
def _is_chrome_running_with_port(port: int) -> bool:
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'])
                if f'--remote-debugging-port={port}' in cmdline:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False
    