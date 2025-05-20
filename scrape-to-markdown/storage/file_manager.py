from datetime import datetime
import glob
import os
from pathlib import Path
import re
from utils.utils import get_last_subpath
from utils.merge_md import extract_title, create_anchor


class FileManager:
    """Manages file operations for saving Markdown content"""
    
    def __init__(self, base_dir: Path = None, timestp: str = "000"):
        """
        Initialize file manager
        
        Args:
            base_dir: Base directory for saving files
        """
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'file_store')
        self.base_dir = base_dir
        self.dir_single = os.path.join(self.base_dir, timestp + "-single")
        self.dir_merged = os.path.join(self.base_dir, timestp + "-merged")
        Path(self.dir_single).mkdir(exist_ok=True, parents=True)
        Path(self.dir_merged).mkdir(exist_ok=True, parents=True)
        print("dir_single", self.dir_single)
        print("dir_merged", self.dir_merged)
    
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
        filepath = os.path.join(self.dir_single, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return str(filepath)
    
    def merge_markdown_files(self, directory_path=None, output_file=None):
        """Merge all markdown files in the directory into a single file with TOC."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.dir_merged, f"merged_markdown_{timestamp}.md")
        
        # Get all markdown files in the directory
        dir_single = self.dir_single
        md_files = glob.glob(os.path.join(dir_single, "*.md"))
        
        if not md_files:
            print(f"No markdown files found in {dir_single}")
            return
        
        # Prepare table of contents and content sections
        toc = ["# Table of Contents\n"]
        content_sections = []
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Extract title
                    title = extract_title(content)
                    anchor = create_anchor(title)
                    
                    # Add to TOC
                    toc.append(f"- [{title}](#{anchor})")
                    
                    # Prepare content section
                    section = f"\n\n## {title} <a id='{anchor}'></a>\n\n{content}"
                    content_sections.append(section)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Combine TOC and content sections
        merged_content = "\n".join(toc) + "\n" + "\n".join(content_sections)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(merged_content)
        
        print(f"Successfully merged {len(md_files)} markdown files into {output_file}")
        return output_file
    