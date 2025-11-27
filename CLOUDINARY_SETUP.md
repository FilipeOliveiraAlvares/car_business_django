# Configuracao do Cloudinary para Armazenamento de MEDIA

## Por que usar Cloudinary?

No Railway (e outras plataformas similares), os arquivos de MEDIA (uploads) nao persistem porque o sistema de arquivos e efemero. A cada deploy ou reinicializacao, os arquivos sao perdidos.

O Cloudinary resolve isso armazenando os arquivos na nuvem de forma permanente.

## Passo 1: Criar conta no Cloudinary

1. Acesse: https://cloudinary.com/
2. Clique em "Sign Up for Free"
3. Crie uma conta gratuita (25GB de armazenamento gratuito)

## Passo 2: Obter credenciais

Apos criar a conta:

1. Acesse o Dashboard: https://console.cloudinary.com/
2. Na pagina inicial, voce vera suas credenciais:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

## Passo 3: Configurar no Railway

1. Acesse seu projeto no Railway
2. Vá em "Variables"
3. Adicione as seguintes variaveis de ambiente:

```
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret
```

**Importante:** Substitua pelos valores reais do seu dashboard do Cloudinary.

## Passo 4: Fazer deploy

Apos adicionar as variaveis:

1. O Railway fara deploy automaticamente
2. Ou faca deploy manual se necessario

## Como funciona

- **Desenvolvimento local:** Se as variaveis do Cloudinary nao estiverem configuradas, o sistema usa o sistema de arquivos local (como antes)
- **Producao (Railway):** Com as variaveis configuradas, todos os uploads vao para o Cloudinary automaticamente

## Testando

1. Acesse o painel admin no Railway
2. Edite uma marca ou loja
3. Faça upload de uma nova logo
4. A logo deve aparecer e persistir mesmo apos reiniciar o container

## Beneficios

- ✅ Arquivos persistem permanentemente
- ✅ 25GB gratuitos
- ✅ CDN global (imagens carregam rapido)
- ✅ Transformacoes automaticas (redimensionar, comprimir, etc)
- ✅ Backup automatico

## Nota

O Cloudinary e gratuito ate 25GB de armazenamento e 25GB de largura de banda por mes. Para a maioria dos casos, isso e mais que suficiente.

