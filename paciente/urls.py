from django.urls import path
from .views import (
    adicionar_doenca, adicionar_medicamento, associar_doencas_medicamentos, buscar_doencas, buscar_medicamento,
    cadastrar_paciente, cadastrar_historia_social, cadastrar_habitos_alimentares, cadastrar_perfil_clinico,
    cadastrar_autonomia_medicamentos, criar_anamnese, detalhe_anamnese, editar_anamnese_bloco, excluir_anamnese_bloco, saude
)

urlpatterns = [
    # Cadastro de paciente
    path('paciente/novo/', cadastrar_paciente, name='paciente_cadastrar_paciente'),

    # Criação e detalhe da anamnese
    path('<int:paciente_id>/anamnese/criar/', criar_anamnese, name='criar_anamnese'),
    path('anamnese/<int:anamnese_id>/', detalhe_anamnese, name='detalhe_anamnese'),

    # Blocos da anamnese
    path('anamnese/<int:anamnese_id>/historia-social/', cadastrar_historia_social, name='cadastrar_historia_social'),
    path('anamnese/<int:anamnese_id>/habitos-alimentares/', cadastrar_habitos_alimentares, name='cadastrar_habitos_alimentares'),
    path('anamnese/<int:anamnese_id>/perfil-clinico/', cadastrar_perfil_clinico, name='cadastrar_perfil_clinico'),
    path('anamnese/<int:anamnese_id>/autonomia-medicamentos/', cadastrar_autonomia_medicamentos, name='cadastrar_autonomia_medicamentos'),
    path('anamnese/<int:anamnese_id>/saude/', saude, name='cadastrar_saude'),
    path('anamnese/<int:anamnese_id>/<str:bloco>/excluir/', excluir_anamnese_bloco, name='excluir_anamnese_bloco'),
    path('anamnese/<int:anamnese_id>/<str:bloco>/editar/', editar_anamnese_bloco, name='editar_anamnese_bloco'),


    # Associação doença/medicamento
    path('anamnese/<int:anamnese_id>/associar_doencas_medicamentos/', associar_doencas_medicamentos, name='associar_doencas_medicamentos'),

    # Auxiliares (autocomplete, adição de dados)
    path('paciente/buscar_medicamento/', buscar_medicamento, name='paciente_buscar_medicamento'),
    path('paciente/buscar_doencas/', buscar_doencas, name='paciente_buscar_doencas'),
    path('anamnese/<int:anamnese_id>/adicionar_medicamento/', adicionar_medicamento, name='adicionar_medicamento'),
    path('paciente/<int:paciente_id>/adicionar_doenca/', adicionar_doenca, name='paciente_adicionar_doenca'),
]
