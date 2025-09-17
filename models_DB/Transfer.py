from extensions import db

class Transfer(db.Model):
    __tablename__ = 'Transferencia'
    
    id = db.Column(db.Integer, primary_key=True)
    id_user_fila = db.Column(db.Integer, db.ForeignKey('Fila.id'), nullable=False)
    id_user_doador = db.Column(db.Integer, db.ForeignKey('Doacao.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data_transferencia = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_fila = db.relationship('Queue', foreign_keys=[id_user_fila])
    user_doador = db.relationship('Donations', foreign_keys=[id_user_doador])