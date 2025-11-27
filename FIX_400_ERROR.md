# Como Corrigir Erro 400 (Bad Request) no Railway

## Causa do Erro

O erro 400 geralmente ocorre por:
1. **CSRF_TRUSTED_ORIGINS** não configurado
2. **ALLOWED_HOSTS** não inclui o domínio do Railway

## Solução Rápida

### Passo 1: Descobrir seu domínio Railway

1. No Railway, vá em **Settings** → **Networking**
2. Copie o domínio (exemplo: `seu-app-production.up.railway.app`)

### Passo 2: Configurar Variáveis de Ambiente

No Railway, vá em **Variables** e adicione/atualize:

```
CSRF_TRUSTED_ORIGINS=https://seu-app-production.up.railway.app
```

**IMPORTANTE:** 
- Use `https://` no início
- Use o domínio EXATO do seu app (sem `www`)
- Se tiver múltiplos domínios, separe por vírgula:
  ```
  CSRF_TRUSTED_ORIGINS=https://app1.railway.app,https://app2.railway.app
  ```

### Passo 3: Verificar ALLOWED_HOSTS

Certifique-se de que `DJANGO_ALLOWED_HOSTS` inclui seu domínio:

```
DJANGO_ALLOWED_HOSTS=seu-app-production.up.railway.app,*.railway.app
```

**Formato:** Separe múltiplos hosts por vírgula, SEM espaços.

### Passo 4: Fazer Redeploy

Após adicionar as variáveis:
1. Vá em **Deployments**
2. Clique nos **3 pontos** do último deploy
3. Selecione **Redeploy**

## Exemplo Completo de Variáveis

```
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seu-app-production.up.railway.app,*.railway.app
CSRF_TRUSTED_ORIGINS=https://seu-app-production.up.railway.app
DJANGO_SESSION_COOKIE_SECURE=True
```

## Verificar se Funcionou

1. Acesse seu site: `https://seu-app-production.up.railway.app`
2. Se ainda der erro 400, verifique os logs do Railway
3. Procure por mensagens como:
   - "CSRF verification failed"
   - "Invalid HTTP_HOST header"

## Debug Adicional

Se ainda não funcionar, adicione temporariamente:

```
DJANGO_DEBUG=True
```

Isso mostrará mensagens de erro mais detalhadas. **Lembre-se de voltar para `False` depois!**

