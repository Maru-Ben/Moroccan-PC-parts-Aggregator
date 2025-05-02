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
import playwright

from .logger import logger

def respect_rate_limits() -> None:
    """Add a random delay between requests to avoid overwhelming servers."""
    time.sleep(random.uniform(1, 3))
    
    
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


async def fetch_with_retry(url, headers=None, max_retries=3, start_method="aiohttp"):
    """
    Fetch a URL using progressively more powerful scraping methods.
    Starts with the specified method and escalates as needed.
    
    Args:
        url: The URL to fetch
        headers: Optional request headers
        max_retries: Maximum number of retry attempts across all methods
        start_method: The scraping method to start with ("aiohttp", "cloudscraper", or "playwright")
    """
    # define scraping methods in order of increasing complexity/power
    methods = ["aiohttp", "cloudscraper", "playwright"]
    
    # find the starting index based on the specified start method
    start_index = methods.index(start_method) if start_method in methods else 0
    
    # try each method starting from the specified one
    retry_count = 0
    for i in range(start_index, len(methods)):
        method = methods[i]
        
        if retry_count >= max_retries:
            logger.warning(f"Exceeded maximum retries ({max_retries}) for {url}")
            return None
            
        logger.info(f"Attempting to fetch {url} using {method} (attempt {retry_count + 1})")
        result = await fetch_async(url, headers, scraper_type=method)
        
        if result is not None:
            logger.info(f"Successfully fetched {url} using {method}")
            return result
            
        retry_count += 1
        
    logger.error(f"All methods failed for {url} after {retry_count} attempts")
    return None


async def fetch_async(url, headers, scraper_type="aiohttp"):
    """
    Fetch a URL using the specified scraper type.
    
    Args:
        url: The URL to fetch
        headers: request headers
        scraper_type: "aiohttp", "cloudscraper", or "playwright"
    """
    try:
        # Method 1: Regular aiohttp (fastest)
        if scraper_type == "aiohttp":
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.warning(f"aiohttp fetch failed for {url} - Status code: {response.status}")
                            return None
                except (aiohttp.ClientTimeout, aiohttp.ClientConnectionError) as e:
                    logger.error(f"aiohttp error fetching {url}: {str(e)}")
                    return None
        
        # Method 2: Cloudscraper (medium)
        elif scraper_type == "cloudscraper":
            import cloudscraper
            loop = asyncio.get_event_loop()
            cloud = cloudscraper.create_scraper()
            
            response = await loop.run_in_executor(
                None, lambda: cloud.get(url, headers=headers)
            )
            
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"cloudscraper fetch failed for {url} - Status code: {response.status_code}")
                return None
        
        # Method 3: Playwright (slowest but most powerful)
        elif scraper_type == "playwright":
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=headers.get("User-Agent"))
                page = await context.new_page()
                
                # Navigate to the URL
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Get the HTML content
                content = await page.content()
                
                # Close browser
                await browser.close()
                
                return content
                
        else:
            logger.error(f"Unknown scraper type: {scraper_type}")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error fetching {url} with {scraper_type}: {str(e)}")
        return None