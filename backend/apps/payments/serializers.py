from rest_framework import serializers
from apps.clients.models import Client
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payer_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'payer', 'payer_details', 'amount', 'percent', 'pay_date']
        extra_kwargs = {
            'payer': {'write_only': True},
        }

    def get_payer_details(self, obj):
        return {
            'id': obj.payer.id,
            'first_name': obj.payer.first_name,
            'last_name': obj.payer.last_name,
            'country': obj.payer.country,
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_percent(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Percent must be between 0 and 100.")
        return value
