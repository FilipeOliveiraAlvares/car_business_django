"""
Utilitários para o módulo de logistas
"""
from garagens.models import Loja


def is_logista(user):
    """
    Verifica se um usuário é logista.
    Um usuário é logista se:
    - Tem pelo menos uma loja associada, OU
    - É staff/admin
    """
    if not user or not user.is_authenticated:
        return False
    
    # Verifica se tem loja associada
    if Loja.objects.filter(usuario=user).exists():
        return True
    
    # Verifica se é staff/admin
    if user.is_staff:
        return True
    
    return False

