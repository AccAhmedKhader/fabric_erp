"""
URL configuration for inventory app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'fabric-rolls', views.FabricRollViewSet)
router.register(r'size-color-matrix', views.SizeColorMatrixViewSet)
router.register(r'batches', views.BatchViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)

app_name = 'inventory'

urlpatterns = [
    path('api/', include(router.urls)),
]