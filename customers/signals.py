import os
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from decouple import config

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    User = get_user_model()

    admin_username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
    admin_email = config('DJANGO_SUPERUSER_EMAIL', default='admin@example.com')
    admin_password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123')

    if not User.objects.filter(username=admin_username).exists():
        print(f'Criando superusuário {admin_username}...')
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
    else:
        print(f'Superusuário {admin_username} já existe.')
