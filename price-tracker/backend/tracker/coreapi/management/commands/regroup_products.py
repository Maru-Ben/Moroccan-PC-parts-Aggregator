from django.core.management.base import BaseCommand
from coreapi.services.product_grouping.processor import ProductProcessor

class Command(BaseCommand):
    help = 'Re-group all products (useful after updating normalization rules)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--category', 
            type=str, 
            help='Only regroup specific category (e.g., gpu)'
        )
    
    def handle(self, *args, **options):
        processor = ProductProcessor()
        
        self.stdout.write("Re-grouping products...")
        
        stats = processor.regroup_all(category=options.get('category'))
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Re-grouped {stats['total']} products\n"
                f"  Updated: {stats['updated']}\n"
                f"  Grouped: {stats['grouped']}\n"
                f"  New groups: {stats['groups_created']}\n"
                f"  Errors: {stats['errors']}"
            )
        )
