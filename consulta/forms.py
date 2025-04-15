from django import forms
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        exclude = ['paciente']
        fields = '__all__'
        widgets = {
            'data_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_proxima_revisao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'evolucao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'prescricoes_exames': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ProblemaSaudeForm(forms.ModelForm):
    class Meta:
        model = ProblemaSaude
        exclude = ['consulta']
        fields = '__all__'
        widgets = {
            'inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'problema': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        exclude = ['consulta']
        model = Medicamento
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.TextInput(attrs={'class': 'form-control'}),
            'desde': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'para_que_servir': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        exclude = ['medicamento']
        fields = '__all__'
        widgets = {
            'causa_rnm': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'classificacao_rnm_1': forms.Select(attrs={'class': 'form-select'}),
            'classificacao_rnm_2': forms.Select(attrs={'class': 'form-select'}),
            'situacao_problema_saude': forms.Select(attrs={'class': 'form-select'}),
        }

class PlanoAtuacaoForm(forms.ModelForm):
    class Meta:
        model = PlanoAtuacao
        exclude = ['consulta']
        fields = '__all__'
        widgets = {
            'objetivos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'descricao_planejamento': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'resultado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'data_intervencao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_alcancado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'registro_intervencao': forms.Select(attrs={'class': 'form-select'}),
            'classificacao_intervencao': forms.Select(attrs={'class': 'form-select'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
        }
