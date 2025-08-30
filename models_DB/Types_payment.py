from Main import db

class TipoPagamento(db.Model):

    __tablename__ = 'Tipo_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
