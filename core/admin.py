from django.contrib import admin
from django.utils.html import format_html

# Configurações do painel
admin.site.site_header = "Car Business - Painel Administrativo"
admin.site.site_title = "Car Business Admin"
admin.site.index_title = "Bem-vindo ao painel do Car Business"

# Função para exibir o logo no cabeçalho
def custom_admin_logo():
    return format_html('<img src="/static/admin/img/logo.png" height="50" alt="Car Business Logo">')

# Substituir o header padrão
admin.site.site_header = format_html(
    '{} <br><small>Car Business - Painel Administrativo</small>',
    custom_admin_logo()
)
