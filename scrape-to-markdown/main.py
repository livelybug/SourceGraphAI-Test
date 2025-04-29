import asyncio
from pprint import pprint
from scrapers.google_scraper import GoogleScraper
import json
from utils.utils import save_url_extract

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
    urls = await search_engine.search(keywords_list, 50)
    print("urls returned:", urls)
    save_url_extract("all", urls, "url_kw_arr.json", 100)
    
    pass

if __name__ == "__main__":
    asyncio.run(main())