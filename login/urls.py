# login/urls.py
from django.urls import path
from login.views import (
    listar_usuarios,
    ver_logs_usuario,
    editar_usuario,
    apagar_usuario,
    cadastrar_usuario,
    login_manual_view,
    logout_view,
)

urlpatterns = [
    # Controle de Acesso (Login/Logout)
    path('login/', login_manual_view, name='manual_login'),
    path('logout/', logout_view, name='logout'),

    # Gerenciamento de Usuários
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('usuarios/<int:usuario_id>/logs/', ver_logs_usuario, name='ver_logs_usuario'),
    path('usuarios/<int:usuario_id>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/apagar/', apagar_usuario, name='apagar_usuario'),
]
