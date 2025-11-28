# Como Usar o Backup Inicial

## 📋 O que é isso?

Este sistema permite fazer backup apenas do essencial (superusuário, marcas, modelos, versões) e restaurar automaticamente no Railway após cada deploy.

## ✅ É uma boa prática?

**SIM!** É uma excelente prática porque:
- ✅ Garante que dados essenciais estejam sempre disponíveis
- ✅ Facilita novos deploys e ambientes
- ✅ Mantém consistência entre ambientes
- ✅ Arquivo pequeno (apenas o essencial)
- ✅ Versionado no Git (histórico de mudanças)

## Passo 1: Fazer Backup Local

No seu terminal local (com o ambiente virtual ativado):

```bash
python manage.py backup_inicial --username SEU_USUARIO_ADMIN
```

Isso cria o arquivo `backup_inicial.json` **na raiz do projeto** com:
- 1 superusuário (o que você especificar)
- Todas as marcas
- Todos os modelos
- Todas as versões

**Exemplo:**
```bash
python manage.py backup_inicial --username admin
```

## Passo 2: Adicionar ao Git

```bash
git add backup_inicial.json
git commit -m "Backup inicial: superusuario, marcas, modelos e versoes"
git push origin main
```

## Passo 3: Configurar Railway (Pre-deploy)

No Railway, vá em **Settings** → **Deploy** e configure o **Pre-deploy Command**:

```
python manage.py migrate --noinput; python manage.py restaurar_backup_inicial || true; python manage.py collectstatic --noinput
```

### O que acontece:

1. **`migrate`** - Aplica migrações do banco
2. **`restaurar_backup_inicial`** - Restaura o backup (com mensagens claras de sucesso)
3. **`|| true`** - Se já existir (erro UNIQUE), continua normalmente
4. **`collectstatic`** - Coleta arquivos estáticos

### Como saber se funcionou?

O comando `restaurar_backup_inicial` mostra mensagens claras:
- ✅ **"BACKUP RESTAURADO COM SUCESSO!"** - Tudo certo
- ⚠️ **"ALGUNS REGISTROS JÁ EXISTEM"** - Normal, dados já estavam lá
- ❌ **"ERRO AO RESTAURAR"** - Algo deu errado (verifique logs)

## Alternativa: Restaurar Manualmente

Se preferir restaurar manualmente (após o deploy):

```bash
railway run python manage.py restaurar_backup_inicial
```

## Atualizar o Backup

Quando adicionar novas marcas/modelos/versões localmente:

1. Refazer o backup:
```bash
python manage.py backup_inicial --username admin
```

2. Commitar e fazer push:
```bash
git add backup_inicial.json
git commit -m "Atualizar backup inicial"
git push origin main
```

3. No próximo deploy, o Railway restaurará automaticamente!

