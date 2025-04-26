from django import forms
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        exclude = ['paciente']
        fields = '__all__'
        widgets = {
            'data_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecione a data da consulta'}),
            'data_proxima_revisao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecione a data da próxima revisão'}),
            'evolucao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Descreva a evolução do paciente'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Qual o motivo da consulta?'}),
            'prescricoes_exames': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Prescrições e exames realizados'}),
        }

class ProblemaSaudeForm(forms.ModelForm):
    class Meta:
        model = ProblemaSaude
        exclude = ['consulta']
        fields = '__all__'
        widgets = {
            'inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de início do problema'}),
            'problema': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do problema de saúde'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        exclude = ['consulta']
        fields = ['nome', 'classe', 'desde', 'prescrita', 'utilizada', 'para_que_servir', 'problema_saude']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.TextInput(attrs={'class': 'form-control'}),
            'desde': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'prescrita': forms.TextInput(attrs={'class': 'form-control'}),  # Widget para o campo prescrita
            'utilizada': forms.TextInput(attrs={'class': 'form-control'}),  # Widget para o campo utilizada
            'para_que_servir': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        exclude = ['medicamento']
        fields = '__all__'
        widgets = {
            'causa_rnm': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descreva a causa do problema'}),
            'classificacao_rnm_1': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione a classificação 1'}),
            'classificacao_rnm_2': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione a classificação 2'}),
            'situacao_problema_saude': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione a situação do problema de saúde'}),
        }

class PlanoAtuacaoForm(forms.ModelForm):
    class Meta:
        model = PlanoAtuacao
        exclude = ['consulta']
        fields = '__all__'
        widgets = {
            'objetivos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Quais são os objetivos para a intervenção?'}),
            'descricao_planejamento': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descreva o planejamento da intervenção'}),
            'resultado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Resultado da intervenção'}),
            'data_intervencao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data da intervenção'}),
            'data_alcancado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de quando o objetivo foi alcançado'}),
            'registro_intervencao': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione o tipo de intervenção'}),
            'classificacao_intervencao': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione a classificação da intervenção'}),
            'prioridade': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione a prioridade'}),
        }
