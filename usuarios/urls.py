from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('painel/', views.painel_usuario, name='painel_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
]
