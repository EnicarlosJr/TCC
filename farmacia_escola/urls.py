from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django_cas_ng import views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paciente/', include('paciente.urls')),
    path('listagem_pacientes/', include('listagem_pacientes.urls')),
    path('consulta/', include('consulta.urls')),
    path('tela_inicial/', include('tela_inicial.urls')),
    path('relatorios/', include('relatorios.urls')),

    path('conta/', include('login.urls')),


    path('', include('tela_inicial.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
