"""
Comando para criar superusuário automaticamente se não existir.
Usa variáveis de ambiente para evitar interação.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria um superusuário se não existir, usando variáveis de ambiente'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD não configuradas. '
                    'Pulando criação de superusuário.'
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superusuário "{username}" já existe.')
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(
            self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!')
        )

