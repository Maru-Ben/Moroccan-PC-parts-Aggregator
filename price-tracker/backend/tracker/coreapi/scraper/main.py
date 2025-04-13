import asyncio
import json
import random
import time
from typing import Dict
import aiohttp
from bs4 import BeautifulSoup

from .logger import logger
from .scapers import extract_ultrapc_products, extract_nextlevelpc_products, extract_techspace_products
from .utils import fetch_async, respect_rate_limits, get_page_with_retry

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

URLS = {
    "https://www.ultrapc.ma": {
        "categories": [
            {"url": "/20-composants", "type": "COMP"},
            {"url": "/58-peripheriques", "type": "PER"}
        ],
        "scraper": "ultrapc"
    },
    "https://nextlevelpc.ma": {
        "categories": [
            {"url": "/143-composants", "type": "COMP"},
            {"url": "/148-peripherique-pc", "type": "PER"},
            {"url": "/189-ecran-pc", "type": "PER"}
        ],
        "scraper": "nextlevelpc"
    },
    "https://techspace.ma": {
        "categories": [
            {"url": "/collections/composants", "type": "COMP"},
            {"url": "/collections/peripheriques", "type": "PER"}
        ],
        "scraper": "techspace"
    }
}


def scrape_websites():
    products = []
    # we check all urls in our dict then we call the concerned function
    for base_url, site_info in URLS.items():
        logger.info(f"Scraping {site_info['scraper']}...")
        category_products = scrape_category(base_url, site_info["categories"], site_info['scraper'])
        products.extend(category_products)
        
    logger.info(f"Scraped {len(products)} total products across {len(URLS)} sites.")
    with open("scraper/json/products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
         
    return products

def scrape_category(url, categories, scraper):
    """scrape one ultrapc category 

    Args:
        url (string): url of the category to scrape
        category_type (array): array of the categories of the website we are scraping
        scraper (string): name of the scraper -- the website
    """
    all_category_products = []
    for category in categories:
        try:
            page = 1 
            category_products = []
            has_products = True
            
            # visiting each page of the category to scrape it
            while has_products:
                page_url = f"{url + category['url']}?page={page}"
                logger.info(f"Scraping: {page_url}")
                
                # Respect rate limits
                respect_rate_limits()
                
                # Get page content based on scraper type
                html_content = None
                if scraper == "ultrapc":
                    html_content = get_page_with_retry(page_url, HEADERS, scraper_type="requests")
                else:
                    html_content = get_page_with_retry(page_url, HEADERS, scraper_type="cloudscraper")
                
                if not html_content:
                    raise Exception(f"Failed to fetch page: {page_url}")

                
                soup = BeautifulSoup(html_content, "html.parser")
                page_products = []

                # Extract products based on site type
                if scraper == "ultrapc":
                    page_products = extract_ultrapc_products(soup, category["type"])
                elif scraper == "nextlevelpc":
                    page_products = extract_nextlevelpc_products(soup, category["type"])
                elif scraper == "techspace":
                    page_products = extract_techspace_products(url, soup, category["type"])
                
                    
                if not page_products:
                    has_products = False
                    logger.info(f"No more products found at page {page} for {url + category['url']}")
                else:
                    category_products.extend(page_products)
                    logger.info(f"Found {len(page_products)} products on page {page}")
                    page += 1
                    
            all_category_products.extend(category_products)
            logger.info(f"Completed scraping {url + category['url']} - found {len(category_products)} products")
            
        except Exception as e:
            logger.error(f"Failed to scrape data from {url} category {category['url']}: {e}")  
            continue
    return all_category_products
 
  
async def scrape_websites_async():
    """Main async function to scrape all websites."""
    tasks = []
    for base_url, site_info in URLS.items():
        for category in site_info["categories"]:
            task = scrape_category_async(base_url, category, site_info["scraper"])
            tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    all_products = [product for sublist in results for product in sublist]
    logger.info(f"Scraped {len(all_products)} total products across {len(URLS)} sites.")
    # Save results to file
    with open("scraper/json/products_async.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)
        
    return all_products
  
async def scrape_category_async(url: str, category: Dict[str, str], scraper: str):
    """Scrape a category asynchronously"""
    try:
        page = 1
        category_products = []
        has_products = True
        
        while has_products:
            page_url = f"{url + category['url']}?page={page}"
            logger.info(f"Async scraping: {page_url}")
            
            # Add delay for rate limiting
            await asyncio.sleep(random.uniform(1, 3))
            if scraper == "nextlevelpc":
                html_content = await fetch_async(page_url, HEADERS, "cloudscraper")
            else:
                html_content = await fetch_async(page_url, HEADERS)
            
            if not html_content:
                raise Exception(f"Failed to get content for {page_url} (Async)")
            
            soup = BeautifulSoup(html_content, "html.parser")
            page_products = []
            
            if scraper == "ultrapc":
                page_products = extract_ultrapc_products(soup, category["type"])
            elif scraper == "nextlevelpc":
                page_products = extract_nextlevelpc_products(soup, category["type"])
            elif scraper == "techspace":
                page_products = extract_techspace_products(url, soup, category["type"])
            
            if not page_products:
                has_products = False
            else:
                category_products.extend(page_products)
                page += 1
        
        if category_products == []:
            raise Exception(f"No products were scrapped from the whole category")
        return category_products
    except aiohttp.ClientError as e:
        logger.error(f"Network error while scraping {url}: {e}")
        logger.warning(f"Falling back to sync may cause partial duplication in {category['url']}")
        return scrape_category(url, [category], scraper)
    except Exception as e:
        logger.error(f"Async scraping failed for {url + category['url']}: {str(e)}")
        logger.warning(f"Falling back to sync may cause partial duplication in {category['url']}")
        # Call sync version instead
        return scrape_category(url, [category], scraper)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape PC parts from Moroccan e-commerce websites')
    parser.add_argument('--method', type=str, choices=['sync', 'async'], 
                      default='sync', help='Scraping method to use')
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    if args.method == 'async':
        logger.info("Starting asynchronous scraping...")
        asyncio.run(scrape_websites_async())
    else:
        logger.info("Starting synchronous scraping...")
        scrape_websites()
        
    elapsed_time = time.time() - start_time
    logger.info(f"Scraping completed in {elapsed_time:.2f} seconds")