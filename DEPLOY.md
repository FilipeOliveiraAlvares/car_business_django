# 🚀 Guia de Deploy - Sistema de Carros

Este guia fornece instruções detalhadas para fazer deploy do sistema em diferentes plataformas.

## 📋 Pré-requisitos

- Conta na plataforma escolhida (Railway, Render, Heroku, etc.)
- Git configurado
- Banco de dados PostgreSQL (geralmente fornecido pela plataforma)

---

## 🎯 Opção 1: Railway (Recomendado - Gratuito)

### Passo 1: Preparar o Repositório

```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparar para deploy"
git push origin main
```

### Passo 2: Criar Projeto no Railway

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório

### Passo 3: Adicionar Banco de Dados PostgreSQL

1. No projeto Railway, clique em "+ New"
2. Selecione "Database" → "Add PostgreSQL"
3. Railway criará automaticamente as variáveis de ambiente:
   - `DATABASE_URL` (conexão completa)
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

### Passo 4: Configurar Variáveis de Ambiente

No Railway, vá em "Variables" e adicione:

```
DJANGO_SECRET_KEY=<gere-uma-chave-secreta>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seu-app.railway.app,seu-dominio.com.br
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_SECURE_SSL_REDIRECT=True
```

**Para gerar uma SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Passo 5: Configurar Build e Deploy

Railway detecta automaticamente Django. Certifique-se de que:
- `Procfile` está na raiz do projeto
- `requirements.txt` está atualizado
- `runtime.txt` especifica a versão do Python

### Passo 6: Executar Migrações

No Railway, vá em "Deployments" → "View Logs" e execute:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Ou configure um comando de build no Railway:
- Settings → Build Command: `python manage.py collectstatic --noinput`
- Settings → Start Command: `gunicorn core.wsgi`

### Passo 7: Criar Superusuário

No terminal do Railway ou localmente conectado ao banco:

```bash
python manage.py createsuperuser
```

---

## 🎯 Opção 2: Render

### Passo 1: Preparar o Repositório

```bash
git add .
git commit -m "Preparar para deploy"
git push origin main
```

### Passo 2: Criar Web Service no Render

1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório

### Passo 3: Configurar Build e Start Commands

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn core.wsgi
```

### Passo 4: Adicionar Banco de Dados PostgreSQL

1. No dashboard Render, clique em "New +" → "PostgreSQL"
2. Escolha um nome e região
3. Render criará automaticamente a variável `DATABASE_URL`

### Passo 5: Configurar Variáveis de Ambiente

No seu Web Service, vá em "Environment" e adicione:

```
DJANGO_SECRET_KEY=<sua-chave-secreta>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seu-app.onrender.com,seu-dominio.com.br
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_SECURE_SSL_REDIRECT=True
```

**Importante:** Render usa `DATABASE_URL` automaticamente. Você pode precisar ajustar o `settings.py` para usar `dj-database-url`:

```bash
pip install dj-database-url
```

E no `settings.py`:
```python
import dj_database_url

# No final do arquivo, após DATABASES
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))
```

### Passo 6: Executar Migrações

No Render, vá em "Shell" e execute:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎯 Opção 3: Heroku

### Passo 1: Instalar Heroku CLI

```bash
# Windows (com Chocolatey)
choco install heroku-cli

# Ou baixe de: https://devcenter.heroku.com/articles/heroku-cli
```

### Passo 2: Login e Criar App

```bash
heroku login
heroku create seu-app-nome
```

### Passo 3: Adicionar PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Passo 4: Configurar Variáveis de Ambiente

```bash
heroku config:set DJANGO_SECRET_KEY="<sua-chave-secreta>"
heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_ALLOWED_HOSTS="seu-app.herokuapp.com,seu-dominio.com.br"
heroku config:set DJANGO_SESSION_COOKIE_SECURE=True
heroku config:set DJANGO_SECURE_SSL_REDIRECT=True
```

### Passo 5: Deploy

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

---

## 🔧 Configurações Importantes

### 1. Arquivos de Mídia (Uploads)

**Problema:** Plataformas como Railway/Render não persistem arquivos de upload.

**Soluções:**

#### Opção A: AWS S3 (Recomendado)
```bash
pip install django-storages boto3
```

No `settings.py`:
```python
INSTALLED_APPS = [
    # ... outros apps
    'storages',
]

# Configurações S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

#### Opção B: Cloudinary (Mais simples)
```bash
pip install cloudinary django-cloudinary-storage
```

#### Opção C: Volume Persistente (Railway/Render Pro)
Configure um volume persistente para a pasta `media/`.

### 2. Domínio Personalizado

1. Configure seu domínio nas variáveis de ambiente:
   ```
   DJANGO_ALLOWED_HOSTS=seu-dominio.com.br,www.seu-dominio.com.br
   ```

2. Configure DNS apontando para sua plataforma:
   - Railway: Adicione domínio em "Settings" → "Domains"
   - Render: Adicione domínio em "Settings" → "Custom Domains"
   - Heroku: `heroku domains:add seu-dominio.com.br`

### 3. SSL/HTTPS

Todas as plataformas mencionadas fornecem SSL automático. Certifique-se de:
- `DJANGO_SESSION_COOKIE_SECURE=True`
- `DJANGO_SECURE_SSL_REDIRECT=True` (se necessário)

---

## 🧪 Testes Pós-Deploy

1. **Acesse o site:** `https://seu-app.railway.app`
2. **Teste o admin:** `https://seu-app.railway.app/admin`
3. **Teste upload de imagens:** Crie um carro e faça upload de fotos
4. **Teste login:** Tanto logista quanto usuário comum
5. **Verifique arquivos estáticos:** CSS/JS devem carregar corretamente

---

## 🐛 Troubleshooting

### Erro: "DisallowedHost"
- Verifique `DJANGO_ALLOWED_HOSTS` inclui seu domínio

### Erro: "Static files not found"
- Execute `python manage.py collectstatic --noinput`
- Verifique `STATIC_ROOT` no `settings.py`

### Erro: "Database connection failed"
- Verifique variáveis de ambiente do PostgreSQL
- Certifique-se de que o banco está rodando

### Erro: "Media files not found"
- Configure armazenamento em nuvem (S3, Cloudinary) ou volume persistente

### Erro: "CSRF verification failed"
- Verifique `CSRF_COOKIE_SECURE` e `CSRF_TRUSTED_ORIGINS`

---

## 📝 Checklist Final

- [ ] `requirements.txt` atualizado
- [ ] `Procfile` criado
- [ ] `runtime.txt` especifica versão Python
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados PostgreSQL criado
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] `collectstatic` executado
- [ ] Domínio configurado (se aplicável)
- [ ] SSL/HTTPS funcionando
- [ ] Upload de mídia configurado (S3/Cloudinary)
- [ ] Testes realizados

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs da plataforma
2. Teste localmente com as mesmas variáveis de ambiente
3. Consulte a documentação da plataforma escolhida

**Boa sorte com o deploy! 🚀**

