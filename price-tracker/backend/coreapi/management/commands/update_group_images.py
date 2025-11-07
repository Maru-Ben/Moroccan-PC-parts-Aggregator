# management/commands/update_group_images.py
from django.core.management.base import BaseCommand
from coreapi.services.product_grouping.processor import ProductProcessor

class Command(BaseCommand):
    help = 'Update representative images for all product groups'
    
    def handle(self, *args, **options):
        processor = ProductProcessor()
        updated_prices, updated_images = processor.update_group_pricing()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated_images} group images, "
                f"{updated_prices} prices"
            )
        )