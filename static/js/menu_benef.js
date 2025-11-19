document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("calcularBtn");
  const btnGrafico = document.getElementById("verGraficoBtn");
  const input = document.getElementById("valorConta");
  const resultado = document.getElementById("resultadoSimulador");
  const graficoContainer = document.getElementById("graficoContainer");
  const canvas = document.getElementById("graficoEconomia");
  const placeholder = document.getElementById("graficoPlaceholder");
  const simuladorCard = document.querySelector(".simulador-card");

  let chartInstance = null;

  // ======= Prevenir comportamento de link no card simulador =======
  if (simuladorCard) {
    simuladorCard.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  }

  // ======= Função: Atualiza o gráfico =======
  function atualizarGrafico(economiaMensal) {
    if (!canvas || !graficoContainer) return;

    const ctx = canvas.getContext("2d");
    const meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
    const dados = meses.map((_, i) => economiaMensal * (0.85 + Math.sin(i / 1.5) * 0.1));

    if (chartInstance) chartInstance.destroy();

    if (placeholder) placeholder.style.display = "none";
    canvas.style.display = "block";

    const grad = ctx.createLinearGradient(0, 0, 0, 400);
    grad.addColorStop(0, "rgba(242,183,5,0.5)");
    grad.addColorStop(1, "rgba(242,183,5,0.1)");

    chartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: meses,
        datasets: [
          {
            label: "Economia Estimada (R$)",
            data: dados,
            borderColor: "#F2B705",
            backgroundColor: grad,
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointBackgroundColor: "#F2B705",
            pointRadius: 5,
            pointHoverRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1000, easing: "easeOutQuart" },
        plugins: {
          legend: {
            labels: { color: "#fff", font: { size: 14, weight: "bold" } },
          },
          tooltip: {
            backgroundColor: "rgba(0,0,0,0.85)",
            borderColor: "#F2B705",
            borderWidth: 1,
            titleColor: "#F2B705",
            bodyColor: "#fff",
            cornerRadius: 8,
            padding: 10,
          },
        },
        scales: {
          x: { ticks: { color: "#ccc" }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { 
            ticks: { 
              color: "#ccc", 
              callback: (val) => `R$ ${val.toFixed(0)}` 
            }, 
            grid: { color: "rgba(255,255,255,0.05)" } 
          },
        },
      },
    });
  }

  // ======= Modal de pagamento =======
  const modal = document.getElementById("modal-pagamento");
  const btnPagamento = document.getElementById("card-pagamento");
  const fecharModal = document.getElementById("fechar-modal");

  if (btnPagamento && modal && fecharModal) {
    btnPagamento.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      modal.classList.add("show");
      modal.style.display = "flex";
    });

    fecharModal.addEventListener("click", () => {
      modal.classList.remove("show");
      setTimeout(() => {
        modal.style.display = "none";
      }, 300);
    });

    // Fechar clicando fora
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("show");
        setTimeout(() => {
          modal.style.display = "none";
        }, 300);
      }
    });

    // Fechar com ESC
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.style.display === "flex") {
        modal.classList.remove("show");
        setTimeout(() => {
          modal.style.display = "none";
        }, 300);
      }
    });
  }

  // ======= Animação nos cards ao passar o mouse =======
  const cards = document.querySelectorAll(".dashboard-cards .card");
  
  cards.forEach(card => {
    card.addEventListener("mouseenter", function() {
      const icon = this.querySelector(".card-icon i");
      if (icon) {
        icon.style.transform = "scale(1.1) rotateY(360deg)";
      }
    });

    card.addEventListener("mouseleave", function() {
      const icon = this.querySelector(".card-icon i");
      if (icon) {
        icon.style.transform = "scale(1) rotateY(0deg)";
      }
    });
  });

  // ======= Adicionar animação de shake ao CSS dinamicamente =======
  const style = document.createElement("style");
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-10px); }
      75% { transform: translateX(10px); }
    }
  `;
  document.head.appendChild(style);
});