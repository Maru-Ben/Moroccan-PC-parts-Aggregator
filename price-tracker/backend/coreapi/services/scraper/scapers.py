from bs4 import BeautifulSoup
from .utils import fetch_async, normalize_spaces,extract_price, generate_product_id
from coreapi.constants import SCRAPING_HEADERS
import logging

logger = logging.getLogger("backend.services")



async def get_content_from_page(page_url: str, scraper: str) -> BeautifulSoup:
    if scraper == "nextlevelpc":
        html_content = await fetch_async(page_url, SCRAPING_HEADERS, "cloudscraper")
    else:
        html_content = await fetch_async(page_url, SCRAPING_HEADERS)
    
    if not html_content:
        raise Exception(f"Failed to get content for {page_url} (Async)")
    
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


async def get_product_name(product_url: str, website: str) -> str:
    soup = await get_content_from_page(page_url=product_url, scraper=website)
    if website == "ultrapc":
        product_name_tag = soup.select_one("div.product-block-info h1.product-title")
        return product_name_tag.text.lower().strip() if product_name_tag else None
    elif website == "techspace":
        product_name_tag = soup.select_one("div.product-meta h1.product-meta__title")
        return product_name_tag.text.lower().strip() if product_name_tag else None
    else:
        return None

    
# Ultra PC               
async def extract_ultrapc_products(soup: BeautifulSoup, category_type: str):
    """Extract from one page all the products then send them in a list

    Args:
        soup (array): bs4 soup
        category_type (string): name of the category in english
    """
    page_products = []
    items = soup.select("div.product-block")
    for item in items:
        try:
            name_and_url_tag = item.select_one(".product-title a") # href is the url and the text is the text
            if not name_and_url_tag:
                continue
            short_description_tag = item.select_one("div.product-description-short") # text of the tag
            image_tag = item.select_one("a.product-thumbnail.img-thumbnail img") # src of the image tag
            price_tag = item.select_one("span.price") # content element of this tag is the price
            availability_tag = item.select_one("div.product-availability") # text 
            
            if "en stock" not in  availability_tag.text.strip().lower():
                continue
            
            product_url = name_and_url_tag["href"] if name_and_url_tag else None
            product_name = name_and_url_tag.text.lower().strip() if name_and_url_tag else None
            
            if "..." in product_name and product_url:
                product_name = await get_product_name(product_url, "ultrapc")
            
            if not product_name:
                logger.error(f"Product name not found for product {product_url}")
                raise Exception("Product name not found")
                
            product = {
                "id": generate_product_id("ultrapc", product_url),
                "name": product_name,
                "url": product_url,
                "short_description": short_description_tag.text.lower().strip() if short_description_tag else None,
                "image_url": image_tag["src"] if image_tag else None,
                "price": float(price_tag["content"].strip()) if price_tag else None,
                "availability": True,
                "category": category_type,
                "website": "ultrapc"
            }        
            page_products.append(product)
        except Exception as e:
            logger.error(f"Error processing ultrapc product: {e}")
            continue
        
    return page_products


# Next Level pc
async def extract_nextlevelpc_products(soup, category_type):
    """Extract from one page all the products then send them in a list

    Args:
        soup (array): bs4 soup
        category_type (string): name of the category in english
    """
    page_products = []
    
    items = soup.select("div.products article.item")
    for item in items:
        try:
            name_tag = item.select_one("div.product-title h3") # the text is the text

            url_tag = item.select_one("div.product-title a") #  href is the url
            if not name_tag or not url_tag:
                logger.warning("couldnt find name_tag or url_tag")
                continue
            image_tag = item.select_one("a.product-thumbnail img.tvproduct-defult-img") # src of the image tag
            price_tag = item.select_one("span.price") # text of the tag
            availability_tag = item.select_one("div.custom-product-badge span.badge-name-text") # text 
            if "en stock" not in availability_tag.text.strip().lower():
                continue
            
            features = item.select("div.product-features li")
            short_description = " | ".join([f.get_text(strip=True) for f in features])
            
            cleaned_price = None
            if price_tag:
                cleaned_price = extract_price(price_tag.text.lower().strip())
                
            product_name = name_tag.text.lower().strip()
            product_url = url_tag["href"]
            
            product = {
                "id": generate_product_id("nextlevelpc", product_url),
                "name": product_name,
                "url": product_url,
                "short_description": normalize_spaces(short_description.lower().strip()) if short_description else None,
                "image_url": image_tag.get("data-cfsrc") or image_tag.get("src") if image_tag else None,
                "price": cleaned_price,
                "availability": True,
                "category": category_type,
                "website": "nextlevelpc"
            }        
            page_products.append(product)
        except Exception as e:
            logger.error(f"Error processing nextlevelpc product: {e}")
            continue
        
    return page_products


# Techspace
async def extract_techspace_products(url, soup, category_type):
    """Extract from one page all the products then send them in a list

    Args:
        soup (string): this is the return of the BeautifySoup call

    Returns:
        url (string): the base url of the website we are scraping
        soup (array): array of the products with details
        category_type (string): name of the category in english
    """
    page_products = []
    items = soup.select("div.product-list div.product-item")
    for item in items:
        try:
            name_and_url_tag = item.select_one("div.product-item__title-info a.product-item__title") # href is the url and the text is the text
            if not name_and_url_tag:
                continue
            image_tag = item.select_one("a.product-item__image-wrapper img.product-item__primary-image") # src of the image tag
            price_tag = item.select_one("span.price") # content element of this tag is the price
            availability_tag = item.select_one("span.product-item__inventory") # text 
            
            if "en stock" not in availability_tag.text.strip().lower():
                continue
            
            image_url = None
            if image_tag:
                srcset = image_tag.get("data-srcset") or image_tag.get("srcset") or image_tag.get("data-src")
                if srcset:
                    # splitting into image URLs and pick the highest resolution
                    images = [s.strip() for s in srcset.split(",")]
                    last_image = images[-1].split(" ")[0]
                    image_url = "https:" + last_image.replace("{width}", "800")
            
            cleaned_price = None
            if price_tag:
                cleaned_price = extract_price(price_tag.text.lower().strip()) 
            
            product_name = name_and_url_tag.text.lower().strip()
            product_url = url + name_and_url_tag["href"]
            
            if "..." in product_name and product_url:
                product_name = await get_product_name(product_url, "techspace")
            
            if not product_name:
                logger.error(f"Product name not found for product {product_url}")
                raise Exception("Product name not found")
            
            product = {
                "id": generate_product_id("techspace", product_url),
                "name": product_name,
                "url": product_url,
                "short_description": None,
                "image_url": image_url,
                "price": cleaned_price,
                "availability": True,
                "category": category_type,
                "website": "techspace"
            }        
            page_products.append(product)
        except Exception as e:
            logger.error(f"Error processing TechSpace product: {e}")
            continue
        
    return page_products
