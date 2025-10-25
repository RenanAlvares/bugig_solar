from extensions import db

class Payment(db.Model):

    __tablename__ = 'Pagamento'

    id = db.Column(db.Integer, primary_key=True)
    id_transferencia = db.Column(db.Integer, db.ForeignKey('Transferencia.id'), nullable=False)
    data_emissao = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_tipo_pagamento = db.Column(db.Integer, db.ForeignKey('tipo_pagamento.id'), nullable=False)
    data_vencimento = db.Column(db.DateTime, nullable=False)
    data_liquidacao = db.Column(db.DateTime, nullable=True)
    valor = db.Column(db.Float, nullable=False)

    transferencia = db.relationship('Transfer', backref='pagamentos')
    tipo_pagamento = db.relationship('TipoPagamento', backref='pagamentos')

