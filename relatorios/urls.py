from django.urls import path
from .views import dashboard_clinico, exportar_dashboard

urlpatterns = [
    path('dashboard/', dashboard_clinico, name='dashboard_clinico'),
    path('dashboard/exportar/', exportar_dashboard, name='exportar_dashboard'),  # ESTE AQUI!
]
