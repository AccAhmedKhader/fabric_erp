"""
Views for inventory management.
"""

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Warehouse, Category, Item, FabricRoll,
    SizeColorMatrix, Batch, StockMovement
)
from .serializers import (
    WarehouseSerializer, CategorySerializer, ItemSerializer,
    FabricRollSerializer, SizeColorMatrixSerializer,
    BatchSerializer, StockMovementSerializer
)


class WarehouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for warehouses.
    """
    queryset = Warehouse.objects.filter(is_active=True)
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'code', 'address']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for categories.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'code', 'description']


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for items.
    """
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['code', 'name', 'description']
    filterset_fields = ['category', 'item_type', 'is_active']


class FabricRollViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fabric rolls.
    """
    queryset = FabricRoll.objects.filter(is_available=True)
    serializer_class = FabricRollSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['roll_number', 'batch_number', 'color']
    filterset_fields = ['quality_status', 'fabric_type', 'warehouse']


class SizeColorMatrixViewSet(viewsets.ModelViewSet):
    """
    API endpoint for size/color matrix.
    """
    queryset = SizeColorMatrix.objects.filter(is_active=True)
    serializer_class = SizeColorMatrixSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['sku', 'size', 'color']
    filterset_fields = ['item', 'size', 'color']


class BatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for batches.
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['batch_number', 'supplier_batch']
    filterset_fields = ['item', 'status']


class StockMovementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for stock movements.
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['reference_number', 'notes']
    filterset_fields = ['movement_type', 'warehouse', 'item']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary of stock movements.
        """
        from django.db.models import Sum
        summary = StockMovement.objects.aggregate(
            total_in=Sum('quantity', filter=models.Q(movement_type__in=['purchase_in', 'transfer_in', 'adjustment_in'])),
            total_out=Sum('quantity', filter=models.Q(movement_type__in=['sale_out', 'transfer_out', 'adjustment_out'])),
            total_value=Sum('total_amount')
        )
        return Response(summary)