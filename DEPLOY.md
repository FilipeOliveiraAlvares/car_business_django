# Deploy no Railway - Guia Completo

## Configuracao no Railway

### 1. Pre-deploy Command
```
python manage.py migrate --noinput; python manage.py restaurar_backup_inicial || true; python manage.py collectstatic --noinput
```

### 2. Custom Start Command
```
gunicorn core.wsgi
```

### 3. Variaveis de Ambiente
```
DJANGO_SECRET_KEY=<sua-chave>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seu-app.railway.app,*.railway.app
DJANGO_SESSION_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://seu-app.railway.app
```

### 4. PostgreSQL
- Criar servico PostgreSQL no Railway
- `DATABASE_URL` e criada automaticamente

## O que o backup_inicial.json contem

- 1 superusuario (admin)
- Todas as marcas (Chevrolet padronizado)
- Todos os modelos
- Todas as versoes

## Atualizar dados localmente

```bash
# 1. Fazer backup
python manage.py backup_inicial --username admin

# 2. Commitar
git add backup_inicial.json
git commit -m "Atualizar backup"
git push origin main

# 3. No proximo deploy, sera restaurado automaticamente
```

## Comandos uteis

```bash
# Restaurar backup manualmente (se necessario)
railway run python manage.py restaurar_backup_inicial
```

## Verificar se funcionou

Nos logs do Railway, procure por:
- `[OK] BACKUP RESTAURADO COM SUCESSO!` - Tudo certo
- `[AVISO] ALGUNS REGISTROS JA EXISTEM` - Normal, dados ja estavam la
