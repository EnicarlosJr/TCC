import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from login.utils import log_atividade



from .models import  Doenca, Medicamento, MedicamentoDoencaPaciente, Paciente, PerfilClinico, Saude
from .forms import (
    DoencaForm, MedicamentoDoencaPacienteForm, MedicamentoForm, PacienteForm, HistoriaSocialForm, HabitosAlimentaresForm,
    PerfilClinicoForm, AutonomiaMedicamentosForm, SaudeForm,
)
@login_required
@log_atividade("Cadastrou um paciente!")
def cadastrar_paciente(request):
    if request.method == "POST":
        
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            # Criação automática das relações se não existirem

            return redirect('paciente_detail', pk=paciente.id)  # Redireciona para os detalhes do paciente
    else:
        form = PacienteForm()

    return render(request, 'cadastrar_paciente.html', {'form': form})

@login_required
@log_atividade("Cadastrou historia social!")
def cadastrar_historia_social(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Se a história social já existir, redireciona
    if hasattr(paciente, 'historia_social') and paciente.historia_social:
        return redirect('paciente_detail', pk=paciente.id)

    if request.method == 'POST':
        form = HistoriaSocialForm(request.POST)
        if form.is_valid():
            historia_social = form.save(commit=False)
            historia_social.paciente = paciente
            historia_social.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = HistoriaSocialForm()

    return render(request, 'historia_social.html', {'form': form, 'paciente': paciente})

@login_required
@log_atividade("Cadastrou Habitos Alimentares!")
def cadastrar_habitos_alimentares(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Se os hábitos alimentares já existirem, redireciona
    if hasattr(paciente, 'habitos_alimentares') and paciente.habitos_alimentares:
        return redirect('paciente_detail', pk=paciente.id)

    if request.method == 'POST':
        form = HabitosAlimentaresForm(request.POST)
        if form.is_valid():
            habitos_alimentares = form.save(commit=False)
            habitos_alimentares.paciente = paciente
            habitos_alimentares.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = HabitosAlimentaresForm()

    return render(request, 'habitos_alimentares.html', {'form': form, 'paciente': paciente})

@login_required
@log_atividade("Cadastrou Perfil Clinico!")
def cadastrar_perfil_clinico(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Se o perfil clínico já existir, redireciona
    if hasattr(paciente, 'perfil_clinico') and paciente.perfil_clinico:
        return redirect('paciente_detail', pk=paciente.id)

    if request.method == 'POST':
        form = PerfilClinicoForm(request.POST)
        if form.is_valid():
            perfil_clinico = form.save(commit=False)
            perfil_clinico.paciente = paciente
            perfil_clinico.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = PerfilClinicoForm()

    return render(request, 'perfil_clinico.html', {'form': form, 'paciente': paciente})

@login_required
@log_atividade("Cadastrou Autonomia Medicamentosa!")
def cadastrar_autonomia_medicamentos(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Se a autonomia de medicamentos já existir, redireciona
    if hasattr(paciente, 'autonomia_medicamentos') and paciente.autonomia_medicamentos:
        return redirect('paciente_detail', pk=paciente.id)

    if request.method == 'POST':
        form = AutonomiaMedicamentosForm(request.POST)
        if form.is_valid():
            autonomia_medicamentos = form.save(commit=False)
            autonomia_medicamentos.paciente = paciente
            autonomia_medicamentos.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = AutonomiaMedicamentosForm()

    return render(request, 'autonomia_medicamentos.html', {'form': form, 'paciente': paciente})


@login_required
@log_atividade("Cadastrou Percp Saúde")
def saude(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Se a saúde já existir, redireciona
    if hasattr(paciente, 'saude') and paciente.saude:
        return redirect('paciente_detail', pk=paciente.id)

    if request.method == 'POST':
        form = SaudeForm(request.POST)
        if form.is_valid():
            saude = form.save(commit=False)
            saude.paciente = paciente
            saude.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = SaudeForm()

    return render(request, 'adicionar_saude.html', {'form': form, 'paciente': paciente})

@login_required
@log_atividade("Cadastrou doença e medicamentos")
def associar_doencas_medicamentos(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return redirect('paciente_detail', pk=paciente.id)

        associacoes = data.get('associacoes', [])

        if not associacoes:
            return JsonResponse({'error': 'Nenhuma associação fornecida.'}, status=400)

        for associacao in associacoes:
            doenca_nome = associacao.get('doenca')
            medicamentos_nomes = associacao.get('medicamentos', [])
            observacao = associacao.get('observacao', '')

            if not doenca_nome or not medicamentos_nomes:
                return JsonResponse({'error': 'Nome da doença e medicamentos são obrigatórios.'}, status=400)

            # Cria ou recupera a doença
            doenca, _ = Doenca.objects.get_or_create(nome=doenca_nome)

            for medicamento_nome in medicamentos_nomes:
                medicamento, _ = Medicamento.objects.get_or_create(nome=medicamento_nome)

                # Cria associação evitando duplicações
                MedicamentoDoencaPaciente.objects.get_or_create(
                    paciente=paciente,
                    medicamento=medicamento,
                    doenca=doenca,
                    defaults={'observacao': observacao}
                )

        return JsonResponse({
            'sucesso': True,
            'message': 'Associações salvas com sucesso.',
            'redirect': f'/paciente/{paciente_id}/'
        })

    elif request.method == 'GET':
        return render(request, 'associar_doencas_medicamentos.html', {'paciente': paciente})

@login_required
@log_atividade("Cadastrou medicamento!")
@require_POST
def adicionar_medicamento(request, paciente_id):
    nome_medicamento = request.POST.get('nome')
    doenca_id = request.POST.get('doenca_id')

    if nome_medicamento and doenca_id:
        try:
            doenca = Doenca.objects.get(id=doenca_id)
        except Doenca.DoesNotExist:
            return JsonResponse({'error': 'Doença não encontrada!'}, status=404)

        medicamento, _ = Medicamento.objects.get_or_create(nome=nome_medicamento)
        paciente = get_object_or_404(Paciente, id=paciente_id)

        MedicamentoDoencaPaciente.objects.get_or_create(
            paciente=paciente,
            medicamento=medicamento,
            doenca=doenca
        )

        return JsonResponse({
            'sucesso': True,
            'id': medicamento.id,
            'nome': medicamento.nome
        })

    return JsonResponse({'sucesso': False, 'error': 'Nome do medicamento e doença são obrigatórios.'}, status=400)



def buscar_doencas(request):
    query = request.GET.get('q', '')  # Pega o termo de busca enviado pelo frontend
    doencas = []

    if query:
        # Busca as doenças que contenham o termo de busca no nome
        doencas = Doenca.objects.filter(nome__icontains=query).values('id', 'nome')

    return JsonResponse(list(doencas), safe=False)

def buscar_medicamento(request):
    query = request.GET.get('q', '')  # Pega o termo de busca enviado pelo frontend
    medicamentos = []

    if query:
        # Busca os medicamentos que contenham o termo de busca no nome
        medicamentos = Medicamento.objects.filter(nome__icontains=query).values('id', 'nome')

    return JsonResponse(list(medicamentos), safe=False)

@login_required
@log_atividade("Cadastrou Doenca")
@require_POST
def adicionar_doenca(request, paciente_id):
    nome = request.POST.get("nome", "").strip()
    if not nome:
        return JsonResponse({"erro": "Nome da doença é obrigatório."}, status=400)

    doenca, _ = Doenca.objects.get_or_create(nome=nome)
    paciente = get_object_or_404(Paciente, id=paciente_id)

    return JsonResponse({"id": doenca.id, "nome": doenca.nome})
