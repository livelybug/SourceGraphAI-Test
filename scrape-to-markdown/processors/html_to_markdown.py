import os
from time import sleep
from typing import List, Optional

import requests
from storage.file_manager import FileManager

jina_key = os.getenv("JINA_API_KEY")
jina_url = "https://r.jina.ai/"
MAX_RETRY_SINGLE = 1
MAX_ROUND = 12


class HTMLToMarkdown:
    """Converts HTML content to Markdown format"""
    
    def __init__(self, file_mn: FileManager, **kwargs):
        """
        Initialize converter with optional configuration
        
        Args:
            **kwargs: Configuration options for the HTML to Markdown converter
        """
        if file_mn is None:
            raise ValueError("file_mn is required")
        self.file_manager = file_mn
    
        
    def convert(self, urls: List[str]) -> Optional[str]:
        """
        Convert HTML content of urls to Markdown
        
        Args:
            url: Source URL
            
        Returns:
            Markdown content as string or None if conversion failed
        """
        print("urls to download: ", urls)
        
        
        # if function fetch_md_via_jina return None, save the url to array urls_failed;
        # After iterate all urls and urls_failed is not empty, 
        # iterate urls_failed to fetch the md from the urls_failed, 
        # and save failed url to a next urls_failed for next round of fetch;
        # Max round of fetch is 12;

        urls_to_fetch = list(urls)
        round_num = 1

        while urls_to_fetch and round_num <= MAX_ROUND:
            print(f"\n--- Fetch round {round_num} ---")
            urls_failed = []
            for url in urls_to_fetch:
                print(f"Processing: {url}")
                sleep(5)
                markdown = self.fetch_md_via_jina(url)
                if not markdown:
                    print(f"Failed to convert: {url}")
                    urls_failed.append(url)
            if not urls_failed:
                urls_to_fetch = []
                break
            
            urls_to_fetch = urls_failed
            round_num += 1

        if urls_to_fetch:
            print(f"Failed to fetch markdown for these URLs after {MAX_ROUND} rounds: {urls_to_fetch}")
        return None

    
    def fetch_md_via_jina(self, url):
        content_url = jina_url + url
        
        headers = {
            # "Accept": "text/event-stream",
            "Authorization": f'Bearer {jina_key}'
        }
        
        # if the request fails, sleep for 5*n seconds and try again, 
        # until try for 12 times. 
        # n is the times of failed request
        for n in range(1, MAX_RETRY_SINGLE + 1):
            try:
                response = requests.get(content_url, headers=headers, timeout=20)
                response.raise_for_status()  # Raise exception for 4xx/5xx status codes            
                print("Request successful!\nResponse content:")

                self.file_manager.save_markdown(response.text, url)
                return response.text

            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {n}): {str(e)}")
                if n < MAX_RETRY_SINGLE:
                    sleep_time = 5 * n
                    print(f"Retrying in {sleep_time} seconds...")
                    sleep(sleep_time)
                else:
                    print("Max retries reached. Giving up.")
        return None