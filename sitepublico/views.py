from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from carros.models import (
    Carro,
    FotoCarro,
    Marca,
    Favorito,
    ModeloVeiculo,
    VersaoVeiculo,
    CategoriaVeiculo,
    VisualizacaoCarro,
)
from garagens.models import Loja, Cidade
from logistas.utils import is_logista


# -------------------- LOGIN INTELIGENTE --------------------
def login_inteligente(request):
    """
    View que mostra página de escolha entre login de logista ou usuário.
    Se o usuário já estiver logado, redireciona para o painel apropriado.
    """
    # Se já está logado, redireciona para o painel apropriado
    if request.user.is_authenticated:
        if is_logista(request.user):
            return redirect('logistas:painel')
        else:
            return redirect('painel_usuario')
    
    # Mostra página de escolha
    return render(request, 'sitepublico/escolher_login.html')


# -------------------- HOME --------------------
def home(request):
    # Otimizado: select_related para evitar N+1 queries
    ultimos_carros = Carro.objects.select_related('marca', 'loja', 'loja__cidade').order_by("-id")[:6]
    marcas = Marca.objects.all().order_by("nome")[:10]

    return render(
        request,
        "sitepublico/home.html",
        {
            "ultimos_carros": ultimos_carros,
            "marcas": marcas,
        },
    )


# -------------------- LISTAGEM --------------------

def listar_carros(request):
    # Otimizado: select_related para evitar N+1 queries
    carros = Carro.objects.select_related('marca', 'loja', 'loja__cidade').prefetch_related('fotos')
    marcas = Marca.objects.all()
    cidades = Cidade.objects.all()

    # --- CAPTURAR FILTROS ---
    marca = request.GET.get("marca")
    cidade = request.GET.get("cidade")
    preco_min = request.GET.get("preco_min")
    preco_max = request.GET.get("preco_max")
    busca = request.GET.get("busca")
    combustivel = request.GET.get("combustivel")
    cambio = request.GET.get("cambio")
    portas = request.GET.get("portas")

    ano_min = request.GET.get("ano_min")
    ano_max = request.GET.get("ano_max")

    # --- APLICAR FILTROS (com validação de tipos) ---
    if marca:
        try:
            carros = carros.filter(marca_id=int(marca))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if cidade:
        try:
            carros = carros.filter(loja__cidade_id=int(cidade))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if preco_min:
        try:
            carros = carros.filter(preco__gte=float(preco_min))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if preco_max:
        try:
            carros = carros.filter(preco__lte=float(preco_max))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if busca:
        # Sanitiza a busca removendo caracteres perigosos
        busca = busca.strip()
        if busca:
            carros = carros.filter(nome__icontains=busca)

    if combustivel:
        carros = carros.filter(combustivel=combustivel)

    if cambio:
        carros = carros.filter(cambio=cambio)

    if portas:
        try:
            carros = carros.filter(portas=int(portas))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if ano_min:
        try:
            carros = carros.filter(ano__gte=int(ano_min))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    if ano_max:
        try:
            carros = carros.filter(ano__lte=int(ano_max))
        except (ValueError, TypeError):
            pass  # Ignora valores inválidos

    # --- LISTAS PARA O TEMPLATE ---
    combustiveis = Carro._meta.get_field("combustivel").choices
    cambios = Carro._meta.get_field("cambio").choices

    portas_opcoes = (
        Carro.objects.order_by("portas")
        .values_list("portas", flat=True)
        .distinct()
    )

    anos = (
        Carro.objects.order_by("ano")
        .values_list("ano", flat=True)
        .distinct()
    )

    return render(request, "sitepublico/listar_carros.html", {
        "carros": carros,
        "marcas": marcas,
        "cidades": cidades,
        "combustiveis": combustiveis,
        "cambios": cambios,
        "portas": portas_opcoes,
        "anos": anos,
    })
# -------------------- DETALHE --------------------



