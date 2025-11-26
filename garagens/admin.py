from django.contrib import admin
from django.utils.html import format_html
from .models import Loja, Cidade

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('logo_miniatura', 'nome', 'telefone', 'usuario', 'limite_carros', 'criado_em')
    readonly_fields = ('logo_preview',)
    search_fields = ('nome', 'telefone', 'usuario__username')
    list_filter = ('usuario',)

    def logo_miniatura(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px;" />', obj.logo.url)
        return "(Sem logo)"
    logo_miniatura.short_description = "Logo"

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.logo.url)
        return "(Sem logo)"
    logo_preview.short_description = "Prévia da Logo"
    
@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome', 'estado')


