import asyncio
import hashlib
import time
import random
from typing import Optional
import unicodedata
import re
import aiohttp
import cloudscraper
import requests

from .logger import logger

def respect_rate_limits() -> None:
    """Add a random delay between requests to avoid overwhelming servers."""
    time.sleep(random.uniform(1, 3))
    
    
def normalize_spaces(text):
    """Normalize spaces in text, including unicode spaces (html text code)"""
    return ''.join(' ' if unicodedata.category(c) == 'Zs' else c for c in text)


def extract_price(price):
    """Extract price value from a string and convert to float."""
    if not price:
        return None
    
    extracted_price = normalize_spaces(price) # handle &nbsp; and others
    match = re.search(r'[\d\s]+[.,]\d{2}', extracted_price)
    if match:
        number = match.group(0).replace(" ", "").replace(",", ".")
        try:
            return float(number)
        except ValueError:
            logger.warning(f"Failed to convert price: {price}")
            return None
    return None


def generate_product_id(name: str, website: str, url:str) -> str:
    """Generate a consistent hash ID for a product."""
    id_string = f"{name}|{website}|{url}"
    return hashlib.md5(id_string.encode()).hexdigest()


def get_page_with_retry(url:str, headers: dict, max_retries: int=3, scraper_type: str = "requests") -> Optional[str]:
    """Fetch page content with retry mechanism for reliability."""
    for attempt in range(max_retries):
        try:
            if scraper_type == "requests":
                response = requests.get(url, headers=headers, timeout=10)
                return response.text
            elif scraper_type == "cloudscraper":
                cloud = cloudscraper.create_scraper()
                return cloud.get(url, timeout=10).text
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                # Exponential backoff
                time.sleep(2 ** attempt)
                continue
            else:
                logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                return None
    return None


async def fetch_async(url, headers, scraper_type="aiohttp"):
    if scraper_type == "cloudscraper":
        loop = asyncio.get_event_loop()
        cloud = cloudscraper.create_scraper()
        return await loop.run_in_executor(
            None, lambda: cloud.get(url, headers=headers).text
        )
    else:
        # Regular aiohttp fetch
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url} - Status code: {response.status}")
                    return None
