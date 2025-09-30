document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os botões de rádio com o name 'tipo_documento'
    const tipoDocumentoRadios = document.querySelectorAll('input[name="tipo_documento"]');
    
    // Seleciona os containers (divs) dos campos que devem ser escondidos/mostrados
    const cpfGroup = document.getElementById('cpf_group');
    const cnpjGroup = document.getElementById('cnpj_group');
    const nomeFantasiaGroup = document.getElementById('nome_fantasia_group');

    // Função para atualizar a visibilidade dos campos
    function toggleDocumentFields() {
        // Pega o valor do radio button que está selecionado
        const selectedValue = document.querySelector('input[name="tipo_documento"]:checked').value;

        if (selectedValue === 'cpf') {
            cpfGroup.style.display = 'block'; // Mostra o campo CPF
            cnpjGroup.style.display = 'none'; // Esconde o campo CNPJ
            nomeFantasiaGroup.style.display = 'none'; // Esconde o campo Nome Fantasia
        } else if (selectedValue === 'cnpj') {
            cpfGroup.style.display = 'none'; // Esconde o campo CPF
            cnpjGroup.style.display = 'block'; // Mostra o campo CNPJ
            nomeFantasiaGroup.style.display = 'block'; // Mostra o campo Nome Fantasia
        }
    }

    // Adiciona um "ouvinte" para cada botão de rádio
    // Quando qualquer um deles for clicado, a função toggleDocumentFields será executada
    tipoDocumentoRadios.forEach(radio => {
        radio.addEventListener('change', toggleDocumentFields);
    });

    // Chama a função uma vez no início para garantir que o estado inicial esteja correto
    // (caso um dos botões já venha pré-selecionado)
    if (document.querySelector('input[name="tipo_documento"]:checked')) {
        toggleDocumentFields();
    }
});