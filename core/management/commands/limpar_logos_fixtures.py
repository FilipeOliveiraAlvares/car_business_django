"""
Comando para remover referencias de logos/imagens dos arquivos JSON de fixtures.
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Remove referencias de logos dos arquivos JSON de fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--marcas',
            type=str,
            default='marcas.json',
            help='Arquivo de marcas (padrao: marcas.json)'
        )

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        marcas_file = base_dir / options['marcas']
        
        self.stdout.write(self.style.SUCCESS('Limpando referencias de logos...\n'))
        
        if not marcas_file.exists():
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo nao encontrado: {marcas_file}'))
            return
        
        self.stdout.write(f'Processando: {marcas_file.name}')
        
        # Carregar arquivo
        with open(marcas_file, 'r', encoding='utf-8') as f:
            marcas_data = json.load(f)
        
        # Remover campo logo de cada marca
        logos_removidos = 0
        for marca in marcas_data:
            if 'logo' in marca['fields'] and marca['fields']['logo']:
                marca['fields']['logo'] = ''
                logos_removidos += 1
        
        # Salvar arquivo atualizado
        with open(marcas_file, 'w', encoding='utf-8') as f:
            json.dump(marcas_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {logos_removidos} referencia(s) de logo removida(s)'))
        self.stdout.write(self.style.SUCCESS(f'Arquivo atualizado: {marcas_file.name}'))

