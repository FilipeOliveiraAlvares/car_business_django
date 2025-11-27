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
        parser.add_argument(
            '--importar-categorias',
            action='store_true',
            help='Importa categorias (padrão: False - categorias já foram importadas no servidor)'
        )

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        modelos_file = base_dir / options['modelos']
        versoes_file = base_dir / options['versoes']
        categorias_file = base_dir / options['categorias']
        marcas_file = base_dir / 'marcas.json'
        
        self.stdout.write(self.style.SUCCESS('Iniciando importacao de dados...\n'))
        
        # Importar categorias (apenas se --importar-categorias for True)
        importar_categorias = options.get('importar_categorias', False)  # Padrão: False (não importar)
        
        if importar_categorias:
            if categorias_file.exists():
                self.stdout.write(f'Importando categorias de: {categorias_file.name}')
                try:
                    call_command('loaddata', str(categorias_file), verbosity=0)
                    self.stdout.write(self.style.SUCCESS('[OK] Categorias importadas com sucesso!'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'[AVISO] Erro ao importar categorias: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'[AVISO] Arquivo de categorias nao encontrado: {categorias_file.name}'))
        else:
            self.stdout.write('[INFO] Pulando importacao de categorias (ja foram importadas no servidor)')
        
        # IMPORTANTE: Importar marcas PRIMEIRO (ordem correta)
        if marcas_file.exists():
            self.stdout.write(f'\nImportando marcas de: {marcas_file.name}')
            try:
                call_command('loaddata', str(marcas_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('[OK] Marcas importadas com sucesso!'))
            except Exception as e:
                if 'UNIQUE constraint' in str(e) or 'duplicate key' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'[AVISO] Algumas marcas ja existem (continuando...)'))
                else:
                    self.stdout.write(self.style.WARNING(f'[AVISO] Erro ao importar marcas: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'[AVISO] Arquivo de marcas nao encontrado: {marcas_file.name}'))
        
        # Importar modelos (depois das marcas)
        if modelos_file.exists():
            self.stdout.write(f'\nImportando modelos de: {modelos_file.name}')
            try:
                call_command('loaddata', str(modelos_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('[OK] Modelos importados com sucesso!'))
            except Exception as e:
                if 'UNIQUE constraint' in str(e) or 'duplicate key' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'[AVISO] Alguns modelos ja existem (continuando...)'))
                elif 'foreign key constraint' in str(e).lower():
                    self.stdout.write(self.style.ERROR(f'[ERRO] Erro de chave estrangeira: Verifique se as marcas foram importadas corretamente'))
                    self.stdout.write(self.style.ERROR(f'Detalhes: {str(e)[:200]}'))
                else:
                    self.stdout.write(self.style.ERROR(f'[ERRO] Erro ao importar modelos: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo de modelos nao encontrado: {modelos_file.name}'))
        
        # Importar versões (depois dos modelos)
        if versoes_file.exists():
            self.stdout.write(f'\nImportando versoes de: {versoes_file.name}')
            try:
                call_command('loaddata', str(versoes_file), verbosity=0)
                self.stdout.write(self.style.SUCCESS('[OK] Versoes importadas com sucesso!'))
            except Exception as e:
                if 'UNIQUE constraint' in str(e) or 'duplicate key' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'[AVISO] Algumas versoes ja existem (continuando...)'))
                elif 'foreign key constraint' in str(e).lower():
                    self.stdout.write(self.style.ERROR(f'[ERRO] Erro de chave estrangeira: Verifique se os modelos foram importados corretamente'))
                    self.stdout.write(self.style.ERROR(f'Detalhes: {str(e)[:200]}'))
                else:
                    self.stdout.write(self.style.ERROR(f'[ERRO] Erro ao importar versoes: {e}'))
        else:
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo de versoes nao encontrado: {versoes_file.name}'))
        
        self.stdout.write(self.style.SUCCESS('\nImportacao concluida!'))

