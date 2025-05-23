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
    
    # Plano de atuação
    path('plano_atuacao/adicionar/', views.adicionar_plano_atuacao, name='adicionar_plano_atuacao'),
    path('plano_atuacao/acompanhamento/<int:plano_id>/', views.atualizar_acompanhamento, name='atualizar_acompanhamento'),
    
    # Visualização de consulta
    path('consulta/<int:consulta_id>/visualizar/', views.visualizar_consulta, name='visualizar_consulta'),
    
    # Excluir objeto
    path('consulta/excluir/<str:model_name>/<int:object_id>/', views.excluir_objeto, name='excluir_objeto'),
    
    # Editar (geral)
    path('editar/<str:model_name>/<int:obj_id>/', views.editar, name='editar'),
    
    # Avaliação fullscreen
    path('consulta/<int:consulta_id>/avaliacao/fullscreen/', views.avaliacao_fullscreen, name='avaliacao_fullscreen'),
]
