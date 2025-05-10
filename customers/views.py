from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer
from .permissions import IsCustomerOwner

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsCustomerOwner            
    ]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
