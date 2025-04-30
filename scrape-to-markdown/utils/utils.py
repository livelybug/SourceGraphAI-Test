import json
import os
from typing import List
from urllib.parse import unquote, urlparse
import psutil
from datetime import datetime

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
        "udemy.com",
        "facebook.com"
    ]
    filtered = []
    for url in urls:
        if not any(domain in url for domain in excluded_domains):
            filtered.append(url)
    return filtered

def save_url_extract(keywords, urls, file_name, max_results: int = 20, file_overwright: str = None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hist_key = f"{now} | {keywords}"

    # Load existing history if file exists
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            try:
                hist_data = json.load(f)
            except Exception:
                hist_data = {}
    else:
        hist_data = {}

    hist_data[hist_key] = urls[:max_results]

    with open(file_name, "w") as f:
        json.dump(hist_data, f, indent=2)
        
    # overwright file with array 
    if file_overwright:
        with open(file_overwright, "w") as f:
            json.dump(urls[:max_results], f, indent=2)
        
def get_last_subpath(url: str) -> str:
    """Extract the last meaningful sub-path from a URL"""
    parsed = urlparse(url)
    domain = "-" + parsed.netloc.replace("www.", "").replace(".com", "")
    path = parsed.path.rstrip('/')  # Remove trailing sliashes
    parts = [unquote(p) for p in path.split('/') if p.strip()]
    return parts[-1] + domain if parts else ''        

def read_json_file(json_file: str):
    with open(json_file, "r") as f:
        py_obj = json.load(f)
        # convert keywords into python object
        if isinstance(py_obj, dict) or isinstance(py_obj, list):
            return py_obj
        else:
            raise ValueError("Unexpected JSON structure for keywords.")

