from Main import app, db
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, SubmitField, PasswordField, IntegerField, RadioField

from models_DB.companies import Companies
from models_DB.types import TipoUser

class FormUser(FlaskForm):

    nome = StringField('Digite o nome:', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer alguma validação se é cliente ou fornecedor (botão)
    tipo_usuario = RadioField('Tipo de usuário:', choices=[('1', 'Cliente'), ('2', 'Fornecedor')], validators=[validators.DataRequired()])

    email = StringField('Digite o e-mail: ', [validators.DataRequired(), validators.Length(min=2, max=150)])

    #fazer a validação do cpf ou cnpj
    tipo_documento = RadioField('CPF ou CNPJ?', choices=[('cpf', 'CPF'), ('cnpj', 'CNPJ')], validators=[validators.DataRequired()])
    cpf = StringField('Digite o CPF', [validators.Optional(), validators.Length(min=11, max=14)])
    cnpj = StringField('Digite o CNPJ', [validators.Optional(), validators.Length(min=14, max=18)])
    nome_fantasia = StringField('Digite o nome fantasia', [validators.Optional(), validators.Length(min=2, max=150)])

    telefone = StringField('Digite o telefone:', [validators.DataRequired(), validators.Length(min=10, max=15)])    
    cep = StringField('Digite o CEP:', [validators.DataRequired(), validators.Length(min=2, max=150)])
    numero = IntegerField('Digite o número do endereço:', [validators.DataRequired()])
    senha = PasswordField('Digite a senha:', [validators.DataRequired(), validators.Length(min=2, max=15)])

    distribuidora = SelectField('Seleciona sua distribuidora:', [validators.DataRequired()])
    cadastrar = SubmitField('Cadastrar novo usuário')

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Distribuidoras do banco
        distribuidoras = db.session.query(Companies).all()
        self.distribuidora.choices = [(str(d.id), d.nome_distribuidora) for d in distribuidoras]

        # Tipos de usuário do banco
        tipos = db.session.query(TipoUser).all()
        self.tipo_usuario.choices = [(str(t.id), t.nome) for t in tipos]'''


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
    
