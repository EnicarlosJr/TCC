from django import forms
from paciente.models import Paciente, HistoriaSocial, HabitosAlimentares, PerfilClinico, AutonomiaMedicamentos, Saude

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome', 'telefone', 'numero_formulario', 'responsavel', 'data_nascimento', 'genero',
            'estado_civil', 'bairro', 'distrito', 'municipio', 'escolaridade', 'ocupacao', 'raca',
            'reside_com', 'observacoes'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecione a data'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Observações adicionais...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class HistoriaSocialForm(forms.ModelForm):
    class Meta:
        model = HistoriaSocial
        fields = [
            'consome_bebida', 'tipos_bebidas', 'quantidade_ingerida', 'frequencia_uso', 'fumante',
            'tempo_parou', 'tempo_fumou', 'pratica_atividade_fisica', 'atividades_fisicas', 'frequencia_atividade', 'observacoes'
        ]
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Observações sobre hábitos de consumo...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class HabitosAlimentaresForm(forms.ModelForm):
    class Meta:
        model = HabitosAlimentares
        fields = [
            'horario_acorda', 'cafe_da_manha', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar',
            'horario_dorme', 'ultima_refeicao', 'observacoes'
        ]
        widgets = {
            'horario_acorda': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_dorme': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Observações sobre hábitos alimentares...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class PerfilClinicoForm(forms.ModelForm):
    class Meta:
        model = PerfilClinico
        fields = [
            'doencas_hereditarias', 'capacidade_atividade', 'quantidade_medicamentos', 'incomodo',
            'ultima_visita_dentista', 'percepcao_saude', 'observacoes'
        ]
        widgets = {
            'ultima_visita_dentista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Observações sobre o perfil clínico...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class AutonomiaMedicamentosForm(forms.ModelForm):
    class Meta:
        model = AutonomiaMedicamentos
        fields = [
            'autonomia_gestao', 'autonomia_outro',
            'dificuldade_tomar', 'dificuldade_outro',
            'esquecimentos', 'toma_no_horario',
            'interrompe_quando_bem', 'interrompe_quando_mal',
            'desconforto_medicamento', 'desconforto_outro',
            'uso_alternativos', 'uso_alternativos_outro',
            'local_guarda', 'forma_descarte', 'forma_descarte_outro',
            'pressao_arterial', 'frequencia_cardiaca', 'glicemia',
            'observacoes_importantes',
        ]

        widgets = {
            # Autonomia
            'autonomia_gestao': forms.RadioSelect(),
            'autonomia_outro': forms.TextInput(attrs={
                'placeholder': 'Quem auxilia com a medicação?',
                'class': 'form-control'
            }),

            # Dificuldade
            'dificuldade_tomar': forms.RadioSelect(),
            'dificuldade_outro': forms.TextInput(attrs={
                'placeholder': 'Descreva a dificuldade',
                'class': 'form-control'
            }),

            # Sim/Não
            'esquecimentos': forms.RadioSelect(),
            'toma_no_horario': forms.RadioSelect(),
            'interrompe_quando_bem': forms.RadioSelect(),
            'interrompe_quando_mal': forms.RadioSelect(),

            # Desconforto
            'desconforto_medicamento': forms.RadioSelect(),
            'desconforto_outro': forms.Textarea(attrs={
                'placeholder': 'Descreva o desconforto e o medicamento',
                'rows': 3,
                'class': 'form-control'
            }),

            # Uso de alternativos
            'uso_alternativos': forms.RadioSelect(),
            'uso_alternativos_outro': forms.Textarea(attrs={
                'placeholder': 'Descreva os produtos ou práticas utilizadas',
                'rows': 2,
                'class': 'form-control'
            }),

            # Guarda
            'local_guarda': forms.Select(attrs={
                'class': 'form-select'
            }),

            # Descarte
            'forma_descarte': forms.RadioSelect(),
            'forma_descarte_outro': forms.TextInput(attrs={
                'placeholder': 'Outro meio de descarte',
                'class': 'form-control'
            }),

            # Rastreamento de saúde
            'pressao_arterial': forms.TextInput(attrs={
                'placeholder': 'Ex: 12x8',
                'class': 'form-control'
            }),
            'frequencia_cardiaca': forms.TextInput(attrs={
                'placeholder': 'Ex: 70 bpm',
                'class': 'form-control'
            }),
            'glicemia': forms.TextInput(attrs={
                'placeholder': 'Ex: 100 mg/dL',
                'class': 'form-control'
            }),

            # Observações
            'observacoes_importantes': forms.Textarea(attrs={
                'placeholder': 'Digite observações relevantes',
                'rows': 3,
                'class': 'form-control'
            }),
        }

        labels = {
            'autonomia_gestao': "Autonomia na Gestão dos Medicamentos",
            'autonomia_outro': "Outro (quem auxilia)",
            'dificuldade_tomar': "Tem alguma dificuldade para tomar os medicamentos?",
            'dificuldade_outro': "Outro (qual dificuldade)",
            'esquecimentos': "Já esqueceu de tomar os medicamentos?",
            'toma_no_horario': "Toma os medicamentos no horário indicado?",
            'interrompe_quando_bem': "Quando se sente bem, deixa de tomar os medicamentos?",
            'interrompe_quando_mal': "Quando se sente mal, deixa de tomar os medicamentos?",
            'desconforto_medicamento': "Sente algum desconforto com algum medicamento?",
            'desconforto_outro': "Descreva o desconforto e o medicamento",
            'uso_alternativos': "Faz uso de chás, medicamentos caseiros ou terapias alternativas?",
            'uso_alternativos_outro': "Descreva os produtos ou práticas utilizadas",
            'local_guarda': "Onde guarda os medicamentos em casa?",
            'forma_descarte': "Como descarta os medicamentos vencidos ou fora de uso?",
            'forma_descarte_outro': "Outro (forma de descarte)",
            'pressao_arterial': "Pressão Arterial",
            'frequencia_cardiaca': "Frequência Cardíaca",
            'glicemia': "Glicemia",
            'observacoes_importantes': "Observações Importantes",
        }

    # Define campos opcionais diretamente no formulário, se o model não definir
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        opcionais = [
            'autonomia_outro', 'dificuldade_outro',
            'desconforto_outro', 'uso_alternativos_outro',
            'forma_descarte_outro',
            'pressao_arterial', 'frequencia_cardiaca', 'glicemia',
            'observacoes_importantes',
        ]

        for field in opcionais:
            self.fields[field].required = False


class SaudeForm(forms.ModelForm):
    class Meta:
        model = Saude
        fields = [
            'incomodo', 'informacoes_importantes', 'ultima_visita_dentista', 'percepcao_saude',
            'justificativa', 'pressao_controlada', 'observacoes'
        ]
        widgets = {
            'ultima_visita_dentista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'informacoes_importantes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Informações importantes sobre saúde...'}),
            'justificativa': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Justifique sua percepção de saúde...'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Observações sobre saúde...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
