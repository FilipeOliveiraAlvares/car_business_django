"""
Template tags para verificar se usuário é logista
"""
from django import template
from logistas.utils import is_logista as check_is_logista

register = template.Library()


@register.filter
def is_logista(user):
    """
    Template filter para verificar se um usuário é logista.
    Uso: {% if user|is_logista %}
    """
    return check_is_logista(user)

