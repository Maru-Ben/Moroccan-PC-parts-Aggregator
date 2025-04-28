from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Website
from .serializers import ProductSerializer, WebsiteSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Case, When, Value, IntegerField

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('query', '')
        
        if query:
            # Fuzzy search
            products = Product.objects.annotate(similarity = TrigramSimilarity('name', query)).filter(similarity__gte=0.1).order_by('-similarity')[:30]
        else:
            products = Product.objects.all()
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
