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
            user_to_backup = None
            if options['username']:
                try:
                    user_to_backup = User.objects.get(username=options['username'], is_superuser=True)
                    self.stdout.write(f'Incluindo superusuario: {user_to_backup.username}')
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Superusuario "{options["username"]}" nao encontrado. '
                            'Fazendo backup sem usuario.'
                        )
                    )

            # Executar dumpdata - gerar um único array JSON válido
            import json
            from pathlib import Path
            
            # Criar lista para armazenar todos os objetos
            all_data = []
            
            # Se tiver usuário, adicionar primeiro
            if user_to_backup:
                tmp_user_file = base_dir / 'tmp_user_backup.json'
                try:
                    with open(tmp_user_file, 'w', encoding='utf-8') as tmp:
                        call_command(
                            'dumpdata',
                            'auth.user',
                            '--pks', str(user_to_backup.id),
                            '--indent', '2',
                            '--natural-foreign',
                            '--natural-primary',
                            stdout=tmp
                        )
                    # Ler o arquivo temporário
                    with open(tmp_user_file, 'r', encoding='utf-8') as tmp_read:
                        user_data = json.load(tmp_read)
                        if isinstance(user_data, list):
                            all_data.extend(user_data)
                        else:
                            all_data.append(user_data)
                finally:
                    # Remover arquivo temporário
                    if tmp_user_file.exists():
                        tmp_user_file.unlink()
            
            # Adicionar modelos
            tmp_models_file = base_dir / 'tmp_models_backup.json'
            try:
                with open(tmp_models_file, 'w', encoding='utf-8') as tmp:
                    call_command(
                        'dumpdata',
                        *models_to_backup,
                        '--indent', '2',
                        '--natural-foreign',
                        '--natural-primary',
                        stdout=tmp
                    )
                # Ler o arquivo temporário
                with open(tmp_models_file, 'r', encoding='utf-8') as tmp_read:
                    models_data = json.load(tmp_read)
                    if isinstance(models_data, list):
                        all_data.extend(models_data)
                    else:
                        all_data.append(models_data)
            finally:
                # Remover arquivo temporário
                if tmp_models_file.exists():
                    tmp_models_file.unlink()
            
            # Escrever tudo em um único array JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)

            file_size = os.path.getsize(output_file)
            file_size_kb = file_size / 1024

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[OK] Backup criado com sucesso!\n'
                    f'Arquivo: {output_file.name}\n'
                    f'Localizacao: {output_file}\n'
                    f'Tamanho: {file_size_kb:.2f} KB\n'
                    f'\nProximo passo: Adicione ao Git e configure o Railway para restaurar automaticamente.'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n[ERRO] Erro: {e}')
            )
            if os.path.exists(output_file):
                os.remove(output_file)

