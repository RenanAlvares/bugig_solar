from Main import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, IntegerField, RadioField

class FormUser(FlaskForm):

    nome = StringField('Digite o nome do novo usuário', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer alguma validação se é cliente ou fornecedor (botão)
    tipo_usuario = RadioField('Tipo de usuário', choices=[('1', 'Cliente'), ('2', 'Fornecedor')], validators=[validators.DataRequired()])

    email = StringField('Digite o e-mail do novo usuário', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer a validação do cpf ou cnpj
    tipo_documento = RadioField('CPF ou CNPJ?', choices=[('cpf', 'CPF'), ('cnpj', 'CNPJ')], validators=[validators.DataRequired()])
    cpf = StringField('Digite o CPF', [validators.Optional(), validators.Length(min=11, max=14)])
    cnpj = StringField('Digite o CNPJ', [validators.Optional(), validators.Length(min=14, max=18)])
    nome_fantasia = StringField('Digite o nome fantasia', [validators.Optional(), validators.Length(min=2, max=150)])

    cep = StringField('Digite o cep do novo usuário', [validators.DataRequired(), validators.Length(min=2, max=150)])
    numero = IntegerField('Digite o número do endereço do novo usuário', [validators.DataRequired()])
    senha = PasswordField('Digite a senha do novo usuário', [validators.DataRequired(), validators.Length(min=2, max=15)])

    cadastrar = SubmitField('Cadastrar novo usuário')

    #valida o tipo de documento
    def validate(self):
        resultado_validacao = FlaskForm.validate(self)
        if not resultado_validacao:
            return False

        # Validação para CNPJ
        if self.tipo_documento.data == 'cnpj':
            if not self.nome_fantasia.data or self.nome_fantasia.data.strip() == '':
                self.nome_fantasia.errors.append(
                    'Por favor, preencha o Nome Fantasia, pois ele é obrigatório para CNPJs.'
                )
                return False

        # Validação para CPF
        if self.tipo_documento.data == 'cpf':
            if not self.cpf.data or self.cpf.data.strip() == '':
                self.cpf.errors.append(
                    'Por favor, informe o CPF, pois ele é obrigatório para este tipo de documento.'
                )
                return False

        return True
    
class FormLogin(FlaskForm):
    email = StringField('Digite seu e-mail', [validators.DataRequired(), validators.Length(min=2, max=150)])
    senha = PasswordField('Digite sua senha', [validators.DataRequired(), validators.Length(min=2, max=15)])
    entrar = SubmitField('Entrar')
