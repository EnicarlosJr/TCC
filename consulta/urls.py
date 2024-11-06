# consulta/urls.py
from django.urls import path
from .views import adicionar_consulta, detalhe_consulta, listar_consultas

urlpatterns = [
    path('adicionar/<int:paciente_id>/', adicionar_consulta, name='adicionar_consulta'),
    path('listar/<int:paciente_id>/', listar_consultas, name='listar_consultas'),
    path('consulta/<int:consulta_id>/', detalhe_consulta, name='detalhe_consulta'), 
]
