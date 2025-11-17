from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, SubmitField

class Payment(FlaskForm):
    tipo_pagamento = SelectField('Selecione o tipo de pagamento', [validators.data_required()], choices=[])

    senha = StringField('Digite a senha para confirmar o pagamento', [validators.data_required(), validators.Length(min=6, max=15)])

    pagar = SubmitField('Pagar')