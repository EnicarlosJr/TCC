from django.db import models




class Doenca(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
    
class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=15)
    responsavel = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    # Relacionamento ManyToMany entre Paciente e Doenca
    doencas = models.ManyToManyField(
        Doenca,
        through='MedicamentoDoencaPaciente',
        related_name='pacientes',
        blank=True
    )    
    # Relacionamento ManyToMany entre Paciente e Medicamento (mediado por Doenca)
    medicamentos = models.ManyToManyField(Medicamento, related_name='pacientes', blank=True)
    genero = models.CharField(
        max_length=15, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro'), ('ND', 'Prefere não dizer')]
    )
    estado_civil = models.CharField(
        max_length=20, choices=[
            ('Casado(a)', 'Casado(a)'),
            ('Solteiro(a)', 'Solteiro(a)'),
            ('Separado(a)', 'Separado(a)'),
            ('Amigado(a)', 'Amigado(a)'),
            ('Viuvo(a)', 'Viúvo(a)'),
            ('Nao consta', 'Não consta'),
            ('Outro', 'Outro'),
        ]
    )
    bairro = models.CharField(max_length=100)
    distrito = models.CharField(max_length=20, choices=[('Rural', 'Zona Rural'), ('Urbano', 'Zona Urbana')])
    municipio = models.CharField(max_length=100)
    escolaridade = models.CharField(
        max_length=30, choices=[
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
        max_length=20, choices=[
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

    def medicamentos_por_doenca(self, doenca):
        return self.medicamentos_doenca_paciente.filter(doenca=doenca)
    def __str__(self):
        return self.nome


class Anamnese(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='anamneses')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anamnese de {self.paciente.nome} em {self.data_criacao.strftime('%d/%m/%Y')}"

class MedicamentoDoencaPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="medicamentos_doenca_paciente")
    anamnese = models.ForeignKey(Anamnese, on_delete=models.CASCADE, related_name="medicamentos_doenca")
    
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True, blank=True)
    doenca = models.ForeignKey(Doenca, on_delete=models.CASCADE, null=True, blank=True)
    
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente.nome} - {self.medicamento.nome if self.medicamento else 'Sem Medicamento'} - {self.doenca.nome if self.doenca else 'Sem Doença'}"


class HistoriaSocial(models.Model):
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='historia')
    consome_bebida = models.CharField(max_length=3, choices=[('nao', 'Não'), ('sim', 'Sim')])
    tipos_bebidas = models.CharField(
        max_length=20, choices=[('fermentadas', 'Bebidas Fermentadas'), ('mistas', 'Bebidas Mistas'), ('destiladas', 'Bebidas Destiladas')], blank=True
    )
    quantidade_ingerida = models.CharField(
        max_length=20, choices=[
            ('1_a_3', '1 a 3 copos'),
            ('4_a_6', '4 a 6 copos'),
            ('7_a_9', '7 a 9 copos'),
            ('acima_de_10', 'Acima de 10 copos'),
            ('nao_informou', 'Não informou'),
        ], blank=True
    )
    frequencia_uso = models.CharField(
        max_length=20, choices=[
            ('todos_os_dias', 'Todos os dias'),
            ('todo_final_de_semana', 'Todo final de semana'),
            ('1_vez_ao_mes', '1 vez ao mês'),
            ('a_cada_3_meses', 'A cada 3 meses'),
            ('raramente', 'Raramente'),
        ], blank=True
    )
    fumante = models.CharField(
        max_length=20, choices=[
            ('sim', 'Sim'), ('nao', 'Não'), ('parou', 'Fumava, mas parou'), ('fumante_passivo', 'Fumante passivo'), ('outro', 'Outro')
        ]
    )
    TEMPO_CHOICES = [
        ("<1M", "Menos de 1 mês"),
        ("1-3M", "De 1 a 3 meses"),
        ("3-6M", "De 3 a 6 meses"),
        ("6M-1A", "De 6 meses a 1 ano"),
        ("1-3A", "De 1 a 3 anos"),
        ("3-5A", "De 3 a 5 anos"),
        ("5-10A", "De 5 a 10 anos"),
        (">10A", "Mais de 10 anos"),
    ]
    tempo_parou = models.CharField(max_length=10, choices=TEMPO_CHOICES, null=True, blank=True)
    tempo_fumou = models.CharField(max_length=10, choices=TEMPO_CHOICES, null=True, blank=True)
    pratica_atividade_fisica = models.BooleanField(default=False)
    atividades_fisicas = models.CharField(max_length=20, blank=True)
    frequencia_atividade = models.CharField(max_length=20, blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"História Social de {self.anamnese.paciente.nome}"


class HabitosAlimentares(models.Model):
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='habitos')
    horario_acorda = models.TimeField(null=True, blank=True)
    cafe_da_manha = models.TextField(blank=True)
    lanche_manha = models.TextField(blank=True)
    almoco = models.TextField(blank=True)
    lanche_tarde = models.TextField(blank=True)
    jantar = models.TextField(blank=True)
    horario_dorme = models.TimeField(null=True, blank=True)
    ultima_refeicao = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Hábitos Alimentares de {self.anamnese.paciente.nome}"


class PerfilClinico(models.Model):
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='perfil')
    capacidade_atividade = models.CharField(max_length=50, blank=True)
    incomodo = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil Clínico de {self.anamnese.paciente.nome}"

