# Deploy Completo no Railway - Guia Passo a Passo

## Passo 1: Criar Novo Projeto no Railway

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório: `car_business_django`

## Passo 2: Adicionar Banco de Dados PostgreSQL

1. No projeto Railway, clique em "+ New"
2. Selecione "Database" → "Add PostgreSQL"
3. Railway criará automaticamente a variável `DATABASE_URL`

## Passo 3: Configurar Variáveis de Ambiente

No Railway, vá em "Variables" e adicione:

```
DJANGO_SECRET_KEY=<gere-uma-chave-secreta>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seu-app.railway.app,*.railway.app
DJANGO_SESSION_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://seu-app.railway.app
```

**Para gerar SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Passo 4: Configurar Comandos de Deploy

### Settings → Deploy

**Pre-deploy Command:**
```
python manage.py migrate --noinput; python manage.py collectstatic --noinput
```

**Custom Start Command:**
```
gunicorn core.wsgi
```

## Passo 5: Criar Superusuário

Após o primeiro deploy, acesse o terminal do Railway e execute:

```bash
python manage.py createsuperuser
```

Ou configure variáveis de ambiente para criar automaticamente:
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=sua-senha-segura
```

E adicione ao Pre-deploy Command:
```
python manage.py migrate --noinput; python manage.py create_superuser_if_not_exists; python manage.py collectstatic --noinput
```

## Passo 6: Importar Dados (Marcas, Modelos, Versões)

Após o deploy, no terminal do Railway:

```bash
python manage.py importar_dados
```

**Nota:** O comando não importa categorias por padrão (já foram importadas).

## Passo 7: Verificar se Está Funcionando

1. Acesse: `https://seu-app.railway.app`
2. Verifique se o logo aparece no topo
3. Teste o admin: `https://seu-app.railway.app/admin`
4. Teste login de logista e usuário

## Troubleshooting

### Arquivos estáticos não aparecem (404)
- Verifique se o `collectstatic` foi executado nos logs
- Confirme que o Pre-deploy Command está configurado corretamente

### Erro "DisallowedHost"
- Verifique se `DJANGO_ALLOWED_HOSTS` inclui seu domínio Railway

### Erro 400 (Bad Request)
- Verifique se `CSRF_TRUSTED_ORIGINS` está configurado com `https://seu-app.railway.app`

### Banco de dados não conecta
- Verifique se o PostgreSQL foi criado
- Confirme que `DATABASE_URL` foi criada automaticamente

## Checklist Final

- [ ] Projeto criado no Railway
- [ ] PostgreSQL adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Pre-deploy Command configurado
- [ ] Custom Start Command configurado
- [ ] Primeiro deploy concluído
- [ ] Superusuário criado
- [ ] Dados importados (marcas, modelos, versões)
- [ ] Site funcionando
- [ ] Logo aparecendo
- [ ] Admin acessível

