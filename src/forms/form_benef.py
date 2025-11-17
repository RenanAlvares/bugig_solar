from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, validators, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class FormBenef(FlaskForm):


    # campos referentes ao upload de arquivos .txt para fazer o calculo
    '''conta1 = FileField(
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
    )'''

    # campos referentes ao upload de imagens das contas de luz
    img1 = FileField(
        "Conta de Luz 1",
        validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], "Apenas arquivos .png, .jpg e .jpeg são permitidos")]
    )
    img2 = FileField(
        "Conta de Luz 2",
        validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], "Apenas arquivos .png, .jpg e .jpeg são permitidos")]
    )
    img3 = FileField(
        "Conta de Luz 3",
        validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], "Apenas arquivos .png, .jpg e .jpeg são permitidos")]
    )

    valor1 = IntegerField('Valor Conta 1:', validators=[validators.DataRequired()])  
    valor2 = IntegerField('Valor Conta 2:', validators=[validators.DataRequired()])  
    valor3 = IntegerField('Valor Conta 3:', validators=[validators.DataRequired()])  

    # vai puxar os valores do banco da tabela de tipo_classes
    classe_consumo = SelectField(
        'Classe de consumo:',
        validators=[validators.DataRequired()],
        choices=[]  # definido depois na rota
    )

    cadastrar = SubmitField('Cadastrar beneficiário')



