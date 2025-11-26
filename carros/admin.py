from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Marca,
    CategoriaVeiculo,
    ModeloVeiculo,
    VersaoVeiculo,
    Carro,
    FotoCarro,
    Favorito,
    VisualizacaoCarro
)


# -----------------------------------------
#  MARCA
# -----------------------------------------
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nome", "logo_preview")
    search_fields = ("nome",)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="40"/>', obj.logo.url)
        return '—'

    logo_preview.short_description = "Logo"


# -----------------------------------------
#  CATEGORIA (Carro, Moto, Caminhão...)
# -----------------------------------------
@admin.register(CategoriaVeiculo)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


# -----------------------------------------
#  MODELO (Corolla, HB20…)
# -----------------------------------------
@admin.register(ModeloVeiculo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ("nome", "marca")
    search_fields = ("nome",)
    list_filter = ("marca",)


# -----------------------------------------
#  VERSÃO (XEI, GLI, LTZ…)
# -----------------------------------------
@admin.register(VersaoVeiculo)
class VersaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "modelo")
    search_fields = ("nome",)
    list_filter = ("modelo__marca", "modelo")


# -----------------------------------------
#  INLINE FOTOS EXTRAS (mantendo sua config)
# -----------------------------------------
class FotoCarroInline(admin.TabularInline):
    model = FotoCarro
    extra = 7
    max_num = 7
    fields = ['imagem']


# -----------------------------------------
#  CARRO — completo e com suas pré-visualizações
# -----------------------------------------
@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):

    list_display = (
        'foto_preview',
        'nome',
        'marca_logo',
        'modelo',
        'versao',
        'ano',
        'preco',
        'km',
        'combustivel',
        'cambio',
        'categoria',
        'loja',
        'destacado',
    )

    list_filter = (
        'marca',
        'modelo',
        'categoria',
        'ano',
        'combustivel',
        'cambio',
        'destacado',
        'loja',
    )

    search_fields = ('nome', 'descricao')

    inlines = [FotoCarroInline]

    # --- FOTO PRINCIPAL ---
    def foto_preview(self, obj):
        if obj.foto_principal:
            return format_html('<img src="{}" height="60"/>', obj.foto_principal.url)
        return '—'

    foto_preview.short_description = 'Foto'

    # --- LOGO DA MARCA ---
    def marca_logo(self, obj):
        if obj.marca and obj.marca.logo:
            return format_html(
                '<img src="{}" height="40" style="margin-right:8px;"> {}',
                obj.marca.logo.url,
                obj.marca.nome
            )
        return obj.marca.nome if obj.marca else '-'

    marca_logo.short_description = 'Marca'


# -----------------------------------------
#  FAVORITOS
# -----------------------------------------
@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carro", "criado_em")
    search_fields = ("usuario__username", "carro__nome")
    list_filter = ("usuario",)


# -----------------------------------------
#  HISTÓRICO DE VISUALIZAÇÕES
# -----------------------------------------
@admin.register(VisualizacaoCarro)
class VisualizacaoCarroAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carro", "data_visualizacao", "ip_address")
    list_filter = ("data_visualizacao",)
    search_fields = ("usuario__username", "carro__nome", "ip_address")
    readonly_fields = ("data_visualizacao",)
    date_hierarchy = "data_visualizacao"
