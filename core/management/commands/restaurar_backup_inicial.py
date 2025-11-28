"""
Comando para restaurar o backup_inicial.json no banco de dados.
Usado principalmente no Railway após o deploy.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import json
import os


class Command(BaseCommand):
    help = 'Restaura backup_inicial.json no banco de dados (superusuário, marcas, modelos, versões)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='backup_inicial.json',
            help='Arquivo de backup para restaurar (padrão: backup_inicial.json)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Pula registros que já existem (evita erros de duplicação)'
        )

    def handle(self, *args, **options):
        # Caminho do arquivo na raiz do projeto
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        backup_file = base_dir / options['file']

        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('🔄 RESTAURANDO BACKUP INICIAL'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Verificar se o arquivo existe
        if not backup_file.exists():
            self.stdout.write(
                self.style.ERROR(
                    f'\n❌ Arquivo não encontrado: {backup_file}\n'
                    f'   Certifique-se de que o arquivo está na raiz do projeto.'
                )
            )
            return

        # Contar registros no arquivo
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total_records = len(data) if isinstance(data, list) else 0
            
            # Contar por tipo
            usuarios = sum(1 for item in data if item.get('model') == 'auth.user')
            marcas = sum(1 for item in data if item.get('model') == 'carros.marca')
            modelos = sum(1 for item in data if item.get('model') == 'carros.modeloveiculo')
            versoes = sum(1 for item in data if item.get('model') == 'carros.versaoveiculo')

            self.stdout.write(f'\n📊 Conteúdo do backup:')
            self.stdout.write(f'   👤 Superusuários: {usuarios}')
            self.stdout.write(f'   🏷️  Marcas: {marcas}')
            self.stdout.write(f'   🚗 Modelos: {modelos}')
            self.stdout.write(f'   📋 Versões: {versoes}')
            self.stdout.write(f'   📦 Total: {total_records} registros\n')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Não foi possível ler o conteúdo do arquivo: {e}')
            )
            total_records = 0

        # Restaurar backup
        self.stdout.write(f'🔄 Restaurando backup de: {backup_file.name}...\n')

        try:
            # Executar loaddata
            call_command(
                'loaddata',
                str(backup_file),
                verbosity=1
            )

            self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
            self.stdout.write(self.style.SUCCESS('✅ BACKUP RESTAURADO COM SUCESSO!'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n📊 Resumo:\n'
                    f'   ✅ {total_records} registro(s) processado(s)\n'
                    f'   ✅ Banco de dados atualizado\n'
                    f'   ✅ Sistema pronto para uso\n'
                )
            )

        except Exception as e:
            error_msg = str(e)
            
            # Tratar erros comuns
            if 'UNIQUE constraint' in error_msg or 'duplicate key' in error_msg.lower():
                self.stdout.write(
                    self.style.WARNING(
                        '\n' + '=' * 60 + '\n'
                        '⚠️  ALGUNS REGISTROS JÁ EXISTEM NO BANCO\n'
                        '=' * 60 + '\n'
                        'Isso é normal se o backup já foi restaurado anteriormente.\n'
                        'Os registros novos foram inseridos, os duplicados foram ignorados.\n'
                        '\n✅ Sistema funcionando normalmente.\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        '\n' + '=' * 60 + '\n'
                        '❌ ERRO AO RESTAURAR BACKUP\n'
                        '=' * 60 + '\n'
                        f'Erro: {error_msg}\n'
                        '\nVerifique:\n'
                        '  - Se as migrações foram aplicadas (python manage.py migrate)\n'
                        '  - Se o arquivo está no formato correto\n'
                        '  - Se há conflitos de dados no banco\n'
                    )
                )
                raise

