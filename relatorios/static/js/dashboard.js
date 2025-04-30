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

// 🎯 Configuração dos Gráficos Chart.js
window.addEventListener('DOMContentLoaded', function () {
  const configs = [
    {
      id: 'graficoFaixaEtaria',
      type: 'bar',
      label: 'Pacientes',
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)'
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
      backgroundColor: 'rgba(255, 159, 64, 0.6)',
      borderColor: 'rgba(255, 159, 64, 1)'
    },
    {
      id: 'graficoIntervencao',
      type: 'bar',
      label: 'Intervenções',
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)'
    }
  ];
 
  configs.forEach(({ id, type, label, backgroundColor, borderColor }) => {
    const el = document.getElementById(id);
    if (!el) return;

    const ctx = el.getContext('2d');
    const labels = JSON.parse(el.dataset.labels || '[]');
    const values = JSON.parse(el.dataset.values || '[]');

    new Chart(ctx, {
      type: type,
      data: {
        labels: labels,
        datasets: [{
          label: label,
          data: values,
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          borderWidth: 1
        }]
      },
      options: {
        animation: { duration: 1500 },
        responsive: true,
        plugins: {
          legend: { display: type === 'pie' },
          datalabels: { display: false }
        },
        scales: type === 'bar' ? { y: { beginAtZero: true } } : {}
      }
    });
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

