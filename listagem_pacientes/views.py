from collections import defaultdict
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Max
from consulta.models import Consulta
from paciente.forms import PacienteForm
from paciente.models import MedicamentoDoencaPaciente, Paciente

class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'  # Caminho correto agora
    context_object_name = 'pacientes'
    paginate_by = 9  # Mostra 9 pacientes por página

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(telefone__icontains=query) |
                Q(municipio__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pacientes = context['pacientes']

        # Consultar últimas datas de consulta
        ultimas_consultas = Consulta.objects.values('paciente_id').annotate(
            ultima_consulta=Max('data_consulta')
        )
        ultima_consulta_dict = {item['paciente_id']: item['ultima_consulta'] for item in ultimas_consultas}

        # Atribuir última consulta para cada paciente listado
        for paciente in pacientes:
            paciente.ultima_consulta = ultima_consulta_dict.get(paciente.id)

        return context



class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'detalhe_paciente.html'
    context_object_name = 'paciente'

    def get_object(self):
        return get_object_or_404(Paciente, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        modo_edicao = self.request.GET.get("editar") == "1"

        context['anamneses'] = paciente.anamneses.all().order_by('-data_criacao')
        context['modo_edicao'] = modo_edicao
        if modo_edicao:
            context['form'] = PacienteForm(instance=paciente)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PacienteForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('paciente_detail', pk=self.object.id)
        context = self.get_context_data()
        context['form'] = form
        context['modo_edicao'] = True
        return self.render_to_response(context)

