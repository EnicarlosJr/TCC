# listagem_pacientes/views.py
from django.views.generic import ListView
from django.db.models import Q
from paciente.models import Paciente
from django.views.generic import DetailView

class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'  # Caminho correto para o template
    context_object_name = 'pacientes'
    paginate_by = 10  # Número de pacientes por página

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


class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'detalhe_paciente.html'
    context_object_name = 'paciente'
