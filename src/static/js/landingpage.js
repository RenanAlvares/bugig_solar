document.addEventListener("DOMContentLoaded", () => {
  
  // ===============================================
  // ANIMAÇÃO FADE IN
  // ===============================================
  const elementos = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver((entradas) => {
    entradas.forEach((entrada) => {
      if (entrada.isIntersecting) {
        entrada.target.classList.add("visible");
        observer.unobserve(entrada.target);
      }
    });
  }, { threshold: 0.1 });

  elementos.forEach(el => observer.observe(el));

  // ===============================================
  // CARROSSEL TOTALMENTE RESPONSIVO E CORRIGIDO
  // ===============================================
  const track = document.querySelector(".carrossel-track");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const wrapper = document.querySelector(".carrossel-wrapper");

  if (track && nextBtn && prevBtn && wrapper) {
    const items = Array.from(document.querySelectorAll(".card-item"));
    
    if (items.length === 0) return;

    let currentIndex = 0;

    // Calcula quantos cards são visíveis
    function getVisibleCards() {
      const wrapperWidth = wrapper.offsetWidth;
      const cardWidth = items[0].offsetWidth;
      const gap = 32; // 2rem
      
      return Math.floor((wrapperWidth + gap) / (cardWidth + gap));
    }

    // Calcula o deslocamento
    function calculateOffset() {
      if (items.length === 0) return 0;
      
      const cardWidth = items[0].offsetWidth;
      const gap = 32;
      
      return currentIndex * (cardWidth + gap);
    }

    // Move o carrossel
    function moveCarousel() {
      const offset = calculateOffset();
      track.style.transform = `translateX(-${offset}px)`;
      updateButtons();
    }

    // Atualiza os botões
    function updateButtons() {
      const visibleCards = getVisibleCards();
      const maxIndex = Math.max(0, items.length - visibleCards);
      
      prevBtn.disabled = currentIndex === 0;
      nextBtn.disabled = currentIndex >= maxIndex;
      
      prevBtn.style.opacity = currentIndex === 0 ? "0.3" : "1";
      nextBtn.style.opacity = currentIndex >= maxIndex ? "0.3" : "1";
    }

    // Próximo
    nextBtn.addEventListener("click", () => {
      const visibleCards = getVisibleCards();
      const maxIndex = Math.max(0, items.length - visibleCards);
      
      if (currentIndex < maxIndex) {
        currentIndex++;
        moveCarousel();
      }
    });

    // Anterior
    prevBtn.addEventListener("click", () => {
      if (currentIndex > 0) {
        currentIndex--;
        moveCarousel();
      }
    });

    // Redimensionar
    let resizeTimeout;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        const visibleCards = getVisibleCards();
        const maxIndex = Math.max(0, items.length - visibleCards);
        
        if (currentIndex > maxIndex) {
          currentIndex = maxIndex;
        }
        
        moveCarousel();
      }, 150);
    });

    // Touch/Swipe para mobile
    let touchStartX = 0;
    let touchEndX = 0;

    wrapper.addEventListener("touchstart", (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    wrapper.addEventListener("touchend", (e) => {
      touchEndX = e.changedTouches[0].clientX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const diff = touchStartX - touchEndX;
      const visibleCards = getVisibleCards();
      const maxIndex = Math.max(0, items.length - visibleCards);
      
      if (diff > 50 && currentIndex < maxIndex) {
        currentIndex++;
        moveCarousel();
      } else if (diff < -50 && currentIndex > 0) {
        currentIndex--;
        moveCarousel();
      }
    }

    // Inicializar
    moveCarousel();
  }
});