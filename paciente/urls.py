from django.urls import path
from .views import (
    adicionar_doenca, adicionar_medicamento, associar_doencas_medicamentos, buscar_doencas, buscar_medicamento, cadastrar_paciente, cadastrar_historia_social, 
    cadastrar_habitos_alimentares, cadastrar_perfil_clinico, cadastrar_autonomia_medicamentos,
    saude
)

urlpatterns = [
    # URL para cadastrar um novo paciente
    path('novo/', cadastrar_paciente, name='cadastrar_paciente'),
    
    # URLs para cadastro de informações de um paciente
    path('paciente/<int:paciente_id>/historia-social/', cadastrar_historia_social, name='cadastrar_historia_social'),
    path('paciente/<int:paciente_id>/habitos-alimentares/', cadastrar_habitos_alimentares, name='cadastrar_habitos_alimentares'),
    path('paciente/<int:paciente_id>/perfil-clinico/', cadastrar_perfil_clinico, name='cadastrar_perfil_clinico'),
    path('paciente/<int:paciente_id>/autonomia-medicamentos/', cadastrar_autonomia_medicamentos, name='cadastrar_autonomia_medicamentos'),
    path('paciente/<int:paciente_id>/saude/', saude, name='cadastrar_saude'),  # URL para a view de saúde
    
    # URL para associar doenças e medicamentos ao paciente
    path('paciente/<int:paciente_id>/associar_doencas_medicamentos/', associar_doencas_medicamentos, name='associar_doencas_medicamentos'),
    path('buscar_medicamento/', buscar_medicamento, name='buscar_medicamento'),
    path('buscar_doencas/', buscar_doencas, name='buscar_doencas'),
    path('adicionar_medicamento/<int:paciente_id>/', adicionar_medicamento, name='adicionar_medicamento'),
    path('adicionar_doenca/<int:paciente_id>/', adicionar_doenca, name='adicionar_doenca'),
            ]
