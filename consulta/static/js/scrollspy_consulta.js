document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.sidebar .nav-link');

    // Função para verificar a visibilidade das seções
    function onScroll() {
        let scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;

        sections.forEach((section, index) => {
            const offsetTop = section.offsetTop;
            const height = section.offsetHeight;

            if (scrollPosition >= offsetTop - 50 && scrollPosition < offsetTop + height - 50) {
                navLinks[index].classList.add('active');
            } else {
                navLinks[index].classList.remove('active');
            }
        });
    }

    // Adiciona o evento de rolagem para atualizar a navegação
    window.addEventListener('scroll', onScroll);

    // Inicializa a verificação ao carregar a página
    onScroll();
});
