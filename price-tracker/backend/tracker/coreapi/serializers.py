from rest_framework import serializers
from models import Product, Website

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['seen', 'created_at', 'updated_at']

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        exclude = ['created_at', 'updated_at']