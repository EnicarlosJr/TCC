document.addEventListener('DOMContentLoaded', () => {
    const btnAbrir = document.getElementById('open-fullscreen');
    const btnFechar = document.getElementById('close-fullscreen');
    const overlay = document.getElementById('avaliacao-fullscreen');

    // Abre o overlay de tela cheia
    btnAbrir?.addEventListener('click', () => {
        overlay?.classList.remove('d-none');
        document.body.style.overflow = 'hidden';  // Impede a rolagem de fundo
    });

    // Fecha o overlay de tela cheia
    btnFechar?.addEventListener('click', () => {
        overlay?.classList.add('d-none');
        document.body.style.overflow = '';  // Restaura a rolagem de fundo
    });
});
