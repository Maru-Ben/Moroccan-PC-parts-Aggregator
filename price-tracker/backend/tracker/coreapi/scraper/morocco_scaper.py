import re
import unicodedata
import requests
from bs4 import BeautifulSoup
import json
import cloudscraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

URLS = {
    "https://www.ultrapc.ma": {
        "categories": [
            {"url": "/20-composants", "type": "Components"},
            {"url": "/58-peripheriques", "type": "Peripherals"}
        ],
        "scraper": "ultrapc"
    },
    "https://nextlevelpc.ma": {
        "categories": [
            {"url": "/143-composants", "type": "Components"},
            {"url": "/148-peripherique-pc", "type": "Peripherals"},
            {"url": "/189-ecran-pc", "type": "Peripherals"}
        ],
        "scraper": "nextlevelpc"
    },
    "https://techspace.ma": {
        "categories": [
            {"url": "/collections/composants", "type": "Components"},
            {"url": "/collections/peripheriques", "type": "Peripherals"}
        ],
        "scraper": "techspace"
    }
}


def scrape_websites():
    products = []
    # we check all urls in our dict then we call the concerned function
    for base_url, site_info in URLS.items():
        print(f"Scraping {site_info['scraper']}...")
        category_products = scrape_category(base_url, site_info["categories"], site_info['scraper'])
        products.extend(category_products)
            
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
         
    return products


def scrape_category(url, categories, scraper):
    """scrape one ultrapc category 

    Args:
        url (string): url of the category to scrape
        category_type (array): array of the categories of the website we are scraping
        scraper (string): name of the scraper -- the website
    """
    for category in categories:
        page = 1 
        category_products = []
        
        # visiting each page of the category to scrape it
        while True:
            page_url = f"{url + category['url']}?page={page}"
            print(f"Scraping: {page_url}")
            page_products = []

            if scraper == "ultrapc":
                response = requests.get(page_url, headers=HEADERS)
                soup = BeautifulSoup(response.text, "html.parser")
                page_products = extract_ultrapc_products(soup, category["type"])
            elif scraper == "nextlevelpc":
                cloud = cloudscraper.create_scraper()  
                html = cloud.get(page_url).text
                soup = BeautifulSoup(html, "html.parser")
                page_products = extract_nextlevelpc_products(soup, category["type"])
            elif scraper == "techspace":
                cloud = cloudscraper.create_scraper()
                html = cloud.get(page_url).text  
                soup = BeautifulSoup(html, "html.parser")
                page_products = extract_techspace_products(url, soup, category["type"])
                
                
            if not page_products:
                break # No more products -- reached the last page
            category_products.extend(page_products)
            page += 1
            break
        
    return category_products   
  
# Ultra PC               
def extract_ultrapc_products(soup, category_type):
    """Extract from one page all the products then send them in a list

    Args:
        soup (string): this is the return of the BeautifySoup call

    Returns:
        soup (array): array of the products with details
        category_type (string): name of the category in english
    """
    page_products = []
    items = soup.select("div.product-block")
    
    for item in items:
        name_and_url_tag = item.select_one(".product-title a") # href is the url and the text is the text
        short_description_tag = item.select_one("div.product-description-short") # text of the tag
        image_tag = item.select_one("a.product-thumbnail.img-thumbnail img") # src of the image tag
        price_tag = item.select_one("span.price") # content element of this tag is the price
        availability_tag = item.select_one("div.product-availability") # text 
        
        if availability_tag.text.strip().lower() != "produit en stock":
            continue
        
        product = {
            "name" : name_and_url_tag.text.lower().strip() if name_and_url_tag else None,
            "url" : name_and_url_tag["href"] if name_and_url_tag else None,
            "short_description": short_description_tag.text.lower().strip() if short_description_tag else None,
            "image_url": image_tag["src"] if image_tag else None,
            "price": float(price_tag["content"].strip()) if price_tag else None,
            "availability": True if (availability_tag.text.lower().strip() == "produit en stock" and availability_tag) else False,
            "category": category_type,
            "website": "ultrapc"
        }        
        page_products.append(product)
        
    return page_products
        
# Next Level pc
def extract_nextlevelpc_products(soup, category_type):
    """Extract from one page all the products then send them in a list

    Args:
        soup (string): this is the return of the BeautifySoup call

    Returns:
        soup (array): array of the products with details
        category_type (string): name of the category in english
    """
    print("scraping nextlevelpc")
    page_products = []
    
    items = soup.select("div.products article.item")
    for item in items:
        name_tag = item.select_one("div.product-title h2") # the text is the text
        url_tag = item.select_one("div.product-title a") #  href is the url
        image_tag = item.select_one("a.product-thumbnail img.tvproduct-defult-img") # src of the image tag
        price_tag = item.select_one("span.price") # text of the tag
        availability_tag = item.select_one("div.custom-product-badge span.badge-name-text") # text 
        if availability_tag.text.strip().lower() != "en stock":
            continue
        
        features = item.select("div.product-features li")
        short_description = " | ".join([f.get_text(strip=True) for f in features])
        
        cleaned_price = None
        if price_tag:
            cleaned_price = extract_price(price_tag.text.lower().strip())
        
        product = {
            "name" : name_tag.text.lower().strip() if name_tag else None,
            "url" : url_tag["href"] if url_tag else None,
            "short_description": normalize_spaces(short_description.lower().strip()) if short_description else None,
            "image_url": image_tag.get("data-cfsrc") or image_tag.get("src") if image_tag else None,
            "price": cleaned_price,
            "availability": True if (availability_tag.text.lower().strip() == "en stock" and availability_tag) else False,
            "category": category_type,
            "website": "nextlevelpc"
        }        
        
        page_products.append(product)
    return page_products


def extract_techspace_products(url, soup, category_type):
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
        name_and_url_tag = item.select_one("div.product-item__title-info a.product-item__title") # href is the url and the text is the text
        image_tag = item.select_one("a.product-item__image-wrapper img.product-item__primary-image") # src of the image tag
        price_tag = item.select_one("span.price") # content element of this tag is the price
        availability_tag = item.select_one("span.product-item__inventory") # text 
        
        if availability_tag.text.strip().lower() != "en stock.":
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
        
        product = {
            "name" : name_and_url_tag.text.lower().strip() if name_and_url_tag else None,
            "url" :  url + name_and_url_tag["href"] if name_and_url_tag else None,
            "short_description": None,
            "image_url": image_url,
            "price": cleaned_price,
            "availability": True if (availability_tag.text.lower().strip() == "en stock." and availability_tag) else False,
            "category": category_type,
            "website": "techspace"
        }        
        page_products.append(product)
        
    return page_products
        

def normalize_spaces(text):
    return ''.join(' ' if unicodedata.category(c) == 'Zs' else c for c in text)

def extract_price(price):
    cleaned_price = None
    extracted_price = normalize_spaces(price) # handle &nbsp; and others
    match = re.search(r'[\d\s]+[.,]\d{2}', extracted_price)
    if match:
        number = match.group(0).replace(" ", "").replace(",", ".")
        cleaned_price = float(number)
        
    return cleaned_price

   
scrape_websites()
