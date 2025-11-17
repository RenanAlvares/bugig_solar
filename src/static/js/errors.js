/* ===================================================
   BUGIGSOLAR - JAVASCRIPT PÁGINA DE ERROS
   =================================================== */

document.addEventListener('DOMContentLoaded', function() {
  
  // ===================================================
  // ANIMAÇÃO DE ENTRADA DOS ELEMENTOS
  // ===================================================
  
  function animarEntrada() {
    const elementos = document.querySelectorAll('.error-page > *');
    
    elementos.forEach((elemento, index) => {
      elemento.style.opacity = '0';
      elemento.style.transform = 'translateY(20px)';
      
      setTimeout(() => {
        elemento.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        elemento.style.opacity = '1';
        elemento.style.transform = 'translateY(0)';
      }, 100 * index);
    });
  }
  
  // ===================================================
  // LOG DE ERRO NO CONSOLE (PARA DESENVOLVIMENTO)
  // ===================================================
  
  function logErroConsole() {
    const errorCode = document.querySelector('.error-page h1');
    const errorMessage = document.querySelector('.error-page p');
    
    if (errorCode && errorMessage) {
      console.group('🚨 Erro Detectado - BugigSolar');
      console.error(`Código: ${errorCode.textContent}`);
      console.warn(`Mensagem: ${errorMessage.textContent}`);
      console.info(`URL: ${window.location.href}`);
      console.info(`Timestamp: ${new Date().toISOString()}`);
      console.groupEnd();
    }
  }
  
  // ===================================================
  // INICIALIZAR TODAS AS FUNÇÕES
  // ===================================================
  
  function inicializar() {
    // Animações de entrada
    setTimeout(animarEntrada, 100);
    
    // Log para desenvolvimento
    logErroConsole();
  }
  
  // Executar inicialização
  inicializar();
  
  // ===================================================
  // ANIMAÇÃO DE CLIQUE NO BOTÃO
  // ===================================================
  
  const btnDefault = document.querySelector('.btn-default');
  if (btnDefault) {
    btnDefault.addEventListener('click', function(e) {
      // Criar ripple effect
      const ripple = document.createElement('span');
      ripple.style.position = 'absolute';
      ripple.style.borderRadius = '50%';
      ripple.style.background = 'rgba(255, 255, 255, 0.5)';
      ripple.style.width = '20px';
      ripple.style.height = '20px';
      ripple.style.pointerEvents = 'none';
      
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.style.transform = 'translate(-50%, -50%) scale(0)';
      ripple.style.animation = 'ripple 0.6s ease-out';
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  }
  
  // Adicionar keyframes do ripple dinamicamente
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ripple {
      to {
        transform: translate(-50%, -50%) scale(15);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
  
});