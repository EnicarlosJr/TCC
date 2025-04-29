# login/utils.py
from functools import wraps
from login.models import LogAtividade

def log_atividade(acao):
    """
    Decorator para registrar ações automáticas no LogAtividade.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            
            if request.user.is_authenticated:
                LogAtividade.objects.create(
                    usuario=request.user,
                    acao=acao,
                    detalhes=f"Path: {request.path}"
                )
            return response

        return _wrapped_view
    return decorator