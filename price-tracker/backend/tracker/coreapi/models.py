from django.db import models
from django.utils.translation import gettext_lazy as _
from coreapi.constants import CATEGORIES


CATEGORY_CHOICES = [(cat, cat.capitalize()) for cat in CATEGORIES]


class Website(models.Model):
    name = models.CharField(_("Website name"), max_length=50)
    created_at = models.DateTimeField(_("First added"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(_("Product name"), max_length=200, db_index=True)
    short_description = models.TextField(_("Product Description"), blank=True, null=True)
    url = models.URLField(_("Product URL"), max_length=200)
    image_url = models.URLField(_("Product Image URL"), max_length=200)
    price = models.DecimalField(_("Product Price"), max_digits=10, decimal_places=2)
    availability = models.BooleanField(_("Product availability"), default=True)
    category = models.CharField(_("Product Category"), choices=CATEGORY_CHOICES)
    
    website = models.ForeignKey(Website, verbose_name=_("Website"), on_delete=models.CASCADE, related_name="products")
    canonical_group = models.ForeignKey('ProductGroup', null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    
    created_at = models.DateTimeField(_("First scraped"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)
    seen = models.BooleanField(default=False)
    
    
class ProductGroup(models.Model):
    canonical_name = models.CharField(_("Canonical product name"), max_length=100, db_index=True)
    category = models.CharField(_("Product Category"), choices=CATEGORY_CHOICES)
    starting_price = models.DecimalField(_("Starting Price"), max_digits=10, decimal_places=2)
    brand = models.CharField(_("Brand"), max_length=100)
    attributes = models.JSONField(_("Products attributes"), default=dict)
    
    created_at = models.DateTimeField(_("First created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)
