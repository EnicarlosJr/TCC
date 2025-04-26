document.addEventListener('DOMContentLoaded', function () {
    const openBtn = document.getElementById('open-fullscreen');
    const closeBtn = document.getElementById('close-fullscreen');
    const overlay = document.getElementById('avaliacao-fullscreen');
    const expandableRows = document.querySelectorAll('.table tbody tr.expandable');

    // Fullscreen Open/Close
    if (openBtn && closeBtn && overlay) {
        openBtn.addEventListener('click', () => {
            overlay.classList.remove('d-none');
            document.body.style.overflow = 'hidden'; // evita scroll duplo
        });

        closeBtn.addEventListener('click', () => {
            overlay.classList.add('d-none');
            document.body.style.overflow = ''; // restaura scroll
        });
    }

    // Expansão de linhas clicáveis (sem afetar botões ou selects)
    if (expandableRows) {
        expandableRows.forEach(row => {
            row.addEventListener('click', function (event) {
                // Ignorar cliques em inputs, selects e botões
                const ignoreTags = ['BUTTON', 'SELECT', 'OPTION', 'TEXTAREA', 'INPUT', 'LABEL'];
                if (ignoreTags.includes(event.target.tagName)) return;

                const detailsRow = this.nextElementSibling;
                if (detailsRow && detailsRow.classList.contains('details-row')) {
                    detailsRow.classList.toggle('d-none');
                }
            });
        });
    }
});
