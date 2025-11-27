from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from carros.models import Carro
from garagens.models import Loja


class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas"""
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'listar_carros',
            'listar_lojas',
        ]

    def location(self, item):
        return reverse(item)


class CarroSitemap(Sitemap):
    """Sitemap para páginas de carros"""
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        # Retorna apenas carros ativos/publicados
        return Carro.objects.all().select_related('marca', 'loja')

    def lastmod(self, obj):
        # Retorna None se não houver campo de data
        # Pode ser implementado quando houver campo de data no modelo
        return None

    def location(self, obj):
        from django.urls import reverse
        return reverse('detalhes_carro', args=[obj.id])


class LojaSitemap(Sitemap):
    """Sitemap para páginas de lojas"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Loja.objects.all().select_related('cidade')

    def location(self, obj):
        from django.urls import reverse
        return reverse('pagina_loja', args=[obj.id])

