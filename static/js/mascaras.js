// Espera o jQuery e Inputmask carregarem completamente
(function() {
  'use strict';
  
  function inicializarMascaras() {
    // Verifica se jQuery e Inputmask estão carregados
    if (typeof $ === "undefined" || typeof $.fn.inputmask === "undefined") {
      console.error("⚠️ jQuery Inputmask não encontrado. Tentando novamente...");
      setTimeout(inicializarMascaras, 100);
      return;
    }

    console.log("✅ jQuery Inputmask carregado!");

    // === Máscaras Visuais ===
    const cpf = $("input[name='cpf']");
    const cnpj = $("input[name='cnpj']");
    const cep = $("input[name='cep']");
    const telefone = $("input[name='telefone']");
    const numero = $("input[name='numero']");

    if (cpf.length) cpf.inputmask("999.999.999-99", { showMaskOnHover: false });
    if (cnpj.length) cnpj.inputmask("99.999.999/9999-99", { showMaskOnHover: false });
    if (cep.length) cep.inputmask("99999-999", { showMaskOnHover: false });
    if (telefone.length) telefone.inputmask("(99) 99999-9999", { showMaskOnHover: false });
    if (numero.length) numero.inputmask("999999", { showMaskOnHover: false });

    // === Mostrar / Esconder CPF / CNPJ ===
    const tipoDocumentoRadios = document.querySelectorAll("input[name='tipo_documento']");
    const cpfGroup = document.getElementById("cpf_group");
    const cnpjGroup = document.getElementById("cnpj_group");
    const nomeFantasiaGroup = document.getElementById("nome_fantasia_group");

    if (tipoDocumentoRadios.length > 0) {
      tipoDocumentoRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
          if (this.value === "cpf") {
            if (cpfGroup) cpfGroup.style.display = "block";
            if (cnpjGroup) cnpjGroup.style.display = "none";
            if (nomeFantasiaGroup) nomeFantasiaGroup.style.display = "none";
          } else if (this.value === "cnpj") {
            if (cpfGroup) cpfGroup.style.display = "none";
            if (cnpjGroup) cnpjGroup.style.display = "block";
            if (nomeFantasiaGroup) nomeFantasiaGroup.style.display = "block";
          }
        });
      });
    }

    // === CRÍTICO: Remover máscaras IMEDIATAMENTE antes do submit ===
    const form = document.getElementById("cadastroForm");
    if (form) {
      // Intercepta o submit com prioridade máxima
      form.addEventListener("submit", function (e) {
        console.log("🔄 Interceptando submit - Removendo máscaras...");
        
        // Remove máscaras usando inputmask
        try {
          if (cpf.length && cpf.inputmask) cpf.inputmask('remove');
          if (cnpj.length && cnpj.inputmask) cnpj.inputmask('remove');
          if (cep.length && cep.inputmask) cep.inputmask('remove');
          if (telefone.length && telefone.inputmask) telefone.inputmask('remove');
          if (numero.length && numero.inputmask) numero.inputmask('remove');
        } catch (error) {
          console.warn("⚠️ Erro ao remover máscaras via inputmask:", error);
        }

        // GARANTIA EXTRA: Limpeza manual forçada
        const campos = ["cpf", "cnpj", "cep", "telefone", "numero"];
        campos.forEach((nomeCampo) => {
          const input = document.querySelector(`input[name='${nomeCampo}']`);
          if (input && input.value) {
            const valorOriginal = input.value;
            const valorLimpo = input.value.replace(/\D/g, "");
            input.value = valorLimpo;
            console.log(`✅ ${nomeCampo}: "${valorOriginal}" → "${valorLimpo}"`);
          }
        });

        console.log("✅ Máscaras removidas! Formulário será enviado agora.");
        // Não previne o submit, apenas limpa os valores
      }, true); // true = useCapture, executa ANTES de outros listeners
      
      console.log("✅ Listener de submit instalado!");
    } else {
      console.error("❌ Formulário #cadastroForm não encontrado!");
    }
  }

  // Inicia quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarMascaras);
  } else {
    inicializarMascaras();
  }
})();