from django.contrib import admin
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'data_consulta', 'motivo_consulta')
    search_fields = ('paciente__nome', 'motivo_consulta')
    list_filter = ('data_consulta',)

@admin.register(ProblemaSaude)
class ProblemaSaudeAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'problema', 'inicio', 'controlado', 'preocupa')
    search_fields = ('problema',)
    list_filter = ('controlado', 'preocupa')

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'problema_saude', 'nome', 'classe', 'desde')
    search_fields = ('nome', 'classe')
    list_filter = ('desde',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('medicamento', 'necessidade', 'efetividade', 'seguranca', 'classificacao_rnm_1')
    search_fields = ('medicamento__nome',)
    list_filter = ('necessidade', 'efetividade', 'seguranca')

@admin.register(PlanoAtuacao)
class PlanoAtuacaoAdmin(admin.ModelAdmin):
    list_display = ('avaliacao', 'medicamento', 'problema_saude', 'prioridade', 'data_intervencao', 'alcancado')
    search_fields = ('objetivos', 'descricao_planejamento')
    list_filter = ('prioridade', 'data_intervencao', 'alcancado')
