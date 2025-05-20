import argparse
import asyncio
import datetime
from pprint import pprint
from scrapers.google_scraper import GoogleScraper
from utils.utils import save_url_extract, read_json_file
from processors.html_to_markdown import HTMLToMarkdown
from storage.file_manager import FileManager

async def main():
    """
    Main entry point for the web scraper application
    
    Process:
    1. Read keywords from file "scrape-to-markdown/config/keywords.json"
    2. Initialize components
    3. Search for URLs based on keywords
    4. Download and process each URL
    5. Save content as Markdown files to dir "scrape-to-markdown/file_store/TIMESTAMP-single"
    6, Merge all markdown files to dir "scrape-to-markdown/file_store/TIMESTAMP-merged"
    """
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    
    parser = argparse.ArgumentParser(description="Web scraper that search keywords to Markdown files")
    parser.add_argument("--skip-search", type=bool, default=False, help="If True, skip search and download from urls in file")
    args = parser.parse_args()
    pprint(args)
    
    # Read keywords from file
    keywords_list = read_json_file("scrape-to-markdown/config/keywords.json")
    print(f"Searching for: {keywords_list}")
    
    # Initialize components
    search_engine = GoogleScraper()
    file_mn = FileManager(timestp=timestamp_str)
    converter = HTMLToMarkdown(file_mn=file_mn)

    urls = []
    # Step 1: Get URLs from search engine
    if not args.skip_search:
        urls = await search_engine.search(keywords_list, 50)
        print("urls returned:", urls)
        save_url_extract(
            "all", urls, 
            "url_kw_arr.json", 100, 
            "scrape-to-markdown/config/kws_urls.json")
    
    # Step 2: Process each URL
    if args.skip_search: # download from previous urls in file
        urls = read_json_file("scrape-to-markdown/config/kws_urls.json")
    converter.convert(urls)
    
    #  Step 3: Merge all mardown files under a folder to one
    file_mn.merge_markdown_files()
    pass

if __name__ == "__main__":
    asyncio.run(main())