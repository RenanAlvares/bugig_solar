from Main import db

class Beneficiaries(db.Model):

    __tablename__ = 'Beneficiarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    consumo_mensal = db.Column(db.Integer, nullable=False)
    id_classe_consumo = db.Column(db.Integer, db.ForeignKey('Tipo_Classes.id'), nullable=False)

    id_user = db.relationship('UsersDB', backref='beneficiarios', lazy=True)
    id_classe_consumo = db.relationship('TipoClasses', backref='beneficiarios', lazy=True)


class Generators(db.Model):

    __tablename__ = 'Geradores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    producao_mensal = db.Column(db.Integer, nullable=False)
    inicio_operacao = db.Column(db.Date, nullable=False)
    id_tipo = db.Column(db.Integer, db.ForeignKey('Tipo_Geracao.id'), nullable=False)

    id_user = db.relationship('UsersDb', backref='geradores', lazy=True)
    id_tipo = db.relationship('TipoGeracao', backref='geradores', lazy=True)