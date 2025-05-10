from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Customer
        fields = ['id', 'user', 'company_name', 'phone_number', 'address']
        read_only_fields = ['id']
