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

    // encontra o index do card "Prédios" (caso o texto mude, ajuste aqui)
    function findPrediosIndex() {
      return items.findIndex(it => {
        const h3 = it.querySelector(".card-texto h3");
        return h3 && h3.textContent.trim().toLowerCase() === "prédios";
      });
    }

    // Calcula quantos cards são visíveis
    function getVisibleCards() {
      const wrapperWidth = wrapper.offsetWidth;
      const cardWidth = items[0].offsetWidth;
      const gap = parseFloat(getComputedStyle(track).gap) || 32;
      return Math.max(1, Math.floor(wrapperWidth / (cardWidth + gap)));
    }

    // Calcula o deslocamento em px
    function calculateOffset() {
      const cardWidth = items[0].offsetWidth;
      const gap = parseFloat(getComputedStyle(track).gap) || 32;
      return currentIndex * (cardWidth + gap);
    }

    // Calcula o maxIndex natural (quando não há forcing)
    function getNaturalMaxIndex(visibleCards) {
      return Math.max(0, items.length - visibleCards);
    }

    // Calcula o maxIndex forçado para que "Prédios" fique como último visível
    function getForcedMaxIndex(visibleCards) {
      const naturalMax = getNaturalMaxIndex(visibleCards);
      const pIndex = findPrediosIndex();
      if (pIndex === -1) return naturalMax; // se não encontrou "Prédios", usa natural
      const forced = Math.max(0, pIndex - (visibleCards - 1));
      return Math.min(naturalMax, forced);
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
      const naturalMax = getNaturalMaxIndex(visibleCards);
      const forcedMax = getForcedMaxIndex(visibleCards);

      // garante que currentIndex nunca ultrapasse o limite forçado
      if (currentIndex > forcedMax) currentIndex = forcedMax;

      prevBtn.disabled = currentIndex === 0;
      nextBtn.disabled = currentIndex >= forcedMax;

      prevBtn.style.opacity = currentIndex === 0 ? "0.3" : "1";
      nextBtn.style.opacity = currentIndex >= forcedMax ? "0.3" : "1";
    }

    // Próximo (usa limite forçado)
    nextBtn.addEventListener("click", () => {
      const visibleCards = getVisibleCards();
      const forcedMax = getForcedMaxIndex(visibleCards);
      if (currentIndex < forcedMax) {
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
        const forcedMax = getForcedMaxIndex(visibleCards);
        if (currentIndex > forcedMax) currentIndex = forcedMax;
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
      const forcedMax = getForcedMaxIndex(visibleCards);

      if (diff > 50 && currentIndex < forcedMax) {
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


//simulador

// =====================================================
// SIMULADOR DE ECONOMIA - LANDING PAGE
// =====================================================

document.addEventListener("DOMContentLoaded", function() {
  
  // ======= Seleção de elementos =======
  const input = document.getElementById("valorConta");
  const btnCalcular = document.getElementById("calcularBtn");
  const resultado = document.getElementById("resultadoSimulador");
  
  // Verificar se os elementos existem
  if (!input || !btnCalcular || !resultado) {
    console.warn("⚠️ Elementos do simulador não encontrados");
    return;
  }

  // ======= Função: Executa o cálculo =======
  function calcularEconomia() {
    const valor = parseFloat(input.value);
    
    if (isNaN(valor) || valor <= 0) {
      // Feedback visual
      input.style.borderColor = "#ef4444";
      input.style.animation = "shake 0.4s ease";
      
      setTimeout(() => {
        input.style.animation = "";
        input.style.borderColor = "rgba(255, 255, 255, 0.1)";
      }, 400);
      
      alert("⚠️ Por favor, insira um valor válido!");
      input.focus();
      return;
    }

    // Resetar estilo do input
    input.style.borderColor = "#10b981";

    // Cálculos
    const precoKwh = 0.95;
    const kwh = valor / precoKwh;
    const economiaPercentual = 0.20; // 20% de economia média
    const economiaMensal = valor * economiaPercentual;
    const economiaAnual = economiaMensal * 12;
    const co2PorKwh = 0.084;
    const kwhEconomizados = kwh * economiaPercentual;
    const co2Evitado = kwhEconomizados * co2PorKwh;

    // Atualizar valores na tela
    const economiaValorEl = document.getElementById("economiaValor");
    const kwhEconomiaEl = document.getElementById("kwhEconomia");
    const co2EvitadoEl = document.getElementById("co2Evitado");
    const economiaAnualEl = document.getElementById("economiaAnual");

    if (economiaValorEl) {
      economiaValorEl.textContent = `R$ ${economiaMensal.toFixed(2)}`;
    }
    
    if (kwhEconomiaEl) {
      kwhEconomiaEl.textContent = `${kwhEconomizados.toFixed(1)} kWh`;
    }
    
    if (co2EvitadoEl) {
      co2EvitadoEl.textContent = `${co2Evitado.toFixed(2)} kg`;
    }
    
    if (economiaAnualEl) {
      economiaAnualEl.textContent = `R$ ${economiaAnual.toFixed(2)}`;
    }

    // Mostrar resultado com animação
    resultado.classList.add("mostrar");
    
    // Scroll suave para o resultado
    setTimeout(() => {
      resultado.scrollIntoView({ 
        behavior: "smooth", 
        block: "nearest",
        inline: "nearest"
      });
    }, 300);
  }

  // ======= Eventos do simulador =======
  btnCalcular.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    calcularEconomia();
  });

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      calcularEconomia();
    }
  });

  // Validação visual em tempo real
  input.addEventListener("input", (e) => {
    const valor = parseFloat(e.target.value);
    
    if (valor && valor > 0) {
      e.target.style.borderColor = "#10b981";
    } else if (e.target.value !== "") {
      e.target.style.borderColor = "#ef4444";
    } else {
      e.target.style.borderColor = "rgba(255, 255, 255, 0.1)";
    }
  });

  // Limpar resultado quando o input for limpo
  input.addEventListener("input", (e) => {
    if (!e.target.value) {
      resultado.classList.remove("mostrar");
    }
  });
});

