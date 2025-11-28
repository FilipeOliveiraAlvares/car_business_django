"""
Comando para fazer backup apenas do essencial:
- 1 superusuário
- Marcas
- Modelos
- Versões
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Faz backup apenas de superusuário, marcas, modelos e versões'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='backup_inicial.json',
            help='Nome do arquivo de backup (padrão: backup_inicial.json)'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username do superusuário para incluir no backup (opcional)'
        )

    def handle(self, *args, **options):
        from pathlib import Path
        
        # Garantir que o arquivo seja salvo na raiz do projeto
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        output_file = base_dir / options['output']
        
        if not output_file.suffix == '.json':
            output_file = output_file.with_suffix('.json')

        self.stdout.write(self.style.SUCCESS('Fazendo backup do essencial...'))

        try:
            # Lista de modelos para fazer backup
            models_to_backup = [
                'carros.Marca',
                'carros.ModeloVeiculo',
                'carros.VersaoVeiculo',
            ]

            # Se username foi fornecido, adicionar o superusuário
            if options['username']:
                try:
                    user = User.objects.get(username=options['username'], is_superuser=True)
                    # Backup com usuário + modelos
                    models_to_backup.insert(0, f'auth.User.{user.id}')
                    self.stdout.write(f'Incluindo superusuário: {user.username}')
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Superusuário "{options["username"]}" não encontrado. '
                            'Fazendo backup sem usuário.'
                        )
                    )

            # Executar dumpdata
            with open(output_file, 'w', encoding='utf-8') as f:
                call_command(
                    'dumpdata',
                    *models_to_backup,
                    '--indent', '2',
                    '--natural-foreign',
                    '--natural-primary',
                    stdout=f
                )

            file_size = os.path.getsize(output_file)
            file_size_kb = file_size / 1024

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Backup criado com sucesso!\n'
                    f'📁 Arquivo: {output_file.name}\n'
                    f'📍 Localização: {output_file}\n'
                    f'📊 Tamanho: {file_size_kb:.2f} KB\n'
                    f'\n💡 Próximo passo: Adicione ao Git e configure o Railway para restaurar automaticamente.'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Erro: {e}')
            )
            if os.path.exists(output_file):
                os.remove(output_file)

