from django.core.management.base import BaseCommand, CommandError
import asyncio, time

from coreapi.models import Product, Website

from coreapi.services.scraper.logger import logger
from coreapi.services.scraper.main import scrape_websites_async, scrape_websites

class Command(BaseCommand):
    help = "Scrape websites for products"
    
    def add_arguments(self, parser):
        parser.add_argument('--method', type=str, choices=['sync', 'async'], 
                    default='async', help='Scraping method to use')
    
    def handle(self, *args, **options):
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
        
        self.ingest_products(products)
        
        ingestion_elapsed_time = time.time() - scraping_elapsed_time - start_time
        logger.info(f"Ingestion completed in {ingestion_elapsed_time:.2f} seconds")
        
    def ingest_products(self, products):
        logger.info("Starting products ingestion into the database")
        Product.objects.all().update(seen = False)
        for product in products:
            website_obj, created = Website.objects.update_or_create(name = product["website"])
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
        Product.objects.filter(seen = False).update(availability = False)