def detalhes_carro(request, carro_id):
    # Otimizado: select_related para evitar N+1 queries
    carro = get_object_or_404(
        Carro.objects.select_related('marca', 'modelo', 'versao', 'loja', 'loja__cidade'),
        id=carro_id
    )

    # contador de visualização
    carro.visualizacoes += 1
    carro.save(update_fields=['visualizacoes'])

    # Registrar visualização no histórico (apenas para usuários autenticados)
    if request.user.is_authenticated:
        # Pega o IP do usuário
        ip_address = None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Usa update_or_create para evitar duplicatas e atualizar data
        from django.utils import timezone
        VisualizacaoCarro.objects.update_or_create(
            usuario=request.user,
            carro=carro,
            defaults={'data_visualizacao': timezone.now(), 'ip_address': ip_address}
        )

    # Otimizado: já vem com prefetch_related se necessário
    fotos_extras = carro.fotos.all()

    # 🔥 Verifica se o carro já é favorito do usuário atual
    if request.user.is_authenticated:
        carro.is_favorito = Favorito.objects.filter(
            usuario=request.user,
            carro=carro
        ).exists()
    else:
        carro.is_favorito = False

    return render(request, 'sitepublico/detalhes_carro.html', {
        'carro': carro,
        'fotos_extras': fotos_extras,
    })


# -------------------- LOJA --------------------
def pagina_loja(request, loja_id):
    # Otimizado: select_related para evitar N+1 queries
    loja = get_object_or_404(Loja.objects.select_related('cidade'), id=loja_id)
    carros = Carro.objects.filter(loja=loja).select_related('marca', 'loja', 'loja__cidade').prefetch_related('fotos')

    return render(request, 'sitepublico/pagina_loja.html', {
        'loja': loja,
        'carros': carros,
    })
    
def listar_lojas(request):
    cidade_id = request.GET.get("cidade")

    lojas = Loja.objects.all()

    if cidade_id:
        lojas = lojas.filter(cidade_id=cidade_id)

    cidades = Cidade.objects.all().order_by("nome")

    return render(request, "sitepublico/listar_lojas.html", {
        "lojas": lojas,
        "cidades": cidades,
    })
    
# -------------------- FAVORITAR / DESFAVORITAR --------------------


@login_required
def favoritar(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    fav, created = Favorito.objects.get_or_create(usuario=request.user, carro=carro)

    if created:
        return JsonResponse({"favoritado": True})

    fav.delete()
    return JsonResponse({"favoritado": False})


# -------------------- LISTA DE FAVORITOS --------------------
@login_required
def favoritos(request):
    itens = Favorito.objects.filter(usuario=request.user).select_related("carro")
    return render(request, "sitepublico/favoritos.html", {"favoritos": itens})


# -------------------- HISTÓRICO DE VISUALIZAÇÕES --------------------
@login_required
def historico_visualizacoes(request):
    """Lista os carros visualizados recentemente pelo usuário"""
    from django.db.models import Max
    
    # Pega os IDs dos carros únicos visualizados, ordenados pela visualização mais recente
    visualizacoes_agrupadas = VisualizacaoCarro.objects.filter(
        usuario=request.user
    ).values('carro').annotate(
        ultima_visualizacao=Max('data_visualizacao')
    ).order_by('-ultima_visualizacao')[:50]
    
    carros_ids = [v['carro'] for v in visualizacoes_agrupadas]
    
    # Busca os carros
    carros_vistos = Carro.objects.filter(
        id__in=carros_ids
    ).select_related('marca', 'loja', 'loja__cidade')
    
    # Cria um dicionário para ordenação rápida
    carros_dict = {carro.id: carro for carro in carros_vistos}
    
    # Ordena mantendo a ordem das visualizações
    carros_ordenados = [carros_dict[cid] for cid in carros_ids if cid in carros_dict]
    
    return render(request, "sitepublico/historico_visualizacoes.html", {
        "carros": carros_ordenados,
        "total": len(carros_ordenados)
    })


@login_required
def limpar_historico(request):
    """Limpa o histórico de visualizações do usuário"""
    if request.method == "POST":
        VisualizacaoCarro.objects.filter(usuario=request.user).delete()
        from django.contrib import messages
        messages.success(request, "Histórico limpo com sucesso!")
        return redirect('historico_visualizacoes')
    return redirect('historico_visualizacoes')



def api_modelos(request, marca_id):
    modelos = ModeloVeiculo.objects.filter(marca_id=marca_id).order_by("nome")

    data = {
        "modelos": [
            {"id": m.id, "nome": m.nome}
            for m in modelos
        ]
    }

    return JsonResponse(data)


def api_versoes(request, modelo_id):
    versoes = VersaoVeiculo.objects.filter(modelo_id=modelo_id).order_by("nome")

    data = {
        "versoes": [
            {"id": v.id, "nome": v.nome}
            for v in versoes
        ]
    }

    return JsonResponse(data)



# Temporariamente desabilitado - será reativado quando houver motos, caminhões, etc.
# def categorias(request):
#     lista = CategoriaVeiculo.objects.all().order_by("nome")
#     return render(request, "sitepublico/categorias.html", {"categorias": lista})


