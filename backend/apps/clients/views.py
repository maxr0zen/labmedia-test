from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Client
from .serializers import ClientSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.prefetch_related('payments').annotate(
        payments_total=Coalesce(Sum('payments__amount'), Value(0, output_field=DecimalField()))
    ).order_by('id')
    serializer_class = ClientSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['first_name', 'last_name', 'country']
    ordering_fields = ['id', 'first_name', 'last_name', 'country', 'payments_total']
    ordering = ['id']
