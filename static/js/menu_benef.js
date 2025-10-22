// =====================================================
// BUGIGSOLAR - SIMULADOR DE ECONOMIA + GRÁFICO INTELIGENTE
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("calcularBtn");
  const btnGrafico = document.getElementById("verGraficoBtn");
  const input = document.getElementById("valorConta");
  const resultado = document.getElementById("resultadoSimulador");
  const graficoContainer = document.getElementById("graficoContainer");
  const canvas = document.getElementById("graficoEconomia");
  const placeholder = document.getElementById("graficoPlaceholder");

  let chartInstance = null;

  // ======= Função: Atualiza o gráfico com base na economia =======
  function atualizarGrafico(economiaMensal) {
    const ctx = canvas.getContext("2d");
    const meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
    const dados = meses.map((_, i) => economiaMensal * (0.85 + Math.sin(i / 1.5) * 0.1));

    if (chartInstance) chartInstance.destroy();

    placeholder.style.display = "none";
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
          x: {
            ticks: { color: "#ccc" },
            grid: { color: "rgba(255,255,255,0.05)" },
          },
          y: {
            ticks: {
              color: "#ccc",
              callback: (val) => `R$ ${val.toFixed(0)}`,
            },
            grid: { color: "rgba(255,255,255,0.05)" },
          },
        },
      },
    });
  }

  // ======= Função: Executa o cálculo e atualiza o gráfico =======
  function calcularEconomia() {
    const valor = parseFloat(input.value);

    if (isNaN(valor) || valor <= 0) {
      alert("⚠️ Por favor, insira um valor válido!");
      input.focus();
      return;
    }

    const precoKwh = 0.95;
    const kwh = valor / precoKwh;
    const economiaPercentual = 0.7;
    const economiaMensal = valor * economiaPercentual;
    const economiaAnual = economiaMensal * 12;
    const co2PorKwh = 0.084;
    const kwhEconomizados = kwh * economiaPercentual;
    const co2Evitado = kwhEconomizados * co2PorKwh;

    document.getElementById("economiaValor").textContent = `R$ ${economiaMensal.toFixed(2)}`;
    document.getElementById("kwhEconomia").textContent = `${kwhEconomizados.toFixed(1)} kWh`;
    document.getElementById("co2Evitado").textContent = `${co2Evitado.toFixed(2)} kg de CO₂`;
    document.getElementById("economiaAnual").textContent = `R$ ${economiaAnual.toFixed(2)}`;

    resultado.classList.add("mostrar");
    atualizarGrafico(economiaMensal);

    setTimeout(() => {
      graficoContainer.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 400);
  }

  // ======= Evento: Clique no botão Calcular =======
  btnCalcular.addEventListener("click", (e) => {
    e.preventDefault();
    calcularEconomia();
  });

  // ======= Evento: Pressionar Enter no input =======
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      calcularEconomia();
    }
  });

  // ======= Evento: Ver Gráfico (de qualquer lugar) =======
  btnGrafico.addEventListener("click", (e) => {
    e.preventDefault();
    graficoContainer.scrollIntoView({ behavior: "smooth", block: "center" });
  });
});
