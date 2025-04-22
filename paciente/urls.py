# urls.py do app paciente
from django.urls import path
from .views import (
    adicionar_doenca, adicionar_medicamento, associar_doencas_medicamentos, buscar_doencas, buscar_medicamento, cadastrar_paciente, cadastrar_historia_social, 
    cadastrar_habitos_alimentares, cadastrar_perfil_clinico, cadastrar_autonomia_medicamentos,
    saude
)

urlpatterns = [
    # URL para cadastrar um novo paciente
    path('paciente/novo/', cadastrar_paciente, name='paciente_cadastrar_paciente'),
    
    # URLs para cadastro de informações de um paciente
    path('paciente/<int:paciente_id>/historia-social/', cadastrar_historia_social, name='paciente_cadastrar_historia_social'),
    path('paciente/<int:paciente_id>/habitos-alimentares/', cadastrar_habitos_alimentares, name='paciente_cadastrar_habitos_alimentares'),
    path('paciente/<int:paciente_id>/perfil-clinico/', cadastrar_perfil_clinico, name='paciente_cadastrar_perfil_clinico'),
    path('paciente/<int:paciente_id>/autonomia-medicamentos/', cadastrar_autonomia_medicamentos, name='paciente_cadastrar_autonomia_medicamentos'),
    path('paciente/<int:paciente_id>/saude/', saude, name='paciente_cadastrar_saude'),  # URL para a view de saúde
    
    # URL para associar doenças e medicamentos ao paciente
    path('paciente/<int:paciente_id>/associar_doencas_medicamentos/', associar_doencas_medicamentos, name='paciente_associar_doencas_medicamentos'),
    path('paciente/buscar_medicamento/', buscar_medicamento, name='paciente_buscar_medicamento'),
    path('paciente/buscar_doencas/', buscar_doencas, name='paciente_buscar_doencas'),
    path('paciente/<int:paciente_id>/adicionar_medicamento/', adicionar_medicamento, name='paciente_adicionar_medicamento'),
    path('paciente/<int:paciente_id>/adicionar_doenca/', adicionar_doenca, name='paciente_adicionar_doenca'),
]
