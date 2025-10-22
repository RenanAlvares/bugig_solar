from flask_wtf import FlaskForm
from wtforms import SelectField, validators, SubmitField

class Payment(FlaskForm):
    tipo_pagamento = SelectField('Selecione o tipo de pagamento', [validators.data_required()], choices=[])

    pagar = SubmitField('Pagar')