"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
import core.admin

# Importar handlers de erro personalizados
from core.views import handler404, handler500

# Importar sitemaps
from sitepublico.sitemaps import StaticViewSitemap, CarroSitemap, LojaSitemap

# Configurar handlers de erro
handler404 = handler404
handler500 = handler500

# Configurar sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'carros': CarroSitemap,
    'lojas': LojaSitemap,
}

# View para robots.txt
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /logista/",
        "Disallow: /usuario/",
        "Disallow: /favoritar/",
        "Disallow: /historico/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logista/', include('logistas.urls')),   # NOVA ROTA CORRETA    
    path('', include('sitepublico.urls')),
    path('usuario/', include('usuarios.urls')),
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]


""" codigo para aparecer a logo"""
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

