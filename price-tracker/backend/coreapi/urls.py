from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductGroupViewSet

router = DefaultRouter()

router.register(r'products', ProductGroupViewSet)

urlpatterns = router.urls