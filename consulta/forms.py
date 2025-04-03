# consulta/forms.py
from django import forms
from consulta.models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['data_consulta', 'evolucao', 'motivo_consulta', 'prescricoes_exames', 'data_proxima_revisao']
        widgets = {
            'data_consulta': forms.DateInput(attrs={'type': 'date'}),
            'evolucao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva a evolução...'}),
            'motivo_consulta': forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Motivo da consulta'}),
            'prescricoes_exames': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Prescrições e exames...'}),
            'data_proxima_revisao': forms.DateInput(attrs={'type': 'date'}),
        }


class ProblemaSaudeForm(forms.ModelForm):
    class Meta:
        model = ProblemaSaude
        fields = ['problema', 'inicio', 'controlado', 'preocupa']
        widgets = {
            'problema': forms.TextInput(attrs={'placeholder': 'Descreva o problema de saúde'}),
            'inicio': forms.DateInput(attrs={'type': 'date'}),
            'controlado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preocupa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'classe', 'desde', 'prescrita', 'utilizada', 'para_que_servir']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do medicamento'}),
            'classe': forms.TextInput(attrs={'placeholder': 'Classe do medicamento'}),
            'desde': forms.DateInput(attrs={'type': 'date'}),
            'prescrita': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'utilizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'para_que_servir': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Para que serve o medicamento...'}),
        }



class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['n', 'e', 's', 'classificacao_rnm_1', 'classificacao_rnm_2', 'situacao_problema_saude', 'causa_rnm']
        widgets = {
            'n': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'e': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            's': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'classificacao_rnm_1': forms.TextInput(attrs={'placeholder': 'Classificação RNM 1'}),
            'classificacao_rnm_2': forms.TextInput(attrs={'placeholder': 'Classificação RNM 2'}),
            'situacao_problema_saude': forms.TextInput(attrs={'placeholder': 'Situação do problema de saúde'}),
            'causa_rnm': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Causa RNM'}),
        }


class PlanoAtuacaoForm(forms.ModelForm):
    class Meta:
        model = PlanoAtuacao
        fields = ['objetivos', 'prioridade', 'registro_intervencao', 'classificacao_intervencao', 'descricao_planejamento', 'data_intervencao', 'alcançado', 'data_alcancado', 'resultado', 'rnm_resolvido', 'o_que_aconteceu']
        widgets = {
            'objetivos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Objetivos do plano de atuação...'}),
            'prioridade': forms.TextInput(attrs={'placeholder': 'Prioridade'}),
            'registro_intervencao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Registro da intervenção...'}),
            'classificacao_intervencao': forms.TextInput(attrs={'placeholder': 'Classificação da intervenção'}),
            'descricao_planejamento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição do planejamento...'}),
            'data_intervencao': forms.DateInput(attrs={'type': 'date'}),
            'alcançado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_alcancado': forms.DateInput(attrs={'type': 'date'}),
            'resultado': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Resultado...'}),
            'rnm_resolvido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'o_que_aconteceu': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que aconteceu com o problema de saúde...'}),
        }
