from django.contrib import admin
from .models import (
    Paciente, Anamnese, Doenca, Medicamento, MedicamentoDoencaPaciente,
    HistoriaSocial, HabitosAlimentares, PerfilClinico, AutonomiaMedicamentos, Saude
)

# Registro simples dos principais modelos
admin.site.register(Paciente)
admin.site.register(Anamnese)
admin.site.register(Doenca)
admin.site.register(Medicamento)
admin.site.register(HistoriaSocial)
admin.site.register(HabitosAlimentares)
admin.site.register(PerfilClinico)
admin.site.register(AutonomiaMedicamentos)
admin.site.register(Saude)


@admin.register(MedicamentoDoencaPaciente)
class MedicamentoDoencaPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'anamnese', 'medicamento', 'doenca', 'observacao')
    list_filter = ('paciente', 'anamnese', 'medicamento', 'doenca')
    search_fields = (
        'paciente__nome',
        'anamnese__paciente__nome',
        'medicamento__nome',
        'doenca__nome',
        'observacao'
    )
