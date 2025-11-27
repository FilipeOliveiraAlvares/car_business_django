from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from functools import wraps

from garagens.models import Loja
from carros.models import Carro, FotoCarro, validar_proporcao_imagem
from carros.forms import CarroForm
from .forms import LojaForm
from .utils import is_logista


# ----------------------------------
# LOGIN E LOGOUT CUSTOMIZADOS
# ----------------------------------
@require_http_methods(["GET", "POST"])
def login_logista(request):
    """View customizada de login para logistas"""
    # Verifica se já está logado como logista
    if request.user.is_authenticated and is_logista(request.user):
        return redirect(reverse("logistas:painel"))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if is_logista(user):
                login(request, user)
                # Redireciona para a próxima página ou painel (com validação de segurança)
                next_url = request.GET.get('next')
                if next_url:
                    # Valida que o next_url é relativo e não aponta para domínios externos
                    from django.utils.http import url_has_allowed_host_and_scheme
                    if url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                        return redirect(next_url)
                return redirect(reverse("logistas:painel"))
            else:
                messages.error(request, "Esta área é apenas para logistas. Você precisa ter uma loja associada à sua conta.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, 'logistas/login.html')


@login_required
def logout_logista(request):
    """View customizada de logout para logistas"""
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect(reverse("logistas:login"))


# ----------------------------------
# PAINEL DO logistas
# ----------------------------------
@login_required
def painel(request):
    lojas = Loja.objects.filter(usuario=request.user)

    if not lojas.exists():
        return render(request, 'logistas/sem_loja.html')

    # Já traz carros e fotos em uma consulta otimizada
    for loja in lojas:
        loja.carros_com_fotos = (
            Carro.objects.filter(loja=loja)
            .select_related("marca", "modelo", "versao")
            .prefetch_related("fotos")
        )

    return render(request, 'logistas/painel.html', {"lojas": lojas})


# ----------------------------------
# ADICIONAR CARRO
# ----------------------------------
@login_required
def adicionar_carro(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id, usuario=request.user)

    # Verifica limite da loja
    if loja.carros.count() >= loja.limite_carros:
        messages.error(request, f"Sua loja atingiu o limite de {loja.limite_carros} carros.")
        return redirect(reverse("logistas:painel"))

    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            # Validação adicional: garantir que foto_principal foi enviada ao criar
            if not request.FILES.get('foto_principal'):
                form.add_error('foto_principal', 'A foto principal é obrigatória para criar um veículo.')
            else:
                # Validar fotos extras antes de salvar
                imagens = request.FILES.getlist("fotos")
                erros_fotos = []
                
                for idx, img in enumerate(imagens[:7], 1):
                    try:
                        # Valida proporção e tamanho
                        validar_proporcao_imagem(img)
                    except ValidationError as e:
                        erros_fotos.append(f"Foto {idx}: {str(e)}")
                
                if erros_fotos:
                    # Adiciona erro ao formulário para exibir
                    for erro in erros_fotos:
                        messages.error(request, erro)
                    messages.error(request, "Corrija as fotos extras antes de salvar.")
                else:
                    carro = form.save(commit=False)
                    carro.loja = loja
                    carro.save()

                    # Fotos adicionais (já validadas)
                    for img in imagens[:7]:
                        FotoCarro.objects.create(carro=carro, imagem=img)

                    messages.success(request, "Carro adicionado com sucesso!")
                    return redirect(reverse("logistas:painel"))
    else:
        form = CarroForm()

    return render(request, "logistas/adicionar_carro.html", {"form": form, "loja": loja})


# ----------------------------------
# EDITAR CARRO
# ----------------------------------
@login_required
def editar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id, loja__usuario=request.user)

    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES, instance=carro)
        if form.is_valid():
            # Validação adicional: garantir que sempre tenha foto_principal
            # Se não enviou nova foto, deve manter a existente
            nova_foto = request.FILES.get('foto_principal')
            if not nova_foto and not carro.foto_principal:
                form.add_error('foto_principal', 'A foto principal é obrigatória. Selecione uma nova foto ou mantenha a atual.')
            else:
                # Validar fotos extras antes de salvar
                imagens = request.FILES.getlist("fotos")
                erros_fotos = []
                
                # Verifica quantas fotos já existem
                fotos_existentes = carro.fotos.count()
                max_fotos = 7
                fotos_restantes = max_fotos - fotos_existentes
                
                if len(imagens) > fotos_restantes:
                    messages.error(request, f"Você pode adicionar no máximo {fotos_restantes} foto(s) extra(s). Este carro já possui {fotos_existentes} foto(s).")
                else:
                    for idx, img in enumerate(imagens, 1):
                        try:
                            # Valida proporção e tamanho
                            validar_proporcao_imagem(img)
                        except ValidationError as e:
                            erros_fotos.append(f"Foto extra {idx}: {str(e)}")
                    
                    if erros_fotos:
                        # Adiciona erro ao formulário para exibir
                        for erro in erros_fotos:
                            messages.error(request, erro)
                        messages.error(request, "Corrija as fotos extras antes de salvar. Remova as fotos inválidas ou substitua por imagens compatíveis.")
                    else:
                        form.save()
                        
                        # Adiciona fotos extras (já validadas)
                        for img in imagens:
                            FotoCarro.objects.create(carro=carro, imagem=img)
                        
                        messages.success(request, "Carro atualizado com sucesso!")
                        return redirect(reverse("logistas:painel"))
    else:
        form = CarroForm(instance=carro)

    # Calcula quantas fotos ainda podem ser adicionadas
    fotos_existentes = carro.fotos.count()
    fotos_restantes = max(0, 7 - fotos_existentes)
    
    return render(request, "logistas/editar_carro.html", {
        "form": form, 
        "carro": carro,
        "fotos_restantes": fotos_restantes
    })


