"""
Comando para exportar marcas do banco de dados para arquivo JSON.
Uso: python manage.py exportar_marcas [--output marcas.json] [--limpar]
"""
from django.core.management.base import BaseCommand
from django.core import serializers
from carros.models import Marca, ModeloVeiculo
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Exporta marcas do banco de dados para arquivo JSON (formato Django fixture)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='marcas.json',
            help='Nome do arquivo de saída (padrão: marcas.json)'
        )
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Remove Corvette e padroniza como Chevrolet antes de exportar'
        )

    def handle(self, *args, **options):
        output_file = Path(options['output'])
        limpar = options['limpar']
        
        self.stdout.write(self.style.SUCCESS('Iniciando exportacao de marcas...\n'))
        
        # Limpar e padronizar se solicitado
        if limpar:
            self.stdout.write('Limpando e padronizando marcas...')
            
            # Buscar marca Chevrolet
            chevrolet = Marca.objects.filter(nome__icontains='chevrolet').first()
            if not chevrolet:
                # Criar Chevrolet se não existir
                chevrolet, created = Marca.objects.get_or_create(nome='Chevrolet')
                if created:
                    self.stdout.write(self.style.SUCCESS('[OK] Marca Chevrolet criada'))
            
            # Buscar marca Corvette
            corvette = Marca.objects.filter(nome__icontains='corvette').first()
            
            if corvette:
                # Atualizar modelos de Corvette para Chevrolet
                modelos_corvette = ModeloVeiculo.objects.filter(marca=corvette)
                count_modelos = modelos_corvette.count()
                
                if count_modelos > 0:
                    self.stdout.write(f'Encontrados {count_modelos} modelo(s) da marca Corvette')
                    modelos_corvette.update(marca=chevrolet)
                    self.stdout.write(self.style.SUCCESS(f'[OK] {count_modelos} modelo(s) atualizado(s) para Chevrolet'))
                
                # Deletar marca Corvette
                corvette.delete()
                self.stdout.write(self.style.SUCCESS('[OK] Marca Corvette removida'))
            else:
                self.stdout.write(self.style.WARNING('[AVISO] Marca Corvette nao encontrada'))
            
            # Padronizar nome de Chevrolet (primeira letra maiúscula)
            if chevrolet.nome != 'Chevrolet':
                chevrolet.nome = 'Chevrolet'
                chevrolet.save()
                self.stdout.write(self.style.SUCCESS('[OK] Marca Chevrolet padronizada'))
        
        # Exportar marcas
        self.stdout.write(f'\nExportando marcas para: {output_file.name}')
        
        marcas = Marca.objects.all().order_by('nome')
        count = marcas.count()
        
        if count == 0:
            self.stdout.write(self.style.ERROR('[ERRO] Nenhuma marca encontrada no banco de dados!'))
            return
        
        # Usar serializador do Django para gerar formato fixture
        data = serializers.serialize('json', marcas, indent=2, ensure_ascii=False)
        
        # Salvar arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(data)
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {count} marca(s) exportada(s) com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'Arquivo salvo em: {output_file.absolute()}'))
        
        # Mostrar lista de marcas
        self.stdout.write('\nMarcas exportadas:')
        for marca in marcas:
            modelos_count = ModeloVeiculo.objects.filter(marca=marca).count()
            self.stdout.write(f'   • {marca.nome} ({modelos_count} modelo(s))')

