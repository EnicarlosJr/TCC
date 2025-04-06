import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


import paciente
from .models import AutonomiaMedicamentos, Doenca, HabitosAlimentares, HistoriaSocial, Medicamento, MedicamentoDoencaPaciente, Paciente, PerfilClinico, Saude
from .forms import (
    DoencaForm, MedicamentoDoencaPacienteForm, MedicamentoForm, PacienteForm, HistoriaSocialForm, HabitosAlimentaresForm,
    PerfilClinicoForm, AutonomiaMedicamentosForm, SaudeForm,
)

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


def associar_doencas_medicamentos(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        try:
            # Tente carregar os dados JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return redirect('paciente_detail', pk=paciente.id)

        associacoes = data.get('associacoes', [])

        if not associacoes:
            return JsonResponse({'error': 'Nenhuma associação fornecida.'}, status=400)

        # Processa as associações (doenças e medicamentos)
        for associacao in associacoes:
            doenca_nome = associacao.get('doenca')
            medicamentos_nomes = associacao.get('medicamentos', [])
            observacao = associacao.get('observacao', '')

            if not doenca_nome or not medicamentos_nomes:
                return JsonResponse({'error': 'Nome da doença e medicamentos são obrigatórios.'}, status=400)

            # Validar e criar doença
            doenca, created = Doenca.objects.get_or_create(nome=doenca_nome)
            
            # Processa os medicamentos
            for medicamento_nome in medicamentos_nomes:
                medicamento, created = Medicamento.objects.get_or_create(nome=medicamento_nome, doenca=doenca)
                
                # Cria a associação entre paciente, medicamento e doença
                MedicamentoDoencaPaciente.objects.create(
                    paciente=paciente,
                    medicamento=medicamento,
                    doenca=doenca,
                    observacao=observacao
                )

        # Retorna uma resposta JSON de sucesso
        return JsonResponse({
            'sucesso': True,
            'message': 'Associações de doenças e medicamentos foram salvas com sucesso.',
            'redirect': f'/paciente/{paciente_id}/'
        })

    elif request.method == 'GET':
        # Se for GET, renderiza a página para o formulário
        return render(request, 'associar_doencas_medicamentos.html', {'paciente': paciente})





def buscar_medicamento(request):
    query = request.GET.get('q', '')  # Pega o termo de busca enviado pelo frontend
    medicamentos = []

    if query:
        # Busca os medicamentos que contenham o termo de busca no nome
        medicamentos = Medicamento.objects.filter(nome__icontains=query).values('id', 'nome')

    return JsonResponse(list(medicamentos), safe=False)

def buscar_doencas(request):
    query = request.GET.get('q', '')  # Pega o termo de busca enviado pelo frontend
    doencas = []

    if query:
        # Busca as doenças que contenham o termo de busca no nome
        doencas = Doenca.objects.filter(nome__icontains=query).values('id', 'nome')

    return JsonResponse(list(doencas), safe=False)

def adicionar_medicamento(request, paciente_id):
    if request.method == 'POST':
        nome_medicamento = request.POST.get('nome')
        doenca_id = request.POST.get('doenca_id')  # Recebe o ID da doença associada ao medicamento
        
        # Verifica se o nome do medicamento e o id da doença foram fornecidos
        if nome_medicamento and doenca_id:
            try:
                # Busca a doença pelo id
                doenca = Doenca.objects.get(id=doenca_id)
            except Doenca.DoesNotExist:
                return JsonResponse({'error': 'Doença não encontrada!'}, status=404)

            # Cria ou recupera o medicamento existente
            medicamento, created = Medicamento.objects.get_or_create(
                nome=nome_medicamento,  # Garantir que o nome seja único
                doenca=doenca  # Aqui associamos a doença diretamente ao medicamento
            )

            # Cria a associação entre medicamento, doença e paciente
            paciente = Paciente.objects.get(id=paciente_id)
            MedicamentoDoencaPaciente.objects.create(
                paciente=paciente,
                medicamento=medicamento,
                doenca=doenca
            )

            return JsonResponse({
                'sucesso': True,
                'id': medicamento.id,
                'nome': medicamento.nome
            })

        return JsonResponse({'error': 'Nome do medicamento e doença são obrigatórios.'}, status=400)

    return JsonResponse({'error': 'Método HTTP inválido!'}, status=405)



def adicionar_doenca(request, paciente_id):
    if request.method == 'POST':
        nome_doenca = request.POST.get('nome')

        if nome_doenca:
            # Verifica se a doença já existe ou cria uma nova
            doenca, created = Doenca.objects.get_or_create(nome=nome_doenca)

            # Tenta recuperar o paciente pelo ID
            paciente = get_object_or_404(Paciente, id=paciente_id)

            # Se a doença for nova, associamos ela ao paciente aqui, se necessário
            # Se precisar associar a doença ao paciente diretamente
            paciente.doencas.add(doenca)  # Associa a doença ao paciente

            return JsonResponse({
                'sucesso': True,
                'id': doenca.id,
                'nome': doenca.nome,
            })

        return JsonResponse({'error': 'O nome da doença é obrigatório!'}, status=400)

    return JsonResponse({'error': 'Método HTTP inválido!'}, status=405)


