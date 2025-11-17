// cadastro.js - Script específico para páginas de cadastro/edição de usuários
(function() {
  'use strict';
  
  console.log("✅ cadastro.js carregado!");

  document.addEventListener('DOMContentLoaded', function () {
    // ==========================================
    // ALTERNAR CPF / CNPJ
    // ==========================================
    const form = document.querySelector('form#editForm') || document.querySelector('form#cadastroForm') || document.querySelector('form');
    const radios = Array.from(document.querySelectorAll('input[name="tipo_documento"]'));
    const cpfGroup = document.getElementById('cpf_group');
    const cnpjGroup = document.getElementById('cnpj_group');
    const nomeFantasiaGroup = document.getElementById('nome_fantasia_group');

    console.log('cadastro.js - radios encontrados:', radios.length, 'form encontrado?', !!form);
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
      console.log('tipo_documento selecionado:', raw);

      if (raw === 'cpf' || raw === '1') {
        showCPF();
      } else if (raw === 'cnpj' || raw === '2') {
        showCNPJ();
      } else {
        hideAll();
      }
    }

    // Registra listeners nos radios
    if (radios.length) {
      radios.forEach(r => r.addEventListener('change', toggleDocumentFields));
    } else {
      console.warn('Nenhum input[name="tipo_documento"] encontrado');
    }

    // Observa mudanças no hidden input
    const hiddenDoc = document.querySelector('input[type="hidden"][name="tipo_documento"], input[type="hidden"][name$="tipo_documento"]');
    if (hiddenDoc) {
      hiddenDoc.addEventListener('change', toggleDocumentFields);
      try {
        const mo = new MutationObserver(toggleDocumentFields);
        mo.observe(hiddenDoc, { attributes: true, attributeFilter: ['value'] });
      } catch (e) {
        console.warn('MutationObserver não disponível:', e);
      }
    }

    // Estado inicial
    toggleDocumentFields();

    // ==========================================
    // FOTO DE PERFIL
    // ==========================================
    const photoUpload = document.getElementById('photo-upload');
    const profileImg = document.getElementById('profile-img');
    const removeBtn = document.querySelector('.remove-btn');
    const defaultAvatar = profileImg?.src || '';

    // Upload de foto
    if (photoUpload && profileImg) {
      photoUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
            profileImg.src = e.target.result;
            console.log("✅ Foto carregada");
          };
          reader.readAsDataURL(file);
        }
      });
    }

    // Remover foto
    if (removeBtn && profileImg) {
      removeBtn.addEventListener('click', function() {
        profileImg.src = defaultAvatar;
        if (photoUpload) photoUpload.value = '';
        console.log("✅ Foto removida");
      });
    }

    // ==========================================
    // DEBUG DO FORMULÁRIO
    // ==========================================
    if (form) {
      form.addEventListener('submit', function (e) {
        console.log('🚀 Form submit disparado!');
        const fd = new FormData(form);
        for (const pair of fd.entries()) {
          console.log(pair[0], ':', pair[1]);
        }
      });
    } else {
      console.warn('Nenhum form encontrado no DOM');
    }
  });
})();