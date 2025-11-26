from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entrar/', views.login_inteligente, name='login_inteligente'),
    path('carros/', views.listar_carros, name='listar_carros'),
    path('carro/<int:carro_id>/', views.detalhes_carro, name='detalhes_carro'),
    path('loja/<int:loja_id>/', views.pagina_loja, name='pagina_loja'),
    path('lojas/', views.listar_lojas, name='listar_lojas'),
      # FAVORITOS
    path("favoritar/<int:carro_id>/", views.favoritar, name="favoritar"),
    path("favoritos/", views.favoritos, name="favoritos"),
    # HISTÓRICO
    path("historico/", views.historico_visualizacoes, name="historico_visualizacoes"),
    path("historico/limpar/", views.limpar_historico, name="limpar_historico"),
    path("api/modelos/<int:marca_id>/", views.api_modelos, name="api_modelos"),
    path("api/versoes/<int:modelo_id>/", views.api_versoes, name="api_versoes"),
    # Temporariamente desabilitado - será reativado quando houver motos, caminhões, etc.
    # path("categorias/", views.categorias, name="categorias"),

]
