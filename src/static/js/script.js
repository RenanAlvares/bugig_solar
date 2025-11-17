// script.js - Scripts gerais do site (dashboard, carrossel, etc.)

// ==========================================
// DASHBOARD - ANIMAÇÕES DE CONTADORES
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  // Valores finais (depois você pega do backend)
  const finalPosicao = 12;
  const finalTempo = 3;
  const finalDoadores = 58;
  const progressPercent = 40;

  // Função de animação de contadores
  function animateCounter(id, finalValue, duration = 2000) {
    const element = document.getElementById(id);
    if (!element) return; // Proteção: só executa se elemento existir
    
    let start = 0;
    const increment = finalValue / (duration / 30);

    const interval = setInterval(() => {
      start += increment;
      if (start >= finalValue) {
        element.textContent = finalValue;
        clearInterval(interval);
      } else {
        element.textContent = Math.floor(start);
      }
    }, 30);
  }

  // Iniciar contadores
  animateCounter("posicao", finalPosicao);
  animateCounter("tempo", finalTempo);
  animateCounter("doadores", finalDoadores);

  // Animar barra de progresso
  const progressBar = document.getElementById("progress-bar");
  if (progressBar) {
    setTimeout(() => {
      progressBar.style.width = progressPercent + "%";
    }, 500);
  }

  // ==========================================
  // FRASES MOTIVACIONAIS ROTATIVAS
  // ==========================================
  const frases = [
    "A solidariedade é a energia que nos move 💡",
    "Cada dia mais perto de sua vez ✨",
    "Você não está sozinho nessa jornada 🤝",
    "Esperança compartilhada é esperança multiplicada 💙"
  ];
  
  let index = 0;
  const fraseElement = document.getElementById("frase-motivacional");
  
  if (fraseElement) {
    setInterval(() => {
      index = (index + 1) % frases.length;
      fraseElement.style.opacity = 0;
      setTimeout(() => {
        fraseElement.textContent = frases[index];
        fraseElement.style.opacity = 1;
      }, 500);
    }, 4000);
  }
});

// ==========================================
// CARROSSEL
// ==========================================
const track = document.querySelector(".carrossel-track");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");

if (track && nextBtn && prevBtn) {
  let index = 0;

  function moveCarousel() {
    const items = document.querySelectorAll(".card-item");
    if (items.length === 0) return;
    
    const itemWidth = items[0].offsetWidth + 16; // margem lateral
    track.style.transform = `translateX(-${index * itemWidth}px)`;
  }

  nextBtn.addEventListener("click", () => {
    const items = document.querySelectorAll(".card-item");
    if (index < items.length - 3) index++;
    moveCarousel();
  });

  prevBtn.addEventListener("click", () => {
    if (index > 0) index--;
    moveCarousel();
  });
}