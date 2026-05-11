from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    payments_count = serializers.IntegerField(source='payments.count', read_only=True)
    total_payments = serializers.DecimalField(
        source='payments_total',
        max_digits=15,
        decimal_places=2,
        read_only=True,
        default=0,
    )

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'country', 'payments_count', 'total_payments']

    def validate_first_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value.strip()

    def validate_last_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value.strip()
