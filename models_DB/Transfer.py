from Main import db

class Transfer(db.Model):
    __tablename__ = 'Transferencia'
    
    id = db.Column(db.Integer, primary_key=True)
    id_user_fila = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    id_user_doador = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data_transferencia = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_fila = db.relationship('User', foreign_keys=[id_user_fila])
    user_doador = db.relationship('User', foreign_keys=[id_user_doador])