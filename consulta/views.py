from collections import defaultdict
from urllib.parse import urlencode
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from login.utils import log_atividade
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao
from .forms import (
    ConsultaForm, PlanoAtuacaoAcompanhamentoForm, PlanoAtuacaoPlanejamentoForm, ProblemaSaudeForm, MedicamentoForm,
    AvaliacaoForm
)
from paciente.models import Paciente

@login_required
@log_atividade("Cadastrou um plano de cuidado!")
# ✅ Criar nova consulta
def create_consulta(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, request.FILES)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
    else:
        form = ConsultaForm()
    return render(request, 'create_consulta.html', {'form': form, 'paciente': paciente})

@login_required
# ✅ Listar todas as consultas de um paciente
def listar_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas_list = Consulta.objects.filter(paciente=paciente).order_by('-data_consulta')

    paginator = Paginator(consultas_list, 6)
    page_number = request.GET.get('page')
    consultas = paginator.get_page(page_number)

    base_url = '?'
    previous_url = next_url = None
    if consultas.has_previous():
        previous_url = base_url + urlencode({'page': consultas.previous_page_number})
    if consultas.has_next():
        next_url = base_url + urlencode({'page': consultas.next_page_number})

    return render(request, 'listar_consultas.html', {
        'paciente': paciente,
        'consultas': consultas,
        'pagination_info': {
            'has_pages': consultas.has_other_pages(),
            'page': consultas.number,
            'total': consultas.paginator.num_pages,
            'previous_url': previous_url,
            'next_url': next_url,
        }
    })

@login_required
# ✅ Detalhe da consulta
def detalhe_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    problemas = consulta.problemas_saude.all()
    medicamentos = consulta.medicamentos.select_related('problema_saude')
    avaliacoes = Avaliacao.objects.filter(medicamento__in=medicamentos).select_related('medicamento')

    planos_qs = PlanoAtuacao.objects.filter(consulta=consulta).select_related(
        'avaliacao__medicamento__problema_saude',
        'medicamento__problema_saude',
        'problema_saude'
    )

    planos = []
    for plano in planos_qs:
        plano.acompanhamento_form = PlanoAtuacaoAcompanhamentoForm(instance=plano)
        planos.append(plano)

    problemas_com_medicamentos = []
    for problema in problemas:
        meds = medicamentos.filter(problema_saude=problema)
        for m in meds:
            m.avaliacao = Avaliacao.objects.filter(medicamento=m).first()
        problemas_com_medicamentos.append({'problema': problema, 'medicamentos': meds})

    medicamentos_sem_problema = medicamentos.filter(problema_saude__isnull=True)
    for m in medicamentos_sem_problema:
        m.avaliacao = Avaliacao.objects.filter(medicamento=m).first()

    context = {
        'consulta': consulta,
        'problemas': problemas,
        'medicamentos': medicamentos,
        'medicamentos_sem_problema': medicamentos_sem_problema,
        'avaliacoes': avaliacoes,
        'planos': planos,
        'problemas_com_medicamentos': problemas_com_medicamentos,
        'problema_form': ProblemaSaudeForm(),
        'medicamento_form': MedicamentoForm(consulta=consulta),
        'avaliacao_form': AvaliacaoForm(),
        'plano_form': PlanoAtuacaoPlanejamentoForm(consulta=consulta),
        'acompanhamento': PlanoAtuacaoAcompanhamentoForm(),
        'form_problemas_edit': {p.id: ProblemaSaudeForm(instance=p) for p in problemas},
    }
    return render(request, 'detalhe_consulta.html', context)