class AutonomiaMedicamentos(models.Model):
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='autonomia')
    OPCOES_AUTONOMIA = [
        ('sem_assistencia', 'Toma medicamento sem assistência'),
        ('assistencia_lembrete', 'Necessita de lembretes ou de assistência'),
        ('incapaz', 'Incapaz de tomar sozinho'),
        ('outro', 'Outro'),
    ]

    autonomia_gestao = models.CharField(
        max_length=30,
        choices=OPCOES_AUTONOMIA,
        verbose_name="Autonomia na gestão dos medicamentos",
        null=True,
        blank=True
    )
    autonomia_outro = models.CharField(
        max_length=255,
        verbose_name="Outro (quem auxilia com a medicação)",
        blank=True,
        null=True
    )

    dificuldade_tomar = models.CharField(
        max_length=10,
        choices=[('sim', 'Sim'), ('nao', 'Não'), ('outro', 'Outro')],
        verbose_name="Tem dificuldade para tomar os medicamentos?"
    )
    dificuldade_outro = models.CharField(
        max_length=255,
        verbose_name="Outro (qual dificuldade)",
        blank=True,
        null=True
    )

    esquecimentos = models.CharField(
        max_length=3,
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        verbose_name="Já esqueceu de tomar os medicamentos?",
        default='nao'
    )

    toma_no_horario = models.CharField(
        max_length=3,
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        verbose_name="Toma os medicamentos no horário indicado?",
        blank=True,
        null=True
    )

    interrompe_quando_bem = models.CharField(
        max_length=3,
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        verbose_name="Quando se sente bem, deixa de tomar?"
    )

    interrompe_quando_mal = models.CharField(
        max_length=3,
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        verbose_name="Quando se sente mal, deixa de tomar?"
    )

    desconforto_medicamento = models.CharField(
        max_length=10,
        choices=[('sim', 'Sim'), ('nao', 'Não'), ('outro', 'Outro')],
        verbose_name="Sente algum desconforto com os medicamentos?"
    )
    desconforto_outro = models.TextField(
        verbose_name="Descreva o desconforto e o medicamento",
        blank=True,
        null=True
    )

    uso_alternativos = models.CharField(
        max_length=10,
        choices=[('sim', 'Sim'), ('nao', 'Não'), ('outro', 'Outro')],
        verbose_name="Faz uso de chás ou terapias alternativas?"
    )
    uso_alternativos_outro = models.TextField(
        verbose_name="Descreva quais",
        blank=True,
        null=True
    )

    LOCAL_GUARDA = [
        ('cozinha_banheiro', 'Cozinha/Banheiro'),
        ('quarto_sala', 'Quarto/Sala'),
        ('copa', 'Copa'),
        ('gavetas', 'Em Gavetas'),
        ('caixas', 'Em Caixas'),
        ('cartelas', 'Cartelas soltas'),
        ('geladeira', 'Geladeira'),
        ('armarios', 'Armários'),
    ]
    local_guarda = models.CharField(
        max_length=30,
        choices=LOCAL_GUARDA,
        verbose_name="Onde guarda os medicamentos em casa?"
    )

    forma_descarte = models.CharField(
        max_length=30,
        choices=[
            ('lixo_comum', 'Lixo Comum'),
            ('vaso_sanitario', 'Joga no Vaso Sanitário'),
            ('queima', 'Queima'),
            ('enterra', 'Enterra no solo'),
            ('outro', 'Outro'),
        ],
        verbose_name="Como descarta os medicamentos vencidos?"
    )
    forma_descarte_outro = models.CharField(
        max_length=255,
        verbose_name="Outro (forma de descarte)",
        blank=True,
        null=True
    )

    # Rastreamento em Saúde
    pressao_arterial = models.CharField(
        max_length=15,
        verbose_name="Pressão Arterial",
        blank=True,
        null=True
    )
    frequencia_cardiaca = models.CharField(
        max_length=10,
        verbose_name="Frequência Cardíaca",
        blank=True,
        null=True
    )
    glicemia = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name="Glicemia",
    )
    observacoes_importantes = models.TextField(
        verbose_name="Observações Importantes",
        blank=True,
        null=True
    )

    def __str__(self):
        if self.paciente:
            return f"Autonomia Medicamentos - {self.anamnese.paciente.nome}"
        return "Autonomia Medicamentos - Paciente não atribuído"



class Saude(models.Model):
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='saude')
    
    # Problemas de saúde e queixas
    INCOMODOS_CHOICES = [
        ('dor', 'Dor'),
        ('queixas', 'Queixas'),
        ('angustias', 'Angústias'),
        ('sono', 'Sono'),
        ('outro', 'Outro'),
    ]
    TEMPO_CHOICES = [
        ("<1M", "Menos de 1 mês"),
        ("1-3M", "De 1 a 3 meses"),
        ("3-6M", "De 3 a 6 meses"),
        ("6M-1A", "De 6 meses a 1 ano"),
        ("1-3A", "De 1 a 3 anos"),
        ("3-5A", "De 3 a 5 anos"),
        ("5-10A", "De 5 a 10 anos"),
        (">10A", "Mais de 10 anos"),
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
    ultima_visita_dentista= models.CharField(max_length=10, choices=TEMPO_CHOICES, null=True, blank=True)
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
        default=False,
        blank=True,
        null=True
    )
    observacoes = models.TextField(
        verbose_name='Observações Importantes:',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Saúde de {self.anamnese.paciente.nome}"
    


