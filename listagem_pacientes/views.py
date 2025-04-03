from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Max
from consulta.models import Consulta
from paciente.models import DoencaPaciente, MedicamentoPaciente, Paciente

class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'  # Caminho correto para o template
    context_object_name = 'pacientes'
    paginate_by = 9  # Número de pacientes por página

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        # Filtros básicos de busca
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(telefone__icontains=query) |
                Q(municipio__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pacientes = self.get_queryset()
        
        # Dicionário para armazenar a última consulta de cada paciente
        ultimas_consultas = Consulta.objects.values('paciente_id').annotate(ultima_consulta=Max('data_consulta'))
        ultima_consulta_dict = {uc['paciente_id']: uc['ultima_consulta'] for uc in ultimas_consultas}

        # Adiciona a informação ao contexto
        for paciente in pacientes:
            paciente.ultima_consulta = ultima_consulta_dict.get(paciente.id, None)

        paginator = Paginator(pacientes, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            pacientes_paginated = paginator.page(page)
        except PageNotAnInteger:
            pacientes_paginated = paginator.page(1)
        except EmptyPage:
            pacientes_paginated = paginator.page(paginator.num_pages)

        context['pacientes'] = pacientes_paginated
        return context

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'detalhe_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        
        # Adicionando doenças e medicamentos ao contexto
        context['doencas'] = DoencaPaciente.objects.filter(paciente=paciente)
        context['medicamentos'] = MedicamentoPaciente.objects.filter(paciente=paciente)

        return context