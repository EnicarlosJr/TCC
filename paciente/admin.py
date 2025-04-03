from django.contrib import admin
from .models import Paciente, DoencaPaciente, MedicamentoPaciente

admin.site.register(DoencaPaciente)
admin.site.register(MedicamentoPaciente)
admin.site.register(Paciente)