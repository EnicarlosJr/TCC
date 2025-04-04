from django.urls import path
from .views import (
    cadastrar_paciente, cadastrar_historia_social, cadastrar_habitos_alimentares,
    cadastrar_perfil_clinico, cadastrar_autonomia_medicamentos, saude
)

urlpatterns = [
    path('novo/', cadastrar_paciente, name='cadastrar_paciente'),
    
    # Corrigindo a URL para 'historia-social' com o id do paciente
    path('paciente/<int:paciente_id>/historia-social/', cadastrar_historia_social, name='cadastrar_historia_social'),
    
    # Corrigindo a URL para 'habitos-alimentares' com o id do paciente
    path('paciente/<int:paciente_id>/habitos-alimentares/', cadastrar_habitos_alimentares, name='cadastrar_habitos_alimentares'),
    
    # Corrigindo a URL para 'perfil-clinico' com o id do paciente
    path('paciente/<int:paciente_id>/perfil-clinico/', cadastrar_perfil_clinico, name='cadastrar_perfil_clinico'),
    
    # Corrigindo a URL para 'autonomia-medicamentos' com o id do paciente
    path('paciente/<int:paciente_id>/autonomia-medicamentos/', cadastrar_autonomia_medicamentos, name='cadastrar_autonomia_medicamentos'),
    path('paciente/<int:paciente_id>/saude/', saude, name='cadastrar_saude'),  # URL para a view de saúde
]
