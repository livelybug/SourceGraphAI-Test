from typing import List
from scrapers.search_engine import SearchEngine
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import subprocess
import psutil
import time
from browser_use_app.search_get_urls import search_get_urls

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

def filter_urls(urls: List[str]) -> List[str]:
    """
    Filter out unwanted URLs (e.g., YouTube)
    
    Args:
        urls: List of URLs to filter
        
    Returns:
        Filtered list of URLs
    """
    excluded_domains = [
        "youtube.com", 
        "youtu.be",
        "google.com",
        "gstatic.com",
        "googleusercontent.com"
    ]
    filtered = []
    for url in urls:
        if not any(domain in url for domain in excluded_domains):
            filtered.append(url)
    return filtered
