# listagem_pacientes/urls.py
from django.urls import path
from .views import PacienteDetailView, PacienteListView

urlpatterns = [
    path('paciente_list/', PacienteListView.as_view(), name='paciente_list'),
    path('paciente/<int:pk>/', PacienteDetailView.as_view(), name='detalhe_paciente'),
    ]

