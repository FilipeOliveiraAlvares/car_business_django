"""
Comando para corrigir IDs de marcas e modelos nos arquivos JSON de fixtures.
Atualiza modelos.json e versoes.json com base nos IDs corretos de marcas.json.
Usa o banco de dados local como referência para mapear nomes -> IDs corretos.
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Corrige IDs de marcas em modelos.json e IDs de modelos em versoes.json baseado em marcas.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--marcas',
            type=str,
            default='marcas.json',
            help='Arquivo de marcas (padrão: marcas.json)'
        )
        parser.add_argument(
            '--modelos',
            type=str,
            default='modelos.json',
            help='Arquivo de modelos (padrão: modelos.json)'
        )
        parser.add_argument(
            '--versoes',
            type=str,
            default='versoes.json',
            help='Arquivo de versões (padrão: versoes.json)'
        )

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        marcas_file = base_dir / options['marcas']
        modelos_file = base_dir / options['modelos']
        versoes_file = base_dir / options['versoes']
        
        self.stdout.write(self.style.SUCCESS('Iniciando correcao de IDs...\n'))
        
        # 1. Carregar marcas.json e criar mapeamento nome -> pk
        if not marcas_file.exists():
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo nao encontrado: {marcas_file}'))
            return
        
        self.stdout.write(f'Carregando marcas de: {marcas_file.name}')
        with open(marcas_file, 'r', encoding='utf-8') as f:
            marcas_data = json.load(f)
        
        # Criar mapeamento: nome_marca -> pk (do marcas.json)
        marcas_map = {}
        for marca in marcas_data:
            nome = marca['fields']['nome'].strip()
            pk = marca['pk']
            # Mapear nome exato
            marcas_map[nome.lower()] = pk
            # Mapear variações comuns
            if 'chevrolet' in nome.lower():
                marcas_map['corvette'] = pk  # Corvette agora é Chevrolet
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {len(marcas_map)} marca(s) mapeada(s)'))
        
        # 2. Carregar modelos.json e corrigir IDs de marcas usando o banco como referência
        if not modelos_file.exists():
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo nao encontrado: {modelos_file}'))
            return
        
        self.stdout.write(f'\nCorrigindo modelos em: {modelos_file.name}')
        with open(modelos_file, 'r', encoding='utf-8') as f:
            modelos_data = json.load(f)
        
        # Usar banco de dados local para mapear marca_id_antigo -> nome_marca -> pk_novo
        from carros.models import Marca, ModeloVeiculo
        
        # Criar mapeamento ID_antigo -> ID_novo
        id_antigo_para_novo = {}
        modelos_corrigidos = 0
        modelos_nao_encontrados = []
        
        for modelo in modelos_data:
            marca_id_antigo = modelo['fields']['marca']
            
            if marca_id_antigo in id_antigo_para_novo:
                # Já mapeado anteriormente
                modelo['fields']['marca'] = id_antigo_para_novo[marca_id_antigo]
                modelos_corrigidos += 1
            else:
                # Buscar no banco de dados local
                try:
                    # Buscar modelo no banco pelo ID
                    modelo_obj = ModeloVeiculo.objects.filter(id=modelo['pk']).first()
                    if modelo_obj:
                        nome_marca = modelo_obj.marca.nome.strip()
                        nome_marca_lower = nome_marca.lower()
                        
                        # Buscar ID correto no marcas.json
                        if nome_marca_lower in marcas_map:
                            novo_id = marcas_map[nome_marca_lower]
                            id_antigo_para_novo[marca_id_antigo] = novo_id
                            modelo['fields']['marca'] = novo_id
                            modelos_corrigidos += 1
                        else:
                            # Tentar buscar marca diretamente no banco
                            marca_obj = Marca.objects.filter(nome__iexact=nome_marca).first()
                            if marca_obj:
                                # Buscar esse ID no marcas.json
                                for m in marcas_data:
                                    if m['fields']['nome'].strip().lower() == nome_marca_lower:
                                        novo_id = m['pk']
                                        id_antigo_para_novo[marca_id_antigo] = novo_id
                                        modelo['fields']['marca'] = novo_id
                                        modelos_corrigidos += 1
                                        break
                                else:
                                    modelos_nao_encontrados.append(f"Modelo {modelo['pk']} ({modelo['fields']['nome']}): marca '{nome_marca}' nao encontrada em marcas.json")
                            else:
                                modelos_nao_encontrados.append(f"Modelo {modelo['pk']} ({modelo['fields']['nome']}): marca '{nome_marca}' nao encontrada no banco")
                    else:
                        # Modelo não existe no banco, tentar pela marca_id antiga
                        marca_obj_antiga = Marca.objects.filter(id=marca_id_antigo).first()
                        if marca_obj_antiga:
                            nome_marca = marca_obj_antiga.nome.strip()
                            nome_marca_lower = nome_marca.lower()
                            
                            if nome_marca_lower in marcas_map:
                                novo_id = marcas_map[nome_marca_lower]
                                id_antigo_para_novo[marca_id_antigo] = novo_id
                                modelo['fields']['marca'] = novo_id
                                modelos_corrigidos += 1
                            else:
                                modelos_nao_encontrados.append(f"Modelo {modelo['pk']}: marca ID {marca_id_antigo} ('{nome_marca}') nao encontrada em marcas.json")
                        else:
                            modelos_nao_encontrados.append(f"Modelo {modelo['pk']}: marca ID {marca_id_antigo} nao encontrada no banco")
                except Exception as e:
                    modelos_nao_encontrados.append(f"Modelo {modelo['pk']}: erro - {str(e)}")
        
        # Salvar modelos.json corrigido
        with open(modelos_file, 'w', encoding='utf-8') as f:
            json.dump(modelos_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {modelos_corrigidos} modelo(s) corrigido(s)'))
        if modelos_nao_encontrados:
            self.stdout.write(self.style.WARNING(f'[AVISO] {len(modelos_nao_encontrados)} modelo(s) nao encontrado(s)'))
            if len(modelos_nao_encontrados) <= 10:
                for msg in modelos_nao_encontrados:
                    self.stdout.write(self.style.WARNING(f'  - {msg}'))
        
        # 3. Carregar versoes.json - os IDs de modelos devem estar corretos agora
        if not versoes_file.exists():
            self.stdout.write(self.style.ERROR(f'[ERRO] Arquivo nao encontrado: {versoes_file}'))
            return
        
        self.stdout.write(f'\nVerificando versoes em: {versoes_file.name}')
        with open(versoes_file, 'r', encoding='utf-8') as f:
            versoes_data = json.load(f)
        
        # Criar conjunto de IDs de modelos válidos
        modelos_ids_validos = {m['pk'] for m in modelos_data}
        
        versoes_corrigidas = 0
        versoes_nao_encontradas = []
        
        for versao in versoes_data:
            modelo_id = versao['fields']['modelo']
            
            # Verificar se o modelo_id existe no modelos.json corrigido
            if modelo_id in modelos_ids_validos:
                versoes_corrigidas += 1
            else:
                # Tentar encontrar pelo banco
                try:
                    from carros.models import VersaoVeiculo
                    versao_obj = VersaoVeiculo.objects.filter(id=versao['pk']).first()
                    if versao_obj:
                        novo_modelo_id = versao_obj.modelo.id
                        # Verificar se esse ID existe no modelos.json
                        if novo_modelo_id in modelos_ids_validos:
                            versao['fields']['modelo'] = novo_modelo_id
                            versoes_corrigidas += 1
                        else:
                            versoes_nao_encontradas.append(f"Versao {versao['pk']}: modelo {novo_modelo_id} nao encontrado em modelos.json")
                    else:
                        versoes_nao_encontradas.append(f"Versao {versao['pk']}: modelo {modelo_id} nao encontrado")
                except Exception as e:
                    versoes_nao_encontradas.append(f"Versao {versao['pk']}: erro - {str(e)}")
        
        # Salvar versoes.json corrigido
        with open(versoes_file, 'w', encoding='utf-8') as f:
            json.dump(versoes_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {versoes_corrigidas} versao(oes) verificada(s)'))
        if versoes_nao_encontradas:
            self.stdout.write(self.style.WARNING(f'[AVISO] {len(versoes_nao_encontradas)} versao(oes) com problema'))
            if len(versoes_nao_encontradas) <= 10:
                for msg in versoes_nao_encontradas:
                    self.stdout.write(self.style.WARNING(f'  - {msg}'))
        
        self.stdout.write(self.style.SUCCESS('\nCorrecao concluida!'))
        self.stdout.write(f'\nArquivos atualizados:')
        self.stdout.write(f'  - {modelos_file.name}')
        self.stdout.write(f'  - {versoes_file.name}')
