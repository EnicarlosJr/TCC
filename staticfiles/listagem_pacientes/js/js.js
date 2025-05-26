document.addEventListener("DOMContentLoaded", () => {
    // Toggle visual dos accordions
    const cards = document.querySelectorAll(".expand-card .card-header");
    cards.forEach(header => {
        header.addEventListener("click", () => {
            const card = header.closest(".expand-card");
            card.classList.toggle("collapsed");
        });
    });

    // Animação suave ao abrir página com hash
    if (window.location.hash) {
        const el = document.querySelector(window.location.hash);
        if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "center" });
        }
    }

    // Efeito "copiado" para botões de ação futuros (ex: copiar número do paciente, se adicionado)
    document.querySelectorAll("[data-copy]").forEach(btn => {
        btn.addEventListener("click", () => {
            const value = btn.getAttribute("data-copy");
            navigator.clipboard.writeText(value).then(() => {
                btn.classList.add("btn-success");
                btn.innerHTML = "✅ Copiado!";
                setTimeout(() => {
                    btn.innerHTML = "📋 Copiar";
                    btn.classList.remove("btn-success");
                }, 1500);
            });
        });
    });

    // Botões com loading visual
    document.querySelectorAll("form button[type=submit]").forEach(btn => {
        btn.addEventListener("click", () => {
            // Deixa o navegador enviar o form normalmente
            setTimeout(() => {
                btn.disabled = true;
                btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processando...`;
            }, 50);
        });
    });
    
});
