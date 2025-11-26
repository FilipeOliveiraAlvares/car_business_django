from django.db import models
from django.contrib.auth.models import User

class Cidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.estado}"


class Loja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    # NOVOS CAMPOS
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)
    maps_url = models.URLField(blank=True, null=True)

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lojas')
    limite_carros = models.PositiveIntegerField(default=10)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True, related_name='lojas')

    def __str__(self):
        return self.nome
