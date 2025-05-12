if (!document.getElementById('avaliacao-fullscreen')?.classList.contains('d-block')) {
    document.addEventListener('DOMContentLoaded', () => {
        const openBtn = document.getElementById('open-fullscreen');
        const closeBtn = document.getElementById('close-fullscreen');
        const fullscreenOverlay = document.getElementById('avaliacao-fullscreen');
        const fullscreenCloneTarget = document.getElementById('avaliacoes-fullscreen-clone');
        const originalSection = document.querySelector('#avaliacoes');
    
        if (openBtn && closeBtn && fullscreenOverlay && fullscreenCloneTarget && originalSection) {
        openBtn.addEventListener('click', () => {
            fullscreenCloneTarget.innerHTML = ''; // limpa conteúdo anterior
            fullscreenCloneTarget.innerHTML = originalSection.innerHTML; // clona conteúdo da avaliação
            fullscreenOverlay.classList.remove('d-none');
            fullscreenOverlay.classList.add('d-block');
            document.body.style.overflow = 'hidden';
        });
    
        closeBtn.addEventListener('click', () => {
            fullscreenOverlay.classList.remove('d-block');
            fullscreenOverlay.classList.add('d-none');
            document.body.style.overflow = '';
        });
        }
    });

}

function toggleFullscreen(show) {
    const overlay = document.getElementById('avaliacao-fullscreen');
    if (!overlay) return;
  
    if (show) {
      overlay.classList.remove('d-none');
      overlay.classList.add('d-block');
      document.body.classList.add('fullscreen-active');
      document.body.style.overflow = 'hidden';
    } else {
      overlay.classList.remove('d-block');
      overlay.classList.add('d-none');
      document.body.classList.remove('fullscreen-active');
      document.body.style.overflow = '';
    }
  }
  