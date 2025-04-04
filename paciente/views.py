from django.shortcuts import render, redirect, get_object_or_404
from .models import AutonomiaMedicamentos, HabitosAlimentares, HistoriaSocial, Paciente, PerfilClinico, Saude
from .forms import (
    PacienteForm, HistoriaSocialForm, HabitosAlimentaresForm,
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
