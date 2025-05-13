from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Customer

decimal_string = RegexValidator(
    regex=r'^\d+(\.\d{1,2})?$',
    message='Use formato numérico, ex: "123.45"'
)

class CustomerSerializer(serializers.ModelSerializer):
    cost_price = serializers.CharField(
        validators=[decimal_string]
    )
    service_price = serializers.CharField(
        validators=[decimal_string]
    )
    profit = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'description',
            'cost_price',
            'service_price',
            'profit',
            'created_at',
            'updated_at',
        ]
