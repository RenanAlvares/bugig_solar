document.addEventListener("DOMContentLoaded", () => {
  // valores de exemplo (pode depois vir do backend via Jinja)
  const finalPosicao = 12;
  const finalTempo = 3;
  const finalDoadores = 58;
  const progressPercent = 40;

  // função de animação de contadores
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

  // iniciar contadores
  animateCounter("posicao", finalPosicao);
  animateCounter("tempo", finalTempo);
  animateCounter("doadores", finalDoadores);

  // animar barra de progresso
  const progressBar = document.getElementById("progress-bar");
  setTimeout(() => {
    progressBar.style.width = progressPercent + "%";
  }, 500);

  // frases motivacionais rotativas
  const frases = [
    "A solidariedade é a energia que nos move 💡",
    "Cada dia mais perto de sua vez ✨",
    "Você não está sozinho nessa jornada 🤝",
    "Esperança compartilhada é esperança multiplicada 💙"
  ];
  let index = 0;
  const fraseElement = document.getElementById("frase-motivacional");
  setInterval(() => {
    index = (index + 1) % frases.length;
    fraseElement.style.opacity = 0;
    setTimeout(() => {
      fraseElement.textContent = frases[index];
      fraseElement.style.opacity = 1;
    }, 500);
  }, 4000);
});
