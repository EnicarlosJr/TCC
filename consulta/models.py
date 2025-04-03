# consulta/models.py
from django.db import models
from paciente.models import Paciente

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    data_consulta = models.DateField()
    evolucao = models.TextField()
    motivo_consulta = models.TextField(max_length=255)
    prescricoes_exames = models.TextField()
    data_proxima_revisao = models.DateField()

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_consulta}"

class ProblemaSaude(models.Model):
    consulta = models.ForeignKey('Consulta', related_name='problemas_saude', on_delete=models.CASCADE)
    problema = models.CharField(max_length=255)
    inicio = models.DateField()
    controlado = models.BooleanField(default=False)
    preocupa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.problema} em {self.consulta.data_consulta}"

class Medicamento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='medicamentos')
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)
    desde = models.DateField()
    prescrita = models.BooleanField(default=False)
    utilizada = models.BooleanField(default=False)
    para_que_servir = models.TextField()

    def __str__(self):
        return f"{self.nome} - {self.classe}"

class Avaliacao(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='avaliacoes')
    n = models.BooleanField(default=False)  # Necessidade
    e = models.BooleanField(default=False)  # Efetividade
    s = models.BooleanField(default=False)  # Segurança
    classificacao_rnm_1 = models.CharField(max_length=255)
    classificacao_rnm_2 = models.CharField(max_length=255)
    situacao_problema_saude = models.CharField(max_length=255)
    causa_rnm = models.TextField()

    def __str__(self):
        return f"Avaliação da consulta em {self.consulta.data_consulta}"

class PlanoAtuacao(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='planos_de_atuacao')
    objetivos = models.TextField()
    prioridade = models.CharField(max_length=255)
    registro_intervencao = models.TextField()
    classificacao_intervencao = models.CharField(max_length=255)
    descricao_planejamento = models.TextField()
    data_intervencao = models.DateField()
    alcançado = models.BooleanField(default=False)
    data_alcancado = models.DateField(null=True, blank=True)
    resultado = models.TextField()
    rnm_resolvido = models.BooleanField(default=False)
    o_que_aconteceu = models.TextField()

    def __str__(self):
        return f"Plano de Ação para consulta em {self.consulta.data_consulta}"
