from django.urls import path
from .views import (
    paciente_create,
    historia_social_alcolismo_create,
    historia_social_tabagismo_create,
    habitos_alimentares_create,
    perfil_clinico_create,
    autonomia_medicamentos_create,
    saude_create,
)

urlpatterns = [
    path('paciente-create/', paciente_create, name='paciente_create'),
    path('historia-social-alcolismo/', historia_social_alcolismo_create, name='historia_social_alcolismo'),
    path('historia-socialtabagismo/', historia_social_tabagismo_create, name='historia_social_tabagismo'),
    path('habitos-alimentares/', habitos_alimentares_create, name='habitos_alimentares'),
    path('perfil-clinico/', perfil_clinico_create, name='perfil_clinico'),
    path('saude/', saude_create, name='saude_create'),
    path('autonomia_medicamentos/create/', autonomia_medicamentos_create, name='autonomia_medicamentos_create'),
]