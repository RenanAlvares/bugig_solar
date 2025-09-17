from extensions import db
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired, MultipleFileField

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, validators
from flask_wtf.file import FileAllowed, FileRequired, MultipleFileField

class FormBenef(FlaskForm):
    
    # fazer upload de 3 arquivos .txt para fazer o calculo e gravar no banco
    arquivos = MultipleFileField(
        'Envie os arquivos:',
        validators=[
            FileRequired(),
            FileAllowed(['txt'], 'Somente arquivos .txt são permitidos!')
        ]
    )

    # vai puxar os valores do banco
    classe_consumo = RadioField(
        'Classe de consumo:',
        validators=[validators.DataRequired()],
        choices=[]  # definido depois na rota
    )

    cadastrar = SubmitField('Cadastrar beneficiário')



