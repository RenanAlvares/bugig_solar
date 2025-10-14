from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators, SelectField

class FormDonation(FlaskForm):
    qtd_doada = IntegerField('Digite a quantidade a ser doada:', [validators.InputRequired()])

    doar = SubmitField('Doar')