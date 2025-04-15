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
    consulta = models.ForeignKey(Consulta, related_name='problemas_saude', on_delete=models.CASCADE)
    problema = models.CharField(max_length=255)
    inicio = models.DateField()
    controlado = models.BooleanField(default=False)
    preocupa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.problema} em {self.consulta.data_consulta}"


class Medicamento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='medicamentos', null=True, blank=True)
    problema_saude = models.ForeignKey(ProblemaSaude, on_delete=models.CASCADE, related_name='medicamentos', null=True, blank=True)
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)
    desde = models.DateField()
    prescrita = models.BooleanField(default=False)
    utilizada = models.BooleanField(default=False)
    para_que_servir = models.TextField()

    def __str__(self):
        return f"{self.nome} - {self.classe}"


class Avaliacao(models.Model):
    medicamento = models.OneToOneField(Medicamento, on_delete=models.CASCADE, related_name='avaliacao', null=True, blank=True)

    CLASSIFICACAO_RNM_1_CHOICES = [
        ("PSNT", "Problema de saúde não tratado"),
        ("EMD", "Efeito de medicamento desnecessário"),
        ("INQ", "Inefetividade não quantitativa"),
        ("IQ", "Inefetividade quantitativa"),
        ("ISQ", "Insegurança quantitativa"),
    ]

    CLASSIFICACAO_RNM_2_CHOICES = CLASSIFICACAO_RNM_1_CHOICES + [("NC", "Não consta")]

    SITUACAO_PROBLEMA_SAUDE_CHOICES = [
        ("PM", "Problema manifestado"),
        ("RA", "Risco de aparecimento"),
    ]

    necessidade = models.BooleanField(default=False)
    efetividade = models.BooleanField(default=False)
    seguranca = models.BooleanField(default=False)
    classificacao_rnm_1 = models.CharField(max_length=50, choices=CLASSIFICACAO_RNM_1_CHOICES)
    classificacao_rnm_2 = models.CharField(max_length=50, choices=CLASSIFICACAO_RNM_2_CHOICES)
    situacao_problema_saude = models.CharField(max_length=50, choices=SITUACAO_PROBLEMA_SAUDE_CHOICES)
    causa_rnm = models.TextField()

    def __str__(self):
        return f"Avaliação de {self.medicamento.nome}" if self.medicamento else "Avaliação sem medicamento"


class PlanoAtuacao(models.Model):
    PRIORIDADE_CHOICES = [
        ("baixa", "Baixa"),
        ("media", "Média"),
        ("alta", "Alta"),
    ]

    REGISTRO_INTERVENCAO_CHOICES = [
        ("quantidade_medicamento", "Intervir na quantidade de medicamento"),
        ("estrategia_farmacologica", "Intervir na estratégia farmacológica"),
        ("educacao_paciente", "Intervir na educação do paciente"),
    ]

    CLASSIFICACAO_INTERVENCAO_CHOICES = [
        ("modificar_dose", "Modificar a dose"),
        ("modificar_dosagem", "Modificar a dosagem"),
        ("modificar_esquema", "Modificar o esquema terapêutico"),
        ("adicionar_medicamento", "Adicionar medicamento"),
        ("retirar_medicamento", "Retirar medicamento"),
        ("substituir_medicamento", "Substituir medicamento"),
        ("modo_uso", "Modo de uso e administração"),
        ("aumentar_adesao", "Aumentar a adesão ao tratamento"),
        ("educar_nao_farmacologico", "Educar em medidas não farmacológicas"),
        ("nao_claro", "Não está claro"),
    ]

    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='planos_de_atuacao')
    objetivos = models.TextField()
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES)
    registro_intervencao = models.CharField(max_length=50, choices=REGISTRO_INTERVENCAO_CHOICES)
    classificacao_intervencao = models.CharField(max_length=50, choices=CLASSIFICACAO_INTERVENCAO_CHOICES)
    descricao_planejamento = models.TextField(null=True, blank=True)
    data_intervencao = models.DateField()
    alcancado = models.BooleanField(default=False)
    data_alcancado = models.DateField(null=True, blank=True)
    resultado = models.TextField(blank=True)
    rnm_resolvido = models.BooleanField(default=False)
    o_que_aconteceu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Plano de Ação para consulta em {self.consulta.data_consulta}"
