from Main import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormLogin(FlaskForm):
    email = StringField('Digite seu e-mail: ', [validators.DataRequired(), validators.Length(min=2, max=150)])
    senha = PasswordField('Digite sua senha: ', [validators.DataRequired(), validators.Length(min=8, max=250)])
    entrar = SubmitField('Entrar')
