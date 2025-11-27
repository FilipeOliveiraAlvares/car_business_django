# 📦 Como Importar Modelos e Versões no Servidor (Railway)

## 📋 Sobre os Arquivos

Você tem arquivos JSON no formato **Django Fixtures**, que é o formato padrão do Django para exportar/importar dados.

### Arquivos:
- `modelos.json` - 143 modelos de veículos
- `versoes.json` - 418 versões de veículos
- `categorias_veiculos.json` - Categorias (Carro, Moto, Caminhão, SUV, etc.)

### ✅ Vantagens:
1. **Formato padrão Django** - Compatível com `loaddata`
2. **Bem estruturado** - Relacionamentos preservados (marca → modelo → versão)
3. **Fácil de importar** - Comando simples
4. **Idempotente** - Pode rodar múltiplas vezes (com tratamento de duplicatas)

---

## 🚀 Opção 1: Usando o Comando Customizado (Recomendado)

Criei um comando customizado que facilita a importação:

### No Servidor (Railway):

1. **Fazer upload dos arquivos JSON para o servidor:**
   - Via Railway CLI ou interface web
   - Ou adicionar ao repositório Git (recomendado)

2. **Acessar o terminal do Railway:**
   - No Railway, vá em seu serviço web
   - Clique em "View Logs" ou use o terminal

3. **Executar o comando:**
   ```bash
   python manage.py importar_dados
   ```

   Ou especificar arquivos customizados:
   ```bash
   python manage.py importar_dados --modelos modelos.json --versoes versoes.json
   ```

---

## 🔧 Opção 2: Usando loaddata Diretamente

### No Servidor (Railway):

```bash
# 1. Importar categorias (se necessário)
python manage.py loaddata categorias_veiculos.json

# 2. Importar modelos
python manage.py loaddata modelos.json

# 3. Importar versões
python manage.py loaddata versoes.json
```

---

## 📤 Como Fazer Upload dos Arquivos para o Servidor

### Método 1: Via Git (Recomendado) ✅

1. **Adicionar os arquivos ao Git:**
   ```bash
   git add modelos.json versoes.json categorias_veiculos.json
   git commit -m "Adicionar dados de modelos e versões"
   git push origin main
   ```

2. **Railway fará deploy automaticamente**

3. **Após o deploy, executar:**
   ```bash
   python manage.py importar_dados
   ```

### Método 2: Via Railway CLI

1. **Instalar Railway CLI:**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Fazer upload:**
   ```bash
   railway up modelos.json versoes.json categorias_veiculos.json
   ```

### Método 3: Via Terminal do Railway

1. **Acessar terminal do Railway**
2. **Usar `scp` ou similar para upload** (mais complexo)

---

## ⚙️ Configuração no Railway

### Adicionar ao Pre-deploy Command (Opcional):

Se quiser importar automaticamente a cada deploy:

```
python manage.py migrate && python manage.py importar_dados && python manage.py collectstatic --noinput
```

**⚠️ ATENÇÃO:** Isso pode causar duplicatas se rodar múltiplas vezes. Use apenas se necessário.

---

## 🔍 Verificar se Funcionou

Após importar, verifique:

```bash
# Contar modelos
python manage.py shell
>>> from carros.models import ModeloVeiculo
>>> ModeloVeiculo.objects.count()
# Deve retornar 143

# Contar versões
>>> from carros.models import VersaoVeiculo
>>> VersaoVeiculo.objects.count()
# Deve retornar 418
```

---

## ⚠️ Tratamento de Duplicatas

Se alguns registros já existirem, você verá erros de `UNIQUE constraint`. 

**Soluções:**

1. **Limpar dados existentes primeiro:**
   ```bash
   python manage.py shell
   >>> from carros.models import ModeloVeiculo, VersaoVeiculo
   >>> ModeloVeiculo.objects.all().delete()
   >>> VersaoVeiculo.objects.all().delete()
   ```

2. **Ou usar o comando com tratamento de erros** (já implementado no comando customizado)

---

## 📝 Exemplo Completo

```bash
# 1. No servidor Railway, após deploy
python manage.py migrate

# 2. Importar dados
python manage.py importar_dados

# 3. Verificar
python manage.py shell
>>> from carros.models import ModeloVeiculo, VersaoVeiculo
>>> print(f"Modelos: {ModeloVeiculo.objects.count()}")
>>> print(f"Versões: {VersaoVeiculo.objects.count()}")
```

---

## 🎯 Recomendações

1. **Adicionar ao Git** - Facilita versionamento e deploy
2. **Usar o comando customizado** - Mais fácil e com tratamento de erros
3. **Fazer backup antes** - Se já tiver dados no servidor
4. **Testar localmente primeiro** - Sempre teste antes de rodar no servidor

---

## ❓ Problemas Comuns

### Erro: "No such file or directory"
- **Solução:** Verifique se os arquivos estão na raiz do projeto

### Erro: "UNIQUE constraint failed"
- **Solução:** Limpe os dados existentes ou use `--skip-existing` (se implementado)

### Erro: "Foreign key constraint failed"
- **Solução:** Certifique-se de que as marcas existem antes de importar modelos

---

**Pronto! Seus dados estarão disponíveis no servidor! 🚀**

