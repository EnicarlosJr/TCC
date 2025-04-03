from datetime import date, time, datetime
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
    DoencaPacienteFormSet,
    MedicamentoPacienteFormSet,
    PacienteForm, 
    HistoriaSocialAlcolismoForm, 
    HistoriaSocialTabagismoForm, 
    HabitosAlimentaresForm, 
    PerfilClinicoForm, 
    AutonomiaMedicamentosForm,
    SaudeForm
)
from .models import Doenca, Medicamento, Paciente

def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Salva os dados do formulário na sessão
            save_to_session(request, 'paciente_form', form.cleaned_data)
            return redirect('historia_social_alcolismo')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('paciente_form', {})
        form = PacienteForm(initial=form_data)

    return render(request, 'paciente_form.html', {'form': form})

def historia_social_alcolismo_create(request):
    if request.method == 'POST':
        form = HistoriaSocialAlcolismoForm(request.POST)
        if form.is_valid():
            # Salvar os dados na sessão
            save_to_session(request, 'historia_social_alcolismo_data', form.cleaned_data)
            return redirect('historia_social_tabagismo')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('historia_social_alcolismo_data', {})
        form = HistoriaSocialAlcolismoForm(initial=form_data)

    return render(request, 'historia_social_alcolismo.html', {'form': form})

def historia_social_tabagismo_create(request):
    if request.method == 'POST':
        form = HistoriaSocialTabagismoForm(request.POST)
        if form.is_valid():
            save_to_session(request, 'historia_social_tabagismo_form', form.cleaned_data)
            return redirect('habitos_alimentares')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('historia_social_tabagismo_form', {})
        form = HistoriaSocialTabagismoForm(initial=form_data)

    return render(request, 'historia_social_tabagismo.html', {'form': form})

def habitos_alimentares_create(request):
    if request.method == 'POST':
        form = HabitosAlimentaresForm(request.POST)
        if form.is_valid():
            # Salvar os dados na sessão
            save_to_session(request, 'habitos_alimentares_data', form.cleaned_data)
            return redirect('perfil_clinico')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('habitos_alimentares_data', {})
        form = HabitosAlimentaresForm(initial=form_data)

    return render(request, 'habitos_alimentares.html', {'form': form})

def perfil_clinico_create(request):
    if request.method == 'POST':
        form = PerfilClinicoForm(request.POST)
        if form.is_valid():
            save_to_session(request, 'perfil_clinico_form', form.cleaned_data)
            return redirect('saude_create')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('perfil_clinico_form', {})
        form = PerfilClinicoForm(initial=form_data)

    return render(request, 'perfil_clinico.html', {'form': form})

def saude_create(request):
    if request.method == 'POST':
        form = SaudeForm(request.POST)
        if form.is_valid():
            save_to_session(request, 'saude_form', form.cleaned_data)
            return redirect('medicamentos_e_doencas_create')  # Redireciona para a próxima etapa
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('saude_form', {})
        form = SaudeForm(initial=form_data)

    return render(request, 'saude_create.html', {'form': form})


def medicamentos_e_doencas_create(request):
    if request.method == 'POST':
        # Carregar os formsets de Medicamento e Doença com os dados do POST
        medicamento_formset = MedicamentoPacienteFormSet(request.POST)
        doenca_formset = DoencaPacienteFormSet(request.POST)

        # Verificar se ambos os formsets são válidos
        if medicamento_formset.is_valid() and doenca_formset.is_valid():
            # Salvar os formsets (o paciente será salvo durante o processo de formset)
            paciente = medicamento_formset.save(commit=False)[0]  # Aqui assume-se que o paciente já foi associado
            paciente.save()  # Salve o paciente após associá-lo aos medicamentos e doenças

            # Associar medicamentos e doenças selecionadas ao paciente
            medicamentos_selecionados = request.POST.getlist('medicamentos_selecionados')
            doencas_selecionadas = request.POST.getlist('doencas_selecionadas')

            # Associar os medicamentos selecionados ao paciente
            for medicamento_id in medicamentos_selecionados:
                try:
                    medicamento = Medicamento.objects.get(id=medicamento_id)
                    paciente.medicamentos.add(medicamento)
                except Medicamento.DoesNotExist:
                    pass  # Caso o medicamento não exista

            # Associar as doenças selecionadas ao paciente
            for doenca_id in doencas_selecionadas:
                try:
                    doenca = Doenca.objects.get(id=doenca_id)
                    paciente.doencas.add(doenca)
                except Doenca.DoesNotExist:
                    pass  # Caso a doença não exista

            # Salvar os formsets de medicamentos e doenças
            medicamento_formset.save()
            doenca_formset.save()

            # Redirecionar para a próxima etapa
            return redirect('autonomia_medicamentos_create')

    else:
        # Para o método GET, preenche os formsets com dados da sessão, se existir
        medicamento_formset = MedicamentoPacienteFormSet()
        doenca_formset = DoencaPacienteFormSet()

    # Passando a lista de medicamentos e doenças já salvas na sessão (se existirem)
    medicamentos_salvos = Medicamento.objects.all()
    doencas_salvas = Doenca.objects.all()

    return render(request, 'medicamentos_e_doencas_create.html', {
        'medicamento_formset': medicamento_formset,
        'doenca_formset': doenca_formset,
        'medicamentos_salvos': medicamentos_salvos,
        'doencas_salvas': doencas_salvas,
    })




def autonomia_medicamentos_create(request):
    if request.method == 'POST':
        form = AutonomiaMedicamentosForm(request.POST)
        if form.is_valid():
            save_to_session(request, 'autonomia_medicamentos_form', form.cleaned_data)

            # Recupera todos os dados da sessão
            paciente_data = {
                **request.session.get('paciente_form', {}),
                **request.session.get('historia_social_alcolismo_data', {}),
                **request.session.get('historia_social_tabagismo_form', {}),
                **request.session.get('habitos_alimentares_data', {}),
                **request.session.get('perfil_clinico_form', {}),
                **request.session.get('saude_form', {}),
                **request.session.get('autonomia_medicamentos_form', {})
            }

            # Criar e salvar o objeto Paciente no banco de dados
            paciente = Paciente.objects.create(**paciente_data)

            # Limpar a sessão
            request.session.flush()

            return redirect('/listagem_pacientes/paciente_list')  # Redireciona para o início
    else:
        # Preencher o formulário com dados salvos na sessão, se existirem
        form_data = request.session.get('autonomia_medicamentos_form', {})
        form = AutonomiaMedicamentosForm(initial=form_data)

    return render(request, 'autonomia_medicamentos.html', {'form': form})

# Função para salvar os dados do formulário na sessão
def save_to_session(request, form_name, form_data):
    # Converte objetos date e time para strings antes de salvar na sessão
    for key, value in form_data.items():
        if isinstance(value, date):
            form_data[key] = value.isoformat()  # Converte date para string no formato ISO
        elif isinstance(value, time):
            form_data[key] = value.isoformat()  # Converte time para string no formato ISO

    # Salva os dados convertidos na sessão
    if form_name in request.session:
        request.session[form_name].update(form_data)
    else:
        request.session[form_name] = form_data

    request.session.modified = True  # Marca a sessão como modificada




