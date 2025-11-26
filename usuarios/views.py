from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario
from .forms import EditarPerfilForm, AlterarSenhaForm
from logistas.utils import is_logista

# ---------------- LOGIN ---------------- 
def login_usuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("password")
        user = authenticate(username=username, password=senha)

        if user:
            # 🔒 impede logista de logar na área de usuário
            if is_logista(user):
                messages.error(request, "Use o login de logista para acessar sua área.")
                return redirect('/logista/login/')
            
            login(request, user)
            return redirect('/usuario/painel/')
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html")



# ---------------- REGISTRAR ---------------- 
def registrar_usuario(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("password", "")

        # Validações
        if not username:
            messages.error(request, "O nome de usuário é obrigatório.")
        elif not senha:
            messages.error(request, "A senha é obrigatória.")
        elif len(senha) < 8:
            messages.error(request, "A senha deve ter no mínimo 8 caracteres.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Esse nome de usuário já existe.")
        elif email and User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
        else:
            try:
                user = User.objects.create_user(username=username, email=email if email else None, password=senha)
                messages.success(request, "Conta criada com sucesso! Faça login.")
                return redirect('login_usuario')
            except Exception as e:
                messages.error(request, f"Erro ao criar conta: {str(e)}")

    return render(request, "usuarios/registrar.html")


# ---------------- PAINEL ---------------- 
@login_required
def painel_usuario(request):
    from carros.models import Favorito, VisualizacaoCarro
    favoritos_count = Favorito.objects.filter(usuario=request.user).count()
    historico_count = VisualizacaoCarro.objects.filter(usuario=request.user).values('carro').distinct().count()
    return render(request, "usuarios/painel.html", {
        "favoritos_count": favoritos_count,
        "historico_count": historico_count
    })


# ---------------- EDITAR PERFIL ---------------- 
@login_required
def editar_perfil(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('painel_usuario')
        # Se houver erro, o formulário será renderizado novamente com os erros
        # O JavaScript manterá o preview da foto usando sessionStorage
        # Mensagens de erro aparecerão nesta página
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user)
    
    return render(request, "usuarios/editar_perfil.html", {"form": form, "perfil": perfil})


# ---------------- ALTERAR SENHA ---------------- 
@login_required
def alterar_senha(request):
    if request.method == "POST":
        form = AlterarSenhaForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('painel_usuario')
    else:
        form = AlterarSenhaForm(request.user)
    
    return render(request, "usuarios/alterar_senha.html", {"form": form})


# ---------------- LOGOUT ---------------- 
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')
