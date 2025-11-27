"""
Comando para importar modelos e versões de veículos a partir de arquivos JSON.
Uso: python manage.py importar_dados [--modelos modelos.json] [--versoes versoes.json]
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Importa modelos e versões de veículos a partir de arquivos JSON (fixtures)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--modelos',
            type=str,
            default='modelos.json',
            help='Caminho para o arquivo JSON de modelos (padrão: modelos.json)'
        )
        parser.add_argument(
            '--versoes',
            type=str,
            default='versoes.json',
            help='Caminho para o arquivo JSON de versões (padrão: versoes.json)'
        )
        parser.add_argument(
            '--categorias',
            type=str,
            default='categorias_veiculos.json',
            help='Caminho para o arquivo JSON de categorias (padrão: categorias_veiculos.json)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Pula registros que já existem (evita erros de duplicação)'
        )

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        modelos_file = base_dir / options['modelos']
        versoes_file = base_dir / options['versoes']
        categorias_file = base_dir / options['categorias']
        
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando importação de dados...\n'))
        
        # Importar categorias (se existir)
        if categorias_file.exists():
            self.stdout.write(f'📦 Importando categorias de: {categorias_file.name}')
            try:
                call_command('loaddata', str(categorias_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('✅ Categorias importadas com sucesso!'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️  Erro ao importar categorias: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Arquivo de categorias não encontrado: {categorias_file.name}'))
        
        # Importar modelos
        if modelos_file.exists():
            self.stdout.write(f'\n📦 Importando modelos de: {modelos_file.name}')
            try:
                call_command('loaddata', str(modelos_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('✅ Modelos importados com sucesso!'))
            except Exception as e:
                if 'UNIQUE constraint' in str(e) or 'duplicate key' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'⚠️  Alguns modelos já existem. Use --skip-existing para ignorar.'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Erro ao importar modelos: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Arquivo de modelos não encontrado: {modelos_file.name}'))
        
        # Importar versões
        if versoes_file.exists():
            self.stdout.write(f'\n📦 Importando versões de: {versoes_file.name}')
            try:
                call_command('loaddata', str(versoes_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('✅ Versões importadas com sucesso!'))
            except Exception as e:
                if 'UNIQUE constraint' in str(e) or 'duplicate key' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'⚠️  Algumas versões já existem. Use --skip-existing para ignorar.'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Erro ao importar versões: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Arquivo de versões não encontrado: {versoes_file.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✨ Importação concluída!'))

