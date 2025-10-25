def validar_documento(tipo_documento, cpf, nome_fantasia):
    erros = {}
    if tipo_documento == 'cpf' and (not cpf or cpf.strip() == ''):
        erros['cpf'] = 'Por favor, informe o CPF.'
    if tipo_documento == 'cnpj' and (not nome_fantasia or nome_fantasia.strip() == ''):
        erros['nome_fantasia'] = 'Por favor, preencha o Nome Fantasia para CNPJs.'
    return erros