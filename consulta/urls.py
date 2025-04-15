from django.urls import path
from . import views

urlpatterns = [
    # Criação e listagem de consultas por paciente
    path('consulta/criar/<int:paciente_id>/', views.create_consulta, name='create_consulta'),
    path('consulta/listar/<int:paciente_id>/', views.listar_consultas, name='listar_consultas'),

    # Detalhe da consulta
    path('consulta/<int:consulta_id>/', views.detalhe_consulta, name='detalhe_consulta'),

    # Adição de dados relacionados à consulta
    path('consulta/<int:consulta_id>/medicamento/adicionar/', views.adicionar_medicamento, name='adicionar_medicamento'),
    path('consulta/<int:consulta_id>/problema/adicionar/', views.adicionar_problema_saude, name='adicionar_problema_saude'),
    path('consulta/avaliacao/adicionar/', views.adicionar_avaliacao, name='adicionar_avaliacao'),
    path('consulta/<int:consulta_id>/plano/adicionar/', views.adicionar_plano_atuacao, name='adicionar_plano_atuacao'),
]
