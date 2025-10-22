document.addEventListener("DOMContentLoaded", () => {
  // ------------------- ANIMAÇÃO DE CONTADORES -------------------
  const posicao = document.getElementById("posicao");
  const tempo = document.getElementById("tempo");
  const doadores = document.getElementById("doadores");
  const progressBar = document.getElementById("progress-bar");

  if (posicao && tempo && doadores && progressBar) {
    function animateCounter(id, finalValue, duration = 2000) {
      const element = document.getElementById(id);
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

    animateCounter("posicao", 12);
    animateCounter("tempo", 3);
    animateCounter("doadores", 58);
    setTimeout(() => progressBar.style.width = "40%", 500);
  }

  // ------------------- FRASES MOTIVACIONAIS -------------------
  const fraseElement = document.getElementById("frase-motivacional");
  if (fraseElement) {
    const frases = [
      "A solidariedade é a energia que nos move 💡",
      "Cada dia mais perto de sua vez ✨",
      "Você não está sozinho nessa jornada 🤝",
      "Esperança compartilhada é esperança multiplicada 💙"
    ];
    let index = 0;
    setInterval(() => {
      index = (index + 1) % frases.length;
      fraseElement.style.opacity = 0;
      setTimeout(() => {
        fraseElement.textContent = frases[index];
        fraseElement.style.opacity = 1;
      }, 500);
    }, 4000);
  }

  // ------------------- CARROSSEL -------------------
  const track = document.querySelector(".carrossel-track");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");

  if (track && nextBtn && prevBtn) {
    let index = 0;

    function moveCarousel() {
      const items = document.querySelectorAll(".card-item");
      if (!items.length) return;
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

    // arrastar com mouse
    let isDragging = false, startX, scrollLeft;
    track.addEventListener("mousedown", e => {
      isDragging = true;
      track.classList.add("dragging");
      startX = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });
    track.addEventListener("mouseleave", () => (isDragging = false));
    track.addEventListener("mouseup", () => (isDragging = false));
    track.addEventListener("mousemove", e => {
      if (!isDragging) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 1.5;
      track.scrollLeft = scrollLeft - walk;
    });

    // ✅ Faz o carrossel começar no 3º card (Casas)
    window.addEventListener("load", () => {
      index = 1;
      moveCarousel();
    });
  }
});
