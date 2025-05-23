from django import forms
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao
from django import forms
from .models import Consulta
from django.utils.safestring import mark_safe
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        exclude = ['paciente']
        fields = '__all__'
        widgets = {
            'data_consulta': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Selecione a data da consulta'
            }),
            'data_proxima_revisao': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Selecione a data da próxima revisão'
            }),
            'evolucao': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descreva a evolução do paciente'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Qual o motivo da consulta?'
            }),
            'prescricoes_exames': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Prescrições e exames realizados'
            }),
            'arquivo_exames': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx,.xls,.xlsx'
            }),
        }


class ProblemaSaudeForm(forms.ModelForm):
    class Meta:
        model = ProblemaSaude
        exclude = ['consulta']
        fields = '__all__'
        widgets = {
            'inicio': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione o tempo de início'
            }),
            'problema': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do problema de saúde'
            }),
            'controlado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preocupa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        exclude = ['consulta']
        fields = ['nome', 'classe', 'desde', 'posologia_prescrita', 'posologia_utilizada', 'entendimento_paciente', 'problema_saude']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.TextInput(attrs={'class': 'form-control'}),
            'desde': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione o tempo de início'
            }),            'posologia_prescrita': forms.TextInput(attrs={'class': 'form-control'}),  # Widget para o campo prescrita
            'posologia_utilizada': forms.TextInput(attrs={'class': 'form-control'}),  # Widget para o campo utilizada
            'entendimento_paciente': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'problema_saude': forms.Select(attrs={'class': 'form-control'})  # Garantindo que o campo problema_saude seja um select estilizado
        }

    def __init__(self, *args, **kwargs):


        consulta = kwargs.pop('consulta', None)  # Captura a consulta passada
        super().__init__(*args, **kwargs)
        
        if consulta:
            print("Consulta recebida:", consulta)
            print("Problemas filtrados:", ProblemaSaude.objects.filter(consulta=consulta))
            # Filtrando os problemas de saúde pela consulta
            self.fields['problema_saude'].queryset = ProblemaSaude.objects.filter(consulta=consulta)
            print(f'Problemas de saúde da consulta {consulta.id if consulta else "não disponível"}: {self.fields["problema_saude"].queryset.all()}')
        else:
            print('Nenhuma consulta associada ao formulário.')

        # Todos os campos opcionais
        for field in self.fields.values():
            field.required = False


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        exclude = ['medicamento']
        fields = '__all__'
        widgets = {
            'causa_rnm': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descreva a causa do problema'}),
            'classificacao_rnm_1': forms.Select(attrs={'class': 'form-select'}),
            'classificacao_rnm_2': forms.Select(attrs={'class': 'form-select'}),
            'situacao_problema_saude': forms.Select(attrs={'class': 'form-select'}),
            'parametro': forms.Select(attrs={'class': 'form-select'}),  # <-- NOVO
            'resultado_do_parametro': forms.Textarea(attrs={  # <-- NOVO
                'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva o resultado do parâmetro'
            }),
        }



TIPO_RELACAO_CHOICES = [
    ('problema_saude', 'Problema de Saúde'),
    ('medicamento', 'Medicamento'),
    ('avaliacao', 'Avaliação'),
    ('relato_anamnese', 'Relato de Anamnese'),
]

class PlanoAtuacaoPlanejamentoForm(forms.ModelForm):
    tipo_relacao = forms.ChoiceField(
        choices=TIPO_RELACAO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_relacao'}),
        label="Tipo de Relacionamento"
    )

    class Meta:
        model = PlanoAtuacao
        fields = [
            'tipo_relacao',
            'problema_saude',
            'medicamento',
            'avaliacao',
            'relato_anamnese',
            'objetivos',
            'prioridade',
            'registro_intervencao',
            'classificacao_intervencao',
            'descricao_planejamento',
            'data_intervencao'
        ]
        widgets = {
            'avaliacao': forms.Select(attrs={'class': 'form-select'}),
            'problema_saude': forms.Select(attrs={
                'class': 'form-select campo-relacao',
                'data-relacao': 'problema_saude',
                'id': 'campo_problema_saude'
            }),
            'medicamento': forms.Select(attrs={
                'class': 'form-select campo-relacao',
                'data-relacao': 'medicamento',
                'id': 'campo_medicamento'
            }),
            'avaliacao': forms.Select(attrs={
                'class': 'form-select campo-relacao',
                'data-relacao': 'avaliacao',
                'id': 'campo_avaliacao'
            }),
            'relato_anamnese': forms.Textarea(attrs={
                'class': 'form-control campo-relacao',
                'rows': 3,
                'placeholder': 'Informe o relato da anamnese...',
                'data-relacao': 'relato_anamnese',
                'id': 'campo_relato_anamnese'
            }),
            'objetivos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva os objetivos da intervenção...'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'registro_intervencao': forms.Select(attrs={'class': 'form-select'}),
            'classificacao_intervencao': forms.Select(attrs={'class': 'form-select'}),
            'descricao_planejamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'data_intervencao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        consulta = kwargs.pop('consulta', None)
        super().__init__(*args, **kwargs)

        if consulta:
            self.fields['problema_saude'].queryset = ProblemaSaude.objects.filter(consulta=consulta)
            self.fields['medicamento'].queryset = Medicamento.objects.filter(consulta=consulta)
            self.fields['avaliacao'].queryset = Avaliacao.objects.filter(medicamento__consulta=consulta)

        # Todos os campos opcionais
        self.fields['problema_saude'].required = False
        self.fields['medicamento'].required = False
        self.fields['avaliacao'].required = False
        self.fields['relato_anamnese'].required = False




class PlanoAtuacaoAcompanhamentoForm(forms.ModelForm):
    class Meta:
        model = PlanoAtuacao
        fields = [
            'alcancado', 'data_alcancado', 'resultado',
            'rnm_resolvido', 'o_que_aconteceu'
        ]
        widgets = {
            'alcancado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'data_alcancado': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'resultado': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descreva o resultado observado...'
            }),
            'rnm_resolvido': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'o_que_aconteceu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Explique o que ocorreu após a intervenção...'
            }),
        }
