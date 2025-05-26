// 🎯 Função para abrir o Modal de Exportação
function openModal() {
  const modal = document.getElementById('modalExportar');
  if (modal) {
    modal.style.display = 'flex';
    setTimeout(() => {
      modal.classList.add('opacity-100');
      modal.classList.remove('opacity-0');
    }, 10);
  }
}

// 🎯 Função para fechar o Modal de Exportação
function closeModal() {
  const modal = document.getElementById('modalExportar');
  if (modal) {
    modal.classList.remove('opacity-100');
    modal.classList.add('opacity-0');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }
}

// 🎯 Função para mostrar e esconder os Filtros
function toggleFiltros() {
  const filtros = document.getElementById('filtros');
  const btn = document.getElementById('toggleFiltros');
  if (filtros && btn) {
    filtros.classList.toggle('hidden');
    btn.innerText = filtros.classList.contains('hidden') ? '🔍 Mostrar Filtros' : '❌ Esconder Filtros';
  }
}

// 🎯 Função para criar gráficos dinamicamente
function criarGrafico(canvas, config) {
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const labels = JSON.parse(canvas.dataset.labels || '[]');
  const values = JSON.parse(canvas.dataset.values || '[]');

  if (!labels.length || !values.length) {
    console.warn(`Gráfico ${canvas.id} sem dados.`);
    canvas.insertAdjacentHTML('afterend', '<p class="text-gray-400 text-sm text-center">⚠️ Sem dados para exibir.</p>');
    canvas.style.display = 'none';
    return;
  }

  new Chart(ctx, {
    type: config.type,
    data: {
      labels: labels,
      datasets: [{
        label: config.label,
        data: values,
        backgroundColor: config.backgroundColor,
        borderColor: config.borderColor || config.backgroundColor,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      animation: { duration: 1500 },
      plugins: {
        legend: { display: config.type === 'pie' },
        tooltip: { enabled: true }
      },
      scales: config.type === 'bar' ? { y: { beginAtZero: true } } : {}
    }
  });
}

// 🎯 Configuração dos Gráficos Chart.js
window.addEventListener('DOMContentLoaded', function () {
  const configs = [
    {
      id: 'graficoFaixaEtaria',
      type: 'bar',
      label: 'Pacientes',
      backgroundColor: 'rgba(54, 162, 235, 0.6)'
    },
    {
      id: 'graficoGenero',
      type: 'pie',
      label: 'Gênero',
      backgroundColor: ['#60A5FA', '#F472B6', '#FCD34D']
    },
    {
      id: 'graficoDoencas',
      type: 'bar',
      label: 'Doenças',
      backgroundColor: 'rgba(255, 159, 64, 0.6)'
    },
    {
      id: 'graficoIntervencao',
      type: 'bar',
      label: 'Intervenções',
      backgroundColor: 'rgba(75, 192, 192, 0.6)'
    },
    {
      id: 'graficoDoencaPaciente',
      type: 'bar',
      label: 'Doenças - Anamnese',
      backgroundColor: 'rgba(153, 102, 255, 0.6)'
    },
    {
      id: 'graficoMedicamentoPaciente',
      type: 'bar',
      label: 'Medicamentos - Anamnese',
      backgroundColor: 'rgba(255, 99, 132, 0.6)'
    },
    {
      id: 'graficoProblemaConsulta',
      type: 'bar',
      label: 'Problemas - Consulta',
      backgroundColor: 'rgba(255, 206, 86, 0.6)'
    },
    {
      id: 'graficoMedicamentoConsulta',
      type: 'bar',
      label: 'Medicamentos - Consulta',
      backgroundColor: 'rgba(75, 192, 192, 0.6)'
    }
  ];

  configs.forEach(config => {
    const canvas = document.getElementById(config.id);
    criarGrafico(canvas, config);
  });
});

// 🎯 Atualiza contador de opções selecionadas no modal
function atualizarContador() {
  const checkboxes = document.querySelectorAll('#formExportar input[name="exportar"]:checked');
  const contador = document.getElementById('contadorSelecionados');
  if (contador) {
    if (checkboxes.length === 0) {
      contador.textContent = "Nenhuma opção selecionada";
    } else if (checkboxes.length === 1) {
      contador.textContent = "1 opção selecionada ✅";
    } else {
      contador.textContent = `${checkboxes.length} opções selecionadas ✅`;
    }
  }
}


