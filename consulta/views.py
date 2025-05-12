# views.py
from collections import defaultdict
from urllib.parse import urlencode
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Consulta, ProblemaSaude, Medicamento, Avaliacao, PlanoAtuacao
from .forms import (
    ConsultaForm, PlanoAtuacaoAcompanhamentoForm, PlanoAtuacaoPlanejamentoForm, ProblemaSaudeForm, MedicamentoForm,
    AvaliacaoForm
)
from paciente.models import Paciente
from django.contrib import messages
from django.core.paginator import Paginator

# Criar nova consulta
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

# Listar todas as consultas de um paciente
def listar_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = paciente.consultas.all()
    return render(request, 'listar_consultas.html', {'paciente': paciente, 'consultas': consultas})

# Detalhe da consulta
def detalhe_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    problemas = ProblemaSaude.objects.filter(consulta=consulta)
    medicamentos = Medicamento.objects.filter(problema_saude__in=problemas).select_related('problema_saude')
    avaliacoes = Avaliacao.objects.filter(medicamento__in=medicamentos).select_related('medicamento')
    avaliacao_principal = avaliacoes.first() if avaliacoes.exists() else None

    # ✅ Buscar todos os planos da consulta (não apenas da primeira avaliação)
    planos_qs = PlanoAtuacao.objects.filter(
        consulta=consulta
    ).select_related('avaliacao__medicamento__problema_saude')

    # ✅ Adiciona o form de acompanhamento para cada plano
    planos = []
    for plano in planos_qs:
        plano.acompanhamento_form = PlanoAtuacaoAcompanhamentoForm(instance=plano)
        planos.append(plano)

    # ✅ Organiza os problemas com medicamentos associados
    problemas_com_medicamentos = []
    for problema in problemas:
        medicamentos_relacionados = problema.medicamentos.all()
        for medicamento in medicamentos_relacionados:
            medicamento.avaliacao = Avaliacao.objects.filter(medicamento=medicamento).first()
        problemas_com_medicamentos.append({
            'problema': problema,
            'medicamentos': medicamentos_relacionados
        })

    form_problemas_edit = {}
    for problema in problemas:
        form_problemas_edit[problema.id] = ProblemaSaudeForm(instance=problema)

    context = {
        'consulta': consulta,
        'problemas': problemas,
        'medicamentos': medicamentos,
        'avaliacoes': avaliacoes,
        'avaliacao': avaliacao_principal,  # usada para exibir nome ou form
        'planos': planos,                  # usado para {% regroup planos by avaliacao %}
        'problema_form': ProblemaSaudeForm(),
        'medicamento_form': MedicamentoForm(consulta=consulta),
        'avaliacao_form': AvaliacaoForm(),
        'plano_form': PlanoAtuacaoPlanejamentoForm(consulta=consulta),
        'acompanhamento': PlanoAtuacaoAcompanhamentoForm(),
        'problemas_com_medicamentos': problemas_com_medicamentos,
        'form_problemas_edit': form_problemas_edit,
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
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
    else:
        form = ProblemaSaudeForm()
    return render(request, 'adicionar_problema_saude.html', {'form': form, 'consulta': consulta})


# Adicionar medicamento
def adicionar_medicamento(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Buscando problemas de saúde associados à consulta
    problemas_saude = ProblemaSaude.objects.filter(consulta=consulta)
    print(f'Problemas de saúde da consulta {consulta_id}: {problemas_saude}')
    
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, consulta=consulta)  # Passando a consulta para o formulário
        problema_saude_id = request.POST.get('problema_saude')  # Pegando o ID do problema de saúde selecionado
        print(f'Problema selecionado: {problema_saude_id}')
        
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.consulta = consulta  # Associando o medicamento à consulta
            print(f'Medicamento associado à consulta: {medicamento.consulta}')
            
            if problema_saude_id:
                try:
                    problema_saude = ProblemaSaude.objects.get(id=problema_saude_id, consulta=consulta)  # Associando o problema de saúde ao medicamento
                    medicamento.problema_saude = problema_saude
                    print(f'Medicamento associado ao problema de saúde: {medicamento.problema_saude}')
                except ProblemaSaude.DoesNotExist:
                    # Adicionando uma mensagem de erro para o usuário
                    messages.error(request, 'Problema de saúde não encontrado para esta consulta.')
                    return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
            
            medicamento.save()
            messages.success(request, 'Medicamento adicionado com sucesso!')
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = MedicamentoForm(consulta=consulta)  # Passando a consulta ao formulário

    # Passando os problemas de saúde para o template
    return render(request, 'adicionar_medicamento.html', {
        'form': form,
        'consulta': consulta,
        'problemas_saude': problemas_saude,  # Passando os problemas de saúde para o template
    })
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
                return redirect('consulta_detalhe_consulta', consulta_id=medicamento.problema_saude.consulta.id)

            avaliacao = form.save(commit=False)
            avaliacao.medicamento = medicamento
            avaliacao.save()
            messages.success(request, "Avaliação adicionada com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=medicamento.problema_saude.consulta.id)


# Adicionar plano de atuação com seleção da avaliação no formulário
def adicionar_plano_atuacao(request):
    if request.method == 'POST':
        form = PlanoAtuacaoPlanejamentoForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            # Definir a consulta com base na avaliação selecionada
            plano.consulta = plano.avaliacao.medicamento.problema_saude.consulta
            plano.save()
            return redirect('consulta_detalhe_consulta', consulta_id=plano.consulta.id)
    else:
        return redirect('home')  # ou exibir erro/404

    return render(request, 'adicionar_plano_atuacao.html', {'form': form})


def atualizar_acompanhamento(request, plano_id):
    plano = get_object_or_404(PlanoAtuacao, id=plano_id)
    if request.method == 'POST':
        form = PlanoAtuacaoAcompanhamentoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            messages.success(request, "Acompanhamento atualizado com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=plano.consulta.id)
    else:
        form = PlanoAtuacaoAcompanhamentoForm(instance=plano)

    return render(request, 'atualizar_acompanhamento.html', {
        'form': form,
        'plano': plano,
    })


def visualizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    paciente = consulta.paciente

    problemas = consulta.problemas_saude.all()
    medicamentos = Medicamento.objects.filter(problema_saude__in=problemas).select_related('problema_saude')
    avaliacoes = Avaliacao.objects.filter(medicamento__in=medicamentos).select_related('medicamento')
    planos = PlanoAtuacao.objects.filter(consulta=consulta).select_related('avaliacao__medicamento__problema_saude')

    # ✅ Agrupar por avaliacao.id
    planos_por_avaliacao = defaultdict(list)
    avaliacoes_por_id = {a.id: a for a in avaliacoes}

    for plano in planos:
        if plano.avaliacao:
            planos_por_avaliacao[plano.avaliacao.id].append(plano)

    context = {
        'consulta': consulta,
        'paciente': paciente,
        'problemas': problemas,
        'medicamentos': medicamentos,
        'avaliacoes': avaliacoes,
        'avaliacoes_por_id': avaliacoes_por_id,  
        'planos': planos

    }

    return render(request, 'visualizar_consulta.html', context)

def editar_problema_saude(request, problema_id):
    problema = get_object_or_404(ProblemaSaude, id=problema_id)

    if request.method == 'POST':
        form = ProblemaSaudeForm(request.POST, instance=problema)
        if form.is_valid():
            form.save()
            return redirect('consulta_detalhe_consulta', consulta_id=problema.consulta.id)
    else:
        form = ProblemaSaudeForm(instance=problema)

    return render(request, 'editar_problema_saude.html', {
        'form': form,
        'problema': problema,
    })



DELETE_MODEL_MAP = {
    'problema': (ProblemaSaude, 'consulta_detalhe_consulta'),
    'medicamento': (Medicamento, 'consulta_detalhe_consulta'),
    'avaliacao': (Avaliacao, 'consulta_detalhe_consulta'),
    'plano': (PlanoAtuacao, 'consulta_detalhe_consulta'),
}

@login_required
def excluir_objeto(request, model_name, object_id):
    if model_name not in DELETE_MODEL_MAP:
        messages.error(request, "Tipo de objeto inválido.")
        return redirect('tela_inicial')

    model_class, redirect_view = DELETE_MODEL_MAP[model_name]
    instance = get_object_or_404(model_class, id=object_id)

    # Identifica a consulta para redirecionamento
    consulta_id = instance.consulta.id if hasattr(instance, 'consulta') else instance.avaliacao.consulta.id

    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Item excluído com sucesso.")
    
    return redirect(redirect_view, consulta_id=consulta_id)


def editar(request, model_name, obj_id):
    MODEL_MAP = {
        'problema': (ProblemaSaude, ProblemaSaudeForm, 'consulta'),
        'medicamento': (Medicamento, MedicamentoForm, 'consulta'),
        'avaliacao': (Avaliacao, AvaliacaoForm, 'consulta'),
        'plano': (PlanoAtuacao, PlanoAtuacaoPlanejamentoForm, 'avaliacao__medicamento__problema_saude__consulta'),

    }

    if model_name not in MODEL_MAP:
        return HttpResponseBadRequest("Tipo de objeto desconhecido.")

    model_class, form_class, consulta_path = MODEL_MAP[model_name]
    instance = get_object_or_404(model_class, id=obj_id)

    # Obter consulta associada via atributo direto ou encadeado
    consulta = instance
    for attr in consulta_path.split("__"):
        consulta = getattr(consulta, attr)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            print(f"Objeto {model_name} editado com sucesso.")
            return redirect('consulta_detalhe_consulta', consulta_id=consulta.id)
        else:
            # ⚠️ Adicione este bloco para debug
            print("Erros no formulário de edição:", form.errors)
    else:
        form = form_class(instance=instance)

    # Sempre retorne algo
    return render(request, 'consulta/editar.html', {
        'form': form,
        'form_name': model_name,
        'consulta': consulta,
    })

def avaliacao_fullscreen(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Reaproveita os dados já utilizados no detalhe
    problemas = ProblemaSaude.objects.filter(consulta=consulta)
    medicamentos = Medicamento.objects.filter(consulta=consulta)
    problemas_com_medicamentos = [
        {
            'problema': problema,
            'medicamentos': medicamentos.filter(problema_saude=problema)
        }
        for problema in problemas
    ]

    from .forms import AvaliacaoForm  # ou ajuste o caminho

    return render(request, 'avaliacao_fullscreen.html', {
        'consulta': consulta,
        'problemas_com_medicamentos': problemas_com_medicamentos,
        'avaliacao_form': AvaliacaoForm(),
    })

def listar_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas_list = Consulta.objects.filter(paciente=paciente).order_by('-data_consulta')

    paginator = Paginator(consultas_list, 6)  # 6 por página
    page_number = request.GET.get('page')
    consultas = paginator.get_page(page_number)

    # Construir URLs de navegação
    base_url = '?'
    previous_url = next_url = None
    if consultas.has_previous():
        previous_url = base_url + urlencode({'page': consultas.previous_page_number})
    if consultas.has_next():
        next_url = base_url + urlencode({'page': consultas.next_page_number})

    context = {
        'paciente': paciente,
        'consultas': consultas,
        'pagination_info': {
            'has_pages': consultas.has_other_pages(),
            'page': consultas.number,
            'total': consultas.paginator.num_pages,
            'previous_url': previous_url,
            'next_url': next_url,
        }
    }
    return render(request, 'listar_consultas.html', context)
