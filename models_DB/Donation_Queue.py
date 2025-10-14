from extensions import db

class Donation(db.Model):

    __tablename__ = 'Doacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade_doacao = db.Column(db.Integer, nullable=False)
    data_doacao = db.Column(db.DateTime, nullable=False)
    id_gerador = db.Column(db.Integer, db.ForeignKey('Geradores.id'), nullable=False)
    quantidade_disponivel = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    # relacionamento ajustado (não deve ter o mesmo nome que algum campo da tabela)
    gerador = db.relationship('Generators', backref='doacoes', lazy=True)


class Queue(db.Model):

    __tablename__ = 'Fila'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_beneficiario = db.Column(db.Integer, db.ForeignKey('Beneficiarios.id'), nullable=False)
    quantidade_solicitada = db.Column(db.Integer, nullable=False)
    data_solicitacao = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    quantidade_recebida = db.Column(db.Integer, nullable=False)

    beneficiario = db.relationship('Beneficiaries', backref='fila', lazy=True)
