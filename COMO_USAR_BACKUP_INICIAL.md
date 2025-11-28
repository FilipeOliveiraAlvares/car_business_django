# Como Usar o Backup Inicial

## Passo 1: Fazer Backup Local

No seu terminal local (com o ambiente virtual ativado):

```bash
python manage.py backup_inicial --username SEU_USUARIO_ADMIN
```

Isso cria o arquivo `backup_inicial.json` com:
- 1 superusuário (o que você especificar)
- Todas as marcas
- Todos os modelos
- Todas as versões

## Passo 2: Adicionar ao Git

```bash
git add backup_inicial.json
git commit -m "Backup inicial: superusuario, marcas, modelos e versoes"
git push origin main
```

## Passo 3: Configurar Railway

Você tem 2 opções:

### Opção A: Adicionar ao Pre-deploy (Automático - Recomendado)

No Railway, vá em **Settings** → **Deploy** e configure o **Pre-deploy Command**:

```
python manage.py migrate --noinput; python manage.py loaddata backup_inicial.json || true; python manage.py collectstatic --noinput
```

O `|| true` garante que se o backup já foi carregado (erro de UNIQUE), o deploy continua.

**Vantagem:** Restaura automaticamente a cada deploy (se necessário)

**Desvantagem:** Pode dar erro de UNIQUE se já existir (mas o `|| true` resolve)

### Opção B: Usar Railway CLI (Manual)

Após o primeiro deploy:

```bash
railway run python manage.py loaddata backup_inicial.json
```

**Vantagem:** Controle total, sem erros

**Desvantagem:** Precisa instalar Railway CLI

## Recomendação

Use a **Opção A** (Pre-deploy). O `|| true` garante que mesmo se der erro de UNIQUE (dados já existem), o deploy continua normalmente.

