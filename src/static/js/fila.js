// Animação do botão ao submeter
document.getElementById('form-creditos')?.addEventListener('submit', function(e) {
  const btn = document.querySelector('.btn-primary');
  if (btn && !btn.classList.contains('loading')) {
    btn.classList.add('loading');
  }
});

// Frases motivacionais rotativas
const frasesMotivacionais = [
  "Estamos juntos para garantir que a solidariedade chegue até você",
  "A solidariedade é a energia que nos move 💡",
  "Cada dia mais perto de sua vez ✨",
  "Você não está sozinho nessa jornada 🤝",
  "Esperança compartilhada é esperança multiplicada 💙"
];

let indexFrase = 0;
const fraseElement = document.getElementById('frase-motivacional');

if (fraseElement) {
  setInterval(() => {
    indexFrase = (indexFrase + 1) % frasesMotivacionais.length;
    fraseElement.style.opacity = 0;
    
    setTimeout(() => {
      fraseElement.textContent = frasesMotivacionais[indexFrase];
      fraseElement.style.opacity = 1;
    }, 500);
  }, 5000);
}

// Validação visual do input
const inputQuantidade = document.querySelector('input[name="qtd_solicitada"]');
if (inputQuantidade) {
  inputQuantidade.addEventListener('input', function(e) {
    const valor = parseFloat(e.target.value);
    
    if (valor && valor > 0) {
      e.target.style.borderColor = 'rgba(16, 185, 129, 0.6)';
    } else if (e.target.value !== '') {
      e.target.style.borderColor = 'rgba(239, 68, 68, 0.6)';
    } else {
      e.target.style.borderColor = 'rgba(242, 183, 5, 0.2)';
    }
  });
}