import os
import re
from datetime import datetime
import glob

def extract_title(content):
    """Extract title from markdown content."""
    # Try to find a title line starting with "Title: "
    title_match = re.search(r'^Title:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    # If no explicit title, try to find the first heading
    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    
    # If no heading, use the first non-empty line
    lines = content.strip().split('\n')
    for line in lines:
        if line.strip():
            return line.strip()
    
    # Fallback
    return "Untitled"

def create_anchor(title):
    """Create a GitHub-style anchor from a title."""
    # Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric chars
    anchor = re.sub(r'[^\w\s-]', '', title.lower())
    anchor = re.sub(r'[\s]+', '-', anchor)
    return anchor

def merge_markdown_files(directory_path, output_file=None):
    """Merge all markdown files in the directory into a single file with TOC."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"merged_markdown_{timestamp}.md"
    
    # Get all markdown files in the directory
    md_files = glob.glob(os.path.join(directory_path, "*.md"))
    
    if not md_files:
        print(f"No markdown files found in {directory_path}")
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

if __name__ == "__main__":
    directory = "scrape-to-markdown/processors/file_store"
    merge_markdown_files(directory)
