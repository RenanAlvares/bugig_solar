from extensions import db
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, SubmitField, PasswordField, IntegerField, RadioField

class FormUser(FlaskForm):

    nome = StringField('Digite o nome:', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer alguma validação se é cliente ou fornecedor (botão)
    tipo_usuario = RadioField('Tipo de usuário:', choices=[('1', 'Beneficiário'), ('2', 'Gerador')], validators=[validators.DataRequired()])

    email = StringField('Digite o e-mail: ', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer a validação do cpf ou cnpj
    tipo_documento = RadioField('CPF ou CNPJ?', choices=[('cpf', 'CPF'), ('cnpj', 'CNPJ')], validators=[validators.DataRequired()])
    cpf = StringField('Digite o CPF', [validators.Optional(), validators.Length(min=11, max=14)])
    cnpj = StringField('Digite o CNPJ', [validators.Optional(), validators.Length(min=14, max=18)])
    nome_fantasia = StringField('Digite o nome fantasia', [validators.Optional(), validators.Length(min=2, max=150)])

    telefone = StringField('Digite o telefone:', [validators.DataRequired(), validators.Length(min=10, max=15)])    
    cep = StringField('Digite o CEP:', [validators.DataRequired(), validators.Length(min=2, max=150)])
    numero = IntegerField('Digite o número do endereço:', [validators.DataRequired()])
    senha = PasswordField('Digite a senha:', [validators.DataRequired(), validators.Length(min=6, max=15)])

    distribuidora = SelectField('Seleciona sua distribuidora:', [validators.DataRequired()], choices=[])
    cadastrar = SubmitField('Cadastrar novo usuário')


    
