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
import core.admin

# Importar handlers de erro personalizados
from core.views import handler404, handler500

# Configurar handlers de erro
handler404 = handler404
handler500 = handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logista/', include('logistas.urls')),   # NOVA ROTA CORRETA    
    path('', include('sitepublico.urls')),
    path('usuario/', include('usuarios.urls')),
]

# Servir arquivos MEDIA
from django.conf import settings
from django.conf.urls.static import static
from core.views import serve_media

if settings.DEBUG:
    # Em desenvolvimento, usar o método padrão do Django
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Em produção, usar view customizada para servir MEDIA
    urlpatterns += [
        path('media/<path:path>', serve_media, name='serve_media'),
    ]

