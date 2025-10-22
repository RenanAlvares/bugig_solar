document.addEventListener('DOMContentLoaded', function () {
    // seletor do form (se tiver id use-o, senão pega o primeiro form)
    const form = document.querySelector('form#editForm') || document.querySelector('form');

    // campos relacionados ao documento
    const radios = Array.from(document.querySelectorAll('input[name="tipo_documento"]'));
    const cpfGroup = document.getElementById('cpf_group');
    const cnpjGroup = document.getElementById('cnpj_group');
    const nomeFantasiaGroup = document.getElementById('nome_fantasia_group');

    console.log('script.js carregado. radios encontrados:', radios.length, 'form encontrado?', !!form);
    console.log('cpf_group?', !!cpfGroup, 'cnpj_group?', !!cnpjGroup, 'nomeFantasia?', !!nomeFantasiaGroup);

    function hideAll() {
        if (cpfGroup) cpfGroup.style.display = 'none';
        if (cnpjGroup) cnpjGroup.style.display = 'none';
        if (nomeFantasiaGroup) nomeFantasiaGroup.style.display = 'none';
    }

    function showCPF() {
        if (cpfGroup) cpfGroup.style.display = 'block';
        if (cnpjGroup) cnpjGroup.style.display = 'none';
        if (nomeFantasiaGroup) nomeFantasiaGroup.style.display = 'none';
    }

    function showCNPJ() {
        if (cpfGroup) cpfGroup.style.display = 'none';
        if (cnpjGroup) cnpjGroup.style.display = 'block';
        if (nomeFantasiaGroup) nomeFantasiaGroup.style.display = 'block';
    }

    // tenta obter o valor selecionado do documento:
    // 1) radio :checked
    // 2) hidden input com name tipo_documento
    // 3) window.__selected_doc (caso template injete essa variável)
    function getSelectedDoc() {
        let sel = '';
        const checked = document.querySelector('input[name="tipo_documento"]:checked');
        if (checked) sel = checked.value;

        if (!sel) {
            const hidden = document.querySelector('input[type="hidden"][name="tipo_documento"], input[type="hidden"][name$="tipo_documento"]');
            if (hidden) sel = hidden.value;
        }

        if (!sel && window && window.__selected_doc) {
            sel = window.__selected_doc;
        }

        return (sel || '').toString().toLowerCase().trim();
    }

    function toggleDocumentFields() {
        const raw = getSelectedDoc();
        console.log('tipo_documento selecionado (compute):', raw);

        if (raw === 'cpf' || raw === '1') {
            showCPF();
        } else if (raw === 'cnpj' || raw === '2') {
            showCNPJ();
        } else {
            hideAll();
        }
    }

    // registra listeners (se houver radios, embora no modo edit eles possam estar disabled)
    if (radios.length) {
        radios.forEach(r => r.addEventListener('change', toggleDocumentFields));
    } else {
        console.warn('Nenhum input[name="tipo_documento"] encontrado — usando hidden input se existir.');
    }

    // observa mudanças no hidden (se houver) para caso o backend atualize dinamicamente
    const hiddenDoc = document.querySelector('input[type="hidden"][name="tipo_documento"], input[type="hidden"][name$="tipo_documento"]');
    if (hiddenDoc) {
        hiddenDoc.addEventListener('change', toggleDocumentFields);
        // MutationObserver para mudanças de value feitas por script
        try {
            const mo = new MutationObserver(toggleDocumentFields);
            mo.observe(hiddenDoc, { attributes: true, attributeFilter: ['value'] });
        } catch (e) {
            // ambiente que não suporta MutationObserver -> ok, só log
            console.warn('MutationObserver não disponível:', e);
        }
    }

    // estado inicial
    toggleDocumentFields();

    // Listener de submit (agora dentro do DOMContentLoaded: garante binding)
    if (form) {
        form.addEventListener('submit', function (e) {
            console.log('🚀 Form submit disparado!');
            const fd = new FormData(form);
            for (const pair of fd.entries()) {
                console.log(pair[0], ':', pair[1]);
            }
            // não previne o submit — apenas debug
        });
    } else {
        console.warn('Nenhum form encontrado no DOM para bind de submit.');
    }
});

document.addEventListener("DOMContentLoaded", () => {
  // valores "finais" simulados (depois você pega do backend)
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


//aqui esta a parte de foto
document.getElementById('photo-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const img = document.getElementById('profile-img');
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Botão de remover imagem
document.querySelector('.remove-btn').addEventListener('click', function() {
    const img = document.getElementById('profile-img');
    img.src = "{{ url_for('static', filename='img/default-avatar.svg') }}";
    document.getElementById('photo-upload').value = "";
});

//animação carrossel

const track = document.querySelector(".carrossel-track");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
let index = 0;

function moveCarousel() {
  const items = document.querySelectorAll(".card-item");
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