from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('farmaceutico', 'Farmacêutico'),
        ('aluno', 'Aluno'),
        ('convidado', 'Convidado'),
    ]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='farmaceutico',
    )

    def __str__(self):
        return self.username

User = get_user_model()

class LogAtividade(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    detalhes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_hora']
