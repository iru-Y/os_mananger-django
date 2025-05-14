from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from decimal import Decimal, InvalidOperation

from .models import Customer
from .serializers import CustomerSerializer
from .permissions import IsCustomerOwner
from .utils.pdf_generator import generate_os_pdf
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        customer = serializer.save(user=self.request.user)
        pdf_buffer = generate_os_pdf(customer)

    def perform_update(self, serializer):
        customer = serializer.save()
        pdf_buffer = generate_os_pdf(customer)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'OS excluída com sucesso.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_path='monthly-summary')
    def monthly_summary(self, request):
      
        today = now()
        qs = self.get_queryset().filter(
            created_at__year=today.year,
            created_at__month=today.month
        )

        total_cost = Decimal('0.00')
        total_service = Decimal('0.00')

        for obj in qs:
            try:
                total_cost += Decimal(obj.cost_price)
            except (InvalidOperation, TypeError):
                pass
            try:
                total_service += Decimal(obj.service_price)
            except (InvalidOperation, TypeError):
                pass

        total_profit = total_service - total_cost

        return Response({
            'total_cost_price':    f'{total_cost:.2f}',
            'total_service_price': f'{total_service:.2f}',
            'total_profit':        f'{total_profit:.2f}',
        }, status=status.HTTP_200_OK)
