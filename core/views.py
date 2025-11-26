from django.shortcuts import render


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

