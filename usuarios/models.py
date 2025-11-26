from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    """Perfil estendido do usuário"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name="Foto de Perfil")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    @receiver(post_save, sender=User)
    def criar_perfil(sender, instance, created, **kwargs):
        """Cria perfil automaticamente quando um usuário é criado"""
        if created:
            PerfilUsuario.objects.create(usuario=instance)
