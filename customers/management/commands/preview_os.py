import os
from django.core.management.base import BaseCommand, CommandError
from customers.models import Customer
from customers.utils.pdf_generator import generate_os_pdf

class Command(BaseCommand):
    help = "Gera o PDF de OS para um Customer e salva em arquivo para preview."

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=int,
            required=True,
            help="ID do Customer cuja OS queremos gerar"
        )
        parser.add_argument(
            '--output',
            type=str,
            default='os_preview.pdf',
            help="Nome do arquivo de saída (ex: os_preview.pdf)"
        )

    def handle(self, *args, **options):
        customer_id = options['id']
        output      = options['output']

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CommandError(f"Customer com ID={customer_id} não encontrado")

        buffer = generate_os_pdf(customer)

        out_dir = os.path.dirname(output) or '.'
        os.makedirs(out_dir, exist_ok=True)

        with open(output, 'wb') as f:
            f.write(buffer.getvalue())

        self.stdout.write(self.style.SUCCESS(
            f"PDF de OS para Customer #{customer_id} salvo em {output}"
        ))