# ----------------------------------
# EXCLUIR CARRO
# ----------------------------------
@login_required
def excluir_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id, loja__usuario=request.user)

    if request.method == "POST":
        carro.delete()
        messages.success(request, "Carro excluído com sucesso!")
        return redirect(reverse("logistas:painel"))

    return render(request, "logistas/confirmar_exclusao.html", {"carro": carro})


# ----------------------------------
# ADICIONAR FOTOS
# ----------------------------------
@login_required
def adicionar_fotos(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id, loja__usuario=request.user)

    max_fotos = 7
    existentes = carro.fotos.count()
    restantes = max_fotos - existentes

    if request.method == 'POST':
        imagens = request.FILES.getlist("fotos")

        if restantes <= 0:
            messages.error(request, "Este carro já possui o máximo de 7 fotos.")
        else:
            adicionadas = 0
            erros_fotos = []
            
            for idx, img in enumerate(imagens[:restantes], 1):
                try:
                    # Valida proporção e tamanho antes de salvar
                    validar_proporcao_imagem(img)
                    FotoCarro.objects.create(carro=carro, imagem=img)
                    adicionadas += 1
                except ValidationError as e:
                    erros_fotos.append(f"Foto {idx}: {str(e)}")
            
            if erros_fotos:
                for erro in erros_fotos:
                    messages.error(request, erro)
                if adicionadas > 0:
                    messages.warning(request, f"{adicionadas} foto(s) adicionada(s), mas algumas foram rejeitadas.")
            elif adicionadas > 0:
                messages.success(request, f"{adicionadas} foto(s) adicionada(s) com sucesso!")
            else:
                messages.warning(request, "Nenhuma foto válida foi adicionada.")
        
        return redirect(reverse("logistas:painel"))

    return render(
        request,
        "logistas/adicionar_fotos.html",
        {"carro": carro, "fotos_restantes": restantes},
    )


# ----------------------------------
# EXCLUIR FOTO
# ----------------------------------
@login_required
def excluir_foto(request, foto_id):
    foto = get_object_or_404(
        FotoCarro,
        id=foto_id,
        carro__loja__usuario=request.user,
    )

    carro = foto.carro
    foto.delete()
    messages.success(request, "Foto excluída.")

    if request.GET.get("from") == "painel":
        return redirect(reverse("logistas:painel"))

    # Usa o nome da URL em vez de caminho hardcoded para evitar erros de rota
    return redirect(reverse("logistas:editar_carro", args=[carro.id]))


# ----------------------------------
# EDITAR LOJA
# ----------------------------------
@login_required
def editar_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id, usuario=request.user)

    if request.method == "POST":
        form = LojaForm(request.POST, request.FILES, instance=loja)
        
        # Debug: verificar se o formulário recebeu dados
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"POST data: {request.POST}")
        logger.info(f"FILES data: {request.FILES}")
        logger.info(f"Form is_valid: {form.is_valid()}")
        
        if form.is_valid():
            try:
                # Garantir que MEDIA_ROOT existe antes de salvar
                from django.conf import settings
                import os
                if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
                    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'logos'), exist_ok=True)
                
                loja_salva = form.save()
                logger.info(f"Loja {loja_id} salva com sucesso: {loja_salva.nome}")
                messages.success(request, "Loja atualizada com sucesso!")
                return redirect(reverse("logistas:painel"))
            except Exception as e:
                error_msg = f"Erro ao salvar loja: {str(e)}"
                logger.error(f"Erro ao salvar loja {loja_id}: {str(e)}", exc_info=True)
                messages.error(request, error_msg)
        else:
            # Mostrar erros do formulário
            logger.warning(f"Formulário inválido. Erros: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LojaForm(instance=loja)

    return render(request, "logistas/editar_loja.html", {"form": form, "loja": loja})
