from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, validators
from flask_wtf import FlaskForm

class FormBenef(FlaskForm):
    
    # fazer upload de 3 arquivos .txt para fazer o calculo e gravar no banco somente a media final
    consumo_mensal = IntegerField('Consumo mensal (kWh):', validators=[validators.DataRequired()])

    # vai puxar os valores do banco da tabela de tipo_classes
    classe_consumo = SelectField(
        'Classe de consumo:',
        validators=[validators.DataRequired()],
        choices=[]  # definido depois na rota
    )

    cadastrar = SubmitField('Cadastrar beneficiário')



