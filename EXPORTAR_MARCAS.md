# 📤 Exportar Marcas do Banco Local

## 🎯 Objetivo

Extrair todas as marcas do seu banco de dados local e gerar um arquivo JSON no formato Django fixture, com opção de limpar e padronizar (remover Corvette e padronizar como Chevrolet).

---

## 🚀 Como Usar

### Opção 1: Exportar sem limpar (apenas exportar)

```bash
.\venv\Scripts\python.exe manage.py exportar_marcas
```

Isso criará o arquivo `marcas.json` na raiz do projeto.

### Opção 2: Limpar e padronizar ANTES de exportar (Recomendado)

```bash
.\venv\Scripts\python.exe manage.py exportar_marcas --limpar
```

**O que faz:**
1. ✅ Busca a marca "Chevrolet" (ou cria se não existir)
2. ✅ Busca a marca "Corvette"
3. ✅ Move todos os modelos de Corvette para Chevrolet
4. ✅ Remove a marca Corvette
5. ✅ Padroniza o nome "Chevrolet" (primeira letra maiúscula)
6. ✅ Exporta todas as marcas para `marcas.json`

### Opção 3: Especificar nome do arquivo de saída

```bash
.\venv\Scripts\python.exe manage.py exportar_marcas --output minhas_marcas.json --limpar
```

---

## 📋 Exemplo de Uso Completo

```bash
# 1. Limpar e exportar
.\venv\Scripts\python.exe manage.py exportar_marcas --limpar

# 2. Verificar o arquivo gerado
# O arquivo marcas.json será criado na raiz do projeto

# 3. (Opcional) Verificar no banco
.\venv\Scripts\python.exe manage.py shell
>>> from carros.models import Marca, ModeloVeiculo
>>> Marca.objects.filter(nome__icontains='chevrolet')
>>> Marca.objects.filter(nome__icontains='corvette')  # Não deve retornar nada
>>> ModeloVeiculo.objects.filter(marca__nome__icontains='chevrolet').count()
```

---

## 📁 Formato do Arquivo Gerado

O arquivo `marcas.json` terá o formato Django fixture:

```json
[
  {
    "model": "carros.marca",
    "pk": 1,
    "fields": {
      "nome": "Chevrolet",
      "logo": ""
    }
  },
  {
    "model": "carros.marca",
    "pk": 2,
    "fields": {
      "nome": "Toyota",
      "logo": ""
    }
  }
]
```

---

## ⚠️ Importante

1. **Backup:** Faça backup do banco antes de usar `--limpar`
2. **Teste local:** Teste primeiro em ambiente de desenvolvimento
3. **Modelos:** Todos os modelos de Corvette serão movidos para Chevrolet
4. **Irreversível:** A remoção de Corvette é permanente (mas você pode importar novamente se tiver backup)

---

## 🔄 Próximos Passos

Após exportar:

1. **Adicionar ao Git:**
   ```bash
   git add marcas.json
   git commit -m "Adicionar marcas exportadas do banco local"
   git push origin main
   ```

2. **Importar no servidor (Railway):**
   ```bash
   python manage.py loaddata marcas.json
   ```

---

## ❓ Problemas Comuns

### Erro: "Marca Chevrolet não encontrada"
- **Solução:** O comando criará automaticamente se não existir

### Erro: "UNIQUE constraint failed"
- **Solução:** Algumas marcas podem já existir. Use `--limpar` apenas uma vez

### Arquivo não gerado
- **Solução:** Verifique se há marcas no banco: `Marca.objects.count()`

---

**Pronto! Seu arquivo `marcas.json` estará pronto para uso! 🚀**

