from extensions import db

class Donation(db.Model):

    __tablename__ = 'Doacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user_doacao = db.Column(db.Integer, db.ForeignKey('Geradores.id'), nullable=False)
    quantidade_doacao = db.Column(db.Integer, nullable=False)
    data_doacao = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    quantidade_recebida = db.Column(db.Integer, nullable=False)

    id_user_doacao = db.relationship('Generators', backref='doacao', lazy=True)


class Queue(db.Model):

    __tablename__ = 'Fila'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user_fila = db.Column(db.Integer, db.ForeignKey('Beneficiarios.id'), nullable=False)
    quantidade_solicitada = db.Column(db.Integer, nullable=False)
    data_solicitacao = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    quantidade_disponível = db.Column(db.Integer, nullable=False)

    id_user = db.relationship('Beneficiaries', backref='fila', lazy=True)