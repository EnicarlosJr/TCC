from datetime import timezone
from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=15)
    numero_formulario = models.CharField(max_length=10)
    responsavel = models.CharField(max_length=100)
    data_nascimento = models.DateField()  # Campo de data
    genero = models.CharField(
        max_length=15, 
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('O', 'Outro'),
            ('ND', 'Prefere não dizer')
        ]
    )
    estado_civil = models.CharField(
        max_length=20, 
        choices=[
            ('Casado(a)', 'Casado(a)'),
            ('Solteiro(a)', 'Solteiro(a)'),
            ('Separado(a)', 'Separado(a)'),
            ('Amigado(a)', 'Amigado(a)'),
            ('Nao consta', 'Não consta'),
            ('Outro', 'Outro'),
        ]
    )
    bairro = models.CharField(max_length=100)
    distrito = models.CharField(max_length=20, choices=[('Rural', 'Zona Rural'), ('Urbano', 'Zona Urbana')])
    municipio = models.CharField(max_length=100)
    escolaridade = models.CharField(
        max_length=30, 
        choices=[
            ('Analfabeto', 'Analfabeto'),
            ('Fundamental incompleto', 'Fundamental incompleto'),
            ('Fundamental completo', 'Fundamental completo'),
            ('Médio incompleto', 'Médio incompleto'),
            ('Ensino médio completo', 'Ensino médio completo'),
            ('Superior incompleto', 'Superior incompleto'),
            ('Superior completo', 'Superior completo'),
            ('Pós-graduação', 'Pós-graduação'),
            ('Nao consta', 'Não consta'),
        ]
    )
    ocupacao = models.CharField(max_length=100)
    raca = models.CharField(
        max_length=20, 
        choices=[
            ('Pardo', 'Pardo'),
            ('Preto', 'Preto'),
            ('Branco', 'Branco'),
            ('Amarelo', 'Amarelo'),
            ('Negro', 'Negro'),
            ('Outro', 'Outro'),
            ('Nao consta', 'Não consta'),
        ]
    )
    reside_com = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True)

    # Campos de História Social - Consumo Bebida
    consome_bebida = models.CharField(
        max_length=3, 
        choices=[
            ('nao', 'Não'),
            ('sim', 'Sim'),
        ]
    )
    tipos_bebidas = models.CharField(
        max_length=20, 
        choices=[
            ('fermentadas', 'Bebidas Fermentadas'),
            ('mistas', 'Bebidas Mistas'),
            ('destiladas', 'Bebidas Destiladas'),
        ], 
        blank=True
    )
    quantidade_ingerida = models.CharField(
        max_length=20, 
        choices=[
            ('1_a_3', '1 a 3 copos'),
            ('4_a_6', '4 a 6 copos'),
            ('7_a_9', '7 a 9 copos'),
            ('acima_de_10', 'Acima de 10 copos'),
            ('nao_informou', 'Não informou'),
        ], 
        blank=True
    )
    frequencia_uso = models.CharField(
        max_length=20, 
        choices=[
            ('todos_os_dias', 'Todos os dias'),
            ('todo_final_de_semana', 'Todo final de semana'),
            ('1_vez_ao_mes', '1 vez ao mês'),
            ('a_cada_3_meses', 'A cada 3 meses'),
            ('raramente', 'Raramente'),
        ], 
        blank=True
    )

    # Campos de História Social - Tabagismo
    fumante = models.CharField(
        max_length=20, 
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não'),
            ('parou', 'Fumava, mas parou'),
            ('fumante_passivo', 'Fumante passivo'),
            ('outro', 'Outro'),
        ]
    )
    tempo_parou = models.IntegerField(null=True, blank=True)  # Tempo que parou de fumar
    tempo_fumou = models.IntegerField(null=True, blank=True)  # Tempo que permaneceu fumando
    pratica_atividade_fisica = models.BooleanField(default=False)
    atividades_fisicas = models.CharField(
        max_length=20, 
        choices=[
            ('caminhar', 'Caminhar'),
            ('pedalar', 'Pedalar'),
            ('danca', 'Dança'),
            ('praticar_esportes', 'Praticar esportes'),
            ('fisioterapia', 'Fisioterapia'),
            ('outro', 'Outro'),
        ], 
        blank=True
    )
    frequencia_atividade = models.CharField(
        max_length=20, 
        choices=[
            ('todos_os_dias', 'Todos os dias'),
            ('1_vez_na_semana', '1 vez na semana'),
            ('2_3_vezes_na_semana', '2 - 3 vezes na semana'),
            ('4_6_vezes_na_semana', '4 - 6 vezes na semana'),
            ('outro', 'Outro'),
        ], 
        blank=True
    )
    duracao_exercicio = models.CharField(max_length=100, blank=True)  # Descrição da duração do exercício
    observacoes_historia_social = models.TextField(blank=True)  # Observações importantes sobre a história social

    # Campos de Hábitos Alimentares
    horario_acorda = models.TimeField(null=True, blank=True)
    cafe_da_manha = models.TextField(blank=True)
    lanche_manha = models.TextField(blank=True)
    almoco = models.TextField(blank=True)
    lanche_tarde = models.TextField(blank=True)
    jantar = models.TextField(blank=True)
    horario_dorme = models.TimeField(null=True, blank=False)  # Permite vazio
    ultima_refeicao = models.TextField(blank=True)
    observacoes_habitos_alimentares = models.TextField(blank=True)

    # Campos de Perfil Clínico
    doencas_hereditarias = models.CharField(max_length=255, blank=True)
    CAPACIDADE_CHOICES = [
        ('excelente', 'Excelente capacidade'),
        ('boa', 'Boa capacidade'),
        ('moderada', 'Capacidade moderada'),
        ('comprometimento_grave', 'Comprometimento grave da capacidade'),
        ('total_comprometimento', 'Total comprometimento de capacidade'),
    ]
    desde_quando_conhecimento = models.DateField(null=True, blank=True)  # Data em que o paciente tomou conhecimento da doença
    quantidade_medicamentos = models.PositiveIntegerField(null=True, blank=True)  # A quantidade de medicamentos de rotina
    capacidade_atividade = models.CharField(max_length=50, choices=CAPACIDADE_CHOICES, blank=True)
    observacoes_importantes = models.TextField(blank=True)

    # Problemas de saúde e queixas
    INCOMODOS_CHOICES = [
        ('dor', 'Dor'),
        ('queixas', 'Queixas'),
        ('angustias', 'Angústias'),
        ('sono', 'Sono'),
        ('outro', 'Outro'),
    ]
    incomodo = models.CharField(
        max_length=100,
        choices=INCOMODOS_CHOICES,
        verbose_name='O senhor(a) sente algo que lhe incomoda? (dor, queixas, angústias, sono)',
        blank=True,
        null=True
    )
    informacoes_importantes = models.TextField(
        verbose_name='Informações importantes: (Alergias, Quedas, Cirurgias)',
        blank=True,
        null=True
    )
    ultima_visita_dentista = models.DateField(
        verbose_name='Última vez que foi ao dentista',
        blank=True,
        null=True
    )
    percepcao_saude = models.IntegerField(
        verbose_name='PERCEPÇÃO GERAL DA SAÚDE (0-10)',
        choices=[(i, str(i)) for i in range(11)],
        blank=True,
        null=True
    )
    justificativa = models.TextField(
        verbose_name='Por quê?',
        blank=True,
        null=True
    )
    pressao_controlada = models.BooleanField(
        verbose_name='Pressão arterial está controlada?',
        default=False
    )
    observacoes = models.TextField(
        verbose_name='Observações Importantes:',
        blank=True,
        null=True
    )

    # Campos de Autonomia em Medicamentos
    assistencia_medicamento = models.CharField(max_length=50, default='', blank=True)
    dificuldade_tomar = models.CharField(max_length=50, default='', blank=True)
    esquecimento_medicamentos = models.BooleanField(default=False)
    horario_medicamentos = models.BooleanField(default=False)
    interrompe_quando_bem = models.BooleanField(default=False)
    interrompe_quando_mal = models.BooleanField(default=False)
    desconforto_medicamento = models.TextField(blank=True)
    uso_terapias_alternativas = models.CharField(max_length=50, default='', blank=True)
    local_armazenamento = models.CharField(max_length=50, default='', blank=True)
    forma_descarte = models.CharField(max_length=50, default='', blank=True)
    rastreamento_saude = models.TextField(blank=True)

    

    def __str__(self):
        return self.nome


class DoencaPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='doencas_paciente')
    nome = models.CharField(max_length=255)
    controlada = models.BooleanField(default=False)  # Se a doença está controlada ou não

    def __str__(self):
        return f"{self.nome} - {self.paciente.nome}"


class MedicamentoPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='medicamentos_paciente')
    nome = models.CharField(max_length=255)
    uso_continuo = models.BooleanField(default=True)  # Se o paciente usa continuamente ou não

    def __str__(self):
        return f"{self.nome} - {self.paciente.nome}"