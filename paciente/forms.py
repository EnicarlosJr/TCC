from django import forms
from .models import Paciente, Doenca, Medicamento
from django.forms import inlineformset_factory

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome', 'telefone', 'numero_formulario', 'responsavel',
            'data_nascimento', 'genero', 'estado_civil', 'bairro',
            'distrito', 'municipio', 'escolaridade', 'ocupacao',
            'raca', 'reside_com', 'observacoes'
        ]

    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

class HistoriaSocialAlcolismoForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'consome_bebida', 'tipos_bebidas', 'quantidade_ingerida',
            'frequencia_uso'
        ]

class HistoriaSocialTabagismoForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'fumante', 'tempo_parou', 'tempo_fumou',
            'pratica_atividade_fisica', 'atividades_fisicas',
            'frequencia_atividade', 'duracao_exercicio',
            'observacoes_historia_social'
        ]

class HabitosAlimentaresForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'horario_acorda', 'cafe_da_manha', 'lanche_manha',
            'almoco', 'lanche_tarde', 'jantar', 'horario_dorme',
            'ultima_refeicao', 'observacoes_habitos_alimentares'
        ]

    horario_acorda = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False  # Permitir que o campo seja vazio
    )

    horario_dorme = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False  # Permitir que o campo seja vazio
    )

class PerfilClinicoForm(forms.ModelForm):
    DOENCAS_HEREDITARIAS_CHOICES = [
        ('hipertensao', 'Hipertensão'),
        ('diabetes', 'Diabetes'),
        ('dislipidemia', 'Dislipidemia (Colesterol Alto)'),
        ('doencas_cardiacas', 'Doenças Cardíacas'),
        ('dpo', 'Doença pulmonar obstrutiva crônica (DPOC)'),
        ('asma', 'Asma'),
        ('depressao_ansiedade', 'Depressão/Ansiedade'),
        ('avc', 'AVC'),
        ('osteoartrite', 'Osteoartrite'),
        ('fibromialgia', 'Fibromialgia'),
        ('outro', 'Outro'),
    ]

    # Campos do formulário
    doencas_hereditarias = forms.MultipleChoiceField(
        choices=DOENCAS_HEREDITARIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    class Meta:
        model = Paciente
        fields = [
            'doencas_hereditarias',
            'desde_quando_conhecimento',
            'quantidade_medicamentos',
            'capacidade_atividade',
            'observacoes_importantes',
        ]
        widgets = {
            'desde_quando_conhecimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes_importantes': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

        data_conhecimento_doenca = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'}),
            required=True
        )

        ultima_visita_dentista = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'}),
            required=True
        )

class SaudeForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'incomodo',
            'informacoes_importantes',
            'ultima_visita_dentista',
            'percepcao_saude',
            'justificativa',
            'pressao_controlada',
            'observacoes'
        ]

        widgets = {
            'ultima_visita_dentista': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'informacoes_importantes': forms.Textarea(attrs={'rows': 4}),
            'justificativa': forms.Textarea(attrs={'rows': 4}),
        }

        labels = {
            'incomodo': 'O senhor(a) sente algo que lhe incomoda? (dor, queixas, angústias, sono)',
            'informacoes_importantes': 'Informações importantes: (Alergias, Quedas, Cirurgias)',
            'ultima_visita_dentista': 'Última vez que foi ao dentista',
            'percepcao_saude': 'PERCEPÇÃO GERAL DA SAÚDE (0-10)',
            'justificativa': 'Por quê?',
            'pressao_controlada': 'Pressão arterial está controlada?',
            'observacoes': 'Observações Importantes:',
        }


class DoencaPacienteForm(forms.ModelForm):
    class Meta:
        model = Doenca
        fields = ['nome']

# Corrigido inlineformset_factory para Doenca
DoencaPacienteFormSet = inlineformset_factory(
    Paciente, Doenca,
    form=DoencaPacienteForm,  # Usando o form DoencaPacienteForm
    extra=1,  # Começa com um formulário vazio
    can_delete=True
)

class MedicamentoPacienteForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome']

# Corrigido inlineformset_factory para Medicamento
MedicamentoPacienteFormSet = inlineformset_factory(
    Paciente, Medicamento,
    form=MedicamentoPacienteForm,  # Usando o form MedicamentoPacienteForm
    extra=1,  # Começa com um formulário vazio
    can_delete=True
)



class AutonomiaMedicamentosForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'assistencia_medicamento', 'dificuldade_tomar',
            'esquecimento_medicamentos', 'horario_medicamentos',
            'interrompe_quando_bem', 'interrompe_quando_mal',
            'desconforto_medicamento', 'uso_terapias_alternativas',
            'local_armazenamento', 'forma_descarte',
            'rastreamento_saude'
        ]
