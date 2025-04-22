# urls.py do app consulta
from django.urls import path
from . import views

urlpatterns = [
    # Criação e listagem de consultas por paciente
    path('consulta/criar/<int:paciente_id>/', views.create_consulta, name='consulta_create_consulta'),
    path('consulta/listar/<int:paciente_id>/', views.listar_consultas, name='consulta_listar_consultas'),

    # Detalhe da consulta
    path('consulta/<int:consulta_id>/', views.detalhe_consulta, name='consulta_detalhe_consulta'),

    # Adição de dados relacionados à consulta
    path('consulta/<int:consulta_id>/medicamento/adicionar/', views.adicionar_medicamento, name='consulta_adicionar_medicamento'),
    path('consulta/<int:consulta_id>/problema/adicionar/', views.adicionar_problema_saude, name='consulta_adicionar_problema_saude'),
    path('consulta/avaliacao/adicionar/', views.adicionar_avaliacao, name='consulta_adicionar_avaliacao'),
    path('consulta/<int:consulta_id>/plano/adicionar/', views.adicionar_plano_atuacao, name='consulta_adicionar_plano_atuacao'),
]
