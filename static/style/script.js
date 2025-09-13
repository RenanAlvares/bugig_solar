function mostrarFuncionalidade(funcao) {
  const aviso = document.getElementById("aviso-funcionalidade");
  const textoAviso = document.getElementById("texto-aviso");

  switch (funcao) {
    case 'Entrar na Fila':
      textoAviso.textContent = "Você será colocado na fila para receber créditos de energia solar assim que estiver disponível.";
      break;
    case 'Fazer Doação':
      textoAviso.textContent = "Você pode doar créditos de energia solar para ajudar quem mais precisa.";
      break;
    case 'Consultar Movimentação':
      textoAviso.textContent = "Aqui você poderá verificar os créditos que você doou ou recebeu.";
      break;
    case 'Simular Economia':
      textoAviso.textContent = "Use o simulador para calcular sua economia na conta de energia com créditos solares.";
      break;
    default:
      textoAviso.textContent = "";
      break;
  }

  // Exibe o quadrado de aviso
  aviso.style.display = "block";
}

// Função para fechar o quadrado de aviso
function fecharAviso() {
  const aviso = document.getElementById("aviso-funcionalidade");
  aviso.style.display = "none";
}

// Simulador de Economia de Energia
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("simulador-form");
  const input = document.getElementById("consumo");
  const resultado = document.getElementById("resultado-simulador");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const consumoMensal = parseFloat(input.value);

    if (isNaN(consumoMensal) || consumoMensal <= 0) {
      resultado.textContent = "Por favor, insira um valor válido para o consumo.";
      resultado.style.color = "red";
      return;
    }

    const tarifaMedia = 0.85;
    const economia = consumoMensal * tarifaMedia * 0.7;

    resultado.style.color = "#2e7d32";
    resultado.textContent = `Você pode economizar cerca de R$ ${economia.toFixed(2)} por mês com energia solar compartilhada.`;
  });
});
