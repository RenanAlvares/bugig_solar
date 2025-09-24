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

  if (form && input && resultado) {
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
  }
});

document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------
    // FOTO DE PERFIL
    // ------------------------------
    const photoUploadInput = document.getElementById('photo-upload');
    const profileImg = document.getElementById('profile-img');
    const removePhotoBtn = document.querySelector('.remove-btn');
    const defaultPlaceholderSrc = profileImg ? profileImg.src : '';

    const resetPhoto = () => {
        if (profileImg) {
            profileImg.src = defaultPlaceholderSrc;
        }
        if (photoUploadInput) photoUploadInput.value = '';
    };

    if (photoUploadInput) {
        photoUploadInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (profileImg) {
                        profileImg.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (removePhotoBtn) {
        removePhotoBtn.addEventListener('click', resetPhoto);
    }
    
    // Exibe campos CPF / CNPJ dinamicamente
    function toggleDocumentoFields() {
        const tipo = document.querySelector('input[name="tipo_documento"]:checked');
        const cpfDiv = document.getElementById("cpf_group");
        const cnpjDiv = document.getElementById("cnpj_group");
        const nomeFantasiaDiv = document.getElementById("nome_fantasia_group");

        if (tipo) {
            if (tipo.value === "cpf") {
                cpfDiv.style.display = "block";
                cnpjDiv.style.display = "none";
                nomeFantasiaDiv.style.display = "none";
            } else {
                cpfDiv.style.display = "none";
                cnpjDiv.style.display = "block";
                nomeFantasiaDiv.style.display = "block";
            }
        }
    }

    window.onload = toggleDocumentoFields;
    const radios = document.getElementsByName("tipo_documento");
    for (let radio of radios) {
        radio.addEventListener("change", toggleDocumentoFields);
    }

    radios.forEach(r => r.addEventListener("change", toggleDocumentoFields));
    toggleDocumentoFields(); // roda na carga da página

    // ------------------------------
    // MÁSCARAS
    // ------------------------------
    const mascaraCpf = (value) => {
        value = value.replace(/\D/g, "");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        return value;
    };

    const mascaraCnpj = (value) => {
        value = value.replace(/\D/g, "");
        value = value.replace(/^(\d{2})(\d)/, "$1.$2");
        value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        value = value.replace(/\.(\d{3})(\d)/, ".$1/$2");
        value = value.replace(/(\d{4})(\d)/, "$1-$2");
        return value;
    };

    if (campoCpf) {
        campoCpf.addEventListener('input', (e) => {
            e.target.value = mascaraCpf(e.target.value);
        });
    }

    if (campoCnpj) {
        campoCnpj.addEventListener('input', (e) => {
            e.target.value = mascaraCnpj(e.target.value);
        });
    }

    // ------------------------------
    // BUSCAR CEP
    // ------------------------------
    const cepField = document.getElementById('cep') || document.querySelector('input[name="cep"]');
    
    if (cepField) {
        // Máscara para CEP
        cepField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });

        // Buscar endereço pelo CEP
        cepField.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
                buscarCEP(cep);
            }
        });
    }
    
    function buscarCEP(cep) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    const logradouro = document.getElementById('logradouro');
                    const bairro = document.getElementById('bairro');
                    const cidade = document.getElementById('cidade');
                    const estado = document.getElementById('estado');
                    
                    if (logradouro) logradouro.value = data.logradouro || '';
                    if (bairro) bairro.value = data.bairro || '';
                    if (cidade) cidade.value = data.localidade || '';
                    if (estado) estado.value = data.uf || '';
                }
            })
            .catch(error => {
                console.error('Erro ao buscar CEP:', error);
            });
    }

    // ------------------------------
    // MÁSCARA TELEFONE
    // ------------------------------
    const telefoneField = document.getElementById('telefone') || document.querySelector('input[name="telefone"]');
    if (telefoneField) {
        telefoneField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{4})(\d{1,4})$/, '$1-$2');
            } else {
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{5})(\d{1,4})$/, '$1-$2');
            }
            e.target.value = value;
        });
    }
});