from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Payment
from .serializers import PaymentSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('payer').order_by('-pay_date')
    serializer_class = PaymentSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payer', 'pay_date']
    search_fields = ['payer__first_name', 'payer__last_name', 'payer__country']
    ordering_fields = ['id', 'amount', 'percent', 'pay_date', 'payer__first_name']
    ordering = ['-pay_date']
