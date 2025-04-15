# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao
from .forms import (
    ConsultaForm, ProblemaSaudeForm, MedicamentoForm,
    AvaliacaoForm, PlanoAtuacaoForm
)
from paciente.models import Paciente
from django.contrib import messages

# Criar nova consulta
def create_consulta(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            return redirect('detalhe_consulta', consulta_id=consulta.id)
    else:
        form = ConsultaForm()
    return render(request, 'create_consulta.html', {'form': form, 'paciente': paciente})

# Listar todas as consultas de um paciente
def listar_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = paciente.consultas.all()
    return render(request, 'listar_consultas.html', {'paciente': paciente, 'consultas': consultas})

# Detalhes da consulta (mostrar botões para adicionar mais dados)
def detalhe_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    problemas = ProblemaSaude.objects.filter(consulta=consulta)
    medicamentos = Medicamento.objects.filter(problema_saude__in=problemas).select_related('problema_saude')
    avaliacoes = Avaliacao.objects.filter(medicamento__in=medicamentos).select_related('medicamento')
    planos = PlanoAtuacao.objects.filter(consulta=consulta)

    # Agrupar medicamentos por problema de saúde
    problemas_com_medicamentos = []
    for problema in problemas:
        medicamentos_relacionados = problema.medicamentos.all()
        for medicamento in medicamentos_relacionados:
            medicamento.avaliacao = Avaliacao.objects.filter(medicamento=medicamento).first()
        problemas_com_medicamentos.append({
            'problema': problema,
            'medicamentos': medicamentos_relacionados
        })

    context = {
        'consulta': consulta,
        'problemas': problemas,
        'medicamentos': medicamentos,
        'avaliacoes': avaliacoes,
        'planos': planos,
        'problema_form': ProblemaSaudeForm(),
        'medicamento_form': MedicamentoForm(),
        'avaliacao_form': AvaliacaoForm(),
        'plano_form': PlanoAtuacaoForm(),
        'problemas_com_medicamentos': problemas_com_medicamentos,
    }

    return render(request, 'detalhe_consulta.html', context)




# Adicionar problema de saúde
def adicionar_problema_saude(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = ProblemaSaudeForm(request.POST)
        if form.is_valid():
            problema = form.save(commit=False)
            problema.consulta = consulta
            problema.save()
            return redirect('detalhe_consulta', consulta_id=consulta.id)
    else:
        form = ProblemaSaudeForm()
    return render(request, 'adicionar_problema_saude.html', {'form': form, 'consulta': consulta})

# Adicionar medicamento
def adicionar_medicamento(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, consulta=consulta)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.consulta = consulta
            medicamento.save()
            return redirect('detalhe_consulta', consulta_id=consulta.id)
    else:
        form = MedicamentoForm(consulta=consulta)
    return render(request, 'adicionar_medicamento.html', {'form': form, 'consulta': consulta})


# Adicionar avaliação
def adicionar_avaliacao(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        medicamento_id = request.POST.get('medicamento')

        if medicamento_id and form.is_valid():
            medicamento = get_object_or_404(Medicamento, id=medicamento_id)

            # Verifica se já existe uma avaliação para esse medicamento
            if hasattr(medicamento, 'avaliacao'):
                messages.error(request, "Este medicamento já possui uma avaliação.")
                return redirect('detalhe_consulta', consulta_id=medicamento.problema_saude.consulta.id)

            avaliacao = form.save(commit=False)
            avaliacao.medicamento = medicamento
            avaliacao.save()
            messages.success(request, "Avaliação adicionada com sucesso.")
            return redirect('detalhe_consulta', consulta_id=medicamento.problema_saude.consulta.id)




# Adicionar plano de atuação
def adicionar_plano_atuacao(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = PlanoAtuacaoForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.consulta = consulta
            plano.save()
            return redirect('detalhe_consulta', consulta_id=consulta.id)
    else:
        form = PlanoAtuacaoForm()
    return render(request, 'adicionar_plano_atuacao.html', {'form': form, 'consulta': consulta})


