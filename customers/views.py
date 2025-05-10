from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Customer
from .serializers import CustomerSerializer
from .permissions import IsCustomerOwner
from .utils.pdf_generator import generate_os_pdf 

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        customer = serializer.save(user=self.request.user)

        pdf_buffer = generate_os_pdf(customer)

        subject = f"Ordem de Serviço #{customer.id}"
        body = render_to_string('emails/os_email.txt', {
            'customer': customer,
            'user':      self.request.user,
        })
        email = EmailMessage(
            subject=subject,
            body=body,
            to=[customer.email, self.request.user.email],
        )
        email.attach(f'OS_{customer.id}.pdf', pdf_buffer.read(), 'application/pdf')
        email.send(fail_silently=False)

    def perform_update(self, serializer):
        customer = serializer.save()
        pdf_buffer = generate_os_pdf(customer)

        subject = f"Ordem de Serviço (Atualizada) #{customer.id}"
        body = render_to_string('emails/os_email.txt', {
            'customer': customer,
            'user':      self.request.user,
        })
        email = EmailMessage(
            subject=subject,
            body=body,
            to=[customer.email, self.request.user.email],
        )
        email.attach(f'OS_{customer.id}.pdf', pdf_buffer.read(), 'application/pdf')
        email.send(fail_silently=False)
