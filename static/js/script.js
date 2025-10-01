document.addEventListener('DOMContentLoaded', function () {
    // elementos
    const radios = Array.from(document.querySelectorAll('input[name="tipo_documento"]'));
    const cpfGroup = document.getElementById('cpf_group');
    const cnpjGroup = document.getElementById('cnpj_group');
    const nomeFantasiaGroup = document.getElementById('nome_fantasia_group');

    // debug rápido (remova ou comente depois)
    console.log('script.js carregado. radios encontrados:', radios.length);
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

    function toggleDocumentFields() {
        const selected = document.querySelector('input[name="tipo_documento"]:checked');
        if (!selected) {
            hideAll();
            console.log('Nenhum tipo_documento selecionado');
            return;
        }

        const raw = (selected.value || '').toString().toLowerCase().trim();
        console.log('tipo_documento selecionado value=', raw);

        // aceita 'cpf'/'cnpj' ou '1'/'2'
        if (raw === 'cpf' || raw === '1') {
            showCPF();
        } else if (raw === 'cnpj' || raw === '2') {
            showCNPJ();
        } else {
            // fallback: tenta basear no label text se houver data-attribute
            console.warn('Valor inesperado em tipo_documento:', raw);
            hideAll();
        }
    }

    // se não encontrar radios, sai (evita erro)
    if (!radios.length) {
        console.warn('Nenhum input[name="tipo_documento"] encontrado.');
        return;
    }

    radios.forEach(r => r.addEventListener('change', toggleDocumentFields));

    // estado inicial
    toggleDocumentFields();
});

// Debug: monitora o submit
const form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', function(e) {
        console.log('🚀 Form submit disparado!');
        console.log('FormData:', new FormData(form));
    });
}