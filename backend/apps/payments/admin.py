from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payer', 'amount', 'percent', 'pay_date')
    list_filter = ('pay_date', 'payer__country')
    search_fields = ('payer__first_name', 'payer__last_name')
    date_hierarchy = 'pay_date'
    ordering = ('-pay_date',)
