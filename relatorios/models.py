from django.db import models
from paciente.models import Paciente

class Relatorio(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_geracao = models.DateField(auto_now_add=True)
    tipo_relatorio = models.CharField(max_length=100)
    conteudo_relatorio = models.TextField()
    
    def __str__(self):
        return f'Relatório de {self.paciente.nome} - {self.tipo_relatorio}'
