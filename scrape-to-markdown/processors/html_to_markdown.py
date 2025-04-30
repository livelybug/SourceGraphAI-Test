import os
from time import sleep
from typing import List, Optional

import requests
from storage.file_manager import FileManager

jina_key = os.getenv("JINA_API_KEY")
jina_url = "https://r.jina.ai/"


class HTMLToMarkdown:
    """Converts HTML content to Markdown format"""
    
    def __init__(self, **kwargs):
        """
        Initialize converter with optional configuration
        
        Args:
            **kwargs: Configuration options for the HTML to Markdown converter
        """
        cr_dir = os.path.join(os.path.dirname(__file__), 'file_store')
        self.file_manager = FileManager(base_dir=cr_dir)
        
        
    def convert(self, html_content: str, urls: List[str]) -> Optional[str]:
        """
        Convert HTML content to Markdown
        
        Args:
            html_content: HTML content as string
            url: Source URL for metadata
            
        Returns:
            Markdown content as string or None if conversion failed
        """
        print("urls to download: ", urls)
        
        successful_files = []
        for url in urls:
            print(f"Processing: {url}")
            sleep(5)
            markdown = self.fetch_md_via_jina(url)
            if not markdown:
                print(f"Failed to convert: {url}")
                continue

    
    def fetch_md_via_jina(self, url):
        content_url = jina_url + url
        
        headers = {
            # "Accept": "text/event-stream",
            "Authorization": f'Bearer {jina_key}'
        }

        try:
            response = requests.get(content_url, headers=headers, timeout=20)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes            
            print("Request successful!\nResponse content:")

            self.file_manager.save_markdown(response.text, url)
            return response.text
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")