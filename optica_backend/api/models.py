from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    # Relación 1 a 1: Cada Usuario tiene un solo Perfil
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    imagen = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'