# consulta/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Consulta, Paciente
from .forms import ConsultaForm, ProblemaSaudeForm, MedicamentoForm, AvaliacaoForm, PlanoAtuacaoForm

def adicionar_consulta(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    

    if request.method == 'POST':
        consulta_form = ConsultaForm(request.POST or None)
        problema_form = ProblemaSaudeForm(request.POST)
        medicamento_form = MedicamentoForm(request.POST)
        avaliacao_form = AvaliacaoForm(request.POST)
        plano_form = PlanoAtuacaoForm(request.POST)

        if consulta_form.is_valid() and problema_form.is_valid() and medicamento_form.is_valid() and \
           avaliacao_form.is_valid() and plano_form.is_valid():
            # Salve os dados da consulta
            consulta = consulta_form.save(commit=False)
            consulta.paciente = paciente  # Atribui a instância do paciente
            consulta.save()

            # Salve os problemas de saúde
            problema = problema_form.save(commit=False)
            problema.consulta = consulta
            problema.save()

            # Salve os medicamentos
            medicamento = medicamento_form.save(commit=False)
            medicamento.consulta = consulta
            medicamento.save()

            # Salve a avaliação
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.consulta = consulta
            avaliacao.save()

            # Salve o plano de atuação
            plano = plano_form.save(commit=False)
            plano.consulta = consulta
            plano.save()

            return redirect('listar_consultas', paciente_id=paciente_id)
    else:
        consulta_form = ConsultaForm()
        problema_form = ProblemaSaudeForm()
        medicamento_form = MedicamentoForm()
        avaliacao_form = AvaliacaoForm()
        plano_form = PlanoAtuacaoForm()

    context = {
        'paciente': paciente,  # Adiciona a instância do paciente ao contexto
        'consulta_form': consulta_form,
        'problema_form': problema_form,
        'medicamento_form': medicamento_form,
        'avaliacao_form': avaliacao_form,
        'plano_form': plano_form,
    }

    return render(request, 'adicionar_consulta.html', context)


def listar_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    # Filtrando as consultas do paciente e ordenando por data
    consultas_list = Consulta.objects.filter(paciente=paciente).order_by('data_consulta')

    # Paginação
    paginator = Paginator(consultas_list, 5)  # 5 consultas por página
    page_number = request.GET.get('page')
    consultas = paginator.get_page(page_number)

    context = {
        'paciente': paciente,
        'consultas': consultas,
    }

    return render(request, 'listar_consultas.html', context)

def detalhe_consulta(request, consulta_id):
    # Obtém a consulta com o ID fornecido ou retorna um 404 se não existir
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Crie o contexto para passar para o template
    context = {
        'consulta': consulta,
    }
    
    # Renderiza o template com os detalhes da consulta
    return render(request, 'detalhe_consulta.html', context)
  
