"""
Stealth utilities for VulnForge
Handles proxy configuration, request delays, and user agent rotation
"""

import random
import time
from typing import Dict, List, Optional
import aiohttp
import asyncio
from datetime import datetime, timedelta

class StealthManager:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        
        self.proxy_list = []
        self.last_request_time = datetime.now()
        self.min_delay = 1.0  # Minimum delay between requests in seconds
        self.max_delay = 3.0  # Maximum delay between requests in seconds
        
    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self.user_agents)
        
    def add_proxy(self, proxy: str):
        """Add a proxy to the list"""
        self.proxy_list.append(proxy)
        
    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the list"""
        return random.choice(self.proxy_list) if self.proxy_list else None
        
    async def apply_delay(self):
        """Apply random delay between requests"""
        delay = random.uniform(self.min_delay, self.max_delay)
        await asyncio.sleep(delay)
        self.last_request_time = datetime.now()
        
    def get_headers(self) -> Dict[str, str]:
        """Get headers with random user agent"""
        return {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
    async def make_request(self, session: aiohttp.ClientSession, url: str, 
                          method: str = "GET", **kwargs) -> Optional[aiohttp.ClientResponse]:
        """Make a request with stealth measures"""
        await self.apply_delay()
        
        headers = kwargs.pop("headers", {})
        headers.update(self.get_headers())
        
        proxy = self.get_random_proxy()
        if proxy:
            kwargs["proxy"] = proxy
            
        try:
            async with session.request(method, url, headers=headers, **kwargs) as response:
                return response
        except Exception as e:
            print(f"Error making request to {url}: {e}")
            return None
            
    def set_delay_range(self, min_delay: float, max_delay: float):
        """Set the delay range between requests"""
        self.min_delay = min_delay
        self.max_delay = max_delay
        
    def load_proxies_from_file(self, file_path: str):
        """Load proxies from a file"""
        try:
            with open(file_path, 'r') as f:
                self.proxy_list = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading proxies from {file_path}: {e}")
            
    def get_request_stats(self) -> Dict:
        """Get statistics about requests"""
        return {
            "total_proxies": len(self.proxy_list),
            "min_delay": self.min_delay,
            "max_delay": self.max_delay,
            "last_request": self.last_request_time.isoformat()
        }

# Create global instance
stealth_manager = StealthManager()

def get_random_user_agent() -> str:
    """Get a random user agent"""
    return stealth_manager.get_random_user_agent()

def get_random_proxy() -> Optional[str]:
    """Get a random proxy from the list"""
    return stealth_manager.get_random_proxy()

def get_request_stats() -> Dict:
    """Get statistics about requests"""
    return stealth_manager.get_request_stats() 