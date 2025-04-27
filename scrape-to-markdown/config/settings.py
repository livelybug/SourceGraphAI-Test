"""
Configuration settings for the web scraper application

Contains:
- Default search parameters
- User agent settings
- Output directory configuration
- Rate limiting settings
"""

# Search settings
MAX_RESULTS = 20
SEARCH_DELAY = 2  # seconds between searches

# Request settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 10  # seconds

# Output settings
OUTPUT_DIRECTORY = "scraped_content"

# Excluded domains
EXCLUDED_DOMAINS = [
    "youtube.com",
    "youtu.be",
    # Add other domains to exclude
]