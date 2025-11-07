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
from coreapi.constants import SCRAPING_WAIT
import logging

logger = logging.getLogger("backend.services")

def respect_rate_limits() -> None:
    """Add a random delay between requests to avoid overwhelming servers."""
    time.sleep(random.uniform(SCRAPING_WAIT["min_seconds"], SCRAPING_WAIT["max_seconds"]))
    
    
def normalize_spaces(text):
    """Normalize spaces in text, including unicode spaces (html text code)"""
    return ''.join(' ' if unicodedata.category(c) == 'Zs' else c for c in text)

def extract_price(price: str) -> Optional[float]:
    """Extract price value from a string and convert to float, handling different formats."""
    if not price:
        return None
    
    normalized = re.sub(r'[^\d.,]', '', price.strip())
    
    if '.' in normalized and ',' in normalized:
        if normalized.rfind('.') < normalized.rfind(','):
            normalized = normalized.replace('.', '').replace(',', '.')
        else:
            normalized = normalized.replace(',', '')
    elif ',' in normalized:
        if len(normalized.split(',')[-1]) != 3:
            normalized = normalized.replace(',', '.')
        else:
            normalized = normalized.replace(',', '')
    
    try:
        return float(normalized)
    except ValueError:
        numbers = re.findall(r'\d+', price)
        if numbers:
            return float(max(numbers, key=len))
        return None


def generate_product_id(website: int, url: str) -> str:
    """Generate a consistent hash ID for a product."""
    input_str = f"{website}|{url}".lower().strip("/")
    return hashlib.sha256(input_str.encode()).hexdigest()

def get_page_with_retry(url:str, headers: dict, max_retries: int=3, scraper_type: str = "requests") -> Optional[str]:
    """Fetch page content with retry mechanism for reliability."""
    for attempt in range(max_retries):
        try:
            if scraper_type == "requests":
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 429: # too many requests
                    wait_time = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
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
    try:
        if scraper_type == "cloudscraper":
            loop = asyncio.get_event_loop()
            cloud = cloudscraper.create_scraper()
            return await loop.run_in_executor(
                None, lambda: cloud.get(url, headers=headers).text
            )
        else:
            # Regular aiohttp fetch
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            return await response.text()
                        elif response.status == 429:
                            logger.warning(f"Rate limited at {url}")
                            raise aiohttp.ClientConnectionError(
                                request_info=response.request_info,
                                history=response.history,
                                status=429
                            )
                        else:
                            logger.warning(f"Failed to fetch {url} - Status code: {response.status}")
                            return None
                except aiohttp.ClientTimeout:
                    logger.error(f"Timeout while fetching {url}")
                    return None
                except aiohttp.ClientConnectionError:
                    logger.error(f"Connection error while fetching {url}")
                    return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {str(e)})")
        return None
            
