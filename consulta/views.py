from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from consulta.models import Avaliacao, Consulta, Medicamento, Paciente, PlanoAtuacao, ProblemaSaude
from consulta.forms import ConsultaForm, ProblemaSaudeForm, MedicamentoForm, AvaliacaoForm, PlanoAtuacaoForm

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

    # Filtrando as consultas do paciente e ordenando por data mais recente
    consultas_list = Consulta.objects.filter(paciente=paciente).order_by('-data_consulta')

    # Paginação (5 consultas por página)
    paginator = Paginator(consultas_list, 5)
    page_number = request.GET.get('page')
    consultas = paginator.get_page(page_number)

    context = {
        'paciente': paciente,
        'consultas': consultas,
    }
    
    return render(request, 'listar_consultas.html', context)

def detalhe_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    # Obtendo os dados relacionados à consulta
    avaliacao = Avaliacao.objects.filter(consulta=consulta).first()
    problemas_saude = ProblemaSaude.objects.filter(consulta=consulta)
    medicamentos = Medicamento.objects.filter(consulta=consulta)
    plano_atuacao = PlanoAtuacao.objects.filter(consulta=consulta).first()  # Se houver apenas um plano por consulta

    context = {
        'consulta': consulta,
        'avaliacao': avaliacao,
        'problemas_saude': problemas_saude,
        'medicamentos': medicamentos,
        'plano_atuacao': plano_atuacao,
    }

    return render(request, 'detalhe_consulta.html', context)