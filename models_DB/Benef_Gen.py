from extensions import db

class Beneficiaries(db.Model):
    __tablename__ = 'Beneficiarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    consumo_mensal = db.Column(db.Integer, nullable=False)
    classe_consumo = db.Column(db.Integer, db.ForeignKey('Tipo_Classes.id'), nullable=False)

    # Relacionamentos (relacionar o nome da classe ao nome da tabela atual)
    usuario = db.relationship('UsersDb', backref='beneficiarios', lazy=True)
    tipo_classe = db.relationship('TipoClasses', backref='beneficiarios', lazy=True)


class Generators(db.Model):
    __tablename__ = 'Geradores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    producao_mensal = db.Column(db.Integer, nullable=False)
    inicio_operacao = db.Column(db.Date, nullable=False)
    id_tipo_geracao = db.Column(db.Integer, db.ForeignKey('Tipo_geracao.id'), nullable=False)

    usuario = db.relationship('UsersDb', backref='geradores', lazy=True)
    tipo_geracao = db.relationship('TipoGeracao', backref='geradores', lazy=True)
