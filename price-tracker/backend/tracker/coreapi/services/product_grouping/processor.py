from coreapi.services.product_grouping.normalizers import gpu
from django.db import transaction
from typing import List, Dict
from coreapi.services.product_grouping.logger import logger
from django.db.models import Min, F
from coreapi.models import Product, ProductGroup, Website
from coreapi.services.product_grouping.models import scraped_product

class ProductProcessor:
    def __init__(self):
        self.normalizers = {
            "gpu": gpu.GPUNormalizer("gpu.json")
        }
    
    
    def ingest_and_group(self, products: List[scraped_product]) -> Dict:
        """
        Ingest scraped products and assign to groups
        
        Args:
            products: List of dicts with scraped product data
            
        Returns:
            dict: Statistics about ingestion/grouping
        """
        stats = {
            'total': len(products),
            'created': 0,
            'updated': 0,
            'groups_created': 0,
            'grouped': 0,
            'errors': 0
        }
        
        # Mark existing products as unseen
        Product.objects.all().update(seen=False)
        
        for product_data in products:
            try:
                self._process_single_product(product_data, stats)
            except Exception as e:
                stats['errors'] += 1
                logger.error(f"Error processing {product_data.get('name')}: {e}")
            
        # Mark unseen product as unavailable
        Product.objects.filter(seen=False).update(availability=False)
        
        # updating setting the group price
        self._update_group_pricing()
        
        return stats
    
    @transaction.atomic
    def _process_single_product(self, product: scraped_product, stats: Dict):
        """Process a single product"""
        website_obj, _ = Website.objects.update_or_create(
            name = product["website"]
        )
        
        group_obj = self._get_or_create_group(product)
        if group_obj:
            stats['grouped'] += 1
        
        # Create/Update product
        product, created = Product.objects.update_or_create(
            id=product["id"],
            defaults={
                "name": product["name"],
                "short_description": product.get("short_description", ""),
                "url": product["url"],
                "image_url": product["image_url"],
                "price": product["price"],
                "availability": product["availability"],
                "website": website_obj,
                "category": product["category"],
                "canonical_group": group_obj,
                "seen": True,
            }
        )
        
        stats['created' if created else 'updated'] += 1
        
    
    def _get_or_create_group(self, product_data: scraped_product):
        """Get or create product group for a product"""
        category = product_data["category"]
        if category not in self.normalizers:
            logger.error(f"No normalizer for category {category}")
            return None
        
        try:
            canonical_product = self.normalizers[category].normalize(product_data['name'])
            group, created = ProductGroup.objects.get_or_create(
                canonical_name= canonical_product.model,
                category=category,
                defaults={
                    'brand': canonical_product.brand,
                    'starting_price': product_data["price"],
                    'attributes': {
                        'chipset': canonical_product.key_specs['chipset'],
                        'model_number': canonical_product.key_specs['model_number'],
                        'model_variant': canonical_product.key_specs.get('model_variant'),
                        'vram': canonical_product.key_specs.get('vram'),
                        'board_partner': canonical_product.key_specs['board_partner'],
                    }
                }
            )
            return group
        except Exception as e:
            logger.warning(f"Could not normalize '{product_data['name']}': {e}")
            return None
    

    def _update_group_pricing(self):
        """Update starting_price for all groups"""
        groups = ProductGroup.objects.all()
        updated = 0
        
        for group in groups:
            min_price = group.products.filter(availability=True).aggregate(
                min_price=Min('price')
            )['min_price']
            
            if min_price and group.starting_price != min_price:
                group.starting_price = min_price
                group.save()
                updated += 1
        return updated
    
    
    def regroup_all(self, category: str = None):
        """Re-group all existing products (useful for rule updates)"""
        filters = {}
        if category:
            filters['category'] = category
        
        # Get products as list of dicts
        products_qs = Product.objects.filter(**filters).select_related('website')
        
        products_data = [
            {
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'url': p.url,
                'image_url': p.image_url,
                'short_description': p.short_description or '',
                'availability': p.availability,
                'category': p.category,
                'website': p.website.name,
            }
            for p in products_qs
        ]
        
        # Process like normal ingestion
        stats = self.ingest_and_group(products_data)
        
        return stats
        
            
