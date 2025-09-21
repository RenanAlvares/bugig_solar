from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, validators
from wtforms import SelectField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class FormBenef(FlaskForm):


    # o usuário tem que incluir 3 arquivos .txt com o valor do consumo mensal das ultimas 3 contas de luz
    
    conta1 = FileField(
        "Conta de Luz 1 (.txt)",
        validators=[FileRequired(), FileAllowed(['txt'], "Apenas arquivos .txt são permitidos")]
    )
    conta2 = FileField(
        "Conta de Luz 2 (.txt)",
        validators=[FileRequired(), FileAllowed(['txt'], "Apenas arquivos .txt são permitidos")]
    )
    conta3 = FileField(
        "Conta de Luz 3 (.txt)",
        validators=[FileRequired(), FileAllowed(['txt'], "Apenas arquivos .txt são permitidos")]
    )
    
    # vai puxar os valores do banco da tabela de tipo_classes
    classe_consumo = SelectField(
        'Classe de consumo:',
        validators=[validators.DataRequired()],
        choices=[]  # definido depois na rota
    )

    cadastrar = SubmitField('Cadastrar beneficiário')



