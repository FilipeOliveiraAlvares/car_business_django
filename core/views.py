from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings
import os
import mimetypes


def handler404(request, exception):
    """
    View personalizada para erro 404 (página não encontrada)
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    View personalizada para erro 500 (erro interno do servidor)
    """
    return render(request, '500.html', status=500)


def serve_media(request, path):
    """
    Serve arquivos MEDIA em produção.
    Necessário porque o WhiteNoise não serve MEDIA por padrão.
    """
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Verifica se o arquivo está dentro do MEDIA_ROOT (segurança)
    if not os.path.abspath(file_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("Arquivo não encontrado")
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Detecta o tipo MIME do arquivo
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        return FileResponse(
            open(file_path, 'rb'),
            content_type=content_type
        )
    else:
        raise Http404("Arquivo não encontrado")

