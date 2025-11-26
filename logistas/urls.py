from django.urls import path
from . import views

app_name = "logistas"

urlpatterns = [
    path('', views.painel, name='painel'),
    
    # LOGIN E LOGOUT (customizados para manter sessão)
    path('login/', views.login_logista, name='login'),
    path('logout/', views.logout_logista, name='logout'),

    # LOJA
    path('editar-loja/<int:loja_id>/', views.editar_loja, name='editar_loja'),

    # CARROS
    path('adicionar-carro/<int:loja_id>/', views.adicionar_carro, name='adicionar_carro'),
    path('editar-carro/<int:carro_id>/', views.editar_carro, name='editar_carro'),
    path('excluir-carro/<int:carro_id>/', views.excluir_carro, name='excluir_carro'),

    # FOTOS
    path('carro/<int:carro_id>/adicionar-fotos/', views.adicionar_fotos, name='adicionar_fotos'),
    path('foto/<int:foto_id>/excluir/', views.excluir_foto, name='excluir_foto'),
]
