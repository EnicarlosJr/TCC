from django.db import models
from django.forms import ValidationError
from paciente.models import Paciente

# Modelo principal de Consulta
from django.db import models

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    data_consulta = models.DateField()
    evolucao = models.TextField()
    motivo_consulta = models.TextField(max_length=255)
    prescricoes_exames = models.TextField()
    data_proxima_revisao = models.DateField(null=True, blank=True)
    exames_arquivo = models.FileField(
        upload_to='exames_consulta/',
        blank=True,
        null=True,
        verbose_name='Arquivo de Exames (PDF, JPG, PNG, DOC etc.)'
    )

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_consulta}"


# Registro de problemas de saúde levantados durante a consulta
class ProblemaSaude(models.Model):
    TEMPO_INICIO_CHOICES = [
        ("<1M", "Menos de 1 mês"),
        ("1-3M", "De 1 a 3 meses"),
        ("3-6M", "De 3 a 6 meses"),
        ("6M-1A", "De 6 meses a 1 ano"),
        ("1-3A", "De 1 a 3 anos"),
        ("3-5A", "De 3 a 5 anos"),
        ("5-10A", "De 5 a 10 anos"),
        (">10A", "Mais de 10 anos"),
    ]

    consulta = models.ForeignKey(Consulta, related_name='problemas_saude', on_delete=models.CASCADE)
    problema = models.CharField(max_length=255)
    inicio = models.CharField(max_length=10, choices=TEMPO_INICIO_CHOICES)
    controlado = models.BooleanField(default=False)
    preocupa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.problema} ({self.get_inicio_display()}) em {self.consulta.data_consulta}"


# Medicamentos relacionados a uma consulta e problema de saúde
class Medicamento(models.Model):
    DESDE_CHOICES = [
        ("<1M", "Menos de 1 mês"),
        ("1-3M", "De 1 a 3 meses"),
        ("3-6M", "De 3 a 6 meses"),
        ("6M-1A", "De 6 meses a 1 ano"),
        ("1-3A", "De 1 a 3 anos"),
        ("3-5A", "De 3 a 5 anos"),
        ("5-10A", "De 5 a 10 anos"),
        (">10A", "Mais de 10 anos"),
    ]
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='medicamentos', null=True, blank=True)
    problema_saude = models.ForeignKey(ProblemaSaude, on_delete=models.CASCADE, related_name='medicamentos', null=True, blank=True)
    
    nome = models.CharField(max_length=255, blank=True)
    classe = models.CharField(max_length=255, blank=True)
    
    desde = models.CharField(max_length=10, choices=DESDE_CHOICES, blank=True)
    posologia_prescrita = models.CharField(max_length=255, blank=True, null=True)
    posologia_utilizada = models.CharField(max_length=255, blank=True, null=True)
    entendimento_paciente = models.TextField(blank=True, null=True)

    def __str__(self):
        nome = self.nome if self.nome else 'N/A'
        classe = self.classe if self.classe else 'N/A'
        return f"{nome} - {classe}"

# Avaliação clínica de medicamentos usados na consulta
class Avaliacao(models.Model):
    medicamento = models.OneToOneField(
        Medicamento, on_delete=models.CASCADE,
        related_name='avaliacao', null=True, blank=True
    )

    CLASSIFICACAO_RNM_1_CHOICES = [
        ("PSNT", "Problema de saúde não tratado"),
        ("EMD", "Efeito de medicamento desnecessário"),
        ("INQ", "Inefetividade não quantitativa"),
        ("IQ", "Inefetividade quantitativa"),
        ("ISQ", "Insegurança quantitativa"),
        ("NC", "Não consta"),
    ]

    CLASSIFICACAO_RNM_2_CHOICES = CLASSIFICACAO_RNM_1_CHOICES

    SITUACAO_PROBLEMA_SAUDE_CHOICES = [
        ("PM", "Problema manifestado"),
        ("RA", "Risco de aparecimento"),
        ("NC", "Não consta"),
    ]

    necessidade = models.BooleanField(null=True, blank=True)
    efetividade = models.BooleanField(null=True, blank=True)
    seguranca = models.BooleanField(null=True, blank=True)


    classificacao_rnm_1 = models.CharField(
        max_length=50, choices=CLASSIFICACAO_RNM_1_CHOICES,
        blank=True, default='NC'
    )
    classificacao_rnm_2 = models.CharField(
        max_length=50, choices=CLASSIFICACAO_RNM_2_CHOICES,
        blank=True, default='NC'
    )
    situacao_problema_saude = models.CharField(
        max_length=50, choices=SITUACAO_PROBLEMA_SAUDE_CHOICES,
        blank=True, default='NC'
    )

    causa_rnm = models.TextField(blank=True, null=True)

    PARÂMETRO_CHOICES = [
        ('SS', 'Sinais e Sintomas'),
        ('SUB', 'Subjetivo'),
        ('LAB', 'Laboratorial'),
    ]

    parametro = models.CharField(max_length=10, choices=PARÂMETRO_CHOICES, blank=True, null=True)
    resultado_do_parametro = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.medicamento and self.medicamento.nome:
            return f"Avaliação de {self.medicamento.nome}"
        return "Avaliação sem medicamento"


# Plano de ação farmacêutica baseado na avaliação da consulta
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

    # Relacionamentos
    avaliacao = models.ForeignKey('Avaliacao', on_delete=models.CASCADE, related_name='planos_atuacao', null=True, blank=True)
    consulta = models.ForeignKey('Consulta', on_delete=models.CASCADE, related_name='planos_de_atuacao')  # opcional
    problema_saude = models.ForeignKey(ProblemaSaude, on_delete=models.CASCADE, related_name='planos_atuacao', null=True, blank=True)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='planos_atuacao', null=True, blank=True)

    # Campo de relato da anamnese
    relato_anamnese = models.TextField(blank=True, null=True)

    # Etapa 1 – Planejamento da Intervenção
    objetivos = models.TextField()
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES)
    registro_intervencao = models.CharField(max_length=50, choices=REGISTRO_INTERVENCAO_CHOICES)
    classificacao_intervencao = models.CharField(max_length=50, choices=CLASSIFICACAO_INTERVENCAO_CHOICES)
    descricao_planejamento = models.TextField(null=True, blank=True)
    data_intervencao = models.DateField()

    # Etapa 2 – Acompanhamento após retorno
    alcancado = models.BooleanField(null=True, blank=True)
    data_alcancado = models.DateField(null=True, blank=True)
    resultado = models.TextField(blank=True)
    rnm_resolvido = models.BooleanField(null=True, blank=True)
    o_que_aconteceu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Plano para {self.avaliacao} - {self.classificacao_intervencao}"