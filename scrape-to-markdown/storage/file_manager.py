
from pathlib import Path
import re
from urllib.parse import urlparse
from utils.utils import get_last_subpath


class FileManager:
    """Manages file operations for saving Markdown content"""
    
    def __init__(self, base_dir: str = "scraped_content"):
        """
        Initialize file manager
        
        Args:
            base_dir: Base directory for saving files
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True, parents=True)
        print("self.base_dir", self.base_dir)
    
    def generate_filename(self, url: str, title: str = None) -> str:
        """
        Generate a valid filename from URL or title
        
        Args:
            url: Source URL
            title: Optional page title
            
        Returns:
            Valid filename with .md extension
        """
        if title:
            # Clean title for filename
            filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
            filename = re.sub(r'[-\s]+', '-', filename)
        else:
            # Use domain and path as filename            
            filename = get_last_subpath(url)
            print("filename", filename)
            
        return f"{filename[:100]}.md"  # Limit length and add extension
    
    def save_markdown(self, content: str, url: str, title: str = None) -> str:
        """
        Save markdown content to file
        
        Args:
            content: Markdown content
            url: Source URL
            title: Optional page title
            
        Returns:
            Path to saved file
        """
        filename = self.generate_filename(url, title)
        filepath = self.base_dir / filename
        # print(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return str(filepath)