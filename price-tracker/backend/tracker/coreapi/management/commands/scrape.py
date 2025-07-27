from django.core.management.base import BaseCommand, CommandError
import asyncio, time, json

from coreapi.models import Product, Website

from coreapi.scraper.logger import logger
from coreapi.scraper.main import scrape_websites_async, scrape_websites

class Command(BaseCommand):
    help = "Scrape websites for products"
    
    def add_arguments(self, parser):
        parser.add_argument('--method', type=str, choices=['sync', 'async'], 
                    default='async', help='Scraping method to use')
        parser.add_argument('--json', type=str, help='Path to JSON file for product ingestion')
        parser.add_argument('--with-delete', action='store_true', help='specify if you want to delete unavailable products at the end')
    
    def handle(self, *args, **options):
        if options['json']:
            self.ingest_products_from_json(options)
        else:
            self.scrape_products(options)

        
    def scrape_products(self, options):
        start_time = time.time()
        products = []
        if options['method'] == 'async':
            logger.info("Starting asynchronous scraping...")
            products = asyncio.run(scrape_websites_async())
        else:
            logger.info("Starting synchronous scraping...")
            products = scrape_websites()
            
        scraping_elapsed_time = time.time() - start_time
        logger.info(f"Scraping completed in {scraping_elapsed_time:.2f} seconds")
        
        self.ingest_products(products, options)
        
        ingestion_elapsed_time = time.time() - scraping_elapsed_time - start_time
        logger.info(f"Ingestion completed in {ingestion_elapsed_time:.2f} seconds")
        
    def ingest_products_from_json(self, options):
        json_file = options['json']
        logger.info(f"Starting products ingestion from {json_file}")
        with open(json_file, 'r', encoding='utf-8') as file:
            products = json.load(file)
        self.ingest_products(products, options)
        
    def ingest_products(self, products, options):
        logger.info("Starting products ingestion into the database")
        Product.objects.all().update(seen = False)
        for product in products:
            website_obj, created = Website.objects.update_or_create(name = product["website"])
            try:
                Product.objects.update_or_create(
                    id = product["id"],
                    defaults={
                        "name": product["name"],
                        "short_description": product.get("short_description", ""),
                        "url": product["url"],
                        "image_url": product["image_url"],
                        "price": product["price"],
                        "availability": product["availability"],
                        "website": website_obj,
                        "category": product["category"],
                        "seen": True,
                    }
                )
            except Exception as e:
                logger.info(f'Error processing product named {product["name"]}, cause: {e}')
        
        if options['with_ delete']:
            logger.info("Deleting unseen products")
            Product.objects.filter(seen = False).delete()
        else:
            Product.objects.filter(seen = False).update(availability = False)
        