@login_required
@log_atividade("Cadastrou Problema de Saúde no plano de cuidado!")
# ✅ Adicionar problema
def adicionar_problema_saude(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = ProblemaSaudeForm(request.POST)
        if form.is_valid():
            problema = form.save(commit=False)
            problema.consulta = consulta
            problema.save()
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
    return render(request, 'adicionar_problema_saude.html', {'form': ProblemaSaudeForm(), 'consulta': consulta})

@login_required
@log_atividade("Cadastrou medicamento no plano de cuidado!")
# ✅ Adicionar medicamento
def adicionar_medicamento(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    problemas_saude = consulta.problemas_saude.all()

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, consulta=consulta)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.consulta = consulta

            if request.POST.get('sem_medicamento'):
                medicamento.nome = medicamento.classe = "N/A"
                medicamento.posologia_prescrita = medicamento.posologia_utilizada = medicamento.entendimento_paciente = "N/A"
                medicamento.problema_saude = None
            else:
                ps_id = request.POST.get('problema_saude')
                if ps_id:
                    medicamento.problema_saude = get_object_or_404(ProblemaSaude, id=ps_id, consulta=consulta)

            medicamento.save()
            messages.success(request, 'Medicamento adicionado com sucesso!')
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
    else:
        form = MedicamentoForm(consulta=consulta)

    return render(request, 'adicionar_medicamento.html', {
        'form': form, 'consulta': consulta, 'problemas_saude': problemas_saude
    })

@login_required
@log_atividade("Cadastrou uma avaliação!")
# ✅ Adicionar avaliação
def adicionar_avaliacao(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        medicamento_id = request.POST.get('medicamento')

        if medicamento_id and form.is_valid():
            medicamento = get_object_or_404(Medicamento, id=medicamento_id)

            if hasattr(medicamento, 'avaliacao'):
                messages.error(request, "Este medicamento já possui uma avaliação.")
                return redirect('consulta_detalhe_consulta', consulta_id=medicamento.consulta.id)

            avaliacao = form.save(commit=False)
            avaliacao.medicamento = medicamento
            avaliacao.save()
            messages.success(request, "Avaliação adicionada com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=medicamento.consulta.id)

@login_required
@log_atividade("Cadastrou uma intervenção!")
# ✅ Adicionar plano de atuação
def adicionar_plano_atuacao(request):
    if request.method == 'POST':
        consulta_id = request.POST.get('consulta_id')
        consulta = get_object_or_404(Consulta, id=consulta_id)

        form = PlanoAtuacaoPlanejamentoForm(request.POST, consulta=consulta)

        if form.is_valid():
            plano = form.save(commit=False)
            tipo_relacao = form.cleaned_data['tipo_relacao']

            if tipo_relacao == 'problema_saude':
                plano.problema_saude = form.cleaned_data['problema_saude']
                plano.consulta = plano.problema_saude.consulta
            elif tipo_relacao == 'medicamento':
                plano.medicamento = form.cleaned_data['medicamento']
                plano.consulta = plano.medicamento.consulta
            elif tipo_relacao == 'relato_anamnese':
                plano.relato_anamnese = form.cleaned_data['relato_anamnese']
                plano.consulta = consulta
            elif tipo_relacao == 'avaliacao':
                plano.avaliacao = form.cleaned_data['avaliacao']
                plano.consulta = plano.avaliacao.medicamento.consulta

            plano.save()
            messages.success(request, "Plano de atuação salvo com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)

    return redirect('consulta_listar_consultas', paciente_id=1)

@login_required
@log_atividade("Atualizou o acompanhamento!")
# ✅ Atualizar acompanhamento
def atualizar_acompanhamento(request, plano_id):
    plano = get_object_or_404(PlanoAtuacao, id=plano_id)
    if request.method == 'POST':
        form = PlanoAtuacaoAcompanhamentoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            messages.success(request, "Acompanhamento atualizado com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=plano.consulta.id)
    return render(request, 'atualizar_acompanhamento.html', {'form': PlanoAtuacaoAcompanhamentoForm(instance=plano), 'plano': plano})

@login_required
# ✅ Visualizar consulta
def visualizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    paciente = consulta.paciente
    problemas = consulta.problemas_saude.all()
    medicamentos = Medicamento.objects.filter(problema_saude__in=problemas).select_related('problema_saude')
    avaliacoes = Avaliacao.objects.filter(medicamento__in=medicamentos).select_related('medicamento')
    planos = PlanoAtuacao.objects.filter(consulta=consulta).select_related('avaliacao__medicamento__problema_saude')

    planos_por_avaliacao = defaultdict(list)
    for plano in planos:
        if plano.avaliacao:
            planos_por_avaliacao[plano.avaliacao.id].append(plano)

    return render(request, 'visualizar_consulta.html', {
        'consulta': consulta,
        'paciente': paciente,
        'problemas': problemas,
        'medicamentos': medicamentos,
        'avaliacoes': avaliacoes,
        'planos': planos
    })

@login_required
@log_atividade("Editou!")
# ✅ Editar objeto
def editar(request, model_name, obj_id):
    MODEL_MAP = {
        'problema': (ProblemaSaude, ProblemaSaudeForm, 'consulta'),
        'medicamento': (Medicamento, MedicamentoForm, 'consulta'),
        'avaliacao': (Avaliacao, AvaliacaoForm, 'medicamento__consulta'),
        'plano': (PlanoAtuacao, PlanoAtuacaoPlanejamentoForm, 'consulta'),
    }

    if model_name not in MODEL_MAP:
        return HttpResponseBadRequest("Tipo de objeto desconhecido.")

    model_class, form_class, consulta_path = MODEL_MAP[model_name]
    instance = get_object_or_404(model_class, id=obj_id)
    consulta = instance
    for attr in consulta_path.split("__"):
        consulta = getattr(consulta, attr)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
    else:
        form = form_class(instance=instance)

    return render(request, 'consulta/editar.html', {'form': form, 'form_name': model_name, 'consulta': consulta})


# ✅ Excluir objeto
@login_required
@log_atividade("Excluiu!")
def excluir_objeto(request, model_name, object_id):
    DELETE_MODEL_MAP = {
        'problema': (ProblemaSaude, 'consulta_detalhe_consulta'),
        'medicamento': (Medicamento, 'consulta_detalhe_consulta'),
        'avaliacao': (Avaliacao, 'consulta_detalhe_consulta'),
        'plano': (PlanoAtuacao, 'consulta_detalhe_consulta'),
    }

    if model_name not in DELETE_MODEL_MAP:
        messages.error(request, "Tipo de objeto inválido.")
        return redirect('tela_inicial')

    model_class, redirect_view = DELETE_MODEL_MAP[model_name]
    instance = get_object_or_404(model_class, id=object_id)
    consulta_id = instance.consulta.id if hasattr(instance, 'consulta') else instance.medicamento.consulta.id

    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Item excluído com sucesso.")

    return redirect(redirect_view, consulta_id=consulta_id)

@login_required
# ✅ Avaliação em tela cheia
def avaliacao_fullscreen(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    # Todos os medicamentos da consulta, relacionados ou não a problemas de saúde
    medicamentos = Medicamento.objects.filter(consulta=consulta).select_related('problema_saude')

    # Problemas de saúde associados à consulta
    problemas = consulta.problemas_saude.all()

    # Agrupar medicamentos com problema de saúde
    problemas_com_medicamentos = [
        {
            'problema': problema,
            'medicamentos': medicamentos.filter(problema_saude=problema)
        }
        for problema in problemas
    ]

    # Medicamentos sem problema de saúde relacionado
    medicamentos_sem_problema = medicamentos.filter(problema_saude__isnull=True)

    context = {
        'consulta': consulta,
        'problemas_com_medicamentos': problemas_com_medicamentos,
        'medicamentos_sem_problema': medicamentos_sem_problema,
        'avaliacao_form': AvaliacaoForm(),
    }

    return render(request, 'avaliacao_fullscreen.html', context)



