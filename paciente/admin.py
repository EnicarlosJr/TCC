from django.contrib import admin
from .models import Doenca, HabitosAlimentares, HistoriaSocial, Medicamento, MedicamentoDoencaPaciente, Paciente, PerfilClinico, AutonomiaMedicamentos, Saude


admin.site.register(Paciente)
admin.site.register(HistoriaSocial)
admin.site.register(HabitosAlimentares)
admin.site.register(PerfilClinico)
admin.site.register(AutonomiaMedicamentos)
admin.site.register(Saude)
admin.site.register(Doenca)
admin.site.register(Medicamento)

@admin.register(MedicamentoDoencaPaciente)
class MedicamentoDoencaPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medicamento', 'doenca', 'observacao')
    list_filter = ('paciente', 'medicamento', 'doenca')
    search_fields = ('paciente__nome', 'medicamento__nome', 'doenca__nome', 'observacao')
