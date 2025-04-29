import unittest
from typing import List
from scrapers.google_scraper import filter_urls

class TestGoogleScraper(unittest.TestCase):
    def test_filter_urls_empty_list(self):
        urls = []
        result = filter_urls(urls)
        self.assertEqual(result, [])
        
    def test_filter_urls_no_excluded_domains(self):
        urls = [
            "https://example.com",
            "https://test.org/page",
            "http://valid-site.net"
        ]
        result = filter_urls(urls)
        self.assertEqual(result, urls)
        
    def test_filter_urls_all_excluded(self):
        urls = [
            "https://youtube.com/watch",
            "https://youtu.be/xyz",
            "https://google.com/search",
            "https://gstatic.com/image",
            "https://googleusercontent.com/file"
        ]
        result = filter_urls(urls)
        self.assertEqual(result, [])
        
    def test_filter_urls_mixed_content(self):
        urls = ["https://www.reddit.com/r/solana/comments/whats-your-memecoin-trading-strategy-heres-mine/",
                "https://trysuper.co/blog/day-trading-memecoins-an-ultimate-guide-2025/",
                "https://www.mobee.io/mobee-academy/blog/strategies-for-profitable-memecoin-trading/",
                "https://www.youtube.com/watch?v=1-hour-memecoin-trading-challenge",
                "https://osl.com/academy/article/5-crypto-trading-strategies-to-ride-momentum/",
                "https://www.businessinsider.com/markets/investing/the-crypto-meme-coin-trading-strategies-used-by-a-hedge-funder-2025-2",
                "https://www.linkedin.com/posts/salim-hanzaz_best-strategies-for-trading-meme-coins-a-full-activity-123456789",
                "https://www.youtube.com/watch?v=best-scaling-strategy-for-small-memecoin-portfolio",
                "https://www.kaloh.xyz/memecoin-moonshot-solana-trading-strategy/",
                "https://cointelegraph.com/news/how-to-trade-memecoins-in-2025"]
        expected = ["https://www.reddit.com/r/solana/comments/whats-your-memecoin-trading-strategy-heres-mine/",
                "https://trysuper.co/blog/day-trading-memecoins-an-ultimate-guide-2025/",
                "https://www.mobee.io/mobee-academy/blog/strategies-for-profitable-memecoin-trading/",
                "https://osl.com/academy/article/5-crypto-trading-strategies-to-ride-momentum/",
                "https://www.businessinsider.com/markets/investing/the-crypto-meme-coin-trading-strategies-used-by-a-hedge-funder-2025-2",
                "https://www.linkedin.com/posts/salim-hanzaz_best-strategies-for-trading-meme-coins-a-full-activity-123456789",
                "https://www.kaloh.xyz/memecoin-moonshot-solana-trading-strategy/",
                "https://cointelegraph.com/news/how-to-trade-memecoins-in-2025"]
        result = filter_urls(urls)
        self.assertEqual(result, expected)
        
    def test_filter_urls_subdomains(self):
        urls = [
            "https://subdomain.example.com",
            "https://videos.youtube.com/watch",
            "https://maps.google.com/location",
            "https://valid.test.org"
        ]
        expected = [
            "https://subdomain.example.com",
            "https://valid.test.org"
        ]
        result = filter_urls(urls)
        self.assertEqual(result, expected)
