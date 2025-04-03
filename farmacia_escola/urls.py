# farmacia_escola/urls.py
from django.contrib import admin
from django.conf.urls.static import static

from django.urls import path, include

from farmacia_escola import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paciente/', include('paciente.urls')),
    path('listagem_pacientes/', include('listagem_pacientes.urls')),
    path('consulta/', include('consulta.urls')),
    path('', include('tela_inicial.urls')),
    path('relatorios/', include('relatorios.urls')),
] 
