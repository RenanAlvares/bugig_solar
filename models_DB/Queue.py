from Main import db

class Queue(db.Model):

    __tablename__ = 'Fila'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user_fila = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    quantidade_solicitada = db.Column(db.Integer, nullable=False)
    distribuidora = db.Column(db.String(100), nullable=False)

    id_user = db.relationship('User', backref='filas', lazy=True)