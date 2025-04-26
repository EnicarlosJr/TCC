document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.sidebar .nav-link');

    function onScroll() {
        let scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;

        sections.forEach((section) => {
            const offsetTop = section.offsetTop;
            const height = section.offsetHeight;

            if (scrollPosition >= offsetTop - 50 && scrollPosition < offsetTop + height - 50) {
                const sectionId = section.getAttribute('id');
                navLinks.forEach(link => {
                    const target = link.getAttribute('href');
                    link.classList.toggle('active', target === `#${sectionId}`);
                });
            }
        });
    }

    // Função debounce para melhorar a performance do scroll
    function debounce(func, wait = 10) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    window.addEventListener('scroll', debounce(onScroll));
    onScroll(); // Inicializa ao carregar a página
});