// =====================================================
// ANIMAÇÃO DE SHAKE PARA ERRO
// =====================================================
const style = document.createElement('style');
style.textContent = `
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
    20%, 40%, 60%, 80% { transform: translateX(8px); }
  }
`;
document.head.appendChild(style);

// =====================================================
// ANIMAÇÕES DE SCROLL (Fade In)
// =====================================================
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observar todos os elementos com classe fade-in
document.querySelectorAll(".fade-in").forEach(el => {
  observer.observe(el);
});

// =====================================================
// CARROSSEL (caso exista na página)
// =====================================================
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const track = document.querySelector(".carrossel-track");

if (prevBtn && nextBtn && track) {
  let currentIndex = 0;
  const cards = document.querySelectorAll(".card-item");
  const totalCards = cards.length;
  
  // Calcular quantos cards aparecem por vez
  function getCardsPerView() {
    if (window.innerWidth >= 1200) return 3;
    if (window.innerWidth >= 768) return 2;
    return 1;
  }

  function updateCarousel() {
    const cardsPerView = getCardsPerView();
    const maxIndex = Math.max(0, totalCards - cardsPerView);
    
    // Limitar o índice
    if (currentIndex > maxIndex) {
      currentIndex = maxIndex;
    }
    
    // Calcular o deslocamento
    const cardWidth = cards[0].offsetWidth;
    const gap = 32; // 2rem = 32px
    const offset = -(currentIndex * (cardWidth + gap));
    
    track.style.transform = `translateX(${offset}px)`;
    
    // Atualizar botões
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= maxIndex;
  }

  nextBtn.addEventListener("click", () => {
    const cardsPerView = getCardsPerView();
    const maxIndex = totalCards - cardsPerView;
    
    if (currentIndex < maxIndex) {
      currentIndex++;
      updateCarousel();
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCarousel();
    }
  });

  // Atualizar ao redimensionar
  window.addEventListener("resize", () => {
    updateCarousel();
  });

  // Inicializar
  updateCarousel();
}

console.log("✅ Landing Page JavaScript carregado com sucesso!");