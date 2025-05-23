import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from login.utils import log_atividade
import paciente
from django.core.exceptions import ObjectDoesNotExist


from .models import  Anamnese, AutonomiaMedicamentos, Doenca, HabitosAlimentares, HistoriaSocial, Medicamento, MedicamentoDoencaPaciente, Paciente, PerfilClinico, Saude
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
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = PacienteForm()
    return render(request, 'cadastrar_paciente.html', {'form': form})

@login_required
@log_atividade("Cadastrou historia social!")
def cadastrar_historia_social(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    if hasattr(anamnese, 'historia'):
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    if request.method == 'POST':
        form = HistoriaSocialForm(request.POST)
        if form.is_valid():
            historia_social = form.save(commit=False)
            historia_social.anamnese = anamnese
            historia_social.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = HistoriaSocialForm()
    return render(request, 'historia_social.html', {'form': form, 'anamnese': anamnese})


@login_required
@log_atividade("Cadastrou Habitos Alimentares!")
def cadastrar_habitos_alimentares(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    if hasattr(anamnese, 'habitos'):
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    if request.method == 'POST':
        form = HabitosAlimentaresForm(request.POST)
        if form.is_valid():
            habitos = form.save(commit=False)
            habitos.anamnese = anamnese
            habitos.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = HabitosAlimentaresForm()
    return render(request, 'habitos_alimentares.html', {'form': form, 'anamnese': anamnese})

@login_required
@log_atividade("Cadastrou Perfil Clinico!")
def cadastrar_perfil_clinico(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    if hasattr(anamnese, 'perfil'):
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    if request.method == 'POST':
        form = PerfilClinicoForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.anamnese = anamnese
            perfil.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = PerfilClinicoForm()
    return render(request, 'perfil_clinico.html', {'form': form, 'anamnese': anamnese})

@login_required
@log_atividade("Cadastrou Autonomia Medicamentosa!")
def cadastrar_autonomia_medicamentos(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    if hasattr(anamnese, 'autonomia'):
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    if request.method == 'POST':
        form = AutonomiaMedicamentosForm(request.POST)
        if form.is_valid():
            autonomia = form.save(commit=False)
            autonomia.anamnese = anamnese
            autonomia.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = AutonomiaMedicamentosForm()
    return render(request, 'autonomia_medicamentos.html', {'form': form, 'anamnese': anamnese})


@login_required
@log_atividade("Cadastrou Percp Saúde")
def saude(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    if hasattr(anamnese, 'saude'):
        return redirect('paciente_detail', anamnese_id=anamnese.id)

    if request.method == 'POST':
        form = SaudeForm(request.POST)
        if form.is_valid():
            saude = form.save(commit=False)
            saude.anamnese = anamnese
            saude.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = SaudeForm()
    return render(request, 'adicionar_saude.html', {'form': form, 'anamnese': anamnese})

@login_required
@login_required
@log_atividade("Cadastrou doença e medicamentos")
def associar_doencas_medicamentos(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)
    paciente = anamnese.paciente  # pode ser usado no template

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos.'}, status=400)

        # Doenças com medicamentos
        associacoes = data.get('associacoes', [])

        for associacao in associacoes:
            doenca_nome = associacao.get('doenca')
            medicamentos_nomes = associacao.get('medicamentos', [])
            observacao = associacao.get('observacao', '')

            if not doenca_nome:
                continue  # Se não tiver nome da doença, ignora

            doenca, _ = Doenca.objects.get_or_create(nome=doenca_nome)

            if medicamentos_nomes:
                for medicamento_nome in medicamentos_nomes:
                    medicamento, _ = Medicamento.objects.get_or_create(nome=medicamento_nome)

                    obj, created = MedicamentoDoencaPaciente.objects.get_or_create(
                        anamnese=anamnese,
                        paciente=paciente,
                        medicamento=medicamento,
                        doenca=doenca
                    )
                    obj.observacao = observacao
                    obj.save()
            else:
                # Doença sem medicamento
                MedicamentoDoencaPaciente.objects.get_or_create(
                    anamnese=anamnese,
                    paciente=paciente,
                    doenca=doenca,
                    medicamento=None,  # Se quiser permitir null=True, senão precisa ajustar o modelo
                    defaults={'observacao': observacao}
                )

        # Doenças isoladas
        for doenca_nome in data.get('doencas_isoladas', []):
            if doenca_nome:
                doenca, _ = Doenca.objects.get_or_create(nome=doenca_nome)
                MedicamentoDoencaPaciente.objects.get_or_create(
                    anamnese=anamnese,
                    paciente=paciente,
                    doenca=doenca,
                    medicamento=None
                )

        # Medicamentos isolados
        for med in data.get('medicamentos_isolados', []):
            nome = med.get('nome')
            observacao = med.get('observacao', '')
            if nome:
                medicamento, _ = Medicamento.objects.get_or_create(nome=nome)
                MedicamentoDoencaPaciente.objects.get_or_create(
                    anamnese=anamnese,
                    paciente=paciente,
                    medicamento=medicamento,
                    doenca=None,  # Se quiser permitir null=True, senão precisa ajustar o modelo
                    defaults={'observacao': observacao}
                )

        return JsonResponse({
            'sucesso': True,
            'message': 'Associações salvas com sucesso.',
            'redirect_url': reverse('paciente_detail', kwargs={'pk': paciente.id})
        })

    # GET
    return render(request, 'associar_doencas_medicamentos.html', {
        'anamnese': anamnese,
        'paciente': paciente
    })


@login_required
@log_atividade("Cadastrou medicamento!")
@require_POST
def adicionar_medicamento(request, anamnese_id):
    nome_medicamento = request.POST.get('nome')
    doenca_id = request.POST.get('doenca_id')

    if nome_medicamento and doenca_id:
        try:
            doenca = Doenca.objects.get(id=doenca_id)
            anamnese = get_object_or_404(Anamnese, id=anamnese_id)
            paciente = anamnese.paciente
        except (Doenca.DoesNotExist, Anamnese.DoesNotExist):
            return JsonResponse({'error': 'Doença ou Anamnese não encontrada!'}, status=404)

        medicamento, _ = Medicamento.objects.get_or_create(nome=nome_medicamento)

        MedicamentoDoencaPaciente.objects.get_or_create(
            paciente=paciente,
            anamnese=anamnese,
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

    doenca, created = Doenca.objects.get_or_create(nome=nome)
    return JsonResponse({"id": doenca.id, "nome": doenca.nome})

@login_required
@log_atividade("Criou uma anamnese!")
def criar_anamnese(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    Anamnese.objects.create(paciente=paciente)
    return redirect('paciente_detail', pk=paciente.id)


@login_required
def detalhe_anamnese(request, anamnese_id):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)
    return render(request, 'paciente_detail.html', {
        'anamnese': anamnese,
        'paciente': anamnese.paciente,
    })

@login_required
@log_atividade("Removeu um bloco da anamnese")
@log_atividade("Removeu um bloco da anamnese")
def excluir_anamnese_bloco(request, anamnese_id, bloco):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    # Mapeia o nome do bloco para o atributo relacionado
    bloco_map = {
        'historia': 'historia',
        'habitos': 'habitos',
        'perfil': 'perfil',
        'autonomia': 'autonomia',
        'saude': 'saude',
    }

    attr = bloco_map.get(bloco)
    if not attr:
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    try:
        objeto = getattr(anamnese, attr)
        objeto.delete()
    except ObjectDoesNotExist:
        pass  # Não existe, então ignora

    return redirect('paciente_detail', pk=anamnese.paciente.id)

@login_required
@log_atividade("Editou um bloco da anamnese")
def editar_anamnese_bloco(request, anamnese_id, bloco):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)

    blocos = {
        'historia': {'model': HistoriaSocial, 'form': HistoriaSocialForm, 'related': 'historia'},
        'habitos': {'model': HabitosAlimentares, 'form': HabitosAlimentaresForm, 'related': 'habitos'},
        'perfil': {'model': PerfilClinico, 'form': PerfilClinicoForm, 'related': 'perfil'},
        'autonomia': {'model': AutonomiaMedicamentos, 'form': AutonomiaMedicamentosForm, 'related': 'autonomia'},
        'saude': {'model': Saude, 'form': SaudeForm, 'related': 'saude'},
    }

    bloco_info = blocos.get(bloco)
    if not bloco_info:
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    # Pega instância do objeto relacionado, ou 404
    instance = getattr(anamnese, bloco_info['related'], None)
    if not instance:
        return redirect('paciente_detail', pk=anamnese.paciente.id)

    FormClass = bloco_info['form']
    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('paciente_detail', pk=anamnese.paciente.id)
    else:
        form = FormClass(instance=instance)

    templates_map = {
    'historia': 'historia_social.html',
    'habitos': 'habitos_alimentares.html',
    'perfil': 'perfil_clinico.html',
    'autonomia': 'autonomia_medicamentos.html',
    'saude': 'adicionar_saude.html',
}
    return render(request, templates_map[bloco], {'form': form, 'anamnese': anamnese})

@login_required
@log_atividade("Excluiu um bloco da anamnese ou a anamnese completa")
@require_POST
def excluir_anamnese_bloco(request, anamnese_id, bloco):
    anamnese = get_object_or_404(Anamnese, id=anamnese_id)
    paciente = anamnese.paciente

    if bloco == 'tudo':
        anamnese.delete()
        return redirect('paciente_detail', pk=paciente.id)

    # Mapeamento dos blocos normais
    blocos = {
        'historia': 'historia',
        'habitos': 'habitos',
        'perfil': 'perfil',
        'autonomia': 'autonomia',
        'saude': 'saude',
    }

    if bloco == 'doencas_medicamentos':
        # Exclui todos os medicamentos associados
        anamnese.medicamentos_doenca.all().delete()
    elif bloco in blocos:
        attr = blocos[bloco]
        try:
            objeto = getattr(anamnese, attr)
            objeto.delete()
        except ObjectDoesNotExist:
            # O bloco não existe, então nada a fazer
            pass
    else:
        # Bloco inválido, opcional: retornar erro ou apenas redirecionar
        pass

    return redirect('paciente_detail', pk=paciente.id)


@login_required
@log_atividade("Editou um paciente!")
def paciente_detail(request, pk):
    paciente = get_object_or_404(Paciente, id=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('paciente_detail', pk=paciente.id)
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'detalhe_paciente.html', {
        'paciente': paciente,
        'form': form,
        'modo_edicao': request.GET.get('editar') == '1'
    })
