from django.shortcuts import render
from django.db.models import Count, F, Case, When, Value, CharField
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from consulta.models import Consulta, Medicamento, ProblemaSaude, Avaliacao, PlanoAtuacao
from paciente.models import Paciente

# Função para agrupar consultas por paciente
def agrupar_consultas_por_paciente(consultas):
    consultas_por_paciente = {}
    for consulta in consultas:
        paciente_id = consulta.paciente.id
        if paciente_id not in consultas_por_paciente:
            consultas_por_paciente[paciente_id] = {
                'paciente': consulta.paciente,
                'consultas': []
            }
        consultas_por_paciente[paciente_id]['consultas'].append(consulta)
    return consultas_por_paciente

# Função para calcular o tempo desde a última consulta
def calcular_tempo_ultima_consulta(paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente).order_by('-data_consulta')
    
    if consultas.exists():
        ultima_consulta = consultas.first()  # Consulta mais recente
        ultima_consulta_data = ultima_consulta.data_consulta
        
        tempo_desde_ultima_consulta = (timezone.now().date() - ultima_consulta_data).days
    else:
        tempo_desde_ultima_consulta = None
    
    return tempo_desde_ultima_consulta

# Função para buscar medicamentos prescritos
def buscar_medicamentos_prescritos():
    return Medicamento.objects.annotate(
        total_prescricoes=Count('consulta__medicamentos')  # Relacionamento com consulta
    ).prefetch_related('consulta__paciente', 'consulta__problemas_saude')

# Função para buscar detalhes dos medicamentos
def buscar_detalhes_medicamentos(medicamentos):
    medicamentos_detalhes = {}
    for medicamento in medicamentos:
        consultas_medicamento = Consulta.objects.filter(medicamentos=medicamento).prefetch_related('paciente', 'problemas_saude')
        pacientes_detalhes = []
        for consulta in consultas_medicamento:
            paciente = consulta.paciente
            problemas_saude = consulta.problemas_saude.all()
            pacientes_detalhes.append({
                'paciente': paciente,
                'problemas_saude': problemas_saude
            })
        medicamentos_detalhes[medicamento] = pacientes_detalhes
    return medicamentos_detalhes

# Função principal para exibir o dashboard
def dashboard(request):
    # Parâmetros de filtro
    filtro_inicio = request.GET.get('inicio', None)
    filtro_fim = request.GET.get('fim', None)
    filtro_problema = request.GET.get('problema', None)
    filtro_medicamento = request.GET.get('medicamento', None)

    # Filtro de data
    if filtro_inicio and filtro_fim:
        filtro_inicio = timezone.datetime.strptime(filtro_inicio, '%Y-%m-%d')
        filtro_fim = timezone.datetime.strptime(filtro_fim, '%Y-%m-%d')
        consultas = Consulta.objects.filter(data_consulta__range=[filtro_inicio, filtro_fim])
    else:
        consultas = Consulta.objects.all()

    # Filtro por problemas de saúde
    if filtro_problema:
        consultas = consultas.filter(problemas_saude__problema=filtro_problema)

    # Filtro por medicamentos prescritos
    if filtro_medicamento:
        consultas = consultas.filter(medicamentos__nome=filtro_medicamento)

    # Total de Consultas realizadas
    total_consultas = consultas.count()

    # Contagem de Medicamentos Prescritos (prescrita=True)
    medicamentos_prescritos = Medicamento.objects.filter(prescrita=True).count()

    # Contagem de Medicamentos Não Prescritos (prescrita=False)
    medicamentos_nao_prescritos = Medicamento.objects.filter(prescrita=False).count()

    # Contagem de Problemas de Saúde
    problemas_saude_count = ProblemaSaude.objects.count()

    # Contagem de Problemas de Saúde mais Comuns (exemplo: 'Hipertensão', 'Diabetes')
    problemas_comuns = ProblemaSaude.objects.filter(problema__in=['Hipertensão', 'Diabetes']).count()

    # Contagem de RNM Resolvido (rnm_resolvido=True no PlanoAtuacao)
    rnm_resolvido = PlanoAtuacao.objects.filter(rnm_resolvido=True).count()

    # Consultas por Paciente
    consultas_por_paciente = consultas.values('paciente__nome').annotate(consultas=Count('id')).order_by('-consultas')

    # Buscar medicamentos e contar a quantidade prescrita para cada paciente
    medicamentos_detalhes = Medicamento.objects.values('nome').annotate(count=Count('id')).order_by('-count')

    # Preparar dados para gráficos
    pacientes_nome = [consulta['paciente__nome'] for consulta in consultas_por_paciente]
    consultas_count = [consulta['consultas'] for consulta in consultas_por_paciente]

    # Preparar dados de medicamentos para gráficos
    medicamentos_nome = [med['nome'] for med in medicamentos_detalhes]
    medicamentos_count = [med['count'] for med in medicamentos_detalhes]

    # Obter lista de problemas de saúde e medicamentos para os filtros
    lista_problemas = ProblemaSaude.objects.all()
    lista_medicamentos = Medicamento.objects.all()

    return render(request, 'relatorios/dashboard.html', {
        'total_consultas': total_consultas,
        'medicamentos_prescritos': medicamentos_prescritos,
        'medicamentos_nao_prescritos': medicamentos_nao_prescritos,
        'problemas_saude_count': problemas_saude_count,
        'problemas_comuns': problemas_comuns,
        'rnm_resolvido': rnm_resolvido,
        'consultas_por_paciente': consultas_por_paciente,
        'medicamentos_detalhes': medicamentos_detalhes,
        'consultas_por_paciente_data': consultas_count,
        'pacientes_nome': pacientes_nome,
        'medicamentos_nome': medicamentos_nome,
        'medicamentos_count': medicamentos_count,
        'problemas_list': lista_problemas,
        'medicamentos_list': lista_medicamentos,
        'filtro_inicio': filtro_inicio,
        'filtro_fim': filtro_fim,
        'filtro_problema': filtro_problema,
        'filtro_medicamento': filtro_medicamento,
    })
