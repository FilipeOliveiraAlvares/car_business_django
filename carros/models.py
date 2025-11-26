from django.db import models
from garagens.models import Loja
from django.core.exceptions import ValidationError
from PIL import Image
from django.contrib.auth.models import User


# -----------------------------
#  VALIDAÇÃO DE IMAGEM
# -----------------------------
def validar_proporcao_imagem(imagem):
    img = Image.open(imagem)
    largura, altura = img.size
    proporcao = largura / altura
    menor_dimensao = min(largura, altura)

    # Tamanho mínimo: 850px na menor dimensão (obrigatório)
    # Recomendado: 1200px para melhor qualidade em telas Retina e zoom
    if menor_dimensao < 850:
        raise ValidationError(
            f"A imagem deve ter no mínimo 850 pixels na menor dimensão (largura ou altura). "
            f"Sua imagem tem {largura}x{altura} pixels. "
            f"A menor dimensão é {menor_dimensao} pixels. "
            f"💡 Dica: Para melhor qualidade, recomendamos pelo menos 1200px."
        )

    # Proporção aceita: entre 1.0 (quadrada) e 2.0 (muito larga)
    # Isso cobre: 1:1 (quadrada), 4:3 (≈1.33), 16:9 (≈1.78), e até 2:1
    if proporcao < 1.0 or proporcao > 2.0:
        raise ValidationError(
            f"A proporção da imagem deve estar entre 1:1 (quadrada) e 2:1 (panorâmica). "
            f"Sua imagem tem proporção {proporcao:.2f}:1 (largura/altura). "
            f"Tamanho atual: {largura}x{altura} pixels."
        )


# -----------------------------
#  CATEGORIA (Carro/Moto/etc)
# -----------------------------
class CategoriaVeiculo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    imagem = models.ImageField(upload_to="categorias/", blank=True, null=True)

    def __str__(self):
        return self.nome


# -----------------------------
#  MARCA (Toyota, Honda, etc)
# -----------------------------
class Marca(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='marcas/', blank=True, null=True)

    def __str__(self):
        return self.nome


# -----------------------------
#  MODELO (Corolla, HB20, etc)
# -----------------------------
class ModeloVeiculo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        unique_together = ('marca', 'nome')

    def __str__(self):
        return f"{self.marca.nome} {self.nome}"


# -----------------------------
#  VERSÃO (GLI, XEI, EXL...)
# -----------------------------
class VersaoVeiculo(models.Model):
    modelo = models.ForeignKey(ModeloVeiculo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.modelo} {self.nome}"


# -----------------------------
#  VEÍCULO (antes Carro)
# -----------------------------
class Carro(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='carros')

    categoria = models.ForeignKey(CategoriaVeiculo, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.ForeignKey(ModeloVeiculo, on_delete=models.SET_NULL, null=True, blank=True)
    versao = models.ForeignKey(VersaoVeiculo, on_delete=models.SET_NULL, null=True, blank=True)

    nome = models.CharField(max_length=100)
    ano = models.IntegerField()

    km = models.PositiveIntegerField(default=0)
    cor = models.CharField(max_length=40, blank=True, null=True)
    portas = models.PositiveSmallIntegerField(default=4)

    combustivel = models.CharField(
        max_length=20,
        choices=[
            ("gasolina", "Gasolina"),
            ("etanol", "Etanol"),
            ("flex", "Flex"),
            ("diesel", "Diesel"),
            ("eletrico", "Elétrico"),
            ("hibrido", "Híbrido"),
        ],
        default="flex"
    )

    cambio = models.CharField(
        max_length=20,
        choices=[
            ("manual", "Manual"),
            ("automatico", "Automático"),
            ("cvt", "CVT"),
            ("automatizado", "Automatizado"),
        ],
        default="manual"
    )

    preco = models.DecimalField(max_digits=10, decimal_places=2)

    descricao = models.TextField(blank=True, null=True)

    foto_principal = models.ImageField(
        upload_to='carros/',
        validators=[validar_proporcao_imagem],
        blank=True, null=True
    )

    visualizacoes = models.IntegerField(default=0)

    destacado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.ano})"


# -----------------------------
#  FOTOS EXTRAS
# -----------------------------
class FotoCarro(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='carros/fotos/', validators=[validar_proporcao_imagem])

    def __str__(self):
        return f"Foto de {self.carro.nome}"


# -----------------------------
#  FAVORITOS
# -----------------------------
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'carro')

    def __str__(self):
        return f"{self.usuario} → {self.carro}"


class VisualizacaoCarro(models.Model):
    """Histórico de visualizações de carros pelos usuários"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visualizacoes', null=True, blank=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='visualizacoes_carro')
    data_visualizacao = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-data_visualizacao']
        indexes = [
            models.Index(fields=['usuario', '-data_visualizacao']),
        ]

    def __str__(self):
        usuario_nome = self.usuario.username if self.usuario else 'Anônimo'
        return f"{usuario_nome} visualizou {self.carro.nome} em {self.data_visualizacao}"
    

