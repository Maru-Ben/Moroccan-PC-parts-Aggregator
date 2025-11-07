from rest_framework import serializers
from .models import Product, Website, ProductGroup
from django.utils.html import mark_safe

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        exclude = ['created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    category = serializers.CharField(source='get_category_display')
    
    class Meta:
        model = Product
        exclude = ['seen', 'created_at', 'updated_at']

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductGroup
        fields = '__all__'
        