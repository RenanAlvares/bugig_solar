from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField, IntegerField, validators
from flask_wtf import FlaskForm

class FormGen(FlaskForm):
    
    producao_mensal = IntegerField('Produção mensal (kWh):', validators=[validators.DataRequired()])
    inicio_operacao = DateField('Digite a data do início de operação:', validators=[validators.DataRequired()])
        
    # vai puxar os valores do tipo de geração direto do banco de dados    
    id_tipo_geracao = SelectField('Qual é seu tipo de geração?', validators=[validators.DataRequired()], choices=[]) 

    cadastrar = SubmitField('Cadastrar gerador')



