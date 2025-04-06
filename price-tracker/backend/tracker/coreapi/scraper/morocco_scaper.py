import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

URLS = {
    "https://www.ultrapc.ma/": {
        "categories": [
            {"url": "20-composants", "type": "Components"},
            {"url": "58-peripheriques", "type": "Peripherals"}
        ],
        "scraper": "ultrapc"
    }
}



def scrape_websites():
    products = []
    # we check all urls in our dict then we call the concerned function
    for base_url, site_info in URLS.items():
        print(f"Scraping {site_info['scraper']}...")
        if site_info['scraper'] == "ultrapc":
            products = scrape_ultrapc(base_url, site_info['categories'])
            
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
         
    return products
        
# Ultra PC     
def scrape_ultrapc(url, categories):
    """ Will receive the url and the category to go to and scrape all products in 
        all categories of ultrapc

    Args:
        url (string): url of the page
        categories (array): category sup url
    """
    products = []
    for category in categories:
        category_products = scrape_ultrapc_category(url + category["url"], category["type"])
        products.extend(category_products)
    return products
                    
def scrape_ultrapc_category(category_url, category_type):
    """scrape one ultrapc category 

    Args:
        category_url (string): url of the category to scrape
        category_type (string): name of the category in english
    """
    page = 1 
    category_products = []
    
    # visiting each page of the category to scrape it
    while True:
        url = f"{category_url}?page={page}"
        print(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        page_products = extract_ultrapc_page_products(soup, category_type)
        if not page_products:
            break # No more products -- reached the last page
        category_products.extend(page_products)
        page += 1
        
    return category_products
        
def extract_ultrapc_page_products(soup, category_type):
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
            "name" : name_and_url_tag.text.strip() if name_and_url_tag else None,
            "url" : name_and_url_tag["href"] if name_and_url_tag else None,
            "short_description": short_description_tag.text.strip() if short_description_tag else None,
            "image_url": image_tag["src"] if image_tag else None,
            "price": price_tag["content"].strip() if price_tag else None,
            "availability": availability_tag.text.strip() if availability_tag else None,
            "category": category_type,
            "website": "ultrapc"
        }        
        page_products.append(product)
        
    return page_products
        
       
         
scrape_websites()
