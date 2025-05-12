// Alterna a exibição do formulário com base no ID
function toggleForm(id) {
    const el = document.getElementById(id);
    if (!el) return;
  
    const isHidden = el.classList.contains("d-none");
  
    // Fecha todos os formulários antes de abrir o novo (opcional)
    document.querySelectorAll('[id^="form"]').forEach(f => f.classList.add("d-none"));
  
    if (isHidden) {
      el.classList.remove("d-none");
      sessionStorage.setItem("formAberto", id);
    } else {
      el.classList.add("d-none");
      sessionStorage.removeItem("formAberto");
    }
  }
  
  // Ao recarregar a página, reabrir o formulário anterior
  document.addEventListener("DOMContentLoaded", () => {
    const lastOpened = sessionStorage.getItem("formAberto");
    if (lastOpened) {
      const el = document.getElementById(lastOpened);
      if (el) {
        el.classList.remove("d-none");
      }
    }
  });
  