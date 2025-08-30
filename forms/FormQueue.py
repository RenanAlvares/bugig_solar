from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, validators

class FormQueue(FlaskForm):
    qtd_solicitada = IntegerField('Digite a quantidade solicitada', [validators.InputRequired()])

    # coerce=int converte o valor selecionado para inteiro, pois é inserido um id na tabela de fila
    distribuidora = SelectField('Selecione sua distribuidora', coerce=int, validators=[validators.InputRequired()])

    submit = SubmitField('Solicitar')