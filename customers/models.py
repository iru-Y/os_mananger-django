from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation

class Customer(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    full_name     = models.CharField(max_length=100)
    email         = models.EmailField()
    phone         = models.CharField(max_length=20)
    description   = models.CharField(max_length=255)
    cost_price    = models.CharField(max_length=20)
    service_price = models.CharField(max_length=20)

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    @property
    def profit(self) -> str:
       
        try:
            cost = Decimal(self.cost_price)
            service = Decimal(self.service_price)
            result = service - cost
            return f"{result:.2f}"
        except (InvalidOperation, TypeError):
            return "0.00"

    def __str__(self):
        return self.full_name
