# farmacia_escola/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django_cas_ng import views as cas_views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Módulos principais
    path('paciente/', include('paciente.urls')),
    path('listagem_pacientes/', include('listagem_pacientes.urls')),
    path('consulta/', include('consulta.urls')),
    path('tela_inicial/', include('tela_inicial.urls')),  # Tela inicial principal
    path('relatorios/', include('relatorios.urls')),

    # Controle de acesso (Login manual e Usuários)
    path('conta/', include('login.urls')),  # <<< Troquei '' para 'conta/', para separar melhor!

    # Login CAS da UFVJM
    #path('accounts/login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
    #path('accounts/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),

    # Home padrão redireciona para Tela Inicial
    path('', include('tela_inicial.urls')),  # Raiz "/" vai para tela_inicial
]

# (opcional) Para servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
