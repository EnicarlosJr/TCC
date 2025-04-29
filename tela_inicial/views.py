from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def tela_inicial(request):
    tipo_usuario = request.user.tipo_usuario  # farmaceutico, aluno, convidado

    context = {
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'tela_inicial.html', context)
