import json
import re
from django.shortcuts import render
from django.db.models import Count, Min, Max, Avg
from datetime import date
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from paciente.models import Paciente, Doenca as DoencaPaciente, Medicamento as MedicamentoPaciente
from consulta.models import Avaliacao, Consulta, ProblemaSaude, PlanoAtuacao, Medicamento as MedicamentoConsulta


def limpar_nome_aba(nome):
    nome_limpo = re.sub(r'[\\/*?:\[\]]', '', nome)
    return nome_limpo[:31]

def exportar_dashboard(request):
    exportar = request.GET.getlist('exportar')
    formato = request.GET.get('formato', 'xml')

    if formato == 'xml':
        root = ET.Element('Dashboard')

        if 'pacientes' in exportar:
            pacientes_tag = ET.SubElement(root, 'Pacientes')
            pacientes = Paciente.objects.all()
            for p in pacientes:
                paciente = ET.SubElement(pacientes_tag, 'Paciente')
                ET.SubElement(paciente, 'Nome').text = p.nome
                ET.SubElement(paciente, 'Nascimento').text = str(p.data_nascimento)
                ET.SubElement(paciente, 'Telefone').text = p.telefone or "Não Informado"
                ET.SubElement(paciente, 'Bairro').text = p.bairro or "Não Informado"
                ET.SubElement(paciente, 'Municipio').text = p.municipio or "Não Informado"

        if 'consultas' in exportar:
            consultas_tag = ET.SubElement(root, 'Consultas')
            consultas = Consulta.objects.all()
            for c in consultas:
                consulta = ET.SubElement(consultas_tag, 'Consulta')
                ET.SubElement(consulta, 'Paciente').text = c.paciente.nome
                ET.SubElement(consulta, 'DataConsulta').text = str(c.data_consulta)
                ET.SubElement(consulta, 'MotivoConsulta').text = c.motivo_consulta or "Não informado"
                ET.SubElement(consulta, 'Evolucao').text = c.evolucao or "Não informado"

        if 'intervencoes' in exportar:
            intervencoes_tag = ET.SubElement(root, 'Intervencoes')
            planos = PlanoAtuacao.objects.exclude(classificacao_intervencao__isnull=True)
            for p in planos:
                intervencao = ET.SubElement(intervencoes_tag, 'Intervencao')
                ET.SubElement(intervencao, 'Paciente').text = p.consulta.paciente.nome
                ET.SubElement(intervencao, 'DataConsulta').text = str(p.consulta.data_consulta)
                ET.SubElement(intervencao, 'Classificacao').text = p.classificacao_intervencao or "Não informado"
                ET.SubElement(intervencao, 'Resultado').text = p.resultado or "Não informado"

        if 'prms' in exportar:
            prms_tag = ET.SubElement(root, 'PRMs')
            avaliacoes = Avaliacao.objects.select_related('medicamento__consulta__paciente').all()
            for a in avaliacoes:
                prm = ET.SubElement(prms_tag, 'PRM')
                ET.SubElement(prm, 'Paciente').text = a.medicamento.consulta.paciente.nome
                ET.SubElement(prm, 'Medicamento').text = a.medicamento.nome
                ET.SubElement(prm, 'Necessidade').text = str(a.necessidade) if a.necessidade is not None else "Não informado"
                ET.SubElement(prm, 'Seguranca').text = str(a.seguranca) if a.seguranca is not None else "Não informado"
                ET.SubElement(prm, 'Efetividade').text = str(a.efetividade) if a.efetividade is not None else "Não informado"

        response = HttpResponse(content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="dashboard_farmacia.xml"'
        tree = ET.ElementTree(root)
        tree.write(response, encoding='unicode')
        return response

    elif formato == 'xlsx':
        wb = Workbook()
        default_sheet = wb.active
        wb.remove(default_sheet)

        def style_header(ws):
            for cell in ws[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')

        if 'pacientes' in exportar:
            ws = wb.create_sheet(limpar_nome_aba('Pacientes'))
            ws.append(['Nome', 'Nascimento', 'Telefone', 'Bairro', 'Municipio'])
            style_header(ws)
            pacientes = Paciente.objects.all()
            for p in pacientes:
                ws.append([p.nome, str(p.data_nascimento), p.telefone or "Não Informado", p.bairro or "Não Informado", p.municipio or "Não Informado"])

        if 'consultas' in exportar:
            ws = wb.create_sheet(limpar_nome_aba('Consultas'))
            ws.append(['Paciente', 'DataConsulta', 'MotivoConsulta', 'Evolucao'])
            style_header(ws)
            consultas = Consulta.objects.all()
            for c in consultas:
                ws.append([c.paciente.nome, str(c.data_consulta), c.motivo_consulta or "Não informado", c.evolucao or "Não informado"])

        if 'intervencoes' in exportar:
            ws = wb.create_sheet(limpar_nome_aba('Intervencoes'))
            ws.append(['Paciente', 'DataConsulta', 'Classificacao', 'Resultado'])
            style_header(ws)
            planos = PlanoAtuacao.objects.exclude(classificacao_intervencao__isnull=True)
            for p in planos:
                ws.append([p.consulta.paciente.nome, str(p.consulta.data_consulta), p.classificacao_intervencao or "Não informado", p.resultado or "Não informado"])

        if 'prms' in exportar:
            ws = wb.create_sheet(limpar_nome_aba('PRMs'))
            ws.append(['Paciente', 'Medicamento', 'Necessidade', 'Seguranca', 'Efetividade'])
            style_header(ws)
            avaliacoes = Avaliacao.objects.select_related('medicamento__consulta__paciente').all()
            for a in avaliacoes:
                ws.append([
                    a.medicamento.consulta.paciente.nome,
                    a.medicamento.nome,
                    str(a.necessidade) if a.necessidade is not None else "Não informado",
                    str(a.seguranca) if a.seguranca is not None else "Não informado",
                    str(a.efetividade) if a.efetividade is not None else "Não informado"
                ])

        if not wb.sheetnames:
            ws = wb.create_sheet('Sem Dados')
            ws.append(['Nenhum dado selecionado'])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="dashboard_farmacia.xlsx"'
        wb.save(response)
        return response

    


def dashboard_clinico(request):


    # Filtros Recebidos
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    doenca_paciente_id = request.GET.get('doenca_paciente')
    medicamento_paciente_id = request.GET.get('medicamento_paciente')
    faixa_etaria_filtro = request.GET.get('faixa_etaria')
    classe_medicamento_filtro = request.GET.get('classe_medicamento')
    problema_saude_filtro = request.GET.get('problema_saude')

    # Bases Iniciais
    pacientes = Paciente.objects.all()
    consultas = Consulta.objects.all()
    planos = PlanoAtuacao.objects.all()

    # Aplicar Filtros
    if data_inicio and data_fim:
        consultas = consultas.filter(data_consulta__range=[data_inicio, data_fim])

    if doenca_paciente_id:
        pacientes = pacientes.filter(doencas__id=doenca_paciente_id)

    if medicamento_paciente_id:
        pacientes = pacientes.filter(medicamentos__id=medicamento_paciente_id)

    if faixa_etaria_filtro:
        try:
            idade_min, idade_max = map(int, faixa_etaria_filtro.split('-'))
            hoje = date.today()
            data_max = hoje.replace(year=hoje.year - idade_min)
            data_min = hoje.replace(year=hoje.year - idade_max - 1)
            pacientes = pacientes.filter(data_nascimento__range=(data_min, data_max))
        except:
            pass

    consultas = consultas.filter(paciente__in=pacientes)
    planos = planos.filter(consulta__in=consultas)

    problemas_consulta = ProblemaSaude.objects.filter(consulta__in=consultas)
    medicamentos_consulta = MedicamentoConsulta.objects.filter(consulta__in=consultas)

    if classe_medicamento_filtro:
        medicamentos_consulta = medicamentos_consulta.filter(classe__icontains=classe_medicamento_filtro)

    if problema_saude_filtro:
        problemas_consulta = problemas_consulta.filter(problema__icontains=problema_saude_filtro)

    # Cards (Indicadores)
    total_pacientes = pacientes.count()
    total_consultas = consultas.count()
    total_intervencoes = planos.exclude(classificacao_intervencao__isnull=True).count()
    total_prm = Avaliacao.objects.filter(medicamento__consulta__in=consultas).count()
    rnm_resolvido = planos.filter(rnm_resolvido=True).count()

    media_intervencoes = planos.values('consulta__paciente').annotate(total=Count('id')).aggregate(avg=Avg('total'))['avg'] or 0
    media_medicamentos = medicamentos_consulta.values('consulta__paciente').annotate(total=Count('id')).aggregate(avg=Avg('total'))['avg'] or 0
    media_prm = Avaliacao.objects.filter(medicamento__consulta__in=consultas).values('medicamento__consulta__paciente').annotate(total=Count('id')).aggregate(avg=Avg('total'))['avg'] or 0
    media_consultas_paciente = consultas.values('paciente').annotate(total=Count('id')).aggregate(avg=Avg('total'))['avg'] or 0

    esquecem = pacientes.filter(autonomia_medicamentos__esquecimentos='sim').count()

    # Gráficos
    grupos = [(0,18), (19,40), (41,60), (61,120)]
    labels_faixa = ["0-18", "19-40", "41-60", "60+"]
    valores_faixa = []
    hoje = date.today()
    for min_age, max_age in grupos:
        data_max = hoje.replace(year=hoje.year - min_age)
        data_min = hoje.replace(year=hoje.year - max_age - 1)
        valores_faixa.append(pacientes.filter(data_nascimento__range=(data_min, data_max)).count())

    genero_data = pacientes.values('genero').annotate(total=Count('id'))
    labels_genero = [g['genero'] or 'Não informado' for g in genero_data]
    valores_genero = [g['total'] for g in genero_data]

    doencas_count = DoencaPaciente.objects.filter(pacientes__in=pacientes).annotate(total=Count('pacientes')).order_by('-total')[:10]
    labels_doenca = [d.nome for d in doencas_count]
    valores_doenca = [d.total for d in doencas_count]

    intervencao_data = planos.values('classificacao_intervencao').annotate(total=Count('id'))
    labels_inter = [i['classificacao_intervencao'] or 'Não informado' for i in intervencao_data]
    valores_inter = [i['total'] for i in intervencao_data]

    # Relatórios auxiliares
    armazenamento = pacientes.values('autonomia_medicamentos__local_guarda').annotate(total=Count('id'))
    descarte = pacientes.values('autonomia_medicamentos__forma_descarte').annotate(total=Count('id'))
    rnm_tipos = planos.values('registro_intervencao').annotate(total=Count('id'))

    intervalo_consultas = Consulta.objects.values('paciente__nome').annotate(
        primeira=Min('data_consulta'),
        ultima=Max('data_consulta'),
        numero_consultas=Count('id')  # 👈 Aqui soma quantas consultas tem
    )

    percepcao = pacientes.values('perfil_clinico__percepcao_saude').annotate(total=Count('id')).order_by('perfil_clinico__percepcao_saude')

    context = {
        'labels_faixa': json.dumps(labels_faixa),
        'valores_faixa': json.dumps(valores_faixa),
        'labels_genero': json.dumps(labels_genero),
        'valores_genero': json.dumps(valores_genero),
        'labels_doenca': json.dumps(labels_doenca),
        'valores_doenca': json.dumps(valores_doenca),
        'labels_inter': json.dumps(labels_inter),
        'valores_inter': json.dumps(valores_inter),

        'total_pacientes': total_pacientes,
        'total_consultas': total_consultas,
        'total_intervencoes': total_intervencoes,
        'total_prm': total_prm,
        'rnm_resolvido': rnm_resolvido,
        'media_intervencoes': round(media_intervencoes, 1),
        'media_medicamentos': round(media_medicamentos, 1),
        'media_prm': round(media_prm, 1),
        'media_consultas_paciente': round(media_consultas_paciente, 1),
        'esquecem': esquecem,

        'armazenamento': armazenamento,
        'descarte': descarte,
        'rnm_tipos': rnm_tipos,
        'intervalo_consultas': intervalo_consultas,
        'percepcao': percepcao,

        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'doenca_paciente': doenca_paciente_id,
            'medicamento_paciente': medicamento_paciente_id,
            'faixa_etaria_filtro': faixa_etaria_filtro,
            'classe_medicamento_filtro': classe_medicamento_filtro,
            'problema_saude_filtro': problema_saude_filtro,
        },
        'dropdowns': {
            'doencas': DoencaPaciente.objects.all(),
            'medicamentos': MedicamentoPaciente.objects.all(),
            'classes_medicamento': MedicamentoConsulta.objects.values_list('classe', flat=True).distinct(),
            'problemas_saude': ProblemaSaude.objects.values_list('problema', flat=True).distinct(),
        },

        'exportar_opcoes': [
            ("Pacientes Atendidos", "pacientes"),
            ("Consultas", "consultas"),
            ("Intervenções Realizadas", "intervencoes"),
            ("Média de Intervenções", "media_intervencoes"),
            ("Total PRMs", "prms"),
            ("PRMs Resolvidos", "prms_resolvidos"),
            ("Média PRMs por Paciente", "media_prm"),
            ("Média de Consultas por Paciente", "media_consultas"),
            ("Armazenamento de Medicamentos", "armazenamento"),
            ("Forma de Descarte", "descarte"),
            ("Percepção de Saúde", "percepcao"),
        ]
    }

    return render(request, 'relatorios/dashboard.html', context)
