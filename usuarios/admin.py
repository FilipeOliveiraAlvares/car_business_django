from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('usuario__username', 'usuario__email', 'telefone')
    readonly_fields = ('data_criacao', 'data_atualizacao')
