from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    profit = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone', 'description', 'cost_price', 'service_price', 'profit', 'created_at', 'updated_at']
