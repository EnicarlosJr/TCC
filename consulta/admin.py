from django.contrib import admin
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao


admin.site.register(Consulta)
admin.site.register(ProblemaSaude)
admin.site.register(Medicamento)
admin.site.register(Avaliacao)
admin.site.register(PlanoAtuacao)
