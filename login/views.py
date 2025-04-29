# login/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from login.forms import CustomUserCreationForm
from login.models import CustomUser, LogAtividade
from login.utils import log_atividade


User = get_user_model()

def validar_email_ufvjm(email):
    """
    Verifica se o email informado pertence ao domínio da UFVJM.
    """
    return email.lower().endswith('@ufvjm.edu.br')

@log_atividade("Logou!")
def login_manual_view(request):
    """
    View de login manual usando email e senha, para ambiente de desenvolvimento.
    Proteções:
    - Valida se o email termina com @ufvjm.edu.br
    - Autentica pelo username associado ao email.
    - Exibe mensagens amigáveis em caso de erro.

    🔒 Em produção, certifique-se de rodar em HTTPS.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validar_email_ufvjm(email):
            messages.error(request, 'Somente emails institucionais (@ufvjm.edu.br) são aceitos.')
            return redirect('manual_login')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
            return redirect('manual_login')

        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            login(request, user_auth)
            return redirect('tela_inicial')
        else:
            messages.error(request, 'Senha incorreta.')

    return render(request, 'manual_login.html')

@login_required
def logout_view(request):
    """
    Faz o logout seguro do usuário e o redireciona para a tela de login.
    """
    logout(request)
    return redirect('manual_login')

@login_required
def cadastrar_usuario(request):
    """
    View para cadastro de novos usuários.
    - Apenas farmacêuticos podem acessar esta view.
    - Valida que o email cadastrado seja da UFVJM.
    - Atribui senha padrão inicial 'farmacia123' (recomendado forçar troca depois).
    
    🔒 Em produção, recomenda-se forçar troca de senha no primeiro acesso.
    """
    if request.user.tipo_usuario != 'farmaceutico':
        return HttpResponseForbidden('Acesso negado. Apenas farmacêuticos podem cadastrar usuários.')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            novo_usuario = form.save(commit=False)

            # Validação de email institucional
            if not novo_usuario.email.endswith('@ufvjm.edu.br'):
                messages.error(request, 'Somente emails institucionais (@ufvjm.edu.br) são permitidos.')
                return render(request, 'cadastrar_usuario.html', {'form': form})

            novo_usuario.set_password('farmacia123')  # Senha padrão (aviso para troca futura)
            novo_usuario.save()

            messages.success(request, f'Usuário {novo_usuario.username} cadastrado com sucesso!')
            return redirect('tela_inicial')

        else:
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados preenchidos.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'cadastrar_usuario.html', {'form': form})

@login_required
def ver_logs_usuario(request, usuario_id):
    if request.user.tipo_usuario != 'farmaceutico':
        return HttpResponseForbidden('Acesso negado.')

    usuario = get_object_or_404(CustomUser, id=usuario_id)
    logs = LogAtividade.objects.filter(usuario=usuario)

    return render(request, 'usuarios/ver_logs_usuario.html', {'usuario': usuario, 'logs': logs})


@login_required
def listar_usuarios(request):
    if request.user.tipo_usuario != 'farmaceutico':
        return HttpResponseForbidden('Acesso negado.')

    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


@login_required
def editar_usuario(request, usuario_id):
    if request.user.tipo_usuario != 'farmaceutico':
        return HttpResponseForbidden('Acesso negado.')

    usuario = get_object_or_404(CustomUser, id=usuario_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tipo_usuario = request.POST.get('tipo_usuario')

        if not email.endswith('@ufvjm.edu.br'):
            messages.error(request, 'Somente emails institucionais (@ufvjm.edu.br) são permitidos.')
            return redirect('editar_usuario', usuario_id=usuario.id)

        usuario.username = username
        usuario.email = email
        usuario.tipo_usuario = tipo_usuario
        usuario.save()

        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('listar_usuarios')

    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
def apagar_usuario(request, usuario_id):
    if request.user.tipo_usuario != 'farmaceutico':
        return HttpResponseForbidden('Acesso negado.')

    usuario = get_object_or_404(CustomUser, id=usuario_id)

    # Segurança: impedir que apague a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode excluir sua própria conta enquanto estiver logado.')
        return redirect('listar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuário "{usuario.username}" excluído com sucesso!')
        return redirect('listar_usuarios')

    return redirect('listar_usuarios')

