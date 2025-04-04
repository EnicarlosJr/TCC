from django.contrib import admin
from .models import HabitosAlimentares, HistoriaSocial, Paciente, PerfilClinico, AutonomiaMedicamentos, Saude


admin.site.register(Paciente)
admin.site.register(HistoriaSocial)
admin.site.register(HabitosAlimentares)
admin.site.register(PerfilClinico)
admin.site.register(AutonomiaMedicamentos)
admin.site.register(Saude)
