import argparse
import asyncio
from pprint import pprint
from typing import List
from scrapers.google_scraper import GoogleScraper
from processors.html_downloader import HTMLDownloader
from processors.html_to_markdown import HTMLToMarkdown
from storage.file_manager import FileManager
from utils.url_validator import URLValidator
import json

async def main():
    """
    Main entry point for the web scraper application
    
    Process:
    1. Read keywords from file "scrape-to-markdown/config/keywords.json"
    2. Initialize components
    3. Search for URLs based on keywords
    4. Download and process each URL
    5. Save content as Markdown files
    """
    
    # Read keywords from file "scrape-to-markdown/config/keywords.json"
    with open("scrape-to-markdown/config/keywords.json", "r") as f:
        keywords = json.load(f)
        # convert keywords into python object
        if isinstance(keywords, dict):
            keywords_list = list(keywords.values())
        elif isinstance(keywords, list):
            keywords_list = keywords
        else:
            raise ValueError("Unexpected JSON structure for keywords.")
        pprint(keywords_list)
    
    # Initialize components
    search_engine = GoogleScraper()
    
    # Step 1: Get URLs from search engine
    print(f"Searching for: {keywords_list}")
    urls = await search_engine.search(keywords_list, max_results=5)
    print("urls returned:", urls)
    
    pass

if __name__ == "__main__":
    asyncio.run(main())