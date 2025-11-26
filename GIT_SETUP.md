# 📦 Guia Rápido: Conectar ao GitHub

## ✅ Commit Local Realizado!

Seu código já foi commitado localmente. Agora você precisa:

## Passo 1: Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito → **"New repository"**
3. Preencha:
   - **Repository name:** `sistema-carros` (ou o nome que preferir)
   - **Description:** "Sistema de gerenciamento de carros"
   - **Visibility:** Escolha **Public** ou **Private**
   - **NÃO marque** "Initialize with README" (já temos arquivos)
4. Clique em **"Create repository"**

## Passo 2: Conectar ao Repositório Remoto

Após criar o repositório, o GitHub mostrará comandos. Use estes comandos:

### Se você escolheu HTTPS:
```bash
git remote add origin https://github.com/SEU-USUARIO/sistema-carros.git
git branch -M main
git push -u origin main
```

### Se você escolheu SSH:
```bash
git remote add origin git@github.com:SEU-USUARIO/sistema-carros.git
git branch -M main
git push -u origin main
```

**Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub!**

## Passo 3: Autenticação

Se usar HTTPS, o GitHub pode pedir:
- **Username:** Seu usuário do GitHub
- **Password:** Use um **Personal Access Token** (não sua senha)

### Como criar um Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clique em **"Generate new token"**
3. Dê um nome (ex: "sistema-carros")
4. Selecione escopo: **`repo`** (acesso completo aos repositórios)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só verá uma vez!)
7. Use esse token como senha quando o Git pedir

## ✅ Pronto!

Após o push, seu código estará no GitHub e você poderá:
- Fazer deploy no Railway/Render conectando ao repositório
- Compartilhar o código
- Fazer backup na nuvem

---

## 🔄 Comandos Úteis para o Futuro

```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push

# Ver histórico
git log --oneline
```

