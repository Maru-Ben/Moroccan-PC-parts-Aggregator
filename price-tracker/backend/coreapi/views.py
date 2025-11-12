from rest_framework import viewsets
from .models import ProductGroup
from .serializers import ProductGroupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, FloatField, Case, When, Value
from django.db.models.functions import Lower, Length, Abs
from django.db.models.expressions import ExpressionWrapper
import re
from django.contrib.postgres.search import TrigramWordSimilarity
from rest_framework.pagination import PageNumberPagination

    
class ProductGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def search(self, request):
        raw_query = request.GET.get('query', '').strip().lower()
        
        if raw_query:
            products = self._get_products(raw_query)
        else:
            products = ProductGroup.objects.all()
        
        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(products, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


    def _dynamic_threshold(self, query_length: int) -> float:
        if query_length <= 3:
            return 0.5  # Strict for "ram"
        elif query_length <= 6:
            return 0.4
        else:
            return 0.25  # Looser for long phrases
    
    
    def _get_products(self, raw_query: str) -> list:
        query = re.sub(r'[\W_]+', ' ', raw_query).strip().lower()
        
        if not query or len(query) < 2:
            products = ProductGroup.objects.order_by('-starting_price')[:20]
        else:
            min_sim = self._dynamic_threshold(len(query))
            first_word = query.split(maxsplit=1)[0] if ' ' in query else query
            query_words = set(raw_query.split())
            
            products = (
                ProductGroup.objects
                .annotate(
                    similarity=TrigramWordSimilarity(query, Lower('canonical_name')),
                    name_len=Length('canonical_name'),
                    prefix_boost=Case(
                        When(canonical_name__istartswith=first_word, then=Value(0.2)),
                        default=Value(0.0),
                        output_field=FloatField()
                    ),
                    length_penalty=ExpressionWrapper(
                        Abs(F('name_len') - len(query)) / (F('name_len') + len(query)),
                        output_field=FloatField()
                    )
                )
                .annotate(
                    score=ExpressionWrapper(
                        F('similarity') + F('prefix_boost') - F('length_penalty') * 0.1,
                        output_field=FloatField()
                    )
                )
                .filter(similarity__gte=min_sim)
                .order_by('-score')[:50]
            )
        
        return products