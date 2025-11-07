from pathlib import Path
from django.core.management.base import BaseCommand
import asyncio, time, json
from coreapi.services.scraper.main import scrape_websites_async, scrape_websites
from coreapi.services.product_grouping.processor import ProductProcessor
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Scrape websites for products and group them"
    
    def add_arguments(self, parser):
        parser.add_argument('--method', type=str, choices=['sync', 'async'], 
                    default='async', help='Scraping method to use')
        parser.add_argument('--file', type=str, help="Path to JSON file with scraped results (skip scraping)")
    
    def handle(self, *args, **options):
        start_time = time.time()
        products = []
        
        file_path = options.get('file')
        
        if not file_path:
            if options['method'] == 'async':
                logger.info("Starting asynchronous scraping...")
                products = asyncio.run(scrape_websites_async())
            else:
                logger.info("Starting synchronous scraping...")
                products = scrape_websites()
        else:
            product_file = Path(file_path)
            if not product_file.exists():
                logger.error(f"File not found: {file_path}")
                return
            try:
                logger.info(f"Loading scraped results from file: {file_path}")
                with product_file.open('r',encoding='UTF-8') as f:
                    products = json.load(f)
                logger.info(f"Loaded {len(products) if isinstance(products, list) else 'unknown'} products from file")
            except Exception as e:
                logger.error(f"Failed to load JSON file: {e}")
                return
            
        scraping_elapsed_time = time.time() - start_time
        logger.info(f"Scraping completed in {scraping_elapsed_time:.2f} seconds")
        
        logger.info("Processing and grouping products...")
        processor = ProductProcessor()
        stats = processor.ingest_and_group(products)
        
        process_time = time.time() - scraping_elapsed_time - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Processed in {process_time:.2f}s\n"
                f"  Created: {stats['created']}\n"
                f"  Updated: {stats['updated']}\n"
                f"  Groups created: {stats['groups_created']}\n"
                f"  Grouped: {stats['grouped']}\n"
                f"  Errors: {stats['errors']}"
            )
        )
    
        
        
