from django.contrib import admin
from .models import Consulta

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('data_consulta', 'motivo_consulta', 'evolucao')  

admin.site.register(Consulta, ConsultaAdmin)
