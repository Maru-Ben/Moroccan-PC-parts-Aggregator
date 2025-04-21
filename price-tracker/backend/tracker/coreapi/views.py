from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Website
from .serializers import ProductSerializer, WebsiteSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    