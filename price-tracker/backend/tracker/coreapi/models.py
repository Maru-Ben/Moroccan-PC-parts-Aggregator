from django.db import models
from django.utils.translation import gettext_lazy as _

class Website(models.Model):
    name = models.CharField(_("Website name"), max_length=50)
    created_at = models.DateTimeField(_("First added"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)

class Product(models.Model):
    class Category(models.TextChoices):
        COMPONENTS = 'COMP', _('Components')
        PERIPHERALS = 'PER', _('Peripherals')
        
    id = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(_("Product name"), max_length=200, db_index=True)
    short_description = models.TextField(_("Product Description"), blank=True, null=True)
    url = models.URLField(_("Product URL"), max_length=200)
    image_url = models.URLField(_("Product Image URL"), max_length=200)
    price = models.DecimalField(_("Product Price"), max_digits=10, decimal_places=2)
    availability = models.BooleanField(_("Product availability"), default=True)
    category = models.CharField(_("Product Category"), max_length=4, choices=Category.choices)
    website = models.ForeignKey(Website, verbose_name=_("Website"), on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(_("First scraped"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)
    seen = models.BooleanField(default=